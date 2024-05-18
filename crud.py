from datetime import datetime
from enum import Enum
import os
from typing import List, Optional
from sqlmodel import Session, select, create_engine
import pandas as pd
from pydantic import BaseModel
from .database import engine
from .models import Lab, Result, User


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)


METRIC_DICT = {
    'DistanceWalkingRunning': {'unit': 'mi', 'new_unit': 'meter(s)', 'dtype': float, 'f': lambda x: x * 1609, 'indicator': 'sum'},
    # 'AppleStandTime': {'unit': 'min', 'new_unit': 'min', 'dtype': int, 'f': lambda x: x / 60, 'indicator': 'sum'},
    'HeartRate': {'unit': 'count/min', 'new_unit': 'count/min', 'dtype': int, 'indicator': 'mean'},
    'VO2Max' : {'unit': 'mL/min·kg', 'new_unit': 'mL/min·kg', 'dtype': float, 'indicator': 'mean'}
}

KEYWORDS_DICT = {
"ERITROCITOS": {"unit": "10^6/uL", "min_value": 4.5, "max_value": 6.5},
"RECUENTO DE ERITROCITOS": {"unit": "10^6/uL", "min_value": 4.5, "max_value": 6.5},
"HEMOGLOBINA": {"unit": "g/dL", "min_value": 13.0, "max_value": 18.0},
"HEMATOCRITO": {"unit": "%", "min_value": 40.0, "max_value": 54.0},
"VCM": {"unit": "fL", "min_value": 80.0, "max_value": 100.0},
"CHM": {"unit": "pg", "min_value": 27.0, "max_value": 33.0},
"CHCM": {"unit": "g/dL", "min_value": 32.0, "max_value": 36.0},
"ADE": {"unit": "%", "min_value": 11.5, "max_value": 14.5},
"PLAQUETAS": {"unit": "10^3/uL", "min_value": 150.0, "max_value": 450.0},
"LEUCOCITOS": {"unit": "10^3/uL", "min_value": 4.0, "max_value": 11.0},
"VPM": {"unit": "fL", "min_value": 7.0, "max_value": 11.0},
"NEUTROFILOS": {"unit": "%", "min_value": 40.0, "max_value": 70.0},
"EOSINOFILOS": {"unit": "%", "min_value": 0.0, "max_value": 5.0},
"BASOFILOS": {"unit": "%", "min_value": 0.0, "max_value": 2.0},
"LINFOCITOS": {"unit": "%", "min_value": 20.0, "max_value": 40.0},
"MONOCITOS": {"unit": "%", "min_value": 2.0, "max_value": 10.0},
"NEUTROFILOS": {"unit": "10^3/uL", "min_value": 2.0, "max_value": 7.5},
"EOSINOFILOS": {"unit": "10^3/uL", "min_value": 0.0, "max_value": 0.5},
"BASOFILOS": {"unit": "10^3/uL", "min_value": 0.0, "max_value": 0.2},
"LINFOCITOS": {"unit": "10^3/uL", "min_value": 1.0, "max_value": 4.0},
"MONOCITOS": {"unit": "10^3/uL", "min_value": 0.1, "max_value": 1.0},
"NITROGENO": {"unit": "mg/dL", "min_value": 7.0, "max_value": 20.0},
"SICLEMIA": {"unit": "mg/dL", "min_value": 70.0, "max_value": 99.0},
"GLOMERULAR": {"unit": "mL/min/1.73m^2", "min_value": 90.0, "max_value": 120.0},
"COLESTEROL": {"unit": "mg/dL", "min_value": 0.0, "max_value": 200.0},
"COLESTEROL TOTAL": {"unit": "mg/dL", "min_value": 0.0, "max_value": 200.0},
"TRIGLICERIDOS": {"unit": "mg/dL", "min_value": 0.0, "max_value": 150.0},
"ALANINO": {"unit": "U/L", "min_value": 7.0, "max_value": 55.0},
"ASPARTATO": {"unit": "U/L", "min_value": 8.0, "max_value": 48.0},
"AMILASA": {"unit": "U/L", "min_value": 40.0, "max_value": 140.0},
"LIPASA": {"unit": "U/L", "min_value": 0.0, "max_value": 160.0},
"HORMONAS": {"unit": "mIU/L", "min_value": 0.4, "max_value": 4.0},
"TSH": {"unit": "mIU/L", "min_value": 0.4, "max_value": 4.0},
"INSULINA": {"unit": "uIU/mL", "min_value": 2.6, "max_value": 24.9},
"PROTEINAS": {"unit": "g/dL", "min_value": 6.0, "max_value": 8.3},
"PROTEINA": {"unit": "g/dL", "min_value": 6.0, "max_value": 8.3},
"CREATININA": {"unit": "mg/dL", "min_value": 0.6, "max_value": 1.2},
"ERITROSEDIMENTACION": {"unit": "mm/h", "min_value": 0.0, "max_value": 20.0},
"TESTOSTERONA": {"unit": "ng/dL", "min_value": 300.0, "max_value": 1000.0}}


class Frequency(str, Enum):
    month = "month"
    week = "week"


class MetricSchema(BaseModel):
    metric: str
    unit: str
    value: float
    max_value: float
    min_value: float


class MedicalProfile(BaseModel):
    user: User
    data: List[MetricSchema]


class ResultDetail(BaseModel):
    id: int
    parameter: str
    value: float
    unit: Optional[str] 


class LabDetail(BaseModel):
    id: int
    user_id: int
    date: datetime
    results: list[ResultDetail]


def get_user_data_in_window(user_id: int, window: Frequency) -> list[MetricSchema]:
    """
    for file_name in os.listdir('.'):
        file_path = os.path.join('.', file_name)
        print(file_path)
        # Read the file using pandas
        # df = pd.read_csv(file_path)
        # Append the dataframe to the list
        # dfs.append(df)
    
    return []
    """

    data_list = list()
    for metric, info in METRIC_DICT.items():
        file_path = f'aiter/data/{user_id}/{metric}_{window.value}.csv'
        try:
            df = pd.read_csv(file_path)
        except FileNotFoundError:
            print(f'Unable to find: {file_path}')
            pass
        else:
            new_unit = info.get('new_unit')
            metric_data = MetricSchema(
                metric=metric,
                unit=new_unit,
                value=df[new_unit].mean(),
                max_value=df[new_unit].max(),
                min_value=df[new_unit].min()
            )
            data_list.append(metric_data)
    
    return data_list







def get_user_data(user_id: int, window: Frequency):
    with Session(engine) as session:
        statement = select(User).where(User.id == user_id)
        results = session.exec(statement)
        user = results.first()
    
    if user:
        return MedicalProfile(user=user, data=get_user_data_in_window(
            user_id=user.id,
            window=window
        ))
    
    # return user


def get_user_by_email(email: str):
    with Session(engine) as session:
        statement = select(User).where(User.email == email)
        results = session.exec(statement)
        for user in results:
            print(user)
    
    return results


def create_user(user: User) -> User:

    with Session(engine) as session:  
        session.add(user)
        session.commit()
    
    print(user)
    return user


def get_lab_results(lab_id: int, session) -> list[ResultDetail]:
    statement = select(Result).where(Result.lab_id == lab_id)
    results = session.exec(statement)
    results_list = list()
    for r in results:
        info = KEYWORDS_DICT.get(r.parameter.upper())
        rd = ResultDetail(
        unit=info['unit'] if info else '',
        id=r.id,
        parameter=r.parameter,
        value=r.value
        )
        results_list.append(rd)
    return results_list


def get_lab(lab_id: int) -> LabDetail:
    with Session(engine) as session:
        statement = select(Lab).where(Lab.id == lab_id)
        results = session.exec(statement)
        lab = results.first()

        return LabDetail(
            id=lab_id,
            user_id=lab.user_id,
            date=lab.date,
            results=get_lab_results(lab_id, session),
        )

    


"""
def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
"""
