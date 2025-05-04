#!/bin/bash

source .venv/bin/activate
python3 -m unittest discover -s src -p "*_test.py"