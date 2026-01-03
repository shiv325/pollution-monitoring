from fastapi import APIRouter, Depends
from ..dependencies import get_current_user
from ..models import User

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me")
def read_me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email
    }
