FROM python:3.10-buster

WORKDIR /app

RUN curl -sSfL https://raw.githubusercontent.com/Enapter/python-sdk/ff9c93718db62b673c553f4bf4a2d6056c19a1ba/extenstions/avahi-debian/install.sh | sh -s
ENTRYPOINT ["bash", "./entrypoint.sh"]

COPY requirements.txt requirements.txt
RUN python -m venv .venv
RUN .venv/bin/pip install -r requirements.txt

COPY script.py script.py

ENTRYPOINT ["bash", "./entrypoint.sh"]

CMD [".venv/bin/python", "script.py"]
