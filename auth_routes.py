from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from .database import engine, Sessionlocal
from .models import User
from .schemas import SignUpModel, LoginModel
from werkzeug.security import generate_password_hash, check_password_hash
from fastapi_jwt_auth import AuthJWT
from fastapi.encoders import jsonable_encoder

auth_router = APIRouter(
    prefix = "/auth",
    tags =["auth"])

# create session instance from Sessionlocal and bind to engine
session = Sessionlocal(bind=engine)


# route without JWT auth required
# @auth_router.get("/")
# async def hello():
#     return {"message": "This is auth routes"}

# JWT required to access this route
@auth_router.get("/")
async def hello(Authorize:AuthJWT=Depends()):

    """
        ## This is a test sample
        returns Authentication hello message
    """
    try:
        Authorize.jwt_required()

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")
    return {"message": "This is auth routes"}


@auth_router.post('/signup', status_code=status.HTTP_201_CREATED)
async def signup(user_info: SignUpModel):

    """
        ## Signing Up User
        Create a new user if username & email does not already exist, requires the following:
        - username: str
        - email: str
        - password: str
        - is_staff: boolean
        - is_active: boolean

    """

    db_email = session.query(User).filter(User.email == user_info.email).first()
    
    if db_email is not None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                             detail="user with the email already exists")


    db_username = session.query(User).filter(User.username == user_info.username).first()

    if db_username is not None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                             detail="User with the username already exists")
    
    new_user = User(
        username=user_info.username,
        email=user_info.email,
        password=generate_password_hash(user_info.password),
        is_staff=user_info.is_staff,
        is_active=user_info.is_active
    )

    session.add(new_user)
    session.commit()
    return new_user


# login routes
@auth_router.post('/login')
async def login(user: LoginModel, Authorize: AuthJWT = Depends()):

    """
        ## Log in to Existing User account
        Requires the following:
        - username: str
        - password: str

        returns 'access' and 'refresh' tokens.
    """
    db_user = session.query(User).filter(User.username == user.username).first()

    if db_user and check_password_hash(db_user.password, user.password):
        access_token = Authorize.create_access_token(subject=db_user.username)
        refresh_token = Authorize.create_refresh_token(subject=db_user.username)

        # access & refresh token dict as response
        response = {
            "access": access_token,
            "refresh": refresh_token
        }

        return jsonable_encoder(response)
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid username or Password")
    

# refreshing given tokens

@auth_router.get('/refresh')
async def refresh_token(Authorize:AuthJWT=Depends()):

    """
        ## Generate fresh access tokens 
        This create a fresh token, it requires:
        - refresh token


    """
    try:
        Authorize.jwt_refresh_token_required()

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Please provide a valid token")
    
    current_user = Authorize.get_jwt_subject()
    access_token = Authorize.create_access_token(subject=current_user)
    return jsonable_encoder({"access": access_token})

