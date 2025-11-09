#!/bin/bash
set -e

echo "🚀 Setting up Redis vs SQL Performance Demo..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Error: Docker is not running. Please start Docker first."
    exit 1
fi

# Get project root directory
PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$PROJECT_ROOT"

# Start Docker containers
echo "📦 Starting Docker containers (PostgreSQL & Redis)..."
docker-compose up -d

# Wait for PostgreSQL to be ready
echo "⏳ Waiting for PostgreSQL to be ready..."
until docker exec postgres pg_isready -U postgres > /dev/null 2>&1; do
    sleep 1
done
echo "✅ PostgreSQL is ready"

# Wait for Redis to be ready
echo "⏳ Waiting for Redis to be ready..."
until docker exec redis redis-cli ping > /dev/null 2>&1; do
    sleep 1
done
echo "✅ Redis is ready"

# Set up Python environment
cd redis-leaderboard
echo "🐍 Setting up Python environment..."

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate venv and install dependencies
echo "Installing dependencies..."
source venv/bin/activate
pip install --upgrade pip -q
pip install -r requirements.txt -q

# Install package in development mode
pip install -e . -q

# Initialize database and generate sample data
echo "📊 Initializing database and generating sample data (100 products)..."
python src/generate_data.py 100

echo ""
echo "✅ Setup complete!"
echo ""
echo "🎯 Quick start commands:"
echo "  cd redis-leaderboard"
echo "  source venv/bin/activate"
echo "  python src/demo.py                    # Run scalability demo"
echo "  python -m src.run_parallel 5          # Compare performance"
echo "  python src/generate_data.py 1000      # Generate more data"
echo ""
echo "📚 See docs/ for more information"
