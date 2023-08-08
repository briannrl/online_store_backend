from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class AddProduct(BaseModel):
    product_name: str
    price: Optional[int] = None
    stock_num: Optional[int] = None

class UpdateProduct(BaseModel):
    product_name: Optional[str]
    price: Optional[int]
    stock_num: Optional[int]

class AddNewProduct(BaseModel):
    name: str
    price: int
    total_stock: int

class ResponseNewProduct(BaseModel):
    id: str
    name: str
    price: int
    total_stock: int
    added_time: datetime
    modified_time: datetime

    class Config:
        orm_mode = True

class ResponseNewProductLikes(BaseModel):
    NewProducts: ResponseNewProduct # KEY = MODEL'S NAME INSIDE THE query()
    total_likes: int

    class Config:
        orm_mode = True

class AddUser(BaseModel):
    email: EmailStr
    password: str
    position: str

class ResponseNewUser(BaseModel):
    email: str
    position: str
    regis_time: datetime

    class Config:
        orm_mode = True

class AddCustomer(BaseModel):
    name: str
    phone_number: str
    subscribe: bool = False
    # contact_person_id: Optional[str]

class UpdateCustomer(AddCustomer):
    subscribe: bool

class ResponseCustomer(BaseModel):
    name: str
    phone_number: str
    modified_time: datetime
    contact_person_id: Optional[str] # USE Optional IF THE FIELDS NULLABLE=TRUE. IF NOT USING Optional, IT WILL RETURN ERROR IF THE FIELD VALUE IS NULL
    contact_person: ResponseNewUser # CONNECTED TO contact_person IN CUSTOMERS MODEL. THIS WILL SHOW DATA WHICH FORMATTED WITH THE SPECIFIED PYDANTIC SCHEMA.
    class Config: # MANDATORY FOR RESPONSE MODEL (OUTPUT FORMAT)
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str
    id: str
    position: str
    exp: int

class Login(BaseModel):
    username: EmailStr
    password: str

class SignUpCustomer(BaseModel):
    email: EmailStr
    password: str

class Like(BaseModel):
    product_id: str

class ResponseLike(Like):
    # new_product_id: str
    product_details: AddNewProduct
    
    class Config:
        orm_mode = True