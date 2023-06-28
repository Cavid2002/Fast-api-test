from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()


data = [
	{"name" : "David", "surname": "Anderson", "age" : 22},
	{"name" : "Simon", "surname": "Henriks", "age" : 21},
	{"name" : "Samantha", "surname": "Shane", "age" : 21}
]


class User(BaseModel):
	name: str
	surname: str
	age: int = Field(ge=0)



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
def add_user(new_user: User):
	data.append(new_user)
	return {"status" : 200, "data" : data}



