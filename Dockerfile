FROM python:3.11

WORKDIR /usr/src/app
ARG FLASK_ENV

# Prevents Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE=1
# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt update && \
    apt install -y --no-install-recommends gcc

# Install python dependencies
COPY requirements /usr/src/app/requirements
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements/$FLASK_ENV.txt

# Copy project
COPY . /usr/src/app

CMD if [ "$FLASK_ENV" = "production" ]; then gunicorn wsgi:app -b 0.0.0.0:8000; else python manage.py; fi
