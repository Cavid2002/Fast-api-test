import smtplib
from os import getenv


sender = getenv('EMAIL_ADDRESS')
password = getenv('PASSWORD')
server = smtplib.SMTP('smtp.gmail.com', 587)


def send_creation_token(reciver: str, domain: str, token: str):
    global sender, password, server
    server.starttls()
    server.login(sender, password)
    subject = "Account creation"
    msg = f"""Subject: {subject}\n\nAccount creation link: {domain}/verify/{token}
    if you are not requested this message ignore it.\n"""
    server.sendmail(sender, reciver, msg)


    
def send_recover_token(reciver: str, token: str):
    global sender, password, server
    server.starttls()
    server.login(sender, password)
    subject = "Password recovery"
    msg = f"""Subject: {subject}\n\nPassword recovery link: {token}
    if you are not requested this message ignore it.\n"""
    server.sendmail(sender, reciver, msg)
