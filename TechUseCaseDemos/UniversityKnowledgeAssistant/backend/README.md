# University Knowledge Assistant - Backend Pipeline

Complete data injection pipeline for web scraping, PDF extraction, and knowledge graph building.

## Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐     ┌──────────────┐
│   Website   │────▶│  Scrapling   │────▶│  Docling    │────▶│ FalkorDB     │
│ (bits-pilani)│     │  (Crawler)   │     │  (PDF Extract)│     │  (Graph)     │
└─────────────┘     └──────────────┘     └─────────────┘     └──────────────┘
                                                    │
                                                    ▼
                                                PageIndex
                                                    │
                                                    ▼
                                            Local SLM (llama.cpp)
```

## Quick Start

```bash
# 1. Install dependencies
pip install scrapling docling falkordb-client python-dotenv

# 2. Start FalkorDB
docker run -d -p 9292:9292 falkordb/falkordb

# 3. Run the pipeline
python backend/data_pipeline.py --url https://www.bits-pilani.ac.in/
```

## File Structure

```
UniversityKnowledgeAssistant/
├── backend/
│   ├── data_pipeline.py      # Main pipeline
│   ├── scrapers/             # Web scrapers
│   ├── extractors/           # PDF/doc extractors
│   ├── processors/           # Data processors
│   └── config.py             # Configuration
├── frontend/                 # Browser demo files
├── docs/                     # Documentation
└── README.md
```