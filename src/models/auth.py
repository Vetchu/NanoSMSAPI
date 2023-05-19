from pydantic import BaseModel


class Auth(BaseModel):
    auth: str
