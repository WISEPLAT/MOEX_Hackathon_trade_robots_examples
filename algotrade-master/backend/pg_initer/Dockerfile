FROM python:3.11-slim AS pg-initer-builder

WORKDIR /opt
COPY requirements.txt .

RUN apt-get update && apt-get install -y --no-install-recommends curl tini \
    && pip install wheel && pip3 wheel -r requirements.txt --wheel-dir=/opt/wheels


FROM python:3.11-slim

COPY --from=pg-initer-builder /opt /opt
COPY --from=pg-initer-builder /usr/bin/tini /usr/bin/tini

WORKDIR /opt/pg_initer
ENTRYPOINT [ "tini", "--" ]
CMD [ "python3", "./src/main.py" ]

COPY ./src ./src
RUN pip install --no-index --find-links=/opt/wheels -r ../requirements.txt