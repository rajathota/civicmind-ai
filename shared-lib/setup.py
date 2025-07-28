"""
Setup configuration for CivicMind Common Library
===============================================

Shared library package for CivicMind microservices architecture.
"""

from setuptools import setup, find_packages

# Read requirements from requirements.txt
def read_requirements():
    with open('requirements.txt', 'r') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name="civicmind-common",
    version="1.0.0",
    description="Shared library for CivicMind microservices",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author="CivicMind AI Team",
    author_email="team@civicmind.ai",
    url="https://github.com/rajathota/civicmind-ai",
    packages=find_packages(),
    install_requires=[
        "pydantic>=2.0.0",
        "fastapi>=0.100.0",
        "httpx>=0.25.0",
        "psutil>=5.9.0",
        "python-jose[cryptography]>=3.3.0",
        "python-multipart>=0.0.6"
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0"
        ]
    },
    python_requires=">=3.11",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Government",
        "Topic :: Internet :: WWW/HTTP :: HTTP Servers"
    ],
    keywords="civic, government, microservices, ai, agents",
    project_urls={
        "Bug Reports": "https://github.com/rajathota/civicmind-ai/issues",
        "Source": "https://github.com/rajathota/civicmind-ai",
        "Documentation": "https://github.com/rajathota/civicmind-ai/docs"
    }
)
