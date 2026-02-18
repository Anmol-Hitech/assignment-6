from pydantic import BaseModel,EmailStr

class UserSchema(BaseModel):
    name:str
    email:EmailStr
    password:str
class UserLogin(BaseModel):
    email:EmailStr
    password:str
class Token(BaseModel):
    access_token:str
    token_type:str

class UserProfile(BaseModel):
    id:int
    email:str

class VerifyOtp(BaseModel):
    otp:int

class ChangePass(BaseModel):
    old_password:str
    new_password:str

class ChangeEmail(BaseModel):
    new_email:str