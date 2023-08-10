from fastapi import FastAPI, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database import connect_database
from schemas import AddProduct, UpdateProduct
import models
from sqlalchemy_database import engine
from routers import customers, users, auth, new_products, like

# models.Base.metadata.create_all(bind=engine) # TO CREATE ALL THE TABLES BASED ON models.py

app = FastAPI()

origins = []

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # HTTP METHODS ALLOWED
    allow_headers=["*"]
)

# POSTGRES DATABASE CONNECTION
# conn, cursor = connect_database()

app.include_router(customers.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(new_products.router)
app.include_router(like.router)

@app.get("/")
def get_routes():
    return {"data":"HOME PAGE"}

# ROUTES WITH PSYCOPG2
# @app.get("/products")
# def get_products():
#     cursor.execute("SELECT * FROM products;")
#     products = cursor.fetchall()
#     return products

# @app.get("/products/{id}")
# def get_product(id: str):
#     cursor.execute(f"SELECT * FROM products WHERE id = '{id}'")
#     product = cursor.fetchone()
#     if not product:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"Post id: {id} does not exist!")
#     return product

# @app.post("/products", status_code=status.HTTP_201_CREATED)
# def add_product(new_product: AddProduct):
#     cursor.execute(f"""SELECT product_name FROM products WHERE product_name = '{new_product.product_name.lower()}'""")
#     check_product = cursor.fetchone()
#     if check_product:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
#                             detail=f"Product {new_product.product_name.lower()} already exists!")
#     cursor.execute(f"""INSERT INTO products (product_name, price, stock_num)
#                     VALUES ('{new_product.product_name.lower()}', {new_product.price}, {new_product.stock_num})""")
#     conn.commit()
#     cursor.execute("SELECT * FROM products;")
#     products = cursor.fetchall()
#     return products

# @app.put("/products/{id}")
# def update_product(id: str, product: UpdateProduct):
#     cursor.execute(f"""UPDATE products 
#                        SET product_name = '{product.product_name.lower()}',
#                             price = {product.price},
#                             stock_num = {product.stock_num},
#                             modified_time = NOW()
#                         WHERE id = '{id}'""")
#     conn.commit()
#     cursor.execute("SELECT * FROM products;")
#     products = cursor.fetchall()
#     return products

# @app.delete("/products/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def remove_product(id: str):
#     cursor.execute(f"""DELETE FROM products WHERE id = '{id}'""")
#     conn.commit()
#     cursor.execute("SELECT * FROM products;")
#     products = cursor.fetchall()
#     return products