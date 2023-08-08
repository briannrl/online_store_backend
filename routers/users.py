from fastapi import status, HTTPException, Depends, APIRouter, Response
from schemas import ResponseNewUser, AddUser
import models, oauth2, utils
from sqlalchemy_database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ResponseNewUser)
def create_user(user: AddUser, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    if current_user.position == "customer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Investors are unauthorized!")
    
    check_user = db.query(models.User).filter_by(email=user.email).first()
    if check_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Email {user.email} already exists!")
    user.password = utils.hash(user.password) # TRANSFORM PASSWORD STRING TO HASH FORMAT FOR SECURITY MEASURE
    user = models.User(**user.model_dump())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.get("/{id}", response_model=ResponseNewUser)
def get_user(id: str, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    if current_user.position == "customer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Investors are unauthorized!")

    check_id = db.query(models.User).filter_by(id=id).first()
    if not check_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} does not exist!")
    return check_id

@router.delete("/{id}")
def delete_user(id: str, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    if current_user.email != "brian@example.com":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"This user is not allowed to delete user data!")
    check_id = db.query(models.User).filter_by(id=id)
    if not check_id.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} does not exist!")
    check_id.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)