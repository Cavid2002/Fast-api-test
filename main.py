from fastapi import FastAPI
from pydantic import BaseModel, Field
from werkzeug.security import generate_password_hash, check_password_hash
from models import User

app = FastAPI()


data = [
	{"name" : "David", "surname": "Anderson", "age" : 22},
	{"name" : "Simon", "surname": "Henriks", "age" : 21},
	{"name" : "Samantha", "surname": "Shane", "age" : 21}
]


class UserBase(BaseModel):
	username: str
	gender: str
	age: int
	email: str
	password: str

@app.get("/")
def homepage():
    msg: str = "Hello world"
    return msg


# @app.get("/user_id/{id}")
# def user(id: str):
#     res = data[id]
#     return {"code" : 200, "user" : res}

@app.get("/user_id/{id}")
def change_user(id: int, new_name: str):
    data[id - 1]["name"] = new_name
    return {"code" : 200, "users" : data}

@app.post("/user_id/{id}")
def change_user_by_post(id: int, new_user: str):
    data[id - 1]["name"] = new_user
    return {"code" : 200, "users" : data}

@app.post("/add_user")
def add_user(new_user: UserBase):
	user = User(username = new_user.username, 
             mail = new_user.email,
             age = new_user.age,
             password = generate_password_hash(new_user.password),
             gender = new_user.gender)
	user.save()
	return {"status" : 200}



