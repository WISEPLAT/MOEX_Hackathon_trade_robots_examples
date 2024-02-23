# frontent/Dockerfile

FROM python:3.11

COPY requirements.txt app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

HEALTHCHECK CMD curl --fail http://localhost:5981/_stcore/health

ENTRYPOINT ["streamlit", "run", "app/app.py", "--server.port=5981", "--server.address=0.0.0.0"]