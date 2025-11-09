#!/bin/bash
cd /Users/sumantkhapre/Downloads/project/MLProject/backend
source venv/bin/activate
export PYTHONPATH=/Users/sumantkhapre/Downloads/project/MLProject/backend:$PYTHONPATH
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload