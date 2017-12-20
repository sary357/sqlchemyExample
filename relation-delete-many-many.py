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
from sqlalchemy import Table
Base=declarative_base()

association_table=Table(
    'association',
    Base.metadata,
    Column('table_a_id', Integer, ForeignKey('table_a.id')),
    Column('table_b_id', Integer, ForeignKey('table_b.id'))
)

class A(Base):
    __tablename__='table_a'
    id=Column(Integer, primary_key=True)
    aname=Column(String(20))
    children=relationship('B', secondary=association_table)
    def __init__(self, name):
        self.aname=name

class B(Base):
    __tablename__='table_b'
    id=Column(Integer, primary_key=True)
    bname=Column(String(20))
    def __init__(self, name):
        self.bname=name

    
if __name__ == '__main__':

    ## pymysql
    engine=create_engine('mysql+pymysql://test:abc123@localhost/testdatabase?charset=utf8', echo=True)

    # insert 
    Base.metadata.create_all(engine)
    Session=sessionmaker(bind=engine)
    session=Session()
    session.query
    #affected_rows=session.query(B).filter_by(bname='b1').delete()
    #session.commit()
    #print(affected_rows)
#    b_list=[B('b1'), B('b2'), B('b3'), B('b4')]
#    a_1=A('a1')
#    a_2=A('a2')

#    a_1.children=b_list
#    a_2.children=b_list
#    session.add(a_1)
#    session.add(a_2)
#    session.commit()
    print("----------------------------------------")
    a=session.query(A).filter_by(aname='a2').first()
    b=a.children
    print(a.id)
    print('  B:' , b)
    index=0
    while index < len(b):
        if b[index].bname=='b3':
            b.remove(b[index])
        index+=1
    print('  B:' , b)
    a.child=b
    session.add(a)
    session.commit()
    
    print("----------------------------------------")
    # query
    for a in session.query(A):
        print('A:' , a.id, 'has the following relationshop:')
        for b in a.children:
            print('    B:', b.id)

    # delete  1 record
    
