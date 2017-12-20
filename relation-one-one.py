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
    user=relationship('User', backref=backref('address', uselist=False ,order_by=id))

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

    user_3=User('user_3','username3','password_3'.encode('utf-8'))
    user_4=User('user_4','username4','password_4'.encode('utf-8'))

    user_3.address=Address('測試31')
    user_4.address=Address('測試41')
    session.add(user_3)
    session.add(user_4)
    session.commit()

    # query
    user_x=session.query(User).filter_by(name='user_3').first()
    print(user_x.name)
    print(user_x.address)
