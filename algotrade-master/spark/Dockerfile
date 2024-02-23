FROM bitnami/spark:3.5.0

USER root

COPY ./requirements.txt /opt
RUN apt-get update && apt-get install -y --no-install-recommends build-essential python3-dev \
     && pip install --upgrade pip && pip install -r /opt/requirements.txt