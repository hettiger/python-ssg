#!/bin/bash

source .venv/bin/activate
python3 src/main.py
cd public && python3 -m http.server 8888