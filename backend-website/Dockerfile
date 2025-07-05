FROM python:3.12.9-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONBUFFERED=1

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip 
RUN pip install -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput || echo "collectstatic skipped"

# Optionally:
RUN pip install gunicorn

EXPOSE 8000

CMD ["gunicorn", "backend.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
