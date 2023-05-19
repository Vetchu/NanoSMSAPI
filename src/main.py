from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.db.base import Base
from src.models.auth import Auth
from src.models.sms import SMS, get_all_sms, insert_sms
from src.utils.const import database_path, auth_var

app = FastAPI()

engine = create_engine(f"sqlite:///{database_path}")
Base.metadata.create_all(engine)

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()


# register_exception(app)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/sms")
async def receive_sms(sms: SMS, auth: Auth):  # , auth: Auth):

    print(sms)
    if not sms:
        raise HTTPException(status_code=404, detail="Item not provided")
    if not auth.auth == auth_var:
        raise HTTPException(status_code=401, detail="Unauthorized")

    insert_status = insert_sms(Session, sms)
    return {
        "id": insert_status,
        "sender": sms.sender,
        "message": sms.message,
    }


@app.get("/sms")
async def list_sms():
    sms = get_all_sms(Session)

    return {"message": sms}
