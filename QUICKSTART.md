# ⚡ Quick Start Guide

Get the Spapperi RAG Agent running in 5 minutes!

## Prerequisites

- Docker installed and running
- OpenAI API key (get one at https://platform.openai.com/api-keys)

## 3-Step Setup

### 1️⃣ Configure Environment

```bash
# Copy the example environment file
cp env.example .env

# Edit .env and add your OpenAI API key
# On macOS/Linux:
nano .env

# On Windows:
notepad .env
```

Add your key:
```
OPENAI_API_KEY=sk-your-actual-api-key-here
```

### 2️⃣ Start the System

```bash
# Build and start all services
docker-compose up --build
```

Wait for these success messages:
```
✓ Database initialized
✓ Documents loaded successfully
```

This will take 3-5 minutes on first run.

### 3️⃣ Open the Interface

Open your browser to: **http://localhost:3000**

That's it! 🎉

## Try Your First Query

Type any of these questions:

- "What products does Spapperi offer?"
- "Dove si trova Spapperi?"
- "Tell me about the TN 100 transplanter"
- "Quali sono le caratteristiche della seminatrice pneumatica?"

## Using the Makefile (Optional)

If you have `make` installed:

```bash
# Start services
make up

# Check health
make health

# View logs
make logs

# Run tests
make test

# Stop services
make down
```

## Troubleshooting

### "Port already in use"

Stop conflicting services:
```bash
# Check what's using port 8000
lsof -i :8000

# Or change ports in docker-compose.yml
```

### "Invalid API key"

1. Check your `.env` file has the correct key
2. Ensure there are no extra spaces
3. Restart backend: `docker-compose restart backend`

### "Database connection failed"

```bash
# Restart PostgreSQL
docker-compose restart postgres

# Wait 10 seconds then restart backend
sleep 10
docker-compose restart backend
```

## What's Running?

- **Frontend**: http://localhost:3000 - Chat interface
- **Backend API**: http://localhost:8000 - REST API
- **API Docs**: http://localhost:8000/docs - Swagger UI
- **Database**: localhost:5432 - PostgreSQL

## Stopping the System

```bash
# Stop services (data preserved)
docker-compose down

# Stop and remove all data
docker-compose down -v
```

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check [TEST_QUESTIONS.md](TEST_QUESTIONS.md) for test queries
- Review [ARCHITECTURE.md](ARCHITECTURE.md) to understand the system

## Need Help?

Check the logs:
```bash
docker-compose logs -f backend
```

Or visit the full [SETUP.md](SETUP.md) guide.

---

**Quick Links**:
- 🏠 [README](README.md) - Full documentation
- 🏗️ [ARCHITECTURE](ARCHITECTURE.md) - System design
- 🧪 [TEST QUESTIONS](TEST_QUESTIONS.md) - Test queries
- 🔧 [SETUP](SETUP.md) - Detailed setup guide


