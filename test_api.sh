#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

# Base URL
BASE_URL="http://localhost:7000"

# Test health endpoint
echo -e "\n${GREEN}Testing health endpoint...${NC}"
curl -s $BASE_URL/health | jq .

# Create admin token
echo -e "\n${GREEN}Creating admin token...${NC}"
ADMIN_RESPONSE=$(curl -s -X POST "$BASE_URL/auth/tokens" \
  -H "Authorization: Bearer admin-token-here" \
  -H "Content-Type: application/json" \
  -d '{"is_admin": true}')

ADMIN_TOKEN=$(echo $ADMIN_RESPONSE | jq -r '.token')
echo "Admin token: $ADMIN_TOKEN"

# List all tokens
echo -e "\n${GREEN}Listing all tokens...${NC}"
curl -s -X GET "$BASE_URL/auth/tokens" \
  -H "Authorization: Bearer $ADMIN_TOKEN" | jq .

# Create regular token
echo -e "\n${GREEN}Creating regular token...${NC}"
REGULAR_RESPONSE=$(curl -s -X POST "$BASE_URL/auth/tokens" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"is_admin": false}')

REGULAR_TOKEN=$(echo $REGULAR_RESPONSE | jq -r '.token')
echo "Regular token: $REGULAR_TOKEN"

# Test image moderation (you need to provide an image)
if [ -f "test_image.jpg" ]; then
    echo -e "\n${GREEN}Testing image moderation...${NC}"
    curl -s -X POST "$BASE_URL/moderate" \
      -H "Authorization: Bearer $REGULAR_TOKEN" \
      -F "file=@test_image.jpg" | jq .
else
    echo -e "\n${RED}No test_image.jpg found for moderation testing${NC}"
fi

# Delete regular token
echo -e "\n${GREEN}Deleting regular token...${NC}"
curl -s -X DELETE "$BASE_URL/auth/tokens/$REGULAR_TOKEN" \
  -H "Authorization: Bearer $ADMIN_TOKEN" | jq .

# Verify token deletion
echo -e "\n${GREEN}Verifying token deletion...${NC}"
curl -s -X GET "$BASE_URL/auth/tokens" \
  -H "Authorization: Bearer $ADMIN_TOKEN" | jq . 