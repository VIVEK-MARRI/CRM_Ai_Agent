#!/bin/bash

# Build production images
docker-compose -f docker-compose.yml build --no-cache

# Optionally tag for registry
# docker tag lead-scoring-agent_backend:latest your-registry/lead-scoring-agent:backend-latest
# docker tag lead-scoring-agent_frontend:latest your-registry/lead-scoring-agent:frontend-latest

# Optionally push to registry
# docker push your-registry/lead-scoring-agent:backend-latest
# docker push your-registry/lead-scoring-agent:frontend-latest

echo "✅ Build complete! Docker images are ready for deployment."
