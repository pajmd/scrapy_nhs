#!/usr/bin/env bash

cd /app/nhs/nhs
python -m pytest -s /app/nhs/tests/test_kafka_pipeline.py