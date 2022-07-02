#!/bin/bash

export USER_ID=$(id -u)

mkdir -p data

docker-compose build
docker-compose up