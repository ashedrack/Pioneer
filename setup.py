from setuptools import setup, find_packages

setup(
    name="cloud-pioneer",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.104.1",
        "uvicorn>=0.24.0",
        "python-dotenv==1.0.0",
        "boto3>=1.29.3",
        "botocore==1.34.14",
        "pydantic>=2.5.1",
        "pydantic-settings==2.1.0",
        "pandas>=2.1.3",
        "numpy>=1.26.2",
        "scikit-learn==1.3.2",
        "joblib==1.3.2",
        "kafka-python==2.0.2"
    ],
    extras_require={
        "test": [
            "pytest>=7.4.3",
            "pytest-asyncio>=0.23.0",
            "pytest-cov>=4.1.0",
            "pytest-mock>=3.12.0",
            "httpx>=0.25.1"
        ]
    }
)
