#!/bin/bash

set -e

echo "Creating new venv..."
python3 -m venv venv
source venv/bin/activate

echo "Installing requirements..."
pip install -r requirements.txt

echo "Setting up database..."
python manage.py migrate

echo "Running local server..."
python manage.py runserver 8000