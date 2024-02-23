FROM python:3.10

RUN python -m pip install pandas fastapi gunicorn uvicorn uvloop httptools datetime psycopg2 
## debugpy


WORKDIR /home/app

# WORKDIR /apifastmoex
# RUN pip install -r requirements.txt

ADD main.py main.py
ADD database.py database.py
ADD date_format.py date_format.py
ADD settings.py settings.py
ADD utils.py utils.py



# # CMD ["python3","-m","debugpy","--listen","localhost:5678","--wait-for-client","main.py"]

# RUN pip install --upgrade pip


# COPY . .

# RUN pip install -r requirements.txt