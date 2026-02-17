"""
Setup script for PAD Framework
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="pad-framework",
    version="1.0.0",
    author="PAD Framework Team",
    author_email="",
    description="Comprehensive framework for Microsoft Power Automate Desktop",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/pad-framework",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "pad=pad_framework.cli:main",
            "pad-framework=pad_framework.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "pad_framework": ["configs/*.yaml", "templates/*.json"],
    },
)
