FROM python:3.9.0-alpine AS django
COPY . .
WORKDIR .
COPY requirements.txt /tmp/requirements.txt
RUN python3 -m pip install -r /tmp/requirements.txt \
    && python3 manage.py collectstatic --noinput \
    && python3 manage.py makemigrations \
    && python3 manage.py migrate \
    && DJANGO_SUPERUSER_PASSWORD=testpass \
    && python manage.py createsuperuser --noinput --username testuser --email admin@admin.com
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]