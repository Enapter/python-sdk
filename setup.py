import setuptools


def main():
    setuptools.setup(
        name="enapter",
        version=read_version(),
        long_description=read_file("README.md"),
        long_description_content_type="text/markdown",
        description="Enapter Python SDK",
        packages=setuptools.find_packages(),
        include_package_data=True,
        url="https://github.com/Enapter/python-sdk",
        author="Roman Novatorov",
        author_email="rnovatorov@enapter.com",
        install_requires=[
            "aiohttp==3.8.*",
            "asyncio-mqtt==0.12.*",
            "dnspython==2.2.*",
            "json-log-formatter==0.5.*",
        ],
    )


def read_version():
    with open("enapter/__init__.py") as f:
        local_scope = {}
        exec(f.readline(), {}, local_scope)
        return local_scope["__version__"]


def read_file(name):
    with open(name) as f:
        return f.read()


if __name__ == "__main__":
    main()
