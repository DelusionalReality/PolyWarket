#!/bin/bash
# Quick test script for Docker deployment

# Get the project root directory (parent of scripts/)
PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$PROJECT_ROOT"

echo "======================================"
echo "Docker Deployment Test"
echo "======================================"
echo ""
echo "Working directory: $PROJECT_ROOT"
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed"
    echo "Please install Docker: https://docs.docker.com/get-docker/"
    exit 1
fi

echo "✓ Docker found: $(docker --version)"

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed"
    echo "Please install Docker Compose"
    exit 1
fi

echo "✓ Docker Compose found: $(docker-compose --version)"
echo ""

# Check if .env exists, if not create from example
if [ ! -f docker/.env ]; then
    echo "Creating docker/.env file from docker/env.example..."
    cp docker/env.example docker/.env
    echo "✓ Created docker/.env file (you can edit it to customize settings)"
else
    echo "✓ docker/.env file already exists"
fi

echo ""
echo "======================================"
echo "Building Docker Image"
echo "======================================"
docker-compose -f docker/docker-compose.yml build

if [ $? -eq 0 ]; then
    echo "✓ Docker image built successfully"
else
    echo "❌ Failed to build Docker image"
    exit 1
fi

echo ""
echo "======================================"
echo "Testing Configuration"
echo "======================================"
docker-compose -f docker/docker-compose.yml config

echo ""
echo "======================================"
echo "Ready to Deploy!"
echo "======================================"
echo ""
echo "To start the monitor:"
echo "  docker-compose -f docker/docker-compose.yml up -d"
echo ""
echo "Or from the docker directory:"
echo "  cd docker && docker-compose up -d"
echo ""
echo "To view logs:"
echo "  docker-compose -f docker/docker-compose.yml logs -f"
echo ""
echo "To stop:"
echo "  docker-compose -f docker/docker-compose.yml down"
echo ""

