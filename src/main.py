import logging
import secrets
from typing import Annotated

from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from starlette import status

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

security = HTTPBasic()

auth = {"login": b"iksde", "password": b"iksde2"}


def get_current_username(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)]
):
    current_username_bytes = credentials.username.encode("utf8")
    is_correct_username = secrets.compare_digest(current_username_bytes, auth["login"])
    current_password_bytes = credentials.password.encode("utf8")
    is_correct_password = secrets.compare_digest(
        current_password_bytes, auth["password"]
    )
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/sms")
async def receive_sms(sms: SMS, auth: Auth):
    logging.info(sms)
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
async def list_sms(username: Annotated[str, Depends(get_current_username)]):
    print(username)
    sms = get_all_sms(Session)

    return {"smsList": sms}
