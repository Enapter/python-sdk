import setuptools


def main() -> None:
    setuptools.setup(
        name="enapter",
        version=read_version(),
        long_description=read_file("README.md"),
        long_description_content_type="text/markdown",
        description="Enapter Python SDK",
        packages=setuptools.find_packages("src"),
        package_dir={"": "src"},
        url="https://github.com/Enapter/python-sdk",
        author="Roman Novatorov",
        author_email="rnovatorov@enapter.com",
        install_requires=[
            "aiomqtt==2.4.*",
            "dnspython==2.8.*",
            "json-log-formatter==1.1.*",
            "httpx==0.28.*",
        ],
    )


def read_version() -> str:
    with open("src/enapter/__init__.py") as f:
        local_scope: dict = {}
        exec(f.readline(), {}, local_scope)
        return local_scope["__version__"]


def read_file(name) -> str:
    with open(name) as f:
        return f.read()


if __name__ == "__main__":
    main()
