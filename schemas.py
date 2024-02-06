from datetime import datetime

from pydantic import BaseModel, Field


class User(BaseModel):
    first_name: str = Field(..., max_length=16, min_length=2)
    last_name: str = Field(..., max_length=16, min_length=2)
    email: str = Field(..., max_length=64)


class UserIn(User):
    hashed_password: str = Field(..., min_length=6)


class UserOut(User):
    id: int


class Item(BaseModel):
    name: str = Field(..., max_length=64)
    description: str = Field(..., max_length=512)
    price: int = Field(gt=0)
    discount: float = Field(gt=0, le=1)
    is_active: bool = True


class ItemOut(Item):
    id: int


class Order(BaseModel):
    id_user: int
    id_item: int
    date: datetime = datetime.now().strftime("%Y-%m-%d %H:%M")
    is_active: bool = True


class OrderOut(Order):
    id: int
