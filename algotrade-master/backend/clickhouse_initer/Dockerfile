FROM python:3.11-slim AS clickhouse-initer-builder

WORKDIR /opt
COPY requirements.txt .

RUN apt-get update && apt-get install -y --no-install-recommends curl tini \
    && pip install wheel && pip3 wheel -r requirements.txt --wheel-dir=/opt/wheels


FROM python:3.11-slim

COPY --from=clickhouse-initer-builder /opt /opt
COPY --from=clickhouse-initer-builder /usr/bin/tini /usr/bin/tini

WORKDIR /opt/clickhouse_initer
ENTRYPOINT [ "tini", "--" ]
CMD [ "python3", "./src/main.py" ]  

COPY ./src ./src
RUN pip install --no-index --find-links=/opt/wheels -r ../requirements.txt
