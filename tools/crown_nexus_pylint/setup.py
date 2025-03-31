"""Setup script for crown_nexus_pylint package."""

from setuptools import setup, find_packages

setup(
    name="crown-nexus-pylint",
    version="0.1.0",
    description="Pylint plugin for Crown Nexus audit checks",
    author="Ryan Serra",
    packages=find_packages(),
    install_requires=[
        "pylint>=3.0.0",
    ],
    python_requires=">=3.8",
)
