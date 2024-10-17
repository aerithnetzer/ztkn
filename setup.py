from setuptools import setup, find_packages

setup(
    name="ztkn",
    version="0.1.0",
    description="CLI Tool for Zettelkasten Graph Visualization",
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
