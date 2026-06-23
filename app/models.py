from sqlalchemy import Column, Integer, String
from app.database import Base


class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    age = Column(Integer)
    gender = Column(String(10))
    disease = Column(String(100))


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(
        String(100),
        unique=True,
        nullable=False
    )

    email = Column(
        String(100),
        unique=True,
        nullable=False
    )

    password = Column(
        String(255),
        nullable=False
    )

    role = Column(
    String(20),
    default="user"
    )



#Predicton History 
class PredictionHistory(Base):
    __tablename__ = "prediction_history"

    id = Column(Integer, primary_key=True, index=True)

    user_email = Column(
        String(100),
        nullable=False
    )

    glucose = Column(Integer)

    prediction = Column(Integer)

    result = Column(String(50))

    

