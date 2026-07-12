#!/bin/zsh
cd "$(dirname "$0")"
python3 servidor-sites.py --host 127.0.0.1 --port 8766
