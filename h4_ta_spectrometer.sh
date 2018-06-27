#!/usr/bin/env bash
export PYTHONPATH=$(pwd)':'${PYTHONPATH}
cd executables
python3 h4_tas.py