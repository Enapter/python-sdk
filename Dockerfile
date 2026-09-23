FROM python:3.14

COPY --from=ghcr.io/astral-sh/uv:0.12.17 /uv /uvx /bin/

WORKDIR /app

ADD pyproject.toml pyproject.toml
ADD uv.lock uv.lock

RUN uv export --frozen --no-dev --no-emit-project -o requirements.txt \
	&& uv pip install --system -r requirements.txt

ADD README.md README.md
ADD LICENSE LICENSE
ADD src src

RUN uv pip install --system --no-deps . \
	&& rm -rf src pyproject.toml uv.lock README.md LICENSE requirements.txt

STOPSIGNAL SIGINT

ENTRYPOINT ["python", "-m", "enapter"]
