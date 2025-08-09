from setuptools import setup, find_packages

setup(
    name="zyntra",
    version="1.0.0",
    author="0xF55",
    description="A simple powerfull module for files handling",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/0xF55/zyntra",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
