from setuptools import setup, find_packages

setup(
    name="gpi",
    version="0.1.0",
    description="SDK framework for Python AI Agentic development",
    author="GPI Team",
    packages=find_packages(),
    install_requires=[
        "requests",
        "flask",
    ],
    python_requires=">=3.7",
) 