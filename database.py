from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker




# my postgres db url 
#db_url = 'database_type://username:password@host:port/database_name'
# if db password contain @ character use %40 instead eg p@ss == p%40ss
db_url = 'postgresql://postgres:atm%40gdc@localhost/pizza_delivery'

engine = create_engine(db_url, echo=True)

# base class for defining our models(tables in db)
Base = declarative_base()

# create session for db interaction
Sessionlocal = sessionmaker()
