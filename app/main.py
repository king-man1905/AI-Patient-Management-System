from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.database import Base, engine
from app import models

from app.routers import (
    patient,
    user,
    predict
)

# Create Tables
Base.metadata.create_all(
    bind=engine
)

# FastAPI App
app = FastAPI(
    title="AI Patient Management System",
    version="1.0.0"
)

# Static Files
app.mount(
    "/static",
    StaticFiles(
        directory="app/static"
    ),
    name="static"
)

# Templates
templates = Jinja2Templates(
    directory="app/templates"
)

# Routers
app.include_router(
    patient.router
)

app.include_router(
    user.router
)

app.include_router(
    predict.router
)

# -----------------------------
# HOME PAGE
# -----------------------------

@app.get("/")
def home(
    request: Request
):

    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )

# -----------------------------
# LOGIN PAGE
# -----------------------------

@app.get("/login")
def login_page(
    request: Request
):

    return templates.TemplateResponse(
        request=request,
        name="login.html"
    )

# -----------------------------
# REGISTER PAGE
# -----------------------------

@app.get("/register")
def register_page(
    request: Request
):

    return templates.TemplateResponse(
        request=request,
        name="register.html"
    )

# -----------------------------
# HEALTH CHECK
# -----------------------------

@app.get("/health")
def health_check():

    return {
        "status": "healthy",
        "message": "API Running Successfully"
    }