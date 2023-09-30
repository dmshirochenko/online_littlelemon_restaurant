## Online Little Lemon Restaurant Platform 🐍Django 📡DjangoDRF 🔐Djoser 🐳Docker 🛢MySQL 🌐API 🧪UnitTest

### Overview

The "Little Lemon" is a comprehensive web application for restaurant management, providing a real-time menu, table bookings, and more.

---

### Table of Contents

1. [Features](#features)
2. [Installation](#installation)
3. [Endpoints](#endpoints)
5. [Tests](#tests)
6. [Contributing](#contributing)

---

### Features

- Real-time Menu Management
- Table Reservation API
- User Authentication and Authorization
- Unit Tests
- MySQL Database Backend
- RESTful API

---

### Installation

```shell
# Activate the virtual environment
pipenv shell

 Install dependencies
pipenv install

Run your MySQL server with the following connection settings:
MY_SQL_DB_NAME='littlelemon_db'
MY_SQL_DB_HOST='127.0.0.1'
MY_SQL_DB_PORT='3306'


You can run it with sqlite as well, change in .env file:
DB_CHOICE='mysql' to DB_CHOICE='sqlite' so it will run with sqlite

Then made migrations:
python manage.py makemigrations
python manage.py migrate

Create superuser:
python manage.py createsuperuser

Run server:
python manage.py runserver
```
---

### Endpoints

This application provides a RESTful API with the following endpoints.

#### Menu Operations

- **List Menu Items:**  
  `GET /menu-items`

- **View Single Menu Item:**  
  `GET /menu-items/<int:pk>`

- **Update Item of the Day:**  
  `POST /item-of-the-day/update/<int:pk>`

#### Category Operations

- **List Categories:**  
  `GET /categories`

#### Cart Operations

- **Perform Operations on Cart:**  
  `POST /cart/menu-items`

#### Order Operations

- **Create or List Orders:**  
  `POST /orders`

- **View Single Order:**  
  `GET /orders/<int:pk>`

- **Assign Order to Delivery Crew:**  
  `POST /orders/assign`

- **Mark Order as Delivered:**  
  `POST /orders/mark-delivered/<int:pk>`

#### User Management

- **List, Create, or Delete Managers:**  
  `GET, POST, DELETE /groups/manager/users`

- **List, Create, or Delete Delivery Crew Members:**  
  `GET, POST, DELETE /groups/delivery-crew/users`

---

### Tests

Unit tests are available in LittleLemonAPI/tests.py.

---

### Contributing

Contributions are welcome. Feel free to open a pull request or issue on GitHub.