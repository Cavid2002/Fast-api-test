from sqlalchemy import String, Integer, ForeignKey, Column, TIMESTAMP,create_engine
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
    mail = Column(String(250), nullable=False)
    password = Column(String(250), nullable=False)
    create_time = Column(TIMESTAMP, default=datetime.utcnow())

    def __repr__(self):
        return f"{self.id} {self.username}"


    def __init__(self, username, mail, password):
        self.username = username
        self.mail = mail
        self.password = password
    
    def save(self):
        session.add(self)
        session.commit()



Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)