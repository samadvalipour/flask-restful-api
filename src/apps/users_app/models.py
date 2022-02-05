from src import db
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import validates
from werkzeug.security import generate_password_hash,check_password_hash
class User(db.Model):
    __tablename__="users"
    id = Column(Integer(),primary_key=True)
    username = Column(String(32), unique=True, nullable=False)
    password = Column(String(128),unique=False,nullable=False)

    @validates('password')
    def validate_password(self,key,value):
        if value == None:
            raise ValueError("password cant be null")
        if len(value)<8:
            raise ValueError("password should be at least 8 characters!")
        return generate_password_hash(value)
    @validates('username')
    def validate_username(self,key,value):
        if value == None:
            raise ValueError("usarname cant be null")
        if not value.isidentifier():
            raise ValueError("username should be identifier")
        return value
    def check_password(self,password):
        return check_password_hash(self.password,password)