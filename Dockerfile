# Start with Python 3.7
FROM python:3.7
WORKDIR /opt/app

# Set environment variables
ENV DJANGO_SETTINGS_MODULE 'littlelemon.settings'
ENV PATH="/opt/app/scripts:${PATH}"
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install Poetry
RUN pip install poetry

# Copy pyproject.toml and poetry.lock for dependency resolution
COPY pyproject.toml poetry.lock /opt/app/

# Install dependencies without creating a virtualenv
RUN poetry config virtualenvs.create false && poetry install --no-dev

# Additional setup and dependency install
# Create necessary directories
RUN mkdir -p /opt/app/staticfiles/ \
    && mkdir -p /opt/app/media/ \
    && apt-get update \
    && apt-get install -y netcat-openbsd

# Copy other project files
COPY . .

# Give permissions to scripts
RUN chmod +x scripts/*

ENTRYPOINT ["run_gunicorn.sh"]
