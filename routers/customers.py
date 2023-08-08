from fastapi import Response, status, HTTPException, Depends, APIRouter # Depends MEANS IF THE PATH OPERATION NEEDS OTHER FUNCTIONS TO ALSO RUN
from sqlalchemy.orm import Session
from schemas import AddCustomer, UpdateCustomer, ResponseCustomer
import models, oauth2
from sqlalchemy_database import get_db
from typing import List

router = APIRouter(
    prefix="/customers",
    tags=['Customers']
)

@router.get("/", response_model=List[ResponseCustomer]) # List[list_type] IS TO TELL PYTHON THAT OUR DATA IS LIST OF LISTS. USE THIS TO SHOW MULTIPLE ROWS IN THE CASE OF SQL DATABASE (ERROR IF NOT USING THIS)
def get_customers(db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user),
                  limit: int = 10, skip: int = 0, search: str = ""): # LIMIT WILL BE USED AS PATH PARAMETER TO LIMIT TOTAL CUSTOMERS VIEWED. FORMAT: existing_path?limit=any_number (USE THIS PATH IN POSTMAN)
    if current_user.position == "customer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"Unauthorized!")
    
    if current_user.position != "owner": # ONLY OWNER WHO CAN ACCESS ALL CUSTOMERS' DATA
        customers = (db.query(models.Customers)
                     .filter_by(contact_person_id=current_user.id)
                     .filter(models.Customers.name.contains(search))
                     .limit(limit)
                     .offset(skip) # OFFSET WILL SKIP THE FIRST NUMBER OF ENTRIES. USEFUL IF YOU WANT MAKE MULTIPLE PAGE LISTS. USE '&' TO SEPARATE BETWEEN MULTIPLE PATH PARAMETER.
                     .all())
    else:
        customers = (db.query(models.Customers)
                     .filter(models.Customers.name.contains(search))
                     .limit(limit)
                     .offset(skip)
                     .all())
    return customers

@router.get("/{id}", response_model=ResponseCustomer)
def get_customer(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    if current_user.position == "customer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"Unauthorized!")
    
    customer = db.query(models.Customers).filter_by(id=id)
    if not customer.all():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Customers with id: {id} does not exist!")
    
    if current_user.position != "owner": # ONLY OWNER WHO HAS NOT RESTRICTED ACCESS TO ANY CUSTOMER'S ID
        if customer.first().contact_person_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"This user can't access customer with id: {id}")  
    
    return customer.first()

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ResponseCustomer)
def add_customer(new_customer: AddCustomer, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    if current_user.position == "customer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"Unauthorized!")
    
    check_name = db.query(models.Customers).filter_by(name=new_customer.name).first()
    if check_name:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Customer with name: {new_customer.name} already exists!")
    # customer = models.Customers(name=new_customer.name, phone_number=new_customer.phone_number,
    #                             subscribe=new_customer.subscribe)
    customer = models.Customers(**new_customer.model_dump(), contact_person_id=current_user.id) # THIS LINE IS EQUAL TO THE ABOVE CODE. model_dump() CHANGE THE DATA TYPE TO DICTIONARY AND ** IS TO UNPACK THE DICTIONARY
    db.add(customer)
    db.commit()
    db.refresh(customer) # TO RETRIEVE THE NEWLY ADDED DATA. WITHOUT THIS, return customer WILL RETURN EMPTY DATA
    return customer

@router.put("/{id}", response_model=ResponseCustomer)
def update_customer(id: int, customer: UpdateCustomer, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    if current_user.position == "customer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"Unauthorized!")
    
    customer_query = db.query(models.Customers).filter_by(id=id)
    
    if not customer_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Customer with id: {id} does not exist!")
    
    if current_user.position != "owner": # ONLY OWNER WHO CAN UPDATE ANY CUSTOMERS' DATA
        if customer_query.first().contact_person_id != current_user.id: # CHECK IF THE CUSTOMER IS UPDATED BY HIS/HER OWN CONTACT PERSON
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail=f"Cannot update customer with id: {id}")
    
    customer_query.update(customer.model_dump(), synchronize_session=False)
    db.commit()
    return customer_query.first()

@router.delete("/{id}")
def remove_customer(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    if current_user.position == "customer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"Unauthorized!")
 
    customer = db.query(models.Customers).filter_by(id=id)
    
    if not customer.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Customer with id: {id} does not exist!")
    
    if current_user.position != "owner":
        if customer.first().contact_person_id != current_user.id: # CHECK IF THE CUSTOMER IS DELETED BY HIS/HER OWN CONTACT PERSON
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail=f"Cannot delete customer with id: {id}")
    
    customer.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)