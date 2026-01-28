FROM python:3.11-alpine3.22

WORKDIR /app

RUN apk add build-base

RUN python -m venv .venv
COPY requirements.txt requirements.txt
RUN .venv/bin/pip install -r requirements.txt

COPY backup.py backup.py
COPY files/ files/

CMD [".venv/bin/python", "backup.py"]
