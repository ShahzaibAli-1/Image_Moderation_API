#!/bin/bash

echo "Waiting for MongoDB to be ready..."
while ! nc -z mongodb 27017; do
  sleep 1
done
echo "MongoDB is ready!"

echo "Initializing database..."
python init_db.py

echo "Starting application..."
uvicorn main:app --host 0.0.0.0 --port 7000 