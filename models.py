from sqlalchemy import String, Integer, ForeignKey, Column, TIMESTAMP,create_engine,Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from os import getenv


engine = create_engine(getenv("DATABASE_URI"), echo=True)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()



class User(Base):
    __tablename__ = "User"
    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    age = Column(Integer, nullable=False) 
    gender = Column(String(1), nullable=False)
    mail = Column(String(250), nullable=False)
    password = Column(String(250), nullable=False)
    create_time = Column(TIMESTAMP, default=datetime.utcnow())
    

    def __repr__(self):
        return f"{self.id} {self.username}"


    def __init__(self, username, mail, password, age, gender):
        self.username = username
        self.mail = mail
        self.password = password
        self.age = age
        self.gender = gender
        
        
    def save(self):
        session.add(self)
        session.commit()
        
    @staticmethod
    def get_user_by_id(id: str):
        user = session.query(User).filter(User.id == id).first()
        return user


class Comment(Base):
    __tablename__ = "Comment"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer,ForeignKey("User.id"))
    comment_body = Column(Text)
    creation_time = Column(TIMESTAMP, default=datetime.utcnow())  
    
    def __init__(self, user_id, comment_body):
        self.user_id = user_id
        self.comment_body = comment_body
    
    def __repr__(self):
        return f"{self.id} {self.comment_body}"

    def save(self):
        session.add(self)
        session.commit()      
    
    @staticmethod
    def get_comment_list(comments) -> list:
        l = []
        for comm in comments:
            l.append(comm.comment_body)
        
        return l

