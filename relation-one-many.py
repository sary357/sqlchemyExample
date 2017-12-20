#!/usr/bin/env python 
# -*- coding: utf-8 -*-
import hashlib
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm import sessionmaker
from sqlalchemy import desc 
from sqlalchemy import func
Base=declarative_base()

class User(Base):
    __tablename__='users'

    id=Column(Integer, primary_key=True)
    name=Column(String(20))
    account=Column(String(20))
    password=Column(String(40))

    def __init__(self, name, account, password):
        self.name=name
        self.account=account
        self.password=hashlib.sha1(password).hexdigest()

    def __repr__(self):
        return "User('{}','{}', '{}')".format(
            self.name,
            self.account,
            self.password
        )

class Address(Base):
    __tablename__='address'
    id=Column(Integer, primary_key=True)
    user_id=Column(Integer, ForeignKey('users.id'))
    address=Column(String(60), nullable=False)
    user=relationship('User', backref=backref('address', order_by=id))

    def __init__(self, address):
        self.address = address

    def __repr__(self):
        return "Address('{}')".format(self.address)
    
if __name__ == '__main__':

    ## pymysql
    engine=create_engine('mysql+pymysql://test:abc123@localhost/testdatabase?charset=utf8', echo=True)

    # insert 
    Base.metadata.create_all(engine)
    Session=sessionmaker(bind=engine)
    session=Session()

    user_1=User('user_1','username1','password_1'.encode('utf-8'))
    user_2=User('user_2','username2','password_2'.encode('utf-8'))

    user_1.address=[Address('測試11')]
    user_2.address=[Address('測試21'),Address('測試22')]
    session.add(user_1)
    session.add(user_2)
    session.commit()

    # query
    user_x=session.query(User).filter_by(name='user_2').first()
    print(user_x.name)
    for a in user_x.address:
        print(a.address)
