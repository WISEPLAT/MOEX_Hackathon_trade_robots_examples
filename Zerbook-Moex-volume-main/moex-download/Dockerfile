FROM python:3.10

RUN python -m pip install asyncio pandas aiohttp datetime psycopg2 

WORKDIR /home/app

COPY . .

# ADD main.py main.py

CMD python3 main.py