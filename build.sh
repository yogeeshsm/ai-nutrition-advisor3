#!/bin/bash
# Render build script

echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Setting up database..."
python -c "import database as db; db.initialize_database()" || echo "Database already initialized"

echo "Build completed successfully!"
