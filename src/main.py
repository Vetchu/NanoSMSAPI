from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine, desc, asc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.scoping import ScopedSession
from starlette.middleware.cors import CORSMiddleware

from src.models.sms import SMS
from src.utils.const import database_path
from src.utils.utils import register_exception

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = create_engine(f"sqlite:///{database_path}")

Session = ScopedSession(sessionmaker())
Session.configure(bind=engine)
session = Session()

register_exception(app)


@app.get("/")
async def root():
    return {"message": "Hello World"}


def get_books_by_publishers(session, ascending=True) -> list:
    """Get a list of publishers and the number of books they've published"""
    if not isinstance(ascending, bool):
        raise ValueError(f"Sorting value invalid: {ascending}")

    direction = asc if ascending else desc

    return direction
    # return (
    #     session.query(Publisher.name, func.count(Book.title).label("total_books"))
    #     .join(Publisher.books)
    #     .group_by(Publisher.name)
    #     .order_by(direction("total_books"))
    # )


class Auth(BaseModel):
    auth: str


@app.post("/sms")
async def receive_sms(sms: SMS):  # , auth: Auth):
    print(sms)
    # if not auth.auth == auth_var:
    #     return None

    books_by_publisher = get_books_by_publishers(session, ascending=False)
    print(books_by_publisher)

    return {"message": "OK"}
