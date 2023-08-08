from fastapi import Response, status, HTTPException, Depends, APIRouter # Depends MEANS IF THE PATH OPERATION NEEDS OTHER FUNCTIONS TO ALSO RUN
from sqlalchemy.orm import Session
from sqlalchemy import func
from schemas import AddNewProduct, ResponseNewProduct, ResponseNewProductLikes
import models, oauth2
from sqlalchemy_database import get_db
from typing import List, Tuple

router = APIRouter(
    prefix="/products",
    tags=["New Products"]
)

@router.get("/", response_model=List[ResponseNewProductLikes])
def get_new_products(db: Session = Depends(get_db)):
    # new_products = db.query(models.NewProducts)
    new_products = (db
                    .query(models.NewProducts, func.count(models.Likes.product_id).label("total_likes"))
                    .join(models.Likes, models.NewProducts.id == models.Likes.product_id, isouter=True)
                    .group_by(models.NewProducts.id))
    print(new_products)
    return new_products.all()

@router.get("/{id}", response_model=ResponseNewProductLikes)
def get_new_product(id: str, db: Session = Depends(get_db)):
    # new_product = db.query(models.NewProducts).filter_by(id=id)
    new_product = (db
                    .query(models.NewProducts, func.count(models.Likes.product_id).label("total_likes"))
                    .join(models.Likes, models.NewProducts.id == models.Likes.product_id, isouter=True)
                    .group_by(models.NewProducts.id)
                    .filter(models.NewProducts.id == id)
                    )

    if not new_product.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Product with id: {id} does not exist!")
    return new_product.first()

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ResponseNewProduct)
def add_new_product(new_product: AddNewProduct,  db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    if current_user.position == "customer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"Unauthorized!")

    check_product = db.query(models.NewProducts).filter_by(name=new_product.name).first()
    if check_product:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Product with name: {new_product.name} already exists!")
    
    product = models.NewProducts(**new_product.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

@router.put("/{id}", response_model=ResponseNewProduct)
def update_new_product(id: str, product: AddNewProduct, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    if current_user.position == "customer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"Unauthorized!")
    
    product_query = db.query(models.NewProducts).filter_by(id=id)
    if not product_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Product with id: {id} does not exist!")
    
    product_query.update(product.model_dump(), synchronize_session=False)
    db.commit()
    return product_query.first()

@router.delete("/{id}")
def remove_product(id: str, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    if current_user.position == "customer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"Unauthorized!")

    product_query = db.query(models.NewProducts).filter_by(id=id)
    if not product_query.first():
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Product with id {id} does not exist!")
    
    product_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)