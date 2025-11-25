# 🏗️ Architecture Documentation

## System Overview

The Spapperi RAG Agent is a production-ready Retrieval-Augmented Generation system designed to provide accurate, contextual information about Spapperi's agricultural machinery products.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                         User Browser                         │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           │ HTTP/HTTPS
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                     React Frontend                           │
│                   (Port 3000)                                │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  - Styled Components UI                                 │ │
│  │  - Chat Interface                                       │ │
│  │  - Real-time Updates                                    │ │
│  └────────────────────────────────────────────────────────┘ │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           │ REST API
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                   FastAPI Backend                            │
│                   (Port 8000)                                │
│  ┌────────────────────────────────────────────────────────┐ │
│  │              API Endpoints                              │ │
│  │  - /query (POST)   - /health (GET)                     │ │
│  │  - /stats (GET)    - /reload-documents (POST)          │ │
│  └────────────┬──────────────────────┬────────────────────┘ │
│               │                       │                      │
│  ┌────────────▼──────────┐  ┌───────▼──────────────────┐  │
│  │    RAG Agent          │  │  Document Loader         │  │
│  │  - Query Processing   │  │  - PDF Extraction        │  │
│  │  - Context Retrieval  │  │  - Text Chunking         │  │
│  │  - Response Gen       │  │  - Embedding Creation    │  │
│  └────────────┬──────────┘  └───────┬──────────────────┘  │
│               │                      │                      │
└───────────────┼──────────────────────┼──────────────────────┘
                │                      │
                │                      │
      ┌─────────▼──────────┐  ┌───────▼──────────┐
      │   OpenAI API       │  │  OpenAI API      │
      │   GPT-4 Turbo      │  │  Embeddings      │
      └────────────────────┘  └──────────────────┘
                │
                │
┌───────────────▼──────────────────────────────────────────┐
│              PostgreSQL + pgvector                        │
│              (Port 5432)                                  │
│  ┌──────────────────────────────────────────────────────┐│
│  │  Documents Table                                      ││
│  │  ├─ id (Integer)                                      ││
│  │  ├─ content (Text)                                    ││
│  │  ├─ source (String)                                   ││
│  │  ├─ metadata (JSON)                                   ││
│  │  └─ embedding (Vector[1536])                          ││
│  │                                                        ││
│  │  Indexes:                                             ││
│  │  └─ Vector similarity index (HNSW/IVFFlat)           ││
│  └──────────────────────────────────────────────────────┘│
└───────────────────────────────────────────────────────────┘
```

## Component Details

### 1. Frontend (React)

**Purpose**: User interface for interacting with the RAG agent

**Key Technologies**:
- React 18
- styled-components for CSS-in-JS
- axios for API communication
- react-markdown for formatted responses

**Features**:
- Real-time chat interface
- Message history
- Source attribution display
- Multi-language support
- Health status monitoring
- Sample questions

**Files**:
- `frontend/src/App.js` - Main application component
- `frontend/public/index.html` - HTML template
- `frontend/Dockerfile` - Container configuration

### 2. Backend (FastAPI + Python)

**Purpose**: API server and RAG orchestration

**Key Technologies**:
- FastAPI for REST API
- LangChain for RAG utilities
- SQLAlchemy for ORM
- OpenAI for LLM and embeddings
- pypdf for PDF processing

**Core Modules**:

#### `main.py`
- FastAPI application initialization
- API endpoint definitions
- CORS configuration
- Startup/shutdown lifecycle management

#### `rag_agent.py`
- Query processing
- Vector similarity search
- Context retrieval
- Response generation with GPT-4

#### `document_loader.py`
- PDF text extraction
- Text chunking (1000 chars, 200 overlap)
- Embedding generation
- Batch processing

#### `database.py`
- SQLAlchemy models
- Database initialization
- pgvector setup

#### `config.py`
- Environment variable management
- Application settings
- Configurable parameters

**Files**:
- `backend/main.py` - Main application
- `backend/rag_agent.py` - RAG logic
- `backend/document_loader.py` - Document processing
- `backend/database.py` - Database layer
- `backend/config.py` - Configuration
- `backend/requirements.txt` - Python dependencies
- `backend/Dockerfile` - Container configuration

### 3. Database (PostgreSQL + pgvector)

**Purpose**: Vector database for semantic search

**Key Technologies**:
- PostgreSQL 16
- pgvector extension
- Vector similarity operations

**Schema**:

```sql
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    source VARCHAR NOT NULL,
    metadata TEXT,
    embedding vector(1536)  -- OpenAI embeddings dimension
);

-- Create vector similarity index
CREATE INDEX ON documents 
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);
```

**Operations**:
- Cosine similarity search (`<=>` operator)
- Top-K retrieval
- Metadata filtering

## Data Flow

### Document Ingestion Flow

```
1. PDF Files
   ↓
2. pypdf Extraction
   ↓
3. Text Chunking (1000 chars, 200 overlap)
   ↓
4. OpenAI Embedding API (text-embedding-3-small)
   ↓
5. PostgreSQL Storage
   - Text content
   - Vector embedding (1536 dimensions)
   - Source metadata
```

### Query Flow

```
1. User Question
   ↓
2. Frontend → POST /query
   ↓
3. Backend RAG Agent
   ↓
4. Embed Query (OpenAI)
   ↓
5. Vector Search (pgvector)
   - Cosine similarity
   - Top 5 results
   ↓
6. Context Assembly
   - Retrieved document chunks
   - Source attribution
   ↓
7. LLM Generation (GPT-4)
   - System prompt
   - Context injection
   - User question
   ↓
8. Response
   - Answer text
   - Source documents
   - Relevance scores
   ↓
9. Frontend Display
```

## RAG Implementation Details

### Chunking Strategy

- **Method**: Recursive Character Text Splitter
- **Chunk Size**: 1000 characters
- **Overlap**: 200 characters
- **Rationale**: Balances context preservation with retrieval precision

### Embedding Model

- **Model**: `text-embedding-3-small`
- **Dimensions**: 1536
- **Cost**: $0.00002 / 1K tokens
- **Performance**: ~62.3% on MTEB benchmark

### Retrieval Strategy

- **Method**: Cosine similarity search
- **Top K**: 5 documents
- **Index**: IVFFlat (for datasets < 1M vectors)
- **Distance Metric**: Cosine distance

### Generation Model

- **Model**: `gpt-4-turbo-preview`
- **Temperature**: 0.7
- **Max Tokens**: 1000
- **Context Window**: 128K tokens

### Prompt Engineering

```
System Prompt:
"You are an expert assistant for Spapperi N.T. S.r.l., 
an Italian agricultural machinery company..."

Context Injection:
[Source: document.pdf]
{relevant chunk 1}

[Source: company_info]
{relevant chunk 2}
...

User Question:
{user's question}
```

## Scaling Considerations

### Current Capacity

- **Documents**: ~150 chunks (4 PDFs + company info)
- **Concurrent Users**: 10-50
- **Query Latency**: 2-5 seconds
- **Storage**: < 1GB

### Scaling Options

#### Horizontal Scaling
- Load balance FastAPI instances
- Separate read replicas for PostgreSQL
- Redis for response caching

#### Vertical Scaling
- Increase PostgreSQL memory
- More CPU cores for embedding generation
- SSD storage for vector indices

#### Optimization
- **Caching**: Cache frequent queries
- **Batching**: Batch embedding requests
- **Compression**: Quantize vectors (1536 → 768)
- **Indexing**: Switch to HNSW for larger datasets

## Security

### Current Implementation

- CORS configuration for cross-origin requests
- Environment variables for secrets
- Docker network isolation
- No authentication (development)

### Production Recommendations

1. **Authentication**: Add JWT or API key auth
2. **HTTPS**: TLS/SSL encryption
3. **Rate Limiting**: Prevent abuse
4. **Input Validation**: Sanitize user queries
5. **Secret Management**: Vault or AWS Secrets Manager
6. **Network Policies**: Firewall rules
7. **Monitoring**: Log all API calls
8. **Backups**: Automated database backups

## Performance Metrics

### Latency Breakdown

- Query Embedding: ~100ms
- Vector Search: ~50ms
- LLM Generation: 2-4s
- **Total**: 2.5-5s

### Cost Estimation (per 1000 queries)

- Embeddings: $0.02 (1000 queries × 50 tokens avg)
- GPT-4 Turbo: $3-5 (context + generation)
- **Total**: ~$3-5 per 1000 queries

### Database Performance

- Vector search: < 100ms for 1K documents
- Scales linearly up to 100K documents
- Consider HNSW index for 100K+ documents

## Monitoring & Observability

### Health Checks

- Database connectivity
- Document count
- API responsiveness

### Metrics to Track

- Query latency (p50, p95, p99)
- Error rates
- OpenAI API usage
- Database query performance
- Memory/CPU usage

### Logging

- All API requests
- Error traces
- Document loading events
- OpenAI API calls

## Disaster Recovery

### Backup Strategy

- **Database**: Daily pg_dump backups
- **Embeddings**: Regenerate from PDFs if needed
- **Configuration**: Version controlled

### Recovery Procedures

1. Restore database from backup
2. Restart services with docker-compose
3. Verify health endpoints
4. Test sample queries

### RTO/RPO

- **RTO** (Recovery Time Objective): < 30 minutes
- **RPO** (Recovery Point Objective): < 24 hours

## Future Enhancements

### Planned Features

1. **Multi-modal support**: Images from PDFs
2. **Conversation memory**: Track dialogue context
3. **Advanced search**: Hybrid search (keyword + vector)
4. **Analytics dashboard**: Query insights
5. **Fine-tuning**: Custom model for domain
6. **Multi-tenancy**: Support multiple companies

### Infrastructure Improvements

1. **Kubernetes**: Container orchestration
2. **CI/CD**: Automated deployments
3. **Monitoring**: Prometheus + Grafana
4. **Caching**: Redis layer
5. **CDN**: Static asset delivery

---

**Document Version**: 1.0  
**Last Updated**: November 2025  
**Maintained By**: Development Team


