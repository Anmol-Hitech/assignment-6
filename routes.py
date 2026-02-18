from fastapi import APIRouter,HTTPException,Depends
from database import get_db
from jose import jwt,JWTError
from sqlalchemy.orm import Session
from config import settings
from models import User
from auth import create_access_token,hash_password,verify_password,get_current_user
from helpers import generate_otp,send_otp_email,correct_email
from schemas import UserSchema,UserProfile,UserLogin,Token,VerifyOtp,ChangePass,ChangeEmail
router=APIRouter()


@router.post("/signup",status_code=201)
def signup(user:UserSchema,db:Session=Depends(get_db)):
    existing_user=(
        db.query(User).filter(User.email==user.email).first()
    )
    if existing_user:
        raise HTTPException(status_code=400)
    hashed_pwd=hash_password(user.password)
    temp_otp=generate_otp()
    new_user=User(email=user.email,password=hashed_pwd,otp=temp_otp)
    send_otp_email("anmol.cce22@sot.pdpu.ac.in",temp_otp)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message":"User created verification pending"}




@router.post("/verify")
def verify_otp(email:str,otp:int,db:Session=Depends(get_db)):
    db_user=db.query(User).filter(User.email==email).first()
    if not db_user:
        raise HTTPException(status_code=400, detail="Not found")
    if(db_user.otp==otp):
        db_user.is_verified=True
    else:
        raise HTTPException(status_code=400,detail="Otp not correct")
    db.commit()
    db.refresh(db_user)
    return {"message":"verified"}



@router.post("/login")
def login(user:UserLogin,db:Session=Depends(get_db)):
    db_user=db.query(User).filter(User.email==user.email).first()
    if db_user.is_verified==False:
        raise HTTPException(status_code=400,detail="Email not verified")
    
    if not db_user:
        raise HTTPException(status_code=400,detail="Invalid credentials")
    
    if db_user.is_Active==False:
        raise HTTPException(status_code=400,detail="Account is inactive")
    
    if not verify_password(user.password,db_user.password):
        raise HTTPException(status_code=400,detail='Invalid password')
    
    access_token=create_access_token(data={"sub":db_user.email})
    return {"access_token":access_token,"token_type":"bearer"}



@router.get("/me",response_model=UserProfile)
def get_profile(current_user:User=Depends(get_current_user)):
    return current_user

@router.patch("/deactivate")
def deactivate_acc(current_user:User=Depends(get_current_user),db:Session=Depends(get_db)):
    if current_user.is_Active==False:
        raise HTTPException(status_code=400,detail="Already deactivated user")
    current_user.is_Active=False
    db.commit()
    db.refresh(current_user)
    return {"message":"Successfully deactivated"}

@router.patch("/activate")
def activate_acc(email:str,db:Session=Depends(get_db)):
    db_user=db.query(User).filter(User.email==email).first()
    db_user.is_Active=True
    db.commit()
    db.refresh(db_user)
    return {"message":"Successfully activated"}

@router.post("/change-password")
def change_pass(data: ChangePass,current_user: User = Depends(get_current_user),db: Session = Depends(get_db)):
    if not verify_password(data.old_password, current_user.password):
        raise HTTPException(status_code=400, detail="Old password incorrect")
    current_user.password = hash_password(data.new_password)
    db.commit()
    return {"message": "Password updated successfully"}

@router.put("/change-email")
def change_email(data:ChangeEmail,current_user:User=Depends(get_current_user),db:Session=Depends(get_db)):
    if not correct_email(data.new_email):
        raise HTTPException(status_code=400,detail="New email does not follow the required email format")
    db_email=db.query(User).filter(User.email==data.new_email).first()
    if db_email:
        raise HTTPException(status_code=400,detail="New email already exists")
    current_user.email=data.new_email
    db.commit()
    return {"message":"New email updated"}
