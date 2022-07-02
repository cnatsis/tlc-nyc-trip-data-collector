# TLC New York City trip data collector

* [Scope](#scope)
* [Run](#run)
    + [Manually](#manually)
    + [Docker](#docker)
+ [Versions](#versions)

## Scope

This project is used to automatically download all files that are uploaded to the Taxi and Limousine Commission (TLC)
Trip Record Data for taxi trips in New York City.

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

Once the downloading of files is complete, they will be stored in the `data` directory.

### Docker

In order to run the application using `Docker` & `docker-compose`, run the following script. This script produces a
Docker image named `com.github.cnatsis/tlc-nyc-trip-data-collector:latest`

```bash
./run_docker.sh
```

**NOTE:** Running this application using ARM architecture processor is currently not supported due to Selenium
incompatibilities.

### Versions

**Python:** 3.8
