#!/usr/bin/env bash
export PYTHONPATH=$(pwd)':'${PYTHONPATH}
cd executables
sudo /root/anaconda3/bin/python h1_sans.py