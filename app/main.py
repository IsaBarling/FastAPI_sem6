from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.sql import func
from models import UserDB, ProductDB, OrderDB


DATABASE_URL = "sqlite:///my_shop.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


app = FastAPI()


# Pydantic модели
class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str


class User(UserCreate):
    id: int


class ProductCreate(BaseModel):
    name: str
    description: str
    price: float


class Product(ProductCreate):
    id: int


class OrderCreate(BaseModel):
    user_id: int
    product_id: int
    date_ordered: str
    status: str


class Order(OrderCreate):
    id: int





# ...

# Маршруты для CRUD операций

# Создать нового пользователя
@app.post("/users/", response_model=User)
async def create_user(user: UserCreate):
    query = UserDB.insert().values(**user.dict())
    user_id = await database.execute(query)
    return {**user.dict(), "id": user_id}


# Получить информацию о пользователе по ID
@app.get("/users/{user_id}", response_model=User)
async def read_user(user_id: int):
    query = UserDB.select().where(UserDB.c.id == user_id)
    user = await database.fetch_one(query)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# Получить список всех пользователей
@app.get("/users/", response_model=list[User])
async def read_users(skip: int = 0, limit: int = 10):
    query = UserDB.select().offset(skip).limit(limit)
    users = await database.fetch_all(query)
    return users


# Обновить информацию о пользователе по ID
@app.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, user: UserCreate):
    query = UserDB.update().where(UserDB.c.id == user_id).values(**user.dict())
    await database.execute(query)
    return {**user.dict(), "id": user_id}


# Удалить пользователя по ID
@app.delete("/users/{user_id}", response_model=User)
async def delete_user(user_id: int):
    query = UserDB.delete().where(UserDB.c.id == user_id)
    deleted_user = await database.execute(query)
    if not deleted_user:
        raise HTTPException(status_code=404, detail="User not found")
    return deleted_user


# Аналогичные маршруты для товаров и заказов могут быть добавлены.

# Создать новый товар
@app.post("/products/", response_model=Product)
async def create_product(product: ProductCreate):
    query = ProductDB.insert().values(**product.dict())
    product_id = await database.execute(query)
    return {**product.dict(), "id": product_id}


# Получить информацию о товаре по ID
@app.get("/products/{product_id}", response_model=Product)
async def read_product(product_id: int):
    query = ProductDB.select().where(ProductDB.c.id == product_id)
    product = await database.fetch_one(query)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


# Получить список всех товаров
@app.get("/products/", response_model=list[Product])
async def read_products(skip: int = 0, limit: int = 10):
    query = ProductDB.select().offset(skip).limit(limit)
    products = await database.fetch_all(query)
    return products


# Обновить информацию о товаре по ID
@app.put("/products/{product_id}", response_model=Product)
async def update_product(product_id: int, product: ProductCreate):
    query = ProductDB.update().where(ProductDB.c.id == product_id).values(**product.dict())
    await database.execute(query)
    return {**product.dict(), "id": product_id}


# Удалить товар по ID
@app.delete("/products/{product_id}", response_model=Product)
async def delete_product(product_id: int):
    query = ProductDB.delete().where(ProductDB.c.id == product_id)
    deleted_product = await database.execute(query)
    if not deleted_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return deleted_product


# Создать новый заказ
@app.post("/orders/", response_model=Order)
async def create_order(order: OrderCreate):
    query = OrderDB.insert().values(**order.dict())
    order_id = await database.execute(query)
    return {**order.dict(), "id": order_id}


# Получить информацию о заказе по ID
@app.get("/orders/{order_id}", response_model=Order)
async def read_order(order_id: int):
    query = OrderDB.select().where(OrderDB.c.id == order_id)
    order = await database.fetch_one(query)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


# Получить список всех заказов
@app.get("/orders/", response_model=list[Order])
async def read_orders(skip: int = 0, limit: int = 10):
    query = OrderDB.select().offset(skip).limit(limit)
    orders = await database.fetch_all(query)
    return orders


# Обновить информацию о заказе по ID
@app.put("/orders/{order_id}", response_model=Order)
async def update_order(order_id: int, order: OrderCreate):
    query = OrderDB.update().where(OrderDB.c.id == order_id).values(**order.dict())
    await database.execute(query)
    return {**order.dict(), "id": order_id}


# Удалить заказ по ID
@app.delete("/orders/{order_id}", response_model=Order)
async def delete_order(order_id: int):
    query = OrderDB.delete().where(OrderDB.c.id == order_id)
    deleted_order = await database.execute(query)
    if not deleted_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return deleted_order


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
