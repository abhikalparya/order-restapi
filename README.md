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

- **GET /orders**: Retrieve a list of orders along with their details and items.

- **GET /orders/{order_id}**: Retrieve a specific order by its ID.

- **POST /orders/create_order**: Create a new order.
  
- **PUT /orders/update**: Update the name of an existing order.
  
- **POST /orders/add_items**: Add items to an existing order.


