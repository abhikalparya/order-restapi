# Flask Order Management API



![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![MySQL](https://img.shields.io/badge/mysql-4479A1.svg?style=for-the-badge&logo=mysql&logoColor=white)


This project is a RESTful API for managing orders and order items.


## ER Diagram
![er_diagram](https://github.com/abhikalparya/FarmEasy/assets/81465377/987d049f-2433-4257-8d2e-b08f24f5bac2)


## Features
- **Create Person**: Create a new person.
- **Create Order**: Create a new order.
- **Add Order Items**: Add items to an existing order.
- **Get Orders**: Retrieve a list of orders along with their details and items.
- **Get Order by ID**: Retrieve a specific order by its ID.
- **Update Order**: Update the name of an existing order.

## Technologies Used
- Flask: Python web framework for building the API.
- MySQL: Database management system for storing order and item data.
- Python MySQL Connector: Python driver for connecting to MySQL databases.
- Postman: API development and testing tool.

## API Endpoints

- **POST /create_person**: Create a new person.
<img width="634" alt="create_person" src="https://github.com/abhikalparya/order-restapi/assets/81465377/09383e16-d24c-4cee-be28-97618eff249c">

- **GET /orders**: Retrieve a list of orders along with their details and items.
<img width="641" alt="display_orders" src="https://github.com/abhikalparya/order-restapi/assets/81465377/ad595067-21e8-4a23-a04b-14e8152bdcf6">

- **GET /orders/{order_id}**: Retrieve a specific order by its ID.
<img width="638" alt="display_one_order" src="https://github.com/abhikalparya/order-restapi/assets/81465377/e64b2218-7bf6-4dce-8e49-e3ab5ca0640f">

- **POST /orders/create_order**: Create a new order.
<img width="635" alt="create_order" src="https://github.com/abhikalparya/order-restapi/assets/81465377/b4e10851-4eaf-4119-be2d-5865e9008f55">

- **PUT /orders/update**: Update the name of an existing order.
<img width="636" alt="update_order" src="https://github.com/abhikalparya/order-restapi/assets/81465377/53734ce7-3676-43f2-a3ce-fa135d81416d">

- **POST /orders/add_items**: Add items to an existing order.
<img width="641" alt="add_items" src="https://github.com/abhikalparya/order-restapi/assets/81465377/b0a910dd-ec9b-4224-8121-b5f60fd56b7d">


