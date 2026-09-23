FROM python:3.14

COPY --from=ghcr.io/astral-sh/uv:0.12.17 /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml pyproject.toml
COPY uv.lock uv.lock

RUN uv export --frozen --no-dev --no-emit-project -o requirements.txt \
	&& uv pip install --system -r requirements.txt

COPY README.md README.md
COPY LICENSE LICENSE
COPY src src

RUN uv pip install --system --no-deps . \
	&& rm -rf src pyproject.toml uv.lock README.md LICENSE requirements.txt

STOPSIGNAL SIGINT

ENTRYPOINT ["python", "-m", "enapter"]
