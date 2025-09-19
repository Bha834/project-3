FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY app.py .

CMD ["gunicorn", "-b", "0.0.0.0:5001", "app:app"]

EXPOSE 5001