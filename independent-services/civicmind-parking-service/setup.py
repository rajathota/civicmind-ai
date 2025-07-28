"""
Setup configuration for CivicMind Parking Service
================================================
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="civicmind-parking-service",
    version="1.0.0",
    author="CivicMind AI Team",
    author_email="team@civicmind.ai",
    description="Independent microservice for parking-related civic issues",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/civicmind-ai/civicmind-parking-service",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Government",
        "Topic :: Government :: Civic Services",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "pytest-httpx>=0.26.0",
            "black>=23.0.0",
            "ruff>=0.1.0",
            "mypy>=1.7.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "parking-service=parking_service.main:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
