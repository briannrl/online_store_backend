from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy_database import Base
from sqlalchemy.sql.expression import text # USE text() TO WRITE RAW POSTGRES QUERY
from sqlalchemy.orm import relationship

class NewProducts(Base):
    __tablename__ = "products"

    id = Column(String, primary_key=True, nullable=False, server_default=text("gen_random_uuid()"))
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    total_stock = Column(Integer, nullable=False)
    added_time = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    modified_time = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"), onupdate=text("now()"))

class Customers(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    subscribe = Column(Boolean, server_default="False", nullable=False)
    regis_time = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    modified_time = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"), onupdate=text("now()"))

    contact_person_id = Column(String, ForeignKey("users.id", ondelete="SET NULL", onupdate="CASCADE"), nullable=True) # ON DELETE SET NULL: IF THE ROW OF THE RESPECTIVE CONTACT_PERSON_ID IS DELETED IN THE PARENT TABLE, THEN CONTACT_PERSON_ID WILL SET TO NULL
                                                                                                                       # ON UPDATE CASCADE: IF THE ID ON THE PARENT TABLE IS CHANGED, THE CONTACT_PERSON_ID WILL ALSO BE UPDATED.

    contact_person = relationship("User") # CREATE CONNECTION WITH User CLASS. NEED TO ADD NEW ELEMENT TO PYDANTIC SCHEMAS FOR THIS TO WORK

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, nullable=False, server_default=text("gen_random_uuid()"))
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False, unique=False)
    position = Column(String, nullable=False)
    regis_time = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    modified_time = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"), onupdate=text("now()"))

class Likes(Base):
    __tablename__ = "likes"

    product_id = Column(String, ForeignKey("products.id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True, nullable=False)
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True, nullable=False)

    product_details = relationship("NewProducts")
# IF TABLE EXIST, WE CANNOT ALTER ANYTHING IN THE TABLE PROPERTIES WITH SQLALCHEMY ORM
# TO ALTER/MIGRATE, USE ALEMBIC