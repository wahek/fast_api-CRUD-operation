import datetime
import random

from fastapi import FastAPI, Path
from models import metadata, database, engine, items, orders, users
import schemas

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


# @app.get('/items', response_model=list[schemas.ItemOut])

@app.get("/fake_users/{count}")
async def get_users(count: int = Path(ge=5)):
    for i in range(count):
        query = users.insert().values(first_name=f'first{i}',
                                      last_name=f'last{i}',
                                      email=f'mail{i}@mail.ru',
                                      hashed_password=hash(f'{i}'),
                                      is_active=True)

        await database.execute(query)
    return {'message': f'{count} fake users create'}


@app.get("/fake_items/{count}")
async def get_items(count: int = Path(ge=5)):
    for i in range(count):
        query = items.insert().values(name=f'name{i}',
                                      description=f'description{i}',
                                      price=10 + i ** 3,
                                      discount=0.8,
                                      is_active=True)

        await database.execute(query)
    return {'message': f'{count} fake items create'}


@app.get("/fake_orders/{count}")
async def get_orders(count: int = Path(ge=5)):
    for i in range(count):
        query = orders.insert().values(id_user=random.randint(1, 5),
                                       id_item=random.randint(1, 5),
                                       date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                                       is_active=True)

        await database.execute(query)
    return {'message': f'{count} fake orders create'}


@app.get('/items', tags=['CRUD ITEM'])
async def get_items_list():
    query = items.select()
    return await database.fetch_all(query)


@app.get('/users', tags=['CRUD USER'])
async def get_items_list():
    query = users.select()
    return await database.fetch_all(query)


@app.get('/orders', tags=['CRUD ORDER'])
async def get_items_list():
    query = orders.select()
    return await database.fetch_all(query)


@app.post('/item', tags=['CRUD ITEM'])
async def new_item(item: schemas.Item):
    query = items.insert().values(**item.dict())
    await database.execute(query)
    return f'{item} Добавлен'


@app.post('/user', tags=['CRUD USER'])
async def new_user(user: schemas.UserIn):
    query = users.insert().values(**user.dict())
    await database.execute(query)
    return f'{user} Добавлен'


@app.post('/order', tags=['CRUD ORDER'])
async def new_order(order: schemas.Order):
    query = orders.insert().values(**order.dict())
    await database.execute(query)
    return f'{order} Добавлен'


@app.put('/order/{order_id}', tags=['CRUD ORDER'])
async def update_order(order_id: int, order: schemas.Order):
    query = orders.update().where(orders.c.id == order_id).values(**order.dict())
    await database.execute(query)
    return f'{order} Обновлён'


@app.put('/user/{user_id}', tags=['CRUD USER'])
async def update_user(user_id: int, user: schemas.UserIn):
    query = users.update().where(users.c.id == user_id).values(**user.dict())
    await database.execute(query)
    return f'{user} Обновлён'


@app.put('/item/{item_id}', tags=['CRUD ITEM'])
async def update_item(item_id: int, item: schemas.Item):
    query = items.update().where(items.c.id == item_id).values(**item.dict())
    await database.execute(query)
    return f'{item} Обновлён'


@app.delete('/item/{item_id}', tags=['CRUD ITEM'])
async def update_item(item_id: int):
    query = items.delete().where(items.c.id == item_id)
    await database.execute(query)
    return f'{item_id} Удалён'


@app.delete('/user/{user_id}', tags=['CRUD USER'])
async def update_user(user_id: int):
    query = users.delete().where(users.c.id == user_id)
    await database.execute(query)
    return f'{user_id} Удалён'


@app.delete('/order/{order_id}', tags=['CRUD ORDER'])
async def update_order(order_id: int):
    query = orders.delete().where(orders.c.id == order_id)
    await database.execute(query)
    return f'{order_id} Удалён'


if __name__ == '__main__':
    metadata.drop_all(engine)
    metadata.create_all(engine)
