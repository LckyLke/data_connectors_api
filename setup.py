from setuptools import setup, find_packages

setup(
    name="confluence_api",
    version="0.1.0",
    description="A tool to fetch data from Confluence",
    author="Luke Friedrichs",
    packages=find_packages(),
    install_requires=[
        "requests",
        "python-dotenv"
    ],
)
