from pydantic import (
    BaseModel,
    Field,
    EmailStr
)


# -----------------------------
# PATIENT CREATE
# -----------------------------

class PatientCreate(BaseModel):

    name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Patient Name"
    )

    age: int = Field(
        ...,
        gt=0,
        lt=120,
        description="Patient Age"
    )

    gender: str = Field(
        ...,
        min_length=3,
        max_length=10
    )

    disease: str = Field(
        ...,
        min_length=2,
        max_length=100
    )


# -----------------------------
# PATIENT UPDATE
# -----------------------------

class PatientUpdate(BaseModel):

    name: str = Field(
        ...,
        min_length=2,
        max_length=100
    )

    age: int = Field(
        ...,
        gt=0,
        lt=120
    )

    gender: str = Field(
        ...,
        min_length=3,
        max_length=10
    )

    disease: str = Field(
        ...,
        min_length=2,
        max_length=100
    )


# -----------------------------
# PATIENT RESPONSE
# -----------------------------

class PatientResponse(BaseModel):

    id: int
    name: str
    age: int
    gender: str
    disease: str

    class Config:
        from_attributes = True


# -----------------------------
# USER CREATE
# -----------------------------

class UserCreate(BaseModel):

    username: str = Field(
        ...,
        min_length=3,
        max_length=50
    )

    email: EmailStr

    password: str = Field(
        ...,
        min_length=6
    )


# -----------------------------
# USER RESPONSE
# -----------------------------

class UserResponse(BaseModel):

    id: int
    username: str
    email: EmailStr
    role: str

    class Config:
        from_attributes = True


# -----------------------------
# USER LOGIN
# -----------------------------

class UserLogin(BaseModel):

    email: EmailStr

    password: str


# -----------------------------
# USER PROFILE
# -----------------------------

class UserProfile(BaseModel):

    id: int
    username: str
    email: EmailStr
    role: str

    class Config:
        from_attributes = True


# -----------------------------
# PREDICTION INPUT
# -----------------------------

class PredictionInput(BaseModel):

    Pregnancies: int = Field(
        ...,
        ge=0
    )

    Glucose: float = Field(
        ...,
        gt=0
    )

    BloodPressure: float = Field(
        ...,
        ge=0
    )

    SkinThickness: float = Field(
        ...,
        ge=0
    )

    Insulin: float = Field(
        ...,
        ge=0
    )

    BMI: float = Field(
        ...,
        ge=0
    )

    DiabetesPedigreeFunction: float = Field(
        ...,
        ge=0
    )

    Age: int = Field(
        ...,
        gt=0,
        lt=120
    )