import dockie
from setuptools import setup, find_packages

install_requires = ["setuptools", "dictquery"]


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
    install_requires=install_requires,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Utilities",
    ],
    project_urls={"GitHub": PROJECT_URL},
)
