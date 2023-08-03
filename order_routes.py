from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from models import User, Order
from schemas import OrderModel, OrderStatusModel
from fastapi_jwt_auth import AuthJWT
from fastapi.encoders import jsonable_encoder
from database import engine, Sessionlocal

order_router = APIRouter(
    prefix="/orders",
    tags= ["orders"])

# creating session instance for db interaction
session = Sessionlocal(bind=engine)

@order_router.get("/")
async def hello(Authorize: AuthJWT = Depends()):
    # using DOCSTRING to document our API routes in swagger UI
    """
        ## This is an Sample Test
        This returns a simple hello world  
    
    """

    try:
        Authorize.jwt_required()

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")
    
    return {"message": "Orders routes here"}

# place_order route

@order_router.post('/order', status_code=status.HTTP_201_CREATED)
async def place_an_order(order: OrderModel, Authorize: AuthJWT = Depends()):
    # DOCSTRING for placing an order
    """
        ## Placing an Order
        Requires the following:
        - quantity : integer
        - pizza_size: str
    
    """
    try:
        Authorize.jwt_required()

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")
    
    current_user= Authorize.get_jwt_subject()
    # get the current user details by querying Users table and 
    user = session.query(User).filter(User.username == current_user).first()

    new_order= Order(
        pizza_size = order.pizza_size,
        quantity = order.quantity
    )

    new_order.user = user
    session.add(new_order)
    session.commit()        # commit above query to db

    # output response
    response = {
        "pizza_size": new_order.pizza_size,
        "quantity": new_order.quantity,
        "id": new_order.id,
        "order_status": new_order.order_status
    }
    # return response a json 
    return jsonable_encoder(response)


# view all orders
@order_router.get('/orders')
async def list_all_orders(Authorize: AuthJWT= Depends()):

    """
        ## List all Orders
        User must be SuperUser/ Admin to view all orders
    
    """

    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")
    
    current_user = Authorize.get_jwt_subject()

    user = session.query(User).filter(User.username == current_user).first()

    if user.is_staff:
        orders= session.query(Order).all()

        return jsonable_encoder(orders)
    
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not a Superuser")

# get order by order_ID
@order_router.get('/orders/{order_id}')
async def get_order_by_id(order_id:int, Authorize: AuthJWT=Depends()):

    """
        ## Get an Order by its ID
        Required the following:
        - order_id: integer
    
    """

    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")
    
    # get user details from jwt token
    user = Authorize.get_jwt_subject()

    current_user = session.query(User).filter(User.username == user).first()

    if current_user.is_staff:
        order = session.query(Order).filter(Order.id == order_id).first()

        return jsonable_encoder(order)
    
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Request not allowed for User")


# get all orders for a user / current user

@order_router.get('/user/orders')
async def get_user_orders(Authorize: AuthJWT= Depends()):

    """
        ## Get Current user's orders
        This returns all orders by currently logged in user
    
    """

    try:
        Authorize.jwt_required()

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")
    
    # get user detail from jwt token
    user = Authorize.get_jwt_subject()

    # query db for the user id above
    current_user = session.query(User).filter(User.username == user).first()

    #user table has relationship with orders tables thus we return orders
    return jsonable_encoder(current_user.orders)


# get specific order by user

@order_router.get('/user/order/{order_id}')
async def get_user_order(order_id:int, Authorize:AuthJWT= Depends()):

    """
        ## Get a User's specific Order by ID
        Requires the following:
        - order id: integer
    
    """

    try:
        Authorize.jwt_required()

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")
    
    # get user details
    user = Authorize.get_jwt_subject()

    # query user from db
    current_user = session.query(User).filter(User.username == user).first()
    # get all orders
    orders = current_user.orders

    # get specific order by id
    for order in orders:
        if order.id == order_id:
            return jsonable_encoder(order)
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= "Order with ID not found")

        
# update a specific order --> this updates all fields
@order_router.put('/order/update/{order_id}/')
async def update_order(order_id: int, order: OrderModel, Authorize: AuthJWT= Depends()):

    """
        ## Update an Existing Order
        Requires the following:
        - quantity: integer
        - pizza_size: str
    
    """

    try:
        Authorize.jwt_required()

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")
    

    order_to_update = session.query(Order).filter(Order.id == order_id).first()

    # changes to be effected
    order_to_update.quantity = order.quantity
    order_to_update.pizza_size = order.pizza_size

    # commit changes to db
    session.commit()

    # creating a custom response to output
    response = {
        "Order_id" : order_to_update.id,
        "Quantity" : order_to_update.quantity,
        "Pizza_size" : order_to_update.pizza_size,
        "order Status": order_to_update.order_status
    }

    return jsonable_encoder(response)


# update a specific field(order status) --> 
@order_router.patch('/order/update/{order_id}')
async def update_order_status(order_id: int,order_status: OrderStatusModel, Authorize: AuthJWT= Depends()):

    """
        ## Update only the Order Status of an Existing Order
        Reqiures the following:
        - order_status:str
    """

    try:
        Authorize.jwt_required()
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")
    
    # get user details
    user = Authorize.get_jwt_subject()

    # query  user from db
    current_user =  session.query(User).filter(User.username == user).first()

    # if user is staff --> fetch specificied order & perform status change, else cannot change status
    if current_user.is_staff:
        order_to_update = session.query(Order).filter(Order.id == order_id).first()

        # set that order status to new status
        order_to_update.order_status = order_status.order_status
        session.commit()

        # creating a custom response to output
        response = {
            "Order_id" : order_to_update.id,
            "Quantity" : order_to_update.quantity,
            "Pizza_size" : order_to_update.pizza_size,
            "order Status": order_to_update.order_status
        }

        return jsonable_encoder(response)
    


# delete an order
@order_router.delete('/order/delete/{order_id}/', status_code= status.HTTP_204_NO_CONTENT)
async def delete_an_order(order_id: int, Authorize: AuthJWT= Depends()):

    """
        ## Delete an existing order
        deletes order by id
        
    
    """

    try:
        Authorize.jwt_required()

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= "Invalid Token")
    
    delete_order = session.query(Order).filter(Order.id == order_id).first()

    # delete the order and commit changes to db
    session.delete(delete_order)

    session.commit()

    return jsonable_encoder(delete_order)
    