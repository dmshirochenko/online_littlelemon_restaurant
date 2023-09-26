# Online Little Lemon Restaurant

## Project Overview
This Django-based web application, "Little Lemon," serves as an online restaurant platform. Users can access the menu, make reservations, and discover more about the restaurant.

**Preparation:**
pipenv shell
pipenv install 

**Run your Mysql server with follwing connection settings:**
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


## Directory Structure
- `littlelemon/`: Main Django project folder
  - `settings.py`: Django settings
  - `urls.py`: URL routing
  - `asgi.py`: ASGI config
  - `wsgi.py`: WSGI config
- `restaurant/`: Django app folder
  - `admin.py`: Admin settings
  - `forms.py`: Form definitions
  - `models.py`: Database models
  - `urls.py`: URL routing for the restaurant app
  - `views.py`: View functions
- `manage.py`: Django management script
- `requirements.txt`: Project dependencies

## Installation
1. Clone the repository.
2. Navigate to the project directory.
3. Install dependencies: `pip install -r requirements.txt`
4. Run migrations: `python manage.py migrate`
5. Start the server: `python manage.py runserver`

## Features
- Home Page: Landing page
- About Page: Restaurant details
- Booking: Reservation functionality
- Menu: Display of menu items

## Models
- `Booking`: Holds booking details
- `Menu`: Contains menu items

## Forms
- `BookingForm`: For reservations

## URLs
- `/`: Home
- `/about/`: About
- `/book/`: Booking
- `/menu/`: Menu
- `/menu_item/<int:pk>/`: Individual menu item

## Settings
- Database: SQLite
- Static files: restaurant/static/
- Templates: restaurant/templates/

## Dependencies
- Django 3.2.7

## Future Improvements
- Implement user authentication
- Incorporate a payment gateway for online orders

## Notes
- SQLite is used for development; consider PostgreSQL for production
- Update the `SECRET_KEY` in `settings.py` for security