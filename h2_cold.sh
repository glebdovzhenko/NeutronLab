#!/usr/bin/env bash
export PYTHONPATH=$(pwd)':'${PYTHONPATH}
cd executables
python3 h2_cold_diff.py