from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.auth import get_current_user

from app import schemas
from app import crud

import pickle

router = APIRouter(
    prefix="/predict",
    tags=["Prediction"]
)

# -----------------------------
# LOAD MODEL
# -----------------------------

with open(
    "app/ml/model.pkl",
    "rb"
) as f:

    model = pickle.load(f)

with open(
    "app/ml/scaler.pkl",
    "rb"
) as f:

    scaler = pickle.load(f)

# -----------------------------
# PREDICT DIABETES
# -----------------------------

@router.post("/")
def predict(

    data: schemas.PredictionInput,

    db: Session = Depends(get_db),

    current_user: str = Depends(
        get_current_user
    )

):

    values = [[
        data.Pregnancies,
        data.Glucose,
        data.BloodPressure,
        data.SkinThickness,
        data.Insulin,
        data.BMI,
        data.DiabetesPedigreeFunction,
        data.Age
    ]]

    scaled_values = scaler.transform(
        values
    )

    prediction = model.predict(
        scaled_values
    )

    result_text = (
        "Diabetic"
        if prediction[0] == 1
        else "Not Diabetic"
    )

    crud.save_prediction(
        db,
        current_user,
        int(data.Glucose),
        int(prediction[0]),
        result_text
    )

    return {
        "prediction": int(
            prediction[0]
        ),
        "result": result_text
    }

# -----------------------------
# USER HISTORY
# -----------------------------

@router.get("/history")
def prediction_history(

    db: Session = Depends(get_db),

    current_user: str = Depends(
        get_current_user
    )

):

    return crud.get_prediction_history(
        db,
        current_user
    )