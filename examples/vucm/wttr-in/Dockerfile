FROM python:3.10-alpine3.16

WORKDIR /app

COPY requirements.txt requirements.txt
RUN python -m venv .venv
RUN .venv/bin/pip install -r requirements.txt

COPY script.py script.py

CMD [".venv/bin/python", "script.py"]
