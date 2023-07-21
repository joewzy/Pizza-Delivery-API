from .database import Base
from sqlalchemy import Column, Integer, Boolean, Text, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_utils.types import ChoiceType

# defining our user model/table in db which inherits from Base.


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(30), unique=True)
    email = Column(String(80), unique=True)
    password = Column(Text, nullable=True)
    is_staff = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)
    orders = relationship('Order', back_populates='user')
    # Order table is related to user table --> using the relationship()


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
    order_status = Column(ChoiceType(choices=ORDER_STATUS), default='PENDING')
    pizza_size = Column(ChoiceType(choices=PIZZA_SIZES), default='SMALL')
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User',back_populates='orders')

    def __repr__(self):
        return f"Order {self.id}"
    
