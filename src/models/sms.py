from typing import Type

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


def map_to_orm(sms: SMS) -> SMSOrm:
    return SMSOrm(message=sms.message, sender=sms.sender)


def insert_sms(Session, sms: SMS) -> int:
    sms_orm = map_to_orm(sms)

    session = Session()
    session.add(sms_orm)
    session.commit()
    session.flush()
    # session.close()
    return sms_orm.id


def get_all_sms(Session) -> list[Type[SMSOrm]]:
    session = Session()
    records: list[Type[SMSOrm]] = session.query(SMSOrm).all()
    session.close()
    # records_mapped: list[SMS] = [SMS.from_orm(record) for record in records]
    return records
