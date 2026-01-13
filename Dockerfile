FROM python:3.14

WORKDIR /app

ADD README.md README.md
ADD setup.py setup.py
ADD src src

RUN pip install . && rm README.md && rm setup.py && rm -rf src

STOPSIGNAL SIGINT

ENTRYPOINT ["python", "-m", "enapter"]
