#!/usr/bin/env bash
set -euo pipefail

BASE_URL=${1:-http://127.0.0.1:8000}

echo "JSON only:"
curl -s -X POST "$BASE_URL/api/v1/translate"   -H "Content-Type: application/json"   -d '{"text":"Machine learning is a subset of AI ...","output_format":"json","include_vocabulary":true}' | jq .

echo
echo "Generate Word:"
curl -s -X POST "$BASE_URL/api/v1/translate"   -H "Content-Type: application/json"   -d '{"text":"Reinforcement learning optimizes actions via rewards.","output_format":"word","include_vocabulary":true}' | jq .
