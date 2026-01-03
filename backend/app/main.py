from fastapi import FastAPI
from app.database import Base, engine
from app.routes import auth, users, admin

Base.metadata.create_all(bind=engine)  # Create tables
app = FastAPI(title="Pollution Monitoring API")

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(admin.router)