from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session

from dotenv import load_dotenv
import os

from app.database import get_db
from app import crud

# -----------------------------
# ENV VARIABLES
# -----------------------------

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

ALGORITHM = os.getenv("ALGORITHM")

ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
)

# -----------------------------
# PASSWORD HASHING
# -----------------------------

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

# -----------------------------
# OAUTH2 SCHEME
# -----------------------------

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/users/login"
)

# -----------------------------
# HASH PASSWORD
# -----------------------------

def hash_password(password: str):

    return pwd_context.hash(password)

# -----------------------------
# VERIFY PASSWORD
# -----------------------------

def verify_password(
    plain_password: str,
    hashed_password: str
):

    return pwd_context.verify(
        plain_password,
        hashed_password
    )

# -----------------------------
# CREATE ACCESS TOKEN
# -----------------------------

def create_access_token(
    data: dict
):

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update(
        {
            "exp": expire
        }
    )

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt

# -----------------------------
# GET CURRENT USER
# -----------------------------

def get_current_user(
    token: str = Depends(oauth2_scheme)
):

    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials"
    )

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        email = payload.get("sub")

        if email is None:
            raise credentials_exception

        return email

    except JWTError:

        raise credentials_exception

# -----------------------------
# GET CURRENT ADMIN
# -----------------------------

def get_current_admin(

    current_user: str = Depends(
        get_current_user
    ),

    db: Session = Depends(
        get_db
    )

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

    if user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )

    return user