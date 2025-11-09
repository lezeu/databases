"""Setup script to make the package properly importable."""
from setuptools import setup, find_packages

setup(
    name="redis-leaderboard",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "redis",
        "matplotlib",
        "faker",
        "psycopg2-binary",
        "psutil",
    ],
    python_requires=">=3.8",
)
