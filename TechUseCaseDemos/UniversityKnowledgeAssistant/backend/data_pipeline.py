#!/usr/bin/env python3
"""
University Knowledge Assistant - Data Pipeline
Complete pipeline for web scraping, PDF extraction, and knowledge graph building.
"""

import asyncio
import argparse
from pathlib import Path
from typing import List, Dict, Any
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Try imports with fallbacks
try:
    from scrapling import HttpClient
    HAS_SCRAPLING = True
except ImportError:
    HAS_SCRAPLING = False
    logger.warning("Scrapling not installed. Web scraping disabled.")

try:
    from docling.pipeline import Pipeline
    from docling.options import PipelineOptions
    from docling.document_converters.pdf_document_converter import PDFDocumentConverter
    HAS_DOCLING = True
except ImportError:
    HAS_DOCLING = False
    logger.warning("Docling not installed. PDF extraction using fallback.")

try:
    from falkordb import FalkorDB
    HAS_FALKORDB = True
except ImportError:
    HAS_FALKORDB = False
    logger.warning("FalkorDB not installed. Using mock mode.")


class DataPipeline:
    """Complete data injection pipeline."""
    
    def __init__(self, db_host: str = "localhost", db_port: int = 9292):
        self.db_host = db_host
        self.db_port = db_port
        self.db = None
        self.page_index = {}
        
    async def initialize(self):
        """Initialize database connection."""
        if HAS_FALKORDB:
            self.db = FalkorDB(host=self.db_host, port=self.db_port)
            logger.info(f"Connected to FalkorDB at {self.db_host}:{self.db_port}")
        else:
            logger.info("Running in mock mode (no DB)")
    
    async def scrape_website(self, url: str) -> List[Dict[str, Any]]:
        """Scrape website content."""
        if not HAS_SCRAPLING:
            logger.error("Scrapling not available")
            return []
        
        logger.info(f"Scraping: {url}")
        client = HttpClient()
        results = []
        
        try:
            # Main page
            response = client.get(url)
            if response and response.text:
                results.append({
                    "source": url,
                    "content": response.text,
                    "type": "web",
                    "timestamp": datetime.now().isoformat()
                })
            
            # Extract links and scrape subpages
            links = client.css_select("a[href]")[:10]  # Limit to 10 pages
            for link in links:
                href = link.get_attribute("href")
                if href and href.startswith("http"):
                    try:
                        sub_response = client.get(href)
                        if sub_response and sub_response.text:
                            results.append({
                                "source": href,
                                "content": sub_response.text,
                                "type": "web",
                                "timestamp": datetime.now().isoformat()
                            })
                    except Exception as e:
                        logger.warning(f"Failed to scrape {href}: {e}")
                        
        except Exception as e:
            logger.error(f"Scraping failed: {e}")
            
        return results
    
    def extract_pdf(self, pdf_path: str) -> Dict[str, Any]:
        """Extract content from PDF using Docling."""
        if not HAS_DOCLING:
            return self._fallback_pdf_extract(pdf_path)
        
        logger.info(f"Extracting PDF: {pdf_path}")
        converter = PDFDocumentConverter()
        result = converter.convert(pdf_path)
        
        return {
            "source": pdf_path,
            "content": result.get_text(),
            "type": "pdf",
            "timestamp": datetime.now().isoformat()
        }
    
    def _fallback_pdf_extract(self, pdf_path: str) -> Dict[str, Any]:
        """Fallback PDF extraction."""
        import PyPDF2
        
        logger.info(f"Fallback extracting: {pdf_path}")
        text = ""
        with open(pdf_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() + "\n"
        
        return {
            "source": pdf_path,
            "content": text,
            "type": "pdf",
            "timestamp": datetime.now().isoformat()
        }
    
    def process_content(self, content: str, source: str) -> Dict[str, Any]:
        """Process and chunk content."""
        # Split into manageable chunks
        chunk_size = 2000
        chunks = []
        words = content.split()
        
        for i in range(0, len(words), chunk_size):
            chunk = " ".join(words[i:i+chunk_size])
            chunks.append({
                "chunk_id": f"{source}_{i//chunk_size}",
                "content": chunk,
                "source": source,
                "position": i//chunk_size
            })
        
        return {
            "source": source,
            "chunks": chunks,
            "total_chunks": len(chunks)
        }
    
    async def build_knowledge_graph(self, documents: List[Dict[str, Any]]):
        """Build knowledge graph in FalkorDB."""
        if not self.db:
            logger.info("Skipping knowledge graph (mock mode)")
            return
        
        logger.info("Building knowledge graph...")
        
        # Create document nodes
        for doc in documents:
            doc_id = doc.get("source", "unknown")
            await self.db.set(f"doc:{doc_id}", {
                "type": doc.get("type", "unknown"),
                "timestamp": doc.get("timestamp", ""),
                "source": doc.get("source", "")
            })
    
    def build_page_index(self, processed_docs: List[Dict[str, Any]]):
        """Build inverted index for page-level retrieval."""
        logger.info("Building page index...")
        
        for doc in processed_docs:
            for chunk in doc.get("chunks", []):
                words = chunk["content"].lower().split()
                for word in set(words):
                    if len(word) > 3:
                        if word not in self.page_index:
                            self.page_index[word] = []
                        self.page_index[word].append({
                            "chunk_id": chunk["chunk_id"],
                            "source": doc["source"],
                            "position": chunk["position"]
                        })
    
    async def run(self, url: str = None, pdf_paths: List[str] = None):
        """Run the complete pipeline."""
        await self.initialize()
        
        documents = []
        processed_docs = []
        
        # Scrape website
        if url:
            scraped = await self.scrape_website(url)
            documents.extend(scraped)
        
        # Extract PDFs
        if pdf_paths:
            for pdf_path in pdf_paths:
                extracted = self.extract_pdf(pdf_path)
                documents.append(extracted)
        
        # Process all documents
        for doc in documents:
            processed = self.process_content(doc["content"], doc["source"])
            processed_docs.append(processed)
        
        # Build knowledge graph
        await self.build_knowledge_graph(documents)
        
        # Build page index
        self.build_page_index(processed_docs)
        
        logger.info(f"Pipeline complete. Processed {len(documents)} documents.")
        return {
            "documents": documents,
            "processed": processed_docs,
            "index_size": len(self.page_index)
        }


async def main():
    parser = argparse.ArgumentParser(description="University Knowledge Assistant Pipeline")
    parser.add_argument("--url", help="University website URL")
    parser.add_argument("--pdf", nargs="+", help="PDF file paths")
    parser.add_argument("--db-host", default="localhost", help="FalkorDB host")
    parser.add_argument("--db-port", type=int, default=9292, help="FalkorDB port")
    
    args = parser.parse_args()
    
    pipeline = DataPipeline(args.db_host, args.db_port)
    result = await pipeline.run(url=args.url, pdf_paths=args.pdf)
    
    print(f"\n✅ Pipeline complete!")
    print(f"   Documents: {len(result['documents'])}")
    print(f"   Index size: {result['index_size']} terms")


if __name__ == "__main__":
    asyncio.run(main())