from setuptools import setup, find_packages
import os

# Read the long description from the README file
with open(os.path.join(os.path.dirname(__file__), "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="ztkn",
    version="0.1.0",
    description="CLI Tool for Zettelkasten Graph Visualization",
    long_description=long_description,
    long_description_content_type="text/markdown",  # Specify the content type
    author="Aerith Netzer",
    author_email="your.email@example.com",
    packages=find_packages(),
    install_requires=[
        "networkx",
        "tqdm",
        "pyvis",
        "flask",
    ],
    entry_points={
        "console_scripts": [
            "ztkn=ztkn.src:main",  # Corrected entry point
        ],
    },
)
