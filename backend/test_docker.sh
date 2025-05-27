#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

# Function to print colored messages
print_message() {
    echo -e "${GREEN}$1${NC}"
}

# Setup Python virtual environment and install dependencies
print_message "Setting up Python environment..."
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install pytest pytest-asyncio

# Start Docker containers
print_message "Starting Docker containers..."
cd ..
docker-compose up -d

# Wait for services to be ready
print_message "Waiting for services to be ready..."
sleep 10

# Initialize database
print_message "Initializing database..."
cd backend
source venv/bin/activate
python app/init_db.py

# Run the tests
print_message "Running tests..."
python -m pytest tests/test_docker.py -v

# Capture the test result
TEST_RESULT=$?

# Stop containers
print_message "Stopping Docker containers..."
cd ..
docker-compose down

# Cleanup virtual environment
print_message "Cleaning up..."
cd backend
deactivate
rm -rf venv

# Exit with the test result
exit $TEST_RESULT 