#!/bin/sh
set -e

# Start SSH service for Azure App Service remote access.
service ssh start

# Start the web app server.
exec gunicorn --bind 0.0.0.0:${PORT:-8000} app:app
