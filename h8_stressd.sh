#!/usr/bin/env bash
export PYTHONPATH=$(pwd)':'${PYTHONPATH}
cd executables
python3 h8_stress_diff.py