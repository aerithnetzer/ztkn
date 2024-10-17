#!/bin/bash

# Clone the repository
git clone https://github.com/aerithnetzer/ztkn/

# Move into the cloned directory
cd ztkn

# Make setup script executable and run it
chmod +x setup.py
python3 setup.py install

# Create a symlink for the ztkn CLI tool
ln -s $(pwd)/src/ztkn.py /usr/local/bin/ztkn
