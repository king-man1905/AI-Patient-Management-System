from sqlalchemy.orm import Session
from app import models, schemas
from app.auth import hash_password
from fastapi import HTTPException


## Create Patient

def create_patient(db: Session, patient: schemas.PatientCreate):

    new_patient = models.Patient(
        name=patient.name,
        age=patient.age,
        gender=patient.gender,
        disease=patient.disease
    )

    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)

    return new_patient


# Get All Patients
def get_all_patients(
    db: Session,
    name: str = None,
    gender: str = None,
    sort_by: str = None,
    skip: int = 0,
    limit: int = 10
):

    query = db.query(
        models.Patient
    )

    if name:
        query = query.filter(
            models.Patient.name.ilike(
                f"%{name}%"
            )
        )

    if gender:
        query = query.filter(
            models.Patient.gender == gender
        )
    
    if sort_by == "name":
        query = query.order_by(
            models.Patient.name
        )

    elif sort_by == "age":
        query = query.order_by(
            models.Patient.age
        )
        
    return query.offset(
        skip
    ).limit(
        limit
    ).all()


#GET patients by ID

def get_patient_by_id(
        db:Session,
        patient_id: int
):
    return db.query(
        models.Patient
    ).filter(
        models.Patient.id == patient_id
    ).first()


#Delete Patients

def delete_patient(
        db: Session,
        patient_id: int
):
    
    patient = db.query(
        models.Patient
    ).filter(
        models.Patient.id == patient_id
    ).first()


    if patient:

        db.delete(patient)
        db.commit()
        

    return patient    


# Upade patient
def update_patient(
        db: Session,
        patient_id: int,
        patient_data: schemas.PatientUpdate
):
    
    patient = db.query(
        models.Patient
    ).filter(
        models.Patient.id == patient_id
    ).first()

    if patient:
        patient.name = patient_data.name
        patient.age = patient_data.age
        patient.gender = patient_data.gender
        patient.disease = patient_data.disease

        db.commit()
        db.refresh(patient)

    return patient    



# CREATE USER
def create_user(
    db: Session,
    user: schemas.UserCreate
):

    existing_email = db.query(
        models.User
    ).filter(
        models.User.email == user.email
    ).first()

    if existing_email:
        raise HTTPException(
            status_code=400,
            detail="Email alraedy registered"
        )

    existing_username = db.query(
        models.User
    ).filter(
        models.User.username == user.username
    ).first()

    if existing_username:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    new_user = models.User(
        username=user.username,
        email=user.email,
        password=hash_password(
            user.password
        ),
        role="user"
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def get_user_by_email(
    db: Session,
    email: str
):

    return db.query(
        models.User
    ).filter(
        models.User.email == email
    ).first()


def get_user_by_id(
    db: Session,
    user_id: int
):
    return db.query(
        models.User
    ).filter(
        models.User.id == user_id
    ).first()


#Save Prediction
def save_prediction(
    db: Session,
    user_email: str,
    glucose: int,
    prediction: int,
    result: str
):

    history = models.PredictionHistory(
        user_email=user_email,
        glucose=glucose,
        prediction=prediction,
        result=result
    )

    db.add(history)
    db.commit()
    db.refresh(history)

    return history

def get_prediction_history(
    db: Session,
    user_email: str
):

    return db.query(
        models.PredictionHistory
    ).filter(
        models.PredictionHistory.user_email == user_email
    ).order_by(
        models.PredictionHistory.id.desc()
    ).all()