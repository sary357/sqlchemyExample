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


if __name__ == '__main__':

    ## pymysql
    engine=create_engine('mysql+pymysql://test:abc123@localhost/testdatabase?charset=utf8', echo=True)

    # insert 
    Base.metadata.create_all(engine)
    Session=sessionmaker(bind=engine)
    session=Session()
    #user_1=User('sary357', 'fuming','password'.encode('utf-8'))
    #session.add(user_1)
    #session.commit()
    #row=session.query(User).filter_by(name='sary357').first()
    #print(row)

    # query
    rows=session.query(User).from_statement('select * from users where id=:id and name=:name').params(id=4).params(name='sary357') #.params(id=1)
    print("-----------------------")
    for r in rows:
        print("-----------------------")
 
        print(r.account)

    print("+-+-+-+-+-+-+-+-+-+-+")
    for r in session.query(User):
        print(r.name)
        print(r.id)

    print("+-+-+-+-+-+-+-+-+-+-+")
    for r in session.query(User.name).filter_by(id=4).filter_by(name='sary357'):
        print(r.name)

    print("+-+-+-+-+-+-+-+-+-+-+")
    for r in session.query(User.id,User.name).filter_by(name='sary357').order_by(User.id.desc()):
        print(str(r.id)+":"+r.name)

    print("+-+-+-+-+-+-+-+-+-+-+")
    for r in session.query(User.id,User.name).filter_by(name='sary357').group_by(User.name):
        print(str(r.id)+":"+r.name)

    print("+-+-+-+-+-+-+-+-+-+-+")
    print("count:"+str(session.query(User.id,User.name).filter_by(name='sary357').count()))

    # delete
    print("+-+-+-+-+-+-+-+-+-+-+")
    user_2=User('user_2','account2','password2'.encode('utf-8'))
    session.add(user_2)
    session.commit()
    print("user_2 count:"+str(session.query(User.id,User.name).filter_by(name='user_2').count()))
    
    print("+-+-+-+-+-+-+-+-+-+-+")
    affected_rows=session.query(User).filter_by(name='user_2').delete()
    session.commit()
    print(affected_rows)

    # update
    print("+-+-+-+-+-+-+-+-+-+-+")
    user_3=User('user_3','account_3','password2'.encode('utf-8'))
    #session.add(user_3)
    #session.commit()
    affected_rows=session.query(User).filter_by(name='user_3').update({'account':'account3_4'})
    session.commit()
    print(affected_rows)
