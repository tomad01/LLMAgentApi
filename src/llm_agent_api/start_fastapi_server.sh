#!/bin/bash
uvicorn app:app --host 0.0.0.0 --port 8000 #> server.log 2>&1 &