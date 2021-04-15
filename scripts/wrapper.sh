#!/bin/bash
set -m
python runner.py&
python api.py
fg %1