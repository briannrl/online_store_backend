from fastapi import Response, status, HTTPException, Depends, APIRouter # Depends MEANS IF THE PATH OPERATION NEEDS OTHER FUNCTIONS TO ALSO RUN
from sqlalchemy.orm import Session

from schemas import Like, ResponseLike
import models, oauth2
from sqlalchemy_database import get_db

router = APIRouter(
    prefix="/like",
    tags=['Likes']
)

# THIS FUNCTION CREATED FOR LIKE TOGGLE BUTTON. DELETE FROM DB IF COMBINATION PRODUCT_ID AND USER_ID EXISTS, AND ADD TO DB IF DOESNT EXIST
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ResponseLike)
def set_like(like: Like, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)): 
    check_product = db.query(models.NewProducts).filter_by(id=like.product_id).first()
    if not check_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No product with id: {like.product_id} in database!")
    
    check_like = db.query(models.Likes).filter_by(product_id=like.product_id, user_id=current_user.id)

    if check_like.first():
        check_like.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        new_like = models.Likes(**like.model_dump(), user_id=current_user.id)
        db.add(new_like)
        db.commit()
        db.refresh(new_like)
        return new_like