# RAG System Implementation with LangChain

This project implements a **Retrieval Augmented Generation (RAG)** system using LangChain and local embeddings to query information from a synthetic PDF document.

## 🗂️ Files Overview

- `honeywell-T-4-User-Manual.pdf` - The synthetic dataset PDF document 
- `create_synthetic_pdf.py` - Script to generate the synthetic PDF
- `rag_system.py` - Main RAG implementation using LangChain
- `demo_rag.py` - Interactive demo script
- `simple_rag_test.py` - Simple retrieval test

## 📋 Features

- **Document Loading**: Loads PDF documents using PyPDFLoader
- **Text Chunking**: Splits documents into manageable chunks
- **Semantic Search**: Uses HuggingFace embeddings for similarity search
- **Vector Database**: ChromaDB for storing document embeddings
- **Interactive Queries**: Command-line interface for asking questions

## 🚀 Quick Start

1. **Install Dependencies**:
   ```bash
   pip install langchain langchain-community pypdf chromadb sentence-transformers
   ```

2. **Run Interactive Demo**:
   ```bash
   python3 demo_rag.py
   ```

3. **Run Batch Demo**:
   ```bash
   python3 demo_rag.py batch
   ```

## 💻 Usage Examples

### Basic RAG Query
```python
from rag_system import RAGSystem

# Initialize RAG system
rag = RAGSystem("honeywell-T-4-User-Manual.pdf")

# Ask a question
result = rag.query("What is Python used for?")
print(result['answer'])
```

### Direct Similarity Search
```python
# Get similar document chunks
chunks = rag.get_similar_chunks("machine learning", k=3)
for chunk in chunks:
    print(chunk['content'])
```

## 📊 Document Content

The synthetic PDF contains diverse information across:

- **Technology & Software** - Python, ML algorithms, cloud computing, APIs
- **Business & Finance** - Financial statements, market analysis, project management  
- **Science & Research** - Scientific method, climate change, genetics
- **Data Tables** - Technology adoption rates and market statistics
- **Q&A Sections** - Common technical questions and answers

## 🔍 Sample Queries You Can Try

- "What programming paradigms does Python support?"
- "What are the main categories of machine learning?"
- "What is the AI market size?"
- "How does SWOT analysis work?"
- "What is CRISPR technology?"
- "When was ChatGPT released?"

## 🏗️ Architecture

```
PDF Document → Text Chunks → Embeddings → Vector Store → Retrieval → Response
```

1. **Document Processing**: PDF loaded and split into chunks
2. **Embedding Generation**: Text converted to vector embeddings
3. **Vector Storage**: Embeddings stored in ChromaDB
4. **Query Processing**: User question embedded and similar chunks retrieved
5. **Response Generation**: Retrieved context formatted into answer

## ⚙️ Configuration

Key parameters you can adjust:

- `chunk_size`: Size of text chunks (default: 1000)
- `chunk_overlap`: Overlap between chunks (default: 200) 
- `k`: Number of similar chunks to retrieve (default: 3)
- Embedding model: `all-MiniLM-L6-v2` (fast, local model)

## 🛠️ Technical Details

- **Embeddings**: HuggingFace `all-MiniLM-L6-v2` model
- **Vector DB**: ChromaDB with persistence
- **Text Splitting**: Recursive character text splitter
- **Retrieval**: Similarity search with configurable k
- **No External API**: Fully local implementation

## 🔧 Troubleshooting

If you encounter issues:

1. Ensure all dependencies are installed
2. Check that the PDF file exists
3. Clear the vector database: `rm -rf chroma_db`
4. Run the simple test: `python3 simple_rag_test.py`

## 📈 Performance

- Document processing: ~10-15 seconds for 3-page PDF
- Query response: ~1-2 seconds per question
- Memory usage: ~500MB with embeddings loaded
- Storage: ~10MB for vector database

This RAG system provides a foundation for building document-based question answering systems using modern NLP techniques.