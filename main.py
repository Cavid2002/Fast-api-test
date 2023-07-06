from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, HTMLResponse, JSONResponse 
from werkzeug.security import generate_password_hash, check_password_hash
from models import User,Comment,session
from smtp import send_creation_token, send_recover_token
from auth import *

DOMAIN = "127.0.0.1:8000"
app = FastAPI()


async def get_user(token: str) -> User:
    decoded = decodeJWT(token)
    user = User.get_user_by_id(decoded["user_id"])
    return user


@app.post("/sign-up")
async def signUp(new_user: UserCreateBase):
    print("HELLO")
    if(session.query(User).filter(User.username == new_user.username).first()):
        return JSONResponse({ "msg" : "Username already taken"})
    if(session.query(User).filter(User.mail == new_user.email).first()):
        return JSONResponse({ "msg" : "Email already in use"})
    
    tk = urandom(20).hex()
    send_creation_token(new_user.email, DOMAIN, tk)
    user_data = {
        "username" : new_user.username,
        "password" : generate_password_hash(new_user.password),
        "age" : new_user.age,
        "gender" : new_user.gender,
        "email" : new_user.email 
    }

    data_token = encodeJWT("user_data", user_data)
    verification_token = encodeJWT("vefirication_token", tk)
    response = JSONResponse({"msg" : "Check your email"})
    response.set_cookie(key = "data_token", 
                        value = data_token["encoded_token"], 
                        max_age = 1000)
    response.set_cookie(key = "verify", value = verification_token, max_age = 1000)
    return response



@app.get("/verify/{token}")
async def creation_verification(token: str, request: Request):
    cookie_token = request.cookies.get("verify")
    if(cookie_token == None):
        return JSONResponse({ "msg" : "No token found"})
    decoded = decodeJWT(cookie_token)
    print("HELLO", cookie_token)
    if(decoded['vefirication_token'] != token):
        return JSONResponse({ "msg" : "Invalid token"})
    decoded_data = decodeJWT(request.cookies.get("data_token"))
    user_data = decoded_data["user_data"]
    user = User(username=user_data["username"],
                password=generate_password_hash(user_data["password"]),
                age=user_data["age"],
                gender=user_data["gender"],
                mail=user_data["email"])
    user.save()
    return JSONResponse({ "msg" : "New user is added!"})





@app.post("/")
async def login(user_data: UserSignInBase):
    user = session.query(User).filter(User.mail == user_data.email).first()
    if(user == None):
        return JSONResponse({"msg" : "User doesn't exists"})
    
    if(check_password_hash(user.password, user_data.password)):
        content = encodeJWT("user_id",user.id)
        response = JSONResponse({"msg" : "Signed in"})
        response.set_cookie(key = "login_token", 
                            value = content["encoded_token"], 
                            max_age = 3600 * ACCESS_TOKEN_EXPIRE_HOURS)
        return response
    response = JSONResponse({ "msg" : "Enter email and password" }, status_code=200)
    return response
            


@app.get("/main")
async def main(request: Request):
    cookie = request.cookies.get("login_token")
    if(cookie == None):
        return JSONResponse({"msg" : "You are not authorized!"}, status_code=401)
    current_user = get_user(cookie)
    comments = session.query(Comment).filter(Comment.user_id == current_user.id)
    comment_list = []
    for com in comments:
        comment_list.append(com.comment_body)
    res = { "username" : current_user.username, 
           "age" : current_user.age, 
           "gender" : current_user.gender,
           "comments" : comment_list}
    return JSONResponse(res)



@app.get("/logout")
async def logout():
    res = JSONResponse({ "msg" : "you logged out"})
    res.delete_cookie("login_token")
    return res
        
			
@app.post("/main/comment")
async def comment(comment: CommentAddBase, request: Request):
    cookie = request.cookies.get("encoded_token")
    if(cookie == None):
        return JSONResponse({ "msg" : "You are not authorized!" }, status_code=401)
    current_user = get_user(cookie)
    new_comment = Comment(user_id=current_user.id, comment_body=comment.comment)
    new_comment.save()
    return JSONResponse({ "msg" : "comment added!" }, status_code=200)