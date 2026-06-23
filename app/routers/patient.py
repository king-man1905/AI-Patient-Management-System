from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app import schemas, crud
from app.auth import (get_current_admin, get_current_user)

router = APIRouter(
    prefix="/patients",
    tags=["Patients"],
    dependencies=[Depends(get_current_user)]
)


# -------------------------
# CREATE PATIENT
# -------------------------

@router.post(
    "/",
    response_model=schemas.PatientResponse,
    status_code=201
)
def create_patient(
    patient: schemas.PatientCreate,
    db: Session = Depends(get_db)
):
    return crud.create_patient(db, patient)


# -------------------------
# GET ALL PATIENTS
# -------------------------

@router.get(
    "/",
    response_model=list[schemas.PatientResponse]
)
def get_patients(

    name: Optional[str] = None,

    gender: Optional[str] = None,

    sort_by: Optional[str] = None,

    skip: int = 0,

    limit: int = 10,

    db: Session = Depends(get_db)
):

    return crud.get_all_patients(
        db,
        name,
        gender,
        sort_by,
        skip,
        limit
    )

# -------------------------
# GET PATIENT BY ID
# -------------------------

@router.get(
    "/{patient_id}",
    response_model=schemas.PatientResponse
)
def get_patient(
    patient_id: int,
    db: Session = Depends(get_db)
):

    patient = crud.get_patient_by_id(
        db,
        patient_id
    )

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    return patient


# -------------------------
# UPDATE PATIENT
# -------------------------

@router.put(
    "/{patient_id}",
    response_model=schemas.PatientResponse
)
def update_patient(
    patient_id: int,
    patient: schemas.PatientUpdate,
    db: Session = Depends(get_db)
):

    updated_patient = crud.update_patient(
        db,
        patient_id,
        patient
    )

    if not updated_patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    return updated_patient


# -------------------------
# DELETE PATIENT
# -------------------------

@router.delete("/{patient_id}")
def delete_patient(
    patient_id: int,
    admin = Depends(
        get_current_admin
    ),
    db: Session = Depends(get_db)
):

    patient = crud.delete_patient(
        db,
        patient_id
    )

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    return {
        "message": "Patient deleted successfully"
    }