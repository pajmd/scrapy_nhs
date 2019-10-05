#!/usr/bin/env bash

cd /app/nhs/nhs
python -m pytest /app/nhs/tests/test_kafka_pipeline.py