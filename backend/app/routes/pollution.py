from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import get_current_user, get_current_admin
from app.models import PollutionData, User
from datetime import datetime
from app.utils.aqi import calculate_aqi
from app.ml.predict import predict_aqi

router = APIRouter(prefix="/pollution", tags=["Pollution"])

# Add new pollution data (admin only)
@router.post("/add")
def add_pollution_data(
    location: str,
    pm25: float,
    pm10: float,
    no2: Optional[float] = None,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    aqi = calculate_aqi(pm25)

    data = PollutionData(
        location=location,
        pm25=pm25,
        pm10=pm10,
        no2=no2,
        aqi=aqi,
        created_by=admin.id,
        recorded_at=datetime.utcnow()
    )
    db.add(data)
    db.commit()
    db.refresh(data)
    return data

# Get all pollution data (any logged-in user)
@router.get("/")
def get_pollution_data(
    location: str | None = None,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    query = db.query(PollutionData)

    if location:
        query = query.filter(PollutionData.location.ilike(f"%{location}%"))

    data = query.order_by(
    PollutionData.recorded_at.desc()
    ).offset(skip).limit(limit).all()

    from app.utils.health import health_category

    return [
        {
            "id": d.id,
            "location": d.location,
            "pm25": d.pm25,
            "pm10": d.pm10,
            "no2": d.no2,
            "aqi": d.aqi,
            "health": health_category(d.aqi),
            "recorded_at": d.recorded_at
        }
        for d in data
    ]

@router.get("/search/{pollution_id}")
def get_pollution_by_id(
    pollution_id: int,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    r = db.get(PollutionData, pollution_id)
    if not r:
        raise HTTPException(404, "Not found")

    data = r.__dict__.copy()
    data["aqi"] = calculate_aqi(r.pm25)
    data.pop("_sa_instance_state", None)
    return data


# Delete pollution data by ID (admin only)
@router.delete("/delete/{pollution_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_pollution_data(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    pollution = db.query(PollutionData).filter(PollutionData.id == id).first()
    if not pollution:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pollution data not found"
        )
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can delete data"
        )
    db.delete(pollution)
    db.commit()

@router.get("/analytics/summary")
def pollution_summary(
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    from sqlalchemy import func

    result = db.query(
        func.avg(PollutionData.aqi),
        func.max(PollutionData.aqi)
    ).first()

    return {
        "average_aqi": round(result[0], 2) if result[0] else None,
        "worst_aqi": result[1]
    }

@router.post("/predict")
def predict_pollution(pm25: float, pm10: float, no2: float):
    aqi = predict_aqi(pm25, pm10, no2)

    return {
        "pm25": pm25,
        "pm10": pm10,
        "no2": no2,
        "predicted_aqi": aqi
    }
