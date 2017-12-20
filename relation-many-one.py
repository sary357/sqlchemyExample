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
    address_id=Column(Integer, ForeignKey('address.id'))
    address=relationship('Address')

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
    address=Column(String(60), nullable=False)

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

    user_5=User('user_5','username5','password_5'.encode('utf-8'))
    user_6=User('user_6','username6','password_6'.encode('utf-8'))

    address_1=Address('我愛台妹')
    user_5.address=address_1
    user_6.address=address_1
    session.add(user_5)
    session.add(user_6)
    session.commit()

    # query
    user_x=session.query(User).filter_by(name='user_5').first()
    print(user_x.name)
    print(user_x.address)
