import re
from src import db
import datetime as dt
from sqlalchemy import Column,Integer,DateTime,String,Text
from sqlalchemy.orm import validates
from werkzeug.security import generate_password_hash,check_password_hash
#
class Site(db.Model):
    __tablename__="sites"
    id = Column(Integer(),primary_key=True)
    create_date = Column(DateTime(),nullable=False,unique=False,default=dt.datetime.utcnow)
    name = Column(String(32),nullable=False,unique=False)
    description = Column(Text(),nullable=True,unique=False)
    address = Column(String(128),nullable=False,unique=True)
    icon = Column(String(256),unique=False,nullable=True)

    @validates('name')
    def validation_name(self,key,value):
        if value is None:
            raise ValueError('name cant be None')
        return value
    @validates('address')
    def valdation_address(self,key,value):
        if value is None:
            raise ValueError('address cant be None')
        regex = re.compile(
            r'^(?:http|ftp)s?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        if not re.fullmatch(regex,value):
            raise ValueError('site address is invalid')
        return value