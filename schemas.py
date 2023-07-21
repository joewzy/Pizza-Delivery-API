from pydantic import BaseModel
from typing import Optional

class SignUpModel(BaseModel):
    id: Optional[int]
    username: str
    email: str
    password: str
    is_staff: Optional[bool]
    is_active: Optional[bool]


    class Config:
        orm_mode =True
        schema_extra= {
            "example":{
                "username": "Josiah",
                "email": "josiah@gmail.com",
                "password": "password",
                "is_staff": False,
                "is_active": True
            }
        }

# class containing our secret key for JWT
class Setting(BaseModel):
    authjwt_secret_key:str = '8708d5592269bb9cb754d0874bda3b8fd1f77cdfc981a2bf88d039d8a125da5f'


# login model
class LoginModel(BaseModel):
    username:str
    password:str


# model for orders by user

class OrderModel(BaseModel):
    id: Optional[int]
    quantity: int
    order_status: Optional[str]="PENDING"
    pizza_size: Optional[str]= "SMALL"
    user_id:Optional[int]

    #config to enable use by db
    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "quantity": 2,
                "pizza_size": "SMALL"
            }
        }  

# pydantic model for Status update
class OrderStatusModel(BaseModel):
    order_status: Optional[str] = "PENDING"

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "order_status": "PENDING"
            }
        }