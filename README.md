# Taxi and Limousine Commission (TLC) | New York city trip data collector

* [Scope](#scope)
* [Run](#run)
    + [Manually](#manually)
    + [Docker](#docker)

## Scope

This project is used to automatically download all files that are uploaded to the TLC Trip Record Data.

## Run

### Manually

```bash
# Create virtual environment (Optional)
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Run
python3 main.py
```

### Docker

In order to run the application using `Docker` & `docker-compose`, run the following script. This script produces a
Docker image named `com.github.cnatsis/tlc-nyc-trip-data-collector:latest`

```bash
./run_docker.sh
```
