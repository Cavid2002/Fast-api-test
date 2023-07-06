from pydantic import BaseModel, Field
from os import urandom
from time import time
from os import getenv,urandom
import jwt


SECRET_KEY = getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 24

class UserCreateBase(BaseModel):
	username: str
	age: int
	gender: str
	email: str
	password: str


class UserSignInBase(BaseModel):
    email: str
    password: str


class CommentAddBase(BaseModel):
    comment: str
    

def encodeJWT(key: str, val) -> dict:
    payload = {
        key : val,
    }
    token = jwt.encode(payload=payload, key=SECRET_KEY, algorithm=ALGORITHM)
    return {"encoded_token" : token}



def decodeJWT(token: str) -> dict:
    decoded_token = jwt.decode(jwt = token, key=SECRET_KEY, algorithms=ALGORITHM)
    return decoded_token



