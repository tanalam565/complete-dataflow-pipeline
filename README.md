# complete-dataflow-pipeline
A complete system for data flow pipeline from document ingestion to tabular and vector databases.
# Property Document Processor

A complete document processing pipeline for property management companies using **OpenRouter API**, SQLite, and ChromaDB. Works in **GitHub Codespaces** and cloud environments!

## Features

 **Document Classification** - Automatically classify invoices, insurance, and IDs  
 **Entity Extraction** - Extract key fields using LLM (via OpenRouter)  
 **OCR Support** - Process PDFs and images  
**Tabular Storage** - SQLite database for structured data  
 **Vector Search** - ChromaDB for semantic document search  
 **Web Interface** - Streamlit UI for easy interaction  
 **Cloud Compatible** - Works in GitHub Codespaces, Streamlit Cloud, etc.

## Why OpenRouter?

-  **Free tier available** (Google Gemini Flash 1.5)
-  **Works in cloud environments** (Codespaces, Streamlit Cloud)
-  **No local installation needed**
-  **Multiple free models** to choose from
-  **Fast inference**

## Installation

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/complete-dataflow-pipeline
cd property-doc-processor
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Install Tesseract OCR

**Mac:**
```bash
brew install tesseract
```

**Ubuntu/Debian (including Codespaces):**
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr
```

**Windows:**
Download from: https://github.com/UB-Mannheim/tesseract/wiki

### 4. Get OpenRouter API Key (FREE)

1. Sign up at https://openrouter.ai
2. Go to https://openrouter.ai/keys
3. Create a new API key
4. Copy the key

### 5. Configure Environment Variables

```bash
# Copy example file
cp .env.example .env

# Edit .env and add your API key
nano .env  # or use any text editor
```

Add to `.env`:
```
OPENROUTER_API_KEY=sk-or-v1-your-key-here
```

## Project Structure

```
property-doc-processor/
│
├── .devcontainer/
│   └── devcontainer.json           # GitHub Codespaces configuration
│
├── .streamlit/
│   └── config.toml                 # Streamlit UI configuration
│
├── models/
│   ├── __init__.py                 # Empty file (makes it a package)
│   ├── classifier.py               # OpenRouter document classification
│   └── extractor.py                # OpenRouter entity extraction
│
├── database/
│   ├── __init__.py                 # Empty file (makes it a package)
│   ├── sqlite_db.py                # SQLite database operations
│   └── vector_db.py                # ChromaDB vector operations
│
├── utils/
│   ├── __init__.py                 # Empty file (makes it a package)
│   └── ocr.py                      # OCR text extraction (PDF/images)
│
├── data/                           # Created automatically at runtime
│   ├── property_data.db            # SQLite database (auto-generated)
│   └── chroma_db/                  # ChromaDB storage (auto-generated)
│
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variables template
├── .env                            # Your actual environment variables (add to .gitignore)
├── .gitignore                      # Git ignore rules
├── README.md                       # Main documentation
├── QUICKSTART.md                   # Quick start guide
└── REPO_STRUCTURE.md               # This file
```

## Usage

### Local Development

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

### GitHub Codespaces

1. Open repo in Codespaces
2. Install Tesseract: `sudo apt-get install tesseract-ocr`
3. Set up `.env` with your OpenRouter key
4. Run: `streamlit run app.py`
5. Codespaces will forward the port automatically

### Features Guide

**1. Upload Documents**
- Upload PDF or image files
- View extracted data and classification
- Save to database

**2. Search Documents**
- Semantic queries like:
  - "Find all HVAC vendor invoices"
  - "Show insurance policies expiring soon"
  - "Find driver licenses"

**3. View Database**
- Browse all records by category
- Download as CSV

## Free Models Available

OpenRouter offers several FREE models:

| Model | Provider | Best For |
|-------|----------|----------|
| `google/gemini-flash-1.5` | Google | **Default** - Fast & accurate |
| `meta-llama/llama-3.2-3b-instruct:free` | Meta | Good alternative |
| `qwen/qwen-2-7b-instruct:free` | Alibaba | Another option |

Change model in `models/classifier.py` and `models/extractor.py`:
```python
"model": "google/gemini-flash-1.5"  # Change this
```

## Document Types Supported

### 📄 Invoices
- Invoice number, vendor name
- Dates, amounts, tax
- Service description
- Vendor contact info

### 🛡️ Insurance
- Policy number, policyholder
- Coverage details, premium
- Dates, deductible

### 🪪 IDs
- Document type, ID number
- Full name, DOB
- Issue/expiry dates
- Address, state/country

## Troubleshooting

### API Key Issues
```bash
# Check if key is loaded
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('OPENROUTER_API_KEY'))"
```

### Tesseract Not Found
```bash
# Ubuntu/Codespaces
sudo apt-get install tesseract-ocr

# Mac
brew install tesseract

# Check installation
tesseract --version
```

### ChromaDB Issues
```bash
# Delete and recreate
rm -rf data/chroma_db
# Restart app
```

## Cost

**Development: $0** 🎉
- OpenRouter free tier: Google Gemini Flash 1.5
- All other tools are free

**Production:**
- If you exceed free tier limits, paid plans start at $0.001 per request
- Monitor usage at https://openrouter.ai/activity

## Deployment Options

### 1. **Local**
```bash
streamlit run app.py
```

### 2. **GitHub Codespaces** (Recommended for demo)
- Click "Code" → "Codespaces" → "Create codespace"
- Automatically installs dependencies
- Add `.env` with API key
- Run `streamlit run app.py`

### 3. **Streamlit Cloud** (Free hosting)
1. Push to GitHub
2. Go to https://streamlit.io/cloud
3. Connect repository
4. Add secrets in Streamlit settings:
   ```
   OPENROUTER_API_KEY = "your-key"
   ```
5. Note: Tesseract may need packages.txt file

### 4. **Docker** (Coming soon)

## API Usage Examples

```python
# Classification
from models.classifier import classify_document
doc_type = classify_document(text)

# Extraction
from models.extractor import extract_entities
entities = extract_entities(text, doc_type)

# Database
from database.sqlite_db import insert_data, get_all_data
insert_data('invoice', entities)
df = get_all_data('invoice')

# Search
from database.vector_db import search_documents
results = search_documents("HVAC invoices", n_results=5)
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENROUTER_API_KEY` | Yes | Your OpenRouter API key |

## Roadmap

- [ ] Batch upload
- [ ] Export to Excel
- [ ] Email notifications
- [ ] Multi-language OCR
- [ ] Custom training
- [ ] REST API
- [ ] Docker deployment
- [ ] Azure deployment guide

## License

MIT

## Contributing

Pull requests welcome!

## Support

- Issues: GitHub Issues
- OpenRouter Docs: https://openrouter.ai/docs
- Streamlit Docs: https://docs.streamlit.io soon"
  - "Find driver licenses"

### 4. View Database

- Navigate to **View Database** page
- Browse all records by category
- Download as CSV

## Document Types Supported

### 📄 Invoices
Extracts:
- Invoice number
- Vendor name
- Dates (invoice, due)
- Amounts (total, subtotal, tax)
- Service description
- Vendor contact info

### 🛡️ Insurance
Extracts:
- Policy number
- Policyholder name
- Insurance company
- Coverage details
- Premium amount
- Dates (effective, expiry)

### 🪪 IDs
Extracts:
- Document type (driver's license, passport, state ID)
- ID number
- Full name
- Date of birth
- Issue/expiry dates
- Address
- State/Country

## API Usage

### Classification
```python
from models.classifier import classify_document

text = "Your document text..."
doc_type = classify_document(text)
# Returns: 'invoice', 'insurance', 'id', or 'unknown'
```

### Entity Extraction
```python
from models.extractor import extract_entities

entities = extract_entities(text, doc_type)
# Returns: dict with extracted fields
```

### Database Operations
```python
from database.sqlite_db import insert_data, get_all_data

# Insert
insert_data('invoice', entities)

# Query
import pandas as pd
df = get_all_data('invoice')
```

### Vector Search
```python
from database.vector_db import search_documents

results = search_documents("HVAC invoices", n_results=5)
```

## Configuration

### Change LLM Model
Edit `models/classifier.py` and `models/extractor.py`:
```python
model='llama3.2'  # Change to 'llama2', 'mistral', etc.
```

Available models: https://ollama.ai/library

### Change Embedding Model
Edit `database/vector_db.py`:
```python
model = SentenceTransformer('all-MiniLM-L6-v2')
# Change to: 'all-mpnet-base-v2', 'paraphrase-MiniLM-L6-v2', etc.
```

## Troubleshooting

### Ollama Connection Error
```bash
# Check if Ollama is running
ollama list

# Start Ollama service
ollama serve
```

### Tesseract Not Found
```bash
# Find Tesseract path
which tesseract  # Mac/Linux
where tesseract  # Windows

# Add to code if needed
import pytesseract
pytesseract.pytesseract.tesseract_cmd = '/path/to/tesseract'
```

### ChromaDB Issues
```bash
# Delete and recreate database
rm -rf data/chroma_db
# Restart app
```

## Performance Tips

- **Large PDFs**: Processing may take 10-30 seconds
- **LLM Speed**: First request is slower (model loading)
- **Batch Processing**: Upload multiple files sequentially
- **OCR Quality**: Use high-resolution scans (300+ DPI)

## Deployment Options

### Local Demo
```bash
streamlit run app.py
```

### Streamlit Cloud (Free)
1. Push to GitHub
2. Go to https://streamlit.io/cloud
3. Deploy from repository
4. Note: Ollama won't work on cloud (use OpenAI API instead)

### Docker (Coming Soon)
```bash
docker build -t doc-processor .
docker run -p 8501:8501 doc-processor
```

## Cost

**Total: $0** 🎉
- All tools are free and open-source
- No API costs
- Runs entirely locally

## Roadmap

- [ ] Batch upload
- [ ] Export to Excel
- [ ] Email notifications
- [ ] Multi-language OCR
- [ ] Custom training
- [ ] REST API
- [ ] Docker deployment

## License

MIT

## Contributing

Pull requests welcome!

## Support

Issues: https://github.com/yourusername/property-doc-processor/issues