"""
Setup script for DJ CLI
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="dj-cli",
    version="0.4.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Create professional quality music using your terminal - with JDCL language support",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/dj-cli",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Multimedia :: Sound/Audio",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pydub>=0.25.1",
        "librosa>=0.10.1",
        "sounddevice>=0.4.6",
        "soundfile>=0.12.1",
        "pedalboard>=0.9.8",
        "mido>=1.3.0",
        "python-rtmidi>=1.5.8",
        "typer>=0.9.0",
        "rich>=13.7.0",
        "numpy>=1.24.0",
        "scipy>=1.11.0",
        "click>=8.1.7",
    ],
    entry_points={
        "console_scripts": [
            "dj-cli=src.main:app",
        ],
    },
)
