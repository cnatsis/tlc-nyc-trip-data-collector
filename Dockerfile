FROM --platform=linux/amd64 python:3.8

RUN apt-get install -y wget

# Adding trusting keys to apt for repositories
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -

# Adding Google Chrome to the repositories
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'

RUN apt-get -y update
RUN apt-get install -y google-chrome-stable

WORKDIR /usr/app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY ./ ./

ENV PYTHONUNBUFFERED=1

STOPSIGNAL SIGINT

ENTRYPOINT ["python", "main.py"]