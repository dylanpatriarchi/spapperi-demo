# 🚀 Setup Guide for Spapperi RAG Agent

Complete setup instructions for the Spapperi RAG Agent system.

## Prerequisites

Before starting, ensure you have the following installed:

- **Docker**: Version 20.10 or higher
- **Docker Compose**: Version 2.0 or higher
- **OpenAI API Key**: Get one from https://platform.openai.com/api-keys

## Step-by-Step Setup

### 1. Environment Configuration

Create a `.env` file in the project root:

```bash
# Copy the example file
cp env.example .env
```

Edit `.env` and add your OpenAI API key:

```env
OPENAI_API_KEY=sk-your-actual-api-key-here
```

### 2. PDF Catalogs

Ensure your PDF catalogs are in the project root:

```
spapperi-demo/
├── Piantatalee-TP.pdf
├── Rincalzatore-SM.pdf
├── Seminatrice-pneumatica-SMP.pdf
└── Stendi-film-SF.pdf
```

These files will be automatically mounted into the Docker container.

### 3. Build and Start Services

```bash
# Build all Docker images
docker-compose build

# Start all services
docker-compose up -d
```

The first startup will take several minutes to:
1. Download base images (Python, Node, PostgreSQL)
2. Install dependencies
3. Initialize the database
4. Process and index all PDF documents
5. Create vector embeddings

### 4. Monitor Startup Progress

Watch the logs to see the initialization:

```bash
# Watch all logs
docker-compose logs -f

# Watch only backend logs
docker-compose logs -f backend

# Check if database is ready
docker-compose logs -f postgres
```

Look for these success messages:

```
backend  | ✓ Database initialized
backend  | Loading company information...
backend  | Processing Piantatalee-TP.pdf...
backend  | Processing Rincalzatore-SM.pdf...
backend  | Processing Seminatrice-pneumatica-SMP.pdf...
backend  | Processing Stendi-film-SF.pdf...
backend  | ✓ All documents loaded successfully!
```

### 5. Verify Installation

Once all services are running, verify the installation:

#### Check Backend Health

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "database_connected": true,
  "documents_loaded": 150
}
```

#### Check Statistics

```bash
curl http://localhost:8000/stats
```

Expected response:
```json
{
  "total_documents": 150,
  "unique_sources": 5,
  "sources": [
    "company_info",
    "Piantatalee-TP.pdf",
    "Rincalzatore-SM.pdf",
    "Seminatrice-pneumatica-SMP.pdf",
    "Stendi-film-SF.pdf"
  ]
}
```

#### Access Frontend

Open your browser and navigate to:
- **Frontend**: http://localhost:3000
- **API Documentation**: http://localhost:8000/docs

### 6. Test the System

Try a simple query:

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What products does Spapperi offer?"}'
```

Or use the web interface at http://localhost:3000

## Troubleshooting

### Issue: Database Connection Failed

**Symptoms**: Backend logs show connection errors

**Solution**:
```bash
# Check if PostgreSQL is running
docker-compose ps postgres

# Restart PostgreSQL
docker-compose restart postgres

# Wait 10 seconds then restart backend
docker-compose restart backend
```

### Issue: OpenAI API Errors

**Symptoms**: "Invalid API key" or rate limit errors

**Solutions**:
1. Verify your API key in `.env` file
2. Check your OpenAI account has available credits
3. Ensure there are no extra spaces in the API key

```bash
# Restart backend with new credentials
docker-compose restart backend
```

### Issue: Documents Not Loading

**Symptoms**: `documents_loaded: 0` in health check

**Solutions**:
```bash
# Check if PDFs are mounted correctly
docker-compose exec backend ls -la /data

# Manually trigger document reload
curl -X POST http://localhost:8000/reload-documents

# Check backend logs for errors
docker-compose logs backend
```

### Issue: Frontend Can't Connect to Backend

**Symptoms**: Network errors in browser console

**Solutions**:
1. Verify backend is running: `docker-compose ps backend`
2. Check backend health: `curl http://localhost:8000/health`
3. Clear browser cache and reload
4. Check CORS configuration in `backend/main.py`

### Issue: Port Already in Use

**Symptoms**: "port is already allocated" error

**Solutions**:
```bash
# Check what's using the ports
lsof -i :8000
lsof -i :3000
lsof -i :5432

# Either stop the conflicting service or change ports in docker-compose.yml
# Example: Change frontend port to 3001
# ports:
#   - "3001:3000"
```

## Advanced Configuration

### Custom Chunk Size

Edit `backend/config.py`:

```python
chunk_size: int = 1500  # Increase for larger chunks
chunk_overlap: int = 300  # Increase overlap proportionally
```

### Use Different OpenAI Model

Edit `.env`:

```env
OPENAI_MODEL=gpt-3.5-turbo  # For faster, cheaper responses
# or
OPENAI_MODEL=gpt-4-turbo-preview  # For better quality
```

### Adjust Number of Retrieved Documents

Edit `backend/config.py`:

```python
top_k_results: int = 10  # Retrieve more context
```

### Change Database Password

Edit `docker-compose.yml`:

```yaml
postgres:
  environment:
    POSTGRES_PASSWORD: your_new_secure_password

backend:
  environment:
    DATABASE_URL: postgresql://spapperi:your_new_secure_password@postgres:5432/spapperi_rag
```

## Production Deployment

### Security Hardening

1. **Change default passwords**:
   - Database password in `docker-compose.yml`
   - Add authentication to API endpoints

2. **Configure CORS properly**:
   Edit `backend/main.py`:
   ```python
   allow_origins=["https://your-domain.com"]  # Specific origin
   ```

3. **Use environment variables for secrets**:
   - Never commit `.env` to version control
   - Use Docker secrets or Kubernetes secrets in production

4. **Enable HTTPS**:
   - Add nginx reverse proxy
   - Configure SSL certificates

### Performance Optimization

1. **Use production builds**:
   ```bash
   # Frontend
   cd frontend
   npm run build
   
   # Serve with nginx instead of development server
   ```

2. **Database optimization**:
   - Increase PostgreSQL memory settings
   - Add indexes for frequent queries
   - Regular VACUUM operations

3. **Caching**:
   - Add Redis for response caching
   - Cache frequently asked questions

### Monitoring

Set up monitoring for:
- API response times
- Database query performance
- Error rates
- OpenAI API usage and costs

## Backup and Recovery

### Backup Database

```bash
# Create backup
docker-compose exec -T postgres pg_dump -U spapperi spapperi_rag > backup_$(date +%Y%m%d).sql

# Restore backup
docker-compose exec -T postgres psql -U spapperi spapperi_rag < backup_20250101.sql
```

### Backup Vector Embeddings

The vector embeddings are stored in PostgreSQL, so database backups include them. However, if you need to regenerate embeddings:

```bash
curl -X POST http://localhost:8000/reload-documents
```

## Updating the System

### Update Application Code

```bash
git pull origin main
docker-compose down
docker-compose build
docker-compose up -d
```

### Update Dependencies

```bash
# Backend
cd backend
pip install -r requirements.txt --upgrade

# Frontend
cd frontend
npm update

# Rebuild containers
docker-compose build
```

### Add New Documents

1. Place new PDF files in the project root
2. Update `backend/document_loader.py`:
   ```python
   pdf_files = [
       "Piantatalee-TP.pdf",
       "Rincalzatore-SM.pdf",
       "Seminatrice-pneumatica-SMP.pdf",
       "Stendi-film-SF.pdf",
       "New-Product-Catalog.pdf"  # Add new file
   ]
   ```
3. Reload documents:
   ```bash
   curl -X POST http://localhost:8000/reload-documents
   ```

## Useful Commands

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# Restart a specific service
docker-compose restart backend

# Access backend shell
docker-compose exec backend bash

# Access database
docker-compose exec postgres psql -U spapperi spapperi_rag

# Check service status
docker-compose ps

# Remove all containers and volumes (CAUTION: deletes data)
docker-compose down -v

# Rebuild without cache
docker-compose build --no-cache
```

## Getting Help

If you encounter issues not covered here:

1. Check the logs: `docker-compose logs -f`
2. Review the API documentation: http://localhost:8000/docs
3. Test with curl commands to isolate the issue
4. Check OpenAI API status: https://status.openai.com/

---

**Setup Complete!** 🎉

Your Spapperi RAG Agent should now be fully operational. Access the web interface at http://localhost:3000 and start asking questions!


