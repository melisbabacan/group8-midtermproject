#!/bin/sh
set -e

# Start SSH service for Azure App Service remote access.
service ssh start

# Start the web app server with the same settings used in App Service.
exec gunicorn --bind=0.0.0.0:${PORT:-8000} --timeout 600 app:app
