FROM python:3.11-slim AS invest-panel-builder

WORKDIR /opt
COPY requirements.txt ./

RUN apt-get update && apt-get install -y --no-install-recommends gcc musl-dev libc-dev librdkafka-dev rustc cargo && \
     pip install --upgrade pip \
     && pip install wheel && pip3 wheel -r requirements.txt --wheel-dir=/opt/wheels


FROM python:3.11-slim

COPY --from=invest-panel-builder /opt /opt
COPY --from=invest-panel-builder /usr/lib/ /usr/lib/

WORKDIR /opt/invest_panel
ENTRYPOINT ["/bin/bash", "-c", "chmod +x ./start.sh && ./start.sh"]

COPY . .
RUN pip install --no-index --find-links=/opt/wheels -r requirements.txt