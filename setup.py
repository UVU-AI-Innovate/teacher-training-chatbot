from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="chatbot",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="An AI-powered chatbot for education",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/chatbot",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "black==24.1.1",
            "isort==5.13.2",
            "flake8==7.0.0",
            "flake8-docstrings==1.7.0",
            "mypy==1.8.0",
            "pre-commit==3.6.0",
            "pytest==8.0.0",
            "pytest-cov==4.1.0",
        ],
    },
) 