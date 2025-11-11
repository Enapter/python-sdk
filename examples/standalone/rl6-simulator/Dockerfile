FROM python:3.13-alpine

WORKDIR /app

RUN apk add build-base

RUN python -m venv .venv
COPY requirements.txt requirements.txt
RUN .venv/bin/pip install -r requirements.txt

COPY script.py script.py

CMD [".venv/bin/python", "script.py"]
