# backend/Dockerfile

FROM python:3.11

COPY requirements.txt app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

CMD ["python", "main.py"]