from sqlalchemy import Column,Integer,String,Boolean,DateTime
from database import Base

class User(Base):
    __tablename__="Users"
    id=Column(Integer,primary_key=True,index=True)
    email=Column(String,nullable=False,index=True)
    password=Column(String,nullable=False)
    otp=Column(Integer,nullable=True)
    is_verified=Column(Boolean,default=False)
    is_Active=Column(Boolean,nullable=False,default=True)
    reset_token=Column(String,nullable=True)
    reset_token_expiry=Column(DateTime(timezone=True),nullable=True)