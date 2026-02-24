from pathlib import Path
from setuptools import setup, find_packages

README = Path(__file__).with_name("README.md")
long_description = README.read_text(encoding="utf-8") if README.exists() else ""

setup(
    name="goftino_wrapper",
    version="0.1.7.2",
    description="A wrapper for Goftino API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Alireza Khalilian",
    author_email="khalilian@payping.io",
    license="MIT",
    keywords=["Goftino", "API", "wrapper"],
    packages=find_packages(where=".", exclude=("tests", "tests.*")),
    include_package_data=True,
    python_requires=">=3.10",
    install_requires=[
        "requests>=2.0.0",
        "pydantic>=2.0.0",
        "pydantic_core>=2.0.0",
        "pytest>=8.4.2",
        "pandas>=2.0.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
