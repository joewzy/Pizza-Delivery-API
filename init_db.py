from .database import engine, Base
from .models import User, Order


Base.metadata.create_all(bind= engine)
# bind with engine in .database file -->actual tables creation
 