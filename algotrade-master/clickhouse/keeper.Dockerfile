
FROM clickhouse/clickhouse-server:23.10.5.20-alpine

COPY ./server_config /etc/clickhouse-server
COPY ./server_config/metrika.xml /etc/metrika.xml

COPY ./server_config/enable_keeper.xml /etc/clickhouse-server/config.d/enable_keeper.xml