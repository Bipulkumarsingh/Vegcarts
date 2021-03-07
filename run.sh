#!/bin/bash

set -e
CPU=$(nproc)
echo "NO. of cpu available: $CPU"
gunicorn -b 127.0.0.1:8006 app:app --reload --threads 2 --workers "$CPU" -t 300