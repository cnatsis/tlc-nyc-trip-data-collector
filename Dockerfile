FROM python:3.8-slim-buster

WORKDIR /usr/app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY ./ ./

ENV PYTHONUNBUFFERED=1

STOPSIGNAL SIGINT

ENTRYPOINT ["python", "main.py"]