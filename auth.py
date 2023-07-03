from pydantic import BaseModel, Field
from os import urandom
from time import time
from os import getenv
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
 


def encodeJWT(userID: str):
    payload = {
        "user_id" : userID,
    }
    token = jwt.encode(payload=payload, key=SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token" : token}



def decodeJWT(token: str):
    decoded_token = jwt.decode(jwt = token, key=SECRET_KEY, algorithms=ALGORITHM)
    return decoded_token