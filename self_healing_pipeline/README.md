# Self-Healing CI/CD Pipeline

## Overview
This project demonstrates a **self-healing CI/CD pipeline** that automatically:
- Retries failed builds
- Quarantines flaky tests
- Switches to mock services when dependencies fail

## Features
- AI-driven retry logic
- Flaky test quarantine
- Mock service substitution
- Dockerized for portability

## Setup
#bash
git clone <repo>
cd self-healing-ci-cd-pipeline
docker-compose up

#sample usage
python src/pipeline.py --config configs/pipeline_config.yaml
