#!/bin/bash
 
cd cam || { echo "Directory 'cam' not found"; exit 1; }
 
source venv/bin/activate || { echo "Failed to activate virtual environment"; exit 1; }
 
cd inside-out-server || { echo "Directory 'inside-out-server' not found"; exit 1; }
 
python multi_shared.py || { echo "Failed to start multi_shared.py"; exit 1; }