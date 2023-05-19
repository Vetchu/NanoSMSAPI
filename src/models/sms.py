from pydantic import BaseModel
from sqlalchemy import Column, String
from sqlalchemy.dialects.sqlite import INTEGER

from src.db.base import Base


class SMSOrm(Base):
    __tablename__ = "sms"

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    message = Column(String)
    sender = Column(String)


class SMS(BaseModel):
    message: str
    sender: str

    class Config:
        orm_mode = True
