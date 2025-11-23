#!/bin/bash
exec uvicorn chiron.api.main:app \
    --host 0.0.0.0 \
    --port 8000 \
    --workers 4 \
    --timeout-keep-alive 20