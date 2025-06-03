#!/usr/bin/env bash

# Navigate to this folder before running:
#    cd remoteuac/backend
#
# Make sure to give this script execute permissions:
#    chmod +x run.sh
#
# Start Uvicorn with auto-reload for development

# cd remoteuac/backend

uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
# --reload makes it auto-reload when you change the code



# If you want to run it in production, you can use:
# uvicorn app.main:app --host
