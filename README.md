## Project Overview

This Django-based web application, "Little Lemon," serves as an online restaurant platform. Users can access the menu, make reservations, and discover more about the restaurant.

**Endpoints for Testing**

1. Does the web application use Django to serve static HTML content?
   - Directory: `restaurant/static`

2. Has the learner committed the project to a Git repository?
   - Repository: [GitHub - online_littlelemon_restaurant](https://github.com/dmshirochenko/online_littlelemon_restaurant)

3. Does the application connect the backend to a MySQL database?
   - Configuration: `littlelemon/settings.py`

4. Are the menu and table booking APIs implemented?
   - **Menu**
     - Get Menu Items: `GET http://127.0.0.1:8000/api/menu-items`
     - Create Menu Item (Superuser only, category must exist):
       ```json
       POST http://127.0.0.1:8000/api/menu-items
       {
           "title": "New item",
           "price": 12,
           "featured": false,
           "is_item_of_the_day": false,
           "category": 1
       }
       ```
   - **Booking**
     - Create Booking:
       ```json
       POST http://127.0.0.1:8000/bookings/
       {
           "first_name": "John",
           "reservation_date": "2023-09-28",
           "reservation_slot": "11"
       }
       ```
     - Check Bookings:
       `GET http://127.0.0.1:8000/bookings/?date=2023-09-28`

5. Is the application set up with user registration and authentication?
   - Registration: `http://127.0.0.1:8000/auth/users/`
   - Login: `http://127.0.0.1:8000/auth/token/login/`

6. Does the application contain unit tests?
   - Test File: `LittleLemonAPI/tests.py`

7. Can the API be tested with the Insomnia REST client?
   - Yes

**Installation:**

```shell
# Activate the virtual environment
pipenv shell

 Install dependencies
pipenv install

**Run your MySQL server with the following connection settings:**

MY_SQL_DB_NAME='littlelemon_db'
MY_SQL_DB_HOST='127.0.0.1'
MY_SQL_DB_PORT='3306'


IF your don't have mysql server, you can change in .env file
DB_CHOICE='mysql' to DB_CHOICE='sqlite' so it will run with sqlite

**Then made migrations:**
python manage.py makemigrations
python manage.py migrate

**Create superuser:**
python manage.py createsuperuser

**Run server:**
python manage.py runserver
