from setuptools import setup, find_packages

setup(
    name="data_connectors_api",
    version="0.1.0",
    description="A tool to fetch data from different soruces",
    author="Luke Friedrichs",
    packages=find_packages(),
    install_requires=[
        "requests",
        "python-dotenv"
    ],
    entry_points={
        'console_scripts': [
            'fetchconf=scripts.run:main',
        ],
    },
)
