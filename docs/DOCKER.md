# Docker Deployment Guide

This guide covers running the Polymarket Trade Monitor using Docker and Docker Compose.

## 🐳 Prerequisites

- Docker installed ([Get Docker](https://docs.docker.com/get-docker/))
- Docker Compose installed (usually comes with Docker Desktop)

## 🚀 Quick Start

### 1. Basic Deployment

```bash
# Navigate to docker directory
cd docker

# Build and start the container
docker-compose up -d

# View logs in real-time
docker-compose logs -f

# Stop the container
docker-compose down
```

### 2. With Custom Configuration

Create a `.env` file (copy from `env.example`):

```bash
cd docker
cp env.example .env
```

Edit `.env`:
```bash
TRADE_THRESHOLD=10000    # Monitor trades over $10,000
POLL_INTERVAL=15         # Check every 15 seconds
```

Then start:
```bash
docker-compose up -d
```

## 📁 Directory Structure

When running with Docker, files are organized as follows:

```
polyWarket/
├── docker/                     # Docker configuration
│   ├── Dockerfile              # Container build instructions
│   ├── docker-compose.yml      # Deployment configuration
│   ├── env.example            # Example environment variables
│   └── .env                   # Your configuration (create this)
│
├── logs/                       # Mounted volume for logs
│   └── polymarket_trades.log
│
└── data/                       # Mounted volume for JSON data
    └── large_trades.json
```

## 🔧 Configuration

### Environment Variables

Configure in `docker/.env` file:

| Variable | Default | Description |
|----------|---------|-------------|
| `TRADE_THRESHOLD` | 5000 | Minimum trade value in USD to log |
| `POLL_INTERVAL` | 30 | Seconds between API checks |

### Volume Mounts

The container mounts two directories to persist data:

- `../logs:/app/logs` - Log files persist in project root `logs/` directory
- `../data:/app/data` - JSON data files persist in project root `data/` directory

## 📊 Viewing Output

### Real-time Logs

```bash
# Follow logs (Ctrl+C to exit, container keeps running)
docker-compose logs -f

# Last 100 lines
docker-compose logs --tail=100

# Logs with timestamps
docker-compose logs -f -t
```

### Log Files

Even with the container stopped, logs are available:

```bash
# View text log
cat logs/polymarket_trades.log

# View JSON data
cat data/large_trades.json

# Watch log in real-time
tail -f logs/polymarket_trades.log
```

## 🔄 Management Commands

### Start/Stop

```bash
# Navigate to docker directory
cd docker

# Start in background
docker-compose up -d

# Start with build (after code changes)
docker-compose up -d --build

# Stop container
docker-compose down

# Stop and remove volumes (CAUTION: deletes logs!)
docker-compose down -v

# Or from project root
docker-compose -f docker/docker-compose.yml up -d
```

### Container Status

```bash
# Check if running
docker-compose ps

# View resource usage
docker stats polymarket-monitor

# Check health status
docker inspect polymarket-monitor | grep -A 5 Health
```

### Logs and Debugging

```bash
# From docker directory
cd docker

# Follow logs
docker-compose logs -f

# Shell into running container
docker-compose exec polymarket-monitor sh

# View container details
docker-compose ps
docker inspect polymarket-monitor
```

## 🔨 Rebuild After Changes

After modifying code:

```bash
# Rebuild and restart
docker-compose up -d --build

# Force complete rebuild
docker-compose build --no-cache
docker-compose up -d
```

## 🎯 Advanced Usage

### Custom Docker Compose Override

Create `docker-compose.override.yml` for local customization:

```yaml
version: '3.8'

services:
  polymarket-monitor:
    environment:
      - TRADE_THRESHOLD=25000
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 1G
```

### Running Multiple Monitors

Monitor different thresholds simultaneously:

```yaml
version: '3.8'

services:
  monitor-high-value:
    build: .
    container_name: polymarket-monitor-high
    environment:
      - TRADE_THRESHOLD=50000
      - POLL_INTERVAL=30
    volumes:
      - ./logs/high:/app/logs
      - ./data/high:/app/data
  
  monitor-medium-value:
    build: .
    container_name: polymarket-monitor-medium
    environment:
      - TRADE_THRESHOLD=5000
      - POLL_INTERVAL=60
    volumes:
      - ./logs/medium:/app/logs
      - ./data/medium:/app/data
```

### Resource Limits

Limit CPU and memory usage:

```yaml
services:
  polymarket-monitor:
    deploy:
      resources:
        limits:
          cpus: '0.5'      # 50% of one CPU core
          memory: 512M     # 512 MB max
        reservations:
          cpus: '0.25'
          memory: 256M
```

## 🐛 Troubleshooting

### Container Won't Start

```bash
# Check logs
docker-compose logs

# Verify configuration
docker-compose config

# Check if ports are available
docker-compose ps
```

### Can't Connect to API

```bash
# Test from inside container
docker-compose exec polymarket-monitor python -c "import requests; print(requests.get('https://data-api.polymarket.com/trades').status_code)"

# Check health
docker inspect polymarket-monitor --format='{{json .State.Health}}'
```

### No Logs Appearing

```bash
# Ensure volumes are mounted
docker-compose exec polymarket-monitor ls -la /app/logs /app/data

# Check permissions
ls -la logs/ data/
```

### High Memory Usage

```bash
# Check current usage
docker stats polymarket-monitor

# Set memory limit in docker-compose.yml
# See Resource Limits section above
```

## 🔐 Security Notes

- The container runs as root by default (standard for Python base image)
- No sensitive data is stored (only public API data)
- No ports are exposed (outbound connections only)
- Consider using Docker secrets for production deployments

## 📝 Example Deployment Workflow

```bash
# 1. Clone/setup project
cd polyWarket

# 2. Navigate to docker directory
cd docker

# 3. Create configuration
cp env.example .env
nano .env  # Edit as needed

# 4. Build and start
docker-compose up -d --build

# 5. Verify it's running
docker-compose ps
docker-compose logs --tail=50

# 6. Monitor in real-time
docker-compose logs -f

# 7. Check collected data (from project root)
cd ..
ls -lh logs/ data/
tail logs/polymarket_trades.log

# 8. Stop when done
cd docker
docker-compose down
```

## 🚀 Production Deployment

For production use:

1. Use environment variables or Docker secrets
2. Set up log rotation (already configured in docker-compose.yml)
3. Configure restart policies (already set to `unless-stopped`)
4. Set resource limits
5. Use health checks (already configured)
6. Consider using Docker Swarm or Kubernetes for high availability

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Best Practices for Writing Dockerfiles](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)

