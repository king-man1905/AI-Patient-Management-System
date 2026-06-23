from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from fastapi.security import (
    OAuth2PasswordRequestForm
)

from sqlalchemy.orm import Session

from app.database import get_db
from app import schemas, crud

from app.auth import (
    verify_password,
    create_access_token,
    get_current_user
)

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# -----------------------------
# REGISTER USER
# -----------------------------

@router.post(
    "/register",
    response_model=schemas.UserResponse,
    status_code=201
)
def register_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):

    new_user = crud.create_user(
        db,
        user
    )

    return new_user


# -----------------------------
# LOGIN USER
# -----------------------------

@router.post("/login")
def login_user(

    form_data: OAuth2PasswordRequestForm = Depends(),

    db: Session = Depends(get_db)

):

    db_user = crud.get_user_by_email(
        db,
        form_data.username
    )

    if not db_user:

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(
        form_data.password,
        db_user.password
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        {
            "sub": db_user.email
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": db_user.username,
        "email": db_user.email

    }


# -----------------------------
# CURRENT USER PROFILE
# -----------------------------

@router.get(
    "/me",
    response_model=schemas.UserProfile
)
def get_me(

    current_user: str = Depends(
        get_current_user
    ),

    db: Session = Depends(get_db)

):

    user = crud.get_user_by_email(
        db,
        current_user
    )

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user