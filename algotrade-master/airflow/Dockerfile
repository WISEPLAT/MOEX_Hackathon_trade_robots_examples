FROM python:3.11-slim AS airflow-builder

WORKDIR /opt
COPY requirements.txt .

RUN apt-get update && apt-get install -y --no-install-recommends build-essential python3-dev g++ \
     && pip install --upgrade pip \
     && pip install wheel && pip3 wheel -r requirements.txt --wheel-dir=/opt/wheels

FROM apache/airflow:slim-2.7.3-python3.11

USER root
COPY --from=airflow-builder /opt /opt
RUN apt-get update && apt-get install -y --no-install-recommends openjdk-17-jdk-headless

USER airflow
ENV PYTHONPATH /opt/airflow/:/opt/airflow/src/
WORKDIR /opt/airflow

COPY requirements.txt entrypoint_airflow.sh ./
COPY clickhouse-native-jdbc-shaded-2.7.1.jar ./
COPY --chown=airflow:root ./dags /opt/airflow/dags

RUN pip install --no-index --find-links=/opt/wheels -r requirements.txt
