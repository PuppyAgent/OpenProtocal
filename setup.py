from setuptools import setup, find_packages

setup(
    name="openprotocal",
    version="0.1.0",
    description="Open Protocal to adapt different protocols and deploy frameworks",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="JZ",
    author_email="zjlpaul@gmail.com",
    url="https://github.com/puppyagent/openprotocal",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: FastAPI",
    ],
    python_requires=">=3.7",
    install_requires=[
        "fastapi>=0.68.0",
        "pydantic>=1.8.0",
    ],
) 