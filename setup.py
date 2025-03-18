from setuptools import setup, find_packages

setup(
    name="fastapi-mcp",
    version="0.1.0",
    description="A JSON-RPC MCP protocol implementation based on FastAPI",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="JZ",
    author_email="zjlpaul@gmail.com",
    url="https://github.com/puppyagent/openprotocal",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: FastAPI",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    install_requires=[
        "fastapi>=0.68.0",
        "pydantic>=1.8.0",
        "uvicorn>=0.15.0",
        "python-multipart>=0.0.5",
    ],
    keywords="fastapi, mcp, json-rpc, api",
) 