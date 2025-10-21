# Complete Repository Structure

                                                            Frontend (Streamlit/Gradio)
                                                                ↓
                                                            Document Upload
                                                                ↓
                                                            Document Classifier (Local AI)
                                                                ↓
                                                            Text Extraction (OCR)
                                                                ↓
                                                            Entity Extraction (Local LLM)
                                                                ↓
                                                            ├── SQLite (tabular data)
                                                            └── ChromaDB (vector embeddings)
## Setup Checklist

### 1. Create Directory Structure
```bash
mkdir -p property-doc-processor/{.devcontainer,.streamlit,models,database,utils,data}
cd property-doc-processor
```

### 2. Create Empty __init__.py Files
```bash
touch models/__init__.py
touch database/__init__.py
touch utils/__init__.py
```

### 3. Create Configuration Files

Copy all artifacts provided:
- ✅ `.devcontainer/devcontainer.json`
- ✅ `.streamlit/config.toml`
- ✅ `models/classifier.py`
- ✅ `models/extractor.py`
- ✅ `database/sqlite_db.py`
- ✅ `database/vector_db.py`
- ✅ `utils/ocr.py`
- ✅ `app.py`
- ✅ `requirements.txt`
- ✅ `.env.example`
- ✅ `.gitignore`
- ✅ `README.md`
- ✅ `QUICKSTART.md`

### 4. Configure Environment
```bash
cp .env.example .env
# Edit .env and add your OPENROUTER_API_KEY
```

### 5. Initialize Git
```bash
git init
git add .
git commit -m "Initial commit: Property document processor"
```

### 6. Push to GitHub
```bash
# Create repo on GitHub first, then:
git remote add origin https://github.com/yourusername/property-doc-processor.git
git branch -M main
git push -u origin main
```

## File Sizes (Approximate)

| File | Lines | Description |
|------|-------|-------------|
| app.py | 120 | Main Streamlit UI |
| models/classifier.py | 100 | Document classification |
| models/extractor.py | 250 | Entity extraction |
| utils/ocr.py | 80 | OCR processing |
| database/sqlite_db.py | 150 | SQLite operations |
| database/vector_db.py | 100 | ChromaDB operations |
| requirements.txt | 9 | Dependencies |
| README.md | 250 | Documentation |
| QUICKSTART.md | 150 | Quick guide |

## Key Dependencies

### Python Packages (requirements.txt)
- `streamlit` - Web UI framework
- `pytesseract` - OCR engine wrapper
- `Pillow` - Image processing
- `PyMuPDF` - PDF text extraction
- `chromadb` - Vector database
- `sentence-transformers` - Text embeddings
- `requests` - HTTP client for OpenRouter API
- `pandas` - Data manipulation
- `python-dotenv` - Environment variables

### System Dependencies
- **Tesseract OCR** - Text extraction from images
  - Mac: `brew install tesseract`
  - Ubuntu: `sudo apt-get install tesseract-ocr`
  - Windows: Download installer

### External Services
- **OpenRouter API** - LLM inference (free tier available)
  - Sign up: https://openrouter.ai
  - Get key: https://openrouter.ai/keys
  - Free model: `google/gemini-flash-1.5`

## Runtime Directories

These are created automatically when you run the app:

```
data/
├── property_data.db              # SQLite database
└── chroma_db/                    # ChromaDB vector store
    ├── chroma.sqlite3
    └── [embedding files]
```

**Important:** Add `data/` to `.gitignore` to avoid committing large database files.

## Environment Variables

Required in `.env` file:

```bash
OPENROUTER_API_KEY=sk-or-v1-your-key-here
```

## Free Models Available via OpenRouter

| Model ID | Provider | Speed | Quality |
|----------|----------|-------|---------|
| `google/gemini-flash-1.5` | Google | ⚡ Fast | ⭐⭐⭐⭐ |
| `meta-llama/llama-3.2-3b-instruct:free` | Meta | ⚡ Fast | ⭐⭐⭐ |
| `qwen/qwen-2-7b-instruct:free` | Alibaba | ⚡ Fast | ⭐⭐⭐ |

Change model in `classifier.py` and `extractor.py` line ~35:
```python
"model": "google/gemini-flash-1.5"
```

## Testing

### Unit Tests (Optional - TODO)
```bash
mkdir tests
touch tests/__init__.py
touch tests/test_classifier.py
touch tests/test_extractor.py
```

### Manual Testing
1. Run `streamlit run app.py`
2. Upload test documents (see QUICKSTART.md)
3. Verify classification
4. Check entity extraction
5. Test semantic search
6. Export CSV data

## Deployment

### GitHub Codespaces ✅ (Recommended for Demo)
- Automatic setup via `.devcontainer/devcontainer.json`
- Just add `.env` with API key
- Run `streamlit run app.py`

### Streamlit Cloud ✅ (Free Hosting)
1. Push to GitHub
2. Connect at streamlit.io/cloud
3. Add secrets in dashboard
4. Deploy!

### Docker 🚧 (Coming Soon)
```dockerfile
# TODO: Create Dockerfile
FROM python:3.11-slim
# ... setup steps
```

### Azure ☁️ (Production)
See README.md for Azure deployment guide (TODO)

## Cost Breakdown

| Component | Development | Production |
|-----------|-------------|------------|
| OpenRouter API | Free tier | ~$0.001/request |
| GitHub Codespaces | Free (60 hrs/mo) | $0.18/hr |
| Streamlit Cloud | Free (1 app) | $20/mo |
| Database Storage | Free (local) | Depends |
| **Total** | **$0** | **~$20-50/mo** |

## Support

- 📖 Docs: README.md
- 🚀 Quick Start: QUICKSTART.md
- 🐛 Issues: GitHub Issues
- 💬 OpenRouter: https://openrouter.ai/docs

## License

MIT