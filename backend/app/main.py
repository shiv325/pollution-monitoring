from fastapi import FastAPI
from .database import Base, engine
from .routes import auth, users

Base.metadata.create_all(bind=engine)  # Create tables

app = FastAPI(title="Pollution Monitoring API")

app.include_router(auth.router)
app.include_router(users.router)