from fastapi import FastAPI,Cookie
from fastapi.responses import RedirectResponse, HTMLResponse
from werkzeug.security import generate_password_hash, check_password_hash
from models import User,session
from auth import *

app = FastAPI()


@app.post("/sign-up")
async def signUp(new_user: UserCreateBase):
    if(session.query(User).filter(User.username == new_user.username).first()):
        return { "msg" : "Username already taken"}
    if(session.query(User).filter(User.email == new_user.email).first()):
        return { "msg" : "Email already in use"}
    
    user = User(username=new_user.username,
                password=generate_password_hash(new_user.password),
                age = new_user.age,
                gender=new_user.gender)
    user.save()




@app.post("/")
async def login(user_data: UserSignInBase, cook: Cookie()):
	user = session.query(User).filter(User.mail == user_data.email).first()
	if(user == None):
		return {"msg" : "User doesn't exists"}
	
	if(check_password_hash(user.password, user_data.password)):
		encodeJWT(user.id)
		return {"msg" : "User logged in"}


@app.get("/main")
async def main():
    pass
			
