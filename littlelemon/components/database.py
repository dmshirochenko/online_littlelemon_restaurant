# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DB_CHOICE = os.getenv("DB_CHOICE", "sqlite")

if DB_CHOICE == "mysql":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": os.getenv("MYSQL_DATABASE", "littlelemon_db"),
            "USER": os.getenv("MYSQL_USER", "changeme"),
            "PASSWORD": os.getenv("MYSQL_PASSWORD", "changeme"),
            "HOST": os.getenv("MYSQL_HOST", "127.0.0.1"),
            "PORT": os.getenv("MYSQL_PORT", "3306"),
        }
    }
elif DB_CHOICE == "postgres":
    DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB"),
        "USER": os.environ.get("POSTGRES_USER"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
        "HOST": os.environ.get("POSTGRES_HOST", "127.0.0.1"),
        "PORT": os.environ.get("POSTGRES_PORT", 5432),
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
