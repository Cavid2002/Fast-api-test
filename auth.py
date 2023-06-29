from pydantic import BaseModel, Field
from os import urandom
from time import time

import jwt


SECRET_KEY = urandom(32).hex()
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MIN = 30

class UserCreateBase(BaseModel):
	gender: str
	age: int
	username: str
	email: str
	password: str


class UserSignInBase(BaseModel):
    email: str
    password: str
 


def encodeJWT(userID: str):
    payload = {
        "user_id" : userID,
        "expire":  time() + 10
    }
    token = jwt.encode(payload=payload, key=SECRET_KEY, algorithm=ALGORITHM)
    return {"access token" : token}



def decodeJWT(token: str):
    decoded_token = jwt.decode(jwt = token, key=SECRET_KEY, algorithms=ALGORITHM)
    if(decoded_token["expire"] <= time()):
        return decoded_token
    else:
        return None