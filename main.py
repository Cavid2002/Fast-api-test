from fastapi import FastAPI
from werkzeug.security import generate_password_hash, check_password_hash
from models import User,session
from auth import *

app = FastAPI()


data = [
	{"name" : "David", "surname": "Anderson", "age" : 22},
	{"name" : "Simon", "surname": "Henriks", "age" : 21},
	{"name" : "Samantha", "surname": "Shane", "age" : 21}
]


@app.route("/", methods=['GET', 'POST'])
async def login(user_data: UserSignInBase):
	user = session.query(User).filter(User.mail == user_data.email).first()
	if(user == None):
		return {"msg" : "User doesn't exists"}
	
	if(check_password_hash(user.password, user_data.password)):
		encodeJWT(user.id)
		
