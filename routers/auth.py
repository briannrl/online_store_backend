from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy_database import get_db
import models, oauth2, utils
from schemas import Token, Login, SignUpCustomer, ResponseNewUser

router = APIRouter(
    tags=['Authentication']
)

@router.post("/login", response_model=Token)
def login(user_credential: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter_by(email=user_credential.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Invalid Credentials")
    
    password_verify = utils.verify(user_credential.password, user.password)
    if not password_verify:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Invalid Credentials")
    
    # CREATE TOKEN
    token = oauth2.create_access_token({"email":user.email, "id":user.id, "position":user.position})

    return {"access_token":token, "token_type":"bearer"}

@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=ResponseNewUser)
def signup(new_user: SignUpCustomer, db: Session = Depends(get_db)):
    check_user = db.query(models.User).filter_by(email=new_user.email).first()
    if check_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Email {new_user.email} already exists!")
    
    new_user.password = utils.hash(new_user.password)
    new_user = models.User(**new_user.model_dump(), position="customer")
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user