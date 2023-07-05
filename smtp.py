import smtplib
from os import getenv


sender = "mygalerynoreply@gmail.com"
password = getenv('PASSWORD')
server = smtplib.SMTP('smtp.gmail.com', 587)


def account_creatin_token(reciver: str, token: str):
    global sender, password, server
    server.starttls()
    server.login(sender, password)
    msg = f'''Account creation link: {token}\n 
    if you are not requested this message ignore it.\n'''
    server.sendmail(from_addr=sender, to_addrs= [reciver])


    
def password_recover_token(reciver: str, token: str):
    global sender, password, server
    server.starttls()
    server.login(sender, password)
    msg = f'''Password recovery link: {token}\n 
    if you are not requested this message ignore it.\n'''
    server.sendmail(from_addr=sender, to_addrs= [reciver])
