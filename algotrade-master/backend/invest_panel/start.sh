#!/bin/bash 

uvicorn src.main:app --host 0.0.0.0 --port $INVEST_PANEL_PORT --reload --log-level debug
# gunicorn src.main:app -k uvicorn.workers.UvicornWorker --reload --bind 0.0.0.0:$INVEST_PANEL_PORT