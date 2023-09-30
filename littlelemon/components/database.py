# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DB_CHOICE = os.getenv("DB_CHOICE", "sqlite")

if DB_CHOICE == "mysql":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": os.getenv("MY_SQL_DB_NAME", "littlelemon_db"),
            "USER": os.getenv("MY_SQL_DB_USER", "changeme"),
            "PASSWORD": os.getenv("MY_SQL_DB_PASSWORD", "changeme"),
            "HOST": os.getenv("MY_SQL_DB_HOST", "127.0.0.1"),
            "PORT": os.getenv("MY_SQL_DB_PORT", "3306"),
        }
    }
elif DB_CHOICE == "sqlite":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    raise ValueError("Invalid DB_CHOICE value")

# for tests.py
if "test" in sys.argv:
    DATABASES["default"] = {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
