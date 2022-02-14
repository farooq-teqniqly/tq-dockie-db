import dockie
from setuptools import setup, find_packages


def long_description():
    with open("README.md", encoding="utf-8") as f:
        return f.read()


PROJECT_URL = "https://github.com/farooq-teqniqly/tq-dockie-db"

setup(
    name="tq-dockie-db",
    version=dockie.__version__,
    description=dockie.__doc__.strip(),
    long_description=long_description(),
    long_description_content_type="text/markdown",
    url=PROJECT_URL,
    author=dockie.__author__,
    author_email="farooq@teqniqly.com",
    license=dockie.__license__,
    packages=find_packages(include=["dockie", "dockie.*"]),
    python_requires=">=3.8",
    install_requires=["setuptools", "dictquery"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Database :: Database Engines/Servers",
    ],
    project_urls={"GitHub": PROJECT_URL},
)
