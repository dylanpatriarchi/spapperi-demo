# 🌾 Spapperi RAG Agent

An intelligent AI-powered assistant for Spapperi N.T. S.r.l., an Italian agricultural machinery company. This system uses Retrieval-Augmented Generation (RAG) to provide accurate information about Spapperi's products, specifications, and company information.

## 🏗️ Architecture

This project consists of three main components:

1. **Backend (Python/FastAPI)**: RAG agent with OpenAI integration
2. **Database (PostgreSQL + pgvector)**: Vector database for semantic search
3. **Frontend (React)**: Modern web interface for user interaction

### Technology Stack

- **Backend**: Python 3.11, FastAPI, LangChain, OpenAI
- **Database**: PostgreSQL 16 with pgvector extension
- **Frontend**: React 18, styled-components, axios
- **Infrastructure**: Docker, Docker Compose

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose installed
- OpenAI API key

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd spapperi-demo
```

2. Create environment file:
```bash
cp env.example .env
```

3. Add your OpenAI API key to `.env`:
```
OPENAI_API_KEY=your_api_key_here
```

4. Start all services:
```bash
docker-compose up --build
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

### First Run

On the first startup, the system will automatically:
1. Initialize the PostgreSQL database with pgvector extension
2. Load company information from the embedded knowledge base
3. Process and index all PDF catalogs
4. Create vector embeddings for semantic search

This process may take a few minutes depending on the size of your catalogs.

## 📚 Features

### Core Capabilities

- **Semantic Search**: Uses vector embeddings to find relevant information
- **Multi-language Support**: Responds in English, Italian, French, and other languages
- **Source Attribution**: Provides references to source documents
- **Real-time Chat Interface**: Modern, responsive web UI
- **PDF Processing**: Automatically extracts and indexes PDF content

### API Endpoints

- `GET /` - Root endpoint with API information
- `GET /health` - Health check and system status
- `POST /query` - Submit questions to the RAG agent
- `GET /stats` - Knowledge base statistics
- `POST /reload-documents` - Reload all documents (admin)

## 🗂️ Project Structure

```
spapperi-demo/
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration settings
│   ├── database.py          # Database models and setup
│   ├── document_loader.py   # PDF and document processing
│   └── rag_agent.py         # RAG implementation
├── frontend/
│   ├── Dockerfile
│   ├── package.json
│   ├── public/
│   │   └── index.html
│   └── src/
│       ├── index.js
│       └── App.js           # Main React component
├── docker-compose.yml       # Docker orchestration
├── env.example              # Environment variables template
├── TEST_QUESTIONS.md        # Test questions for validation
└── README.md               # This file
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | Your OpenAI API key | *Required* |
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://spapperi:spapperi_password@postgres:5432/spapperi_rag` |
| `OPENAI_MODEL` | OpenAI model to use | `gpt-4-turbo-preview` |
| `EMBEDDING_MODEL` | Embedding model | `text-embedding-3-small` |
| `CHUNK_SIZE` | Text chunk size for indexing | `1000` |
| `CHUNK_OVERLAP` | Overlap between chunks | `200` |
| `TOP_K_RESULTS` | Number of results to retrieve | `5` |

### Customization

To add more documents:
1. Place PDF files in the project root
2. Update `document_loader.py` to include new files in the `pdf_files` list
3. Restart the backend service or call the `/reload-documents` endpoint

## 🧪 Testing

See `TEST_QUESTIONS.md` for a comprehensive list of test questions in multiple languages to validate the system's responses.

Example test:
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What products does Spapperi offer?"}'
```

## 📊 Knowledge Base

The system includes:
- **Company Information**: History, location, contact details
- **Product Catalogs**: 4 PDF catalogs covering different machinery lines
  - Piantatalee-TP.pdf (Transplanters)
  - Rincalzatore-SM.pdf (Ridge formers)
  - Seminatrice-pneumatica-SMP.pdf (Pneumatic seeders)
  - Stendi-film-SF.pdf (Film layers)

## 🔍 How It Works

1. **Document Ingestion**: PDFs are processed and split into chunks
2. **Embedding Creation**: Each chunk is converted to a vector embedding using OpenAI
3. **Storage**: Chunks and embeddings are stored in PostgreSQL with pgvector
4. **Query Processing**: User questions are converted to embeddings
5. **Retrieval**: Most relevant chunks are found using cosine similarity
6. **Generation**: OpenAI generates a response using retrieved context
7. **Response**: Answer is returned with source attribution

## 🛠️ Development

### Running Locally (without Docker)

1. **Backend**:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

2. **Frontend**:
```bash
cd frontend
npm install
npm start
```

3. **Database**:
```bash
docker run --name postgres \
  -e POSTGRES_USER=spapperi \
  -e POSTGRES_PASSWORD=spapperi_password \
  -e POSTGRES_DB=spapperi_rag \
  -p 5432:5432 \
  pgvector/pgvector:pg16
```

### API Documentation

FastAPI provides automatic interactive documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🌍 Multi-language Support

The agent can understand and respond in multiple languages:
- **English**: Primary language
- **Italian** (Italiano): Full support
- **French** (Français): Full support
- **Spanish** (Español): Full support
- **German** (Deutsch): Full support

The language is automatically detected from the user's question.

## 📝 Maintenance

### Updating Documents

To update the knowledge base:
```bash
curl -X POST http://localhost:8000/reload-documents
```

### Database Backup

```bash
docker exec spapperi-db pg_dump -U spapperi spapperi_rag > backup.sql
```

### Logs

View logs:
```bash
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f postgres
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📄 License

This project is proprietary software for Spapperi N.T. S.r.l.

## 📞 Contact

**Spapperi N.T. S.r.l.**
- Address: Via Pietro Ercolani, 5 b, 06012 Città di Castello PG, Italy
- Phone: +39 075 85 78 156
- Fax: +39 075 85 78 848
- Email: info@spapperi.com
- Website: https://www.spapperi.com/it/

## 🙏 Acknowledgments

- OpenAI for GPT-4 and embedding models
- PostgreSQL and pgvector teams
- FastAPI and React communities
- LangChain for RAG utilities

---

**Version**: 1.0.0  
**Last Updated**: November 2025


