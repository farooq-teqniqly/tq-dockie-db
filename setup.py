"""
Setup module.
"""

from setuptools import setup, find_packages
import dockie


def long_description():
    """
    Returns the text of the readme.
    :return: The text of the readme.
    """
    with open("README.md", encoding="utf-8") as file:
        return file.read()


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
    python_requires=">=3.9",
    install_requires=[],
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
