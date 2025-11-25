#!/bin/bash

# Test script for Spapperi RAG Agent API
# Usage: ./scripts/test-api.sh

API_URL="http://localhost:8000"

echo "🧪 Testing Spapperi RAG Agent API"
echo "=================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test 1: Health Check
echo -e "${YELLOW}Test 1: Health Check${NC}"
response=$(curl -s -o /dev/null -w "%{http_code}" "$API_URL/health")
if [ $response -eq 200 ]; then
    echo -e "${GREEN}✓ Health check passed${NC}"
    curl -s "$API_URL/health" | python3 -m json.tool
else
    echo -e "${RED}✗ Health check failed (HTTP $response)${NC}"
fi
echo ""

# Test 2: Statistics
echo -e "${YELLOW}Test 2: Statistics${NC}"
response=$(curl -s -o /dev/null -w "%{http_code}" "$API_URL/stats")
if [ $response -eq 200 ]; then
    echo -e "${GREEN}✓ Stats retrieved${NC}"
    curl -s "$API_URL/stats" | python3 -m json.tool
else
    echo -e "${RED}✗ Stats retrieval failed (HTTP $response)${NC}"
fi
echo ""

# Test 3: English Query
echo -e "${YELLOW}Test 3: English Query${NC}"
echo "Question: What products does Spapperi offer?"
response=$(curl -s -X POST "$API_URL/query" \
    -H "Content-Type: application/json" \
    -d '{"question": "What products does Spapperi offer?"}')
if echo "$response" | jq -e '.answer' > /dev/null 2>&1; then
    echo -e "${GREEN}✓ English query successful${NC}"
    echo "$response" | jq '.answer'
else
    echo -e "${RED}✗ English query failed${NC}"
fi
echo ""

# Test 4: Italian Query
echo -e "${YELLOW}Test 4: Italian Query${NC}"
echo "Domanda: Dove si trova Spapperi?"
response=$(curl -s -X POST "$API_URL/query" \
    -H "Content-Type: application/json" \
    -d '{"question": "Dove si trova Spapperi?"}')
if echo "$response" | jq -e '.answer' > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Italian query successful${NC}"
    echo "$response" | jq '.answer'
else
    echo -e "${RED}✗ Italian query failed${NC}"
fi
echo ""

# Test 5: French Query
echo -e "${YELLOW}Test 5: French Query${NC}"
echo "Question: Quels sont les produits de Spapperi?"
response=$(curl -s -X POST "$API_URL/query" \
    -H "Content-Type: application/json" \
    -d '{"question": "Quels sont les produits de Spapperi?"}')
if echo "$response" | jq -e '.answer' > /dev/null 2>&1; then
    echo -e "${GREEN}✓ French query successful${NC}"
    echo "$response" | jq '.answer'
else
    echo -e "${RED}✗ French query failed${NC}"
fi
echo ""

# Test 6: Technical Query
echo -e "${YELLOW}Test 6: Technical Query${NC}"
echo "Question: What are the specifications of the TN 100 transplanter?"
response=$(curl -s -X POST "$API_URL/query" \
    -H "Content-Type: application/json" \
    -d '{"question": "What are the specifications of the TN 100 transplanter?"}')
if echo "$response" | jq -e '.answer' > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Technical query successful${NC}"
    echo "$response" | jq '.sources'
else
    echo -e "${RED}✗ Technical query failed${NC}"
fi
echo ""

echo "=================================="
echo -e "${GREEN}✓ Testing complete!${NC}"


