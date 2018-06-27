#!/usr/bin/env bash
export PYTHONPATH=$(pwd)':'${PYTHONPATH}
cd executables
python3 h1_sans.py