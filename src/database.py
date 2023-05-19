from typing import Type

from sqlalchemy.orm import sessionmaker

from db.base import Base
from main import engine
from models.sms import SMS, SMSOrm

Session = sessionmaker(bind=engine)


def create_tables():
    Base.metadata.create_all(bind=engine)


def map_to_orm(sms: SMS) -> SMSOrm:
    return SMSOrm(message=sms.message, sender=sms.sender)


def insert_sms(sms: SMS):
    sms_orm = map_to_orm(sms)

    session = Session()
    session.add(sms_orm)
    session.commit()
    session.close()


def get_all_sms() -> list[Type[SMSOrm]]:
    session = Session()
    records: list[Type[SMSOrm]] = session.query(SMSOrm).all()
    session.close()
    # records_mapped: list[SMS] = [SMS.from_orm(record) for record in records]
    return records
