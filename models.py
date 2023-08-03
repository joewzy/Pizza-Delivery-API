from database import Base
from sqlalchemy import Column, Integer, Boolean, Text, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_utils.types import ChoiceType
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

# defining our user model/table in db which inherits from Base.
# sqlalchemy does not modified / make change to columns if table already exists
# table is left untouched if it exists thus no new chages are made
# alembic can be used for these kind of changes

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(30), unique=True)
    email = Column(String(80), unique=True)
    password = Column(Text, nullable=True)
    is_staff = Column(Boolean, server_default="False")
    is_active = Column(Boolean, server_default="False")
    orders = relationship('Order', back_populates='user')
    date_created = Column(TIMESTAMP(timezone=True),nullable= False, server_default=text('now()'))
    # Order table is related to user table --> using the relationship()
    # server_default requires a str 
    # sets the column property to given string duting table creation

    def __repr__(self):
        return f"User {self.username}"


class Order(Base):
    # creating a tuple of tuples containing our options to select from
    # then import ChoiceType from sqlaclchemy_utils.types 
    ORDER_STATUS = (
        ('PENDING', 'pending'),
        ('IN-TRANSIT', 'in-transit'),
        ('DELIVERED', 'delivered')
    )

    PIZZA_SIZES = (
        ('SMALL', 'small'),
        ('MEDIUM', 'medium'),
        ('LARGE', 'large'),
        ('EXTRA-LARGE', 'extra-large')
    )
    __tablename__ = 'orders'
    id = Column(Integer,primary_key=True)
    quantity = Column(Integer, nullable=False)
    order_status = Column(ChoiceType(choices=ORDER_STATUS), server_default='PENDING')
    pizza_size = Column(ChoiceType(choices=PIZZA_SIZES), server_default='SMALL')
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User',back_populates='orders')
    date_created =  Column(TIMESTAMP(timezone=True), nullable= False, server_default= text('now()'))

    def __repr__(self):
        return f"Order {self.id}"
    
