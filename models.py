from datetime import datetime
from enum import Enum
from typing import List, Optional
from sqlmodel import Field, SQLModel, Relationship


METRIC_DICT = {
    'DistanceWalkingRunning': {'unit': 'mi', 'new_unit': 'meter(s)', 'dtype': float, 'f': lambda x: x * 1609, 'indicator': 'sum'},
    'AppleStandTime': {'unit': 'min', 'new_unit': 'min', 'dtype': int, 'f': lambda x: x / 60, 'indicator': 'sum'},
    'HeartRate': {'unit': 'count/min', 'new_unit': 'count/min', 'dtype': int, 'indicator': 'mean'}
}


class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    date_of_birth: datetime
    height: float  # cms
    weight: float  # kg
    name: str
    email: str
    created_datetime: datetime = Field(default_factory=datetime.now)
    updated_datetime: datetime = Field(default_factory=datetime.now)


class MetricEntry(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int | None = Field(default=None, foreign_key="user.id")
    metric: str
    value: float
    max_value: float
    min_value: float
    # window: Frequency
    start_date: datetime


class Lab(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    date: str = Field(index=True, default_factory=datetime.now)
    user_id: int | None = Field(default=None, foreign_key="user.id")
    results: List["Result"] = Relationship(back_populates="lab")


class Result(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    lab_id: int = Field(foreign_key="lab.id")
    parameter: str 
    value: float
    lab: Lab = Relationship(back_populates="results")
