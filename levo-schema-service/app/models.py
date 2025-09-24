from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
import datetime

class Application(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    services: List["Service"] = Relationship(back_populates="application")

class Service(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    application_id: Optional[int] = Field(default=None, foreign_key="application.id")
    schemas: List["SchemaRecord"] = Relationship(back_populates="service")
    application: Optional[Application] = Relationship(back_populates="services")

class SchemaRecord(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    application_id: int
    service_id: Optional[int] = None
    version: int
    filename: str
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    service: Optional[Service] = Relationship(back_populates="schemas")
