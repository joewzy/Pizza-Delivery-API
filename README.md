# Pizza Delivery
API projects(Pizza Delivery)
### Simple Pizza Delivery API's
This project was builts for fun and for learning FastAPI, sqlalchemy and postgresql.The method,route, function and user groups access is as follows:

METHOD        ROUTE                               FUNCTIONALITY	                USER GROUP

POST	     /auth/signup/                         Register new user	             All users

POST	     /auth/login/	                        Login user	                    All users

POST	     /orders/order/	                      Place an order	                All users

PUT	       /orders/order/update/{order_id}/	    Update an order	                All users

PUT	       /orders/order/status/{order_id}/	    Update order status	            Superusers

DELETE	   /orders/order/delete/{order_id}/	    Delete/Remove an order	        All users

GET	       /orders/user/orders/	                Get user's orders	              All users

GET	       /orders/orders/	                    List all orders made	          Superusers

GET	       /orders/orders/{order_id}/	          Retrieve an order	              Superusers

GET	       /orders/user/order/{order_id}/	      Get user's specific order	      Superusers

GET	      /docs/	                              View API documentation	        All users



### To run 
- Set up a virtual environment (venv).
- install Python 3.6 or above.
- install postgresql.
- set up postgresql and config url in the database.py file.
- create database by running init_db.py
- run project using uvicorn.
