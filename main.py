from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, HTMLResponse, JSONResponse 
from werkzeug.security import generate_password_hash, check_password_hash
from models import User,session
from auth import *

app = FastAPI()


@app.post("/sign-up")
async def signUp(new_user: UserCreateBase):
    if(session.query(User).filter(User.username == new_user.username).first()):
        return JSONResponse({ "msg" : "Username already taken"})
    if(session.query(User).filter(User.mail == new_user.email).first()):
        return JSONResponse({ "msg" : "Email already in use"})
    
    user = User(username=new_user.username,
                password=generate_password_hash(new_user.password),
                age = new_user.age,
                gender=new_user.gender,
                mail=new_user.email)
    user.save()
    res = JSONResponse({"msg" : "New User added"})
    return res




@app.post("/")
async def login(user_data: UserSignInBase):
    user = session.query(User).filter(User.mail == user_data.email).first()
    print(user)
    if(user == None):
        return JSONResponse({"msg" : "User doesn't exists"})
    
    if(check_password_hash(user.password, user_data.password)):
        content = encodeJWT(user.id)
        response = JSONResponse({"msg" : "Signed in"})
        response.set_cookie(key="access_token", 
                            value=content["access_token"], 
                            max_age= 3600 * ACCESS_TOKEN_EXPIRE_HOURS)
        return response        


@app.get("/main")
async def main(request: Request):
    cookie = request.cookies.get("access_token")
    print(cookie)
    if(cookie == None):
        return JSONResponse({"msg" : "You are not authorized!"}, status_code=401)
    else:
        decodeJWT(cookie)
        current_user = User.get_user_by_id(cookie["user_id"])
        res = { "Username" : current_user.name, 
               "Age" : current_user.age, 
               "Gender" : current_user.age}
        return JSONResponse(res)
        
			
