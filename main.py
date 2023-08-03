from fastapi import FastAPI
from auth_routes import auth_router
from order_routes import order_router
from fastapi_jwt_auth import AuthJWT
from schemas import Setting


app = FastAPI()

# AuthJWT load_config method to load our custom Setting from .schemas  
@AuthJWT.load_config
def get_config():
    return Setting()

# adding auth_router & order_router to the main.py  
app.include_router(auth_router)
app.include_router(order_router)


@app.get("/")
def root():
    return {"message": "Back to basics"}

