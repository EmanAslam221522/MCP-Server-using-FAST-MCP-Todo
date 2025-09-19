import os
import warnings
warnings.filterwarnings('ignore')

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.llms.base import LLM
from langchain.callbacks.manager import CallbackManagerForLLMRun
from typing import Optional, List, Any


class LocalLLM(LLM):
    """A simple local LLM that extracts and formats retrieved context."""
    
    @property
    def _llm_type(self) -> str:
        return "local"

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        # The prompt typically contains context and question
        # Let's find the actual content between context markers
        
        # Look for the pattern where context documents are provided
        if "Context:" in prompt or "context" in prompt.lower():
            # Split by common delimiters and find content
            parts = prompt.split('\n\n')
            
            # Find the most content-rich part (usually the retrieved documents)
            best_content = ""
            max_length = 0
            
            for part in parts:
                # Skip very short parts or parts that look like instructions
                if len(part) > max_length and len(part) > 50:
                    # Avoid instructional text
                    if not any(word in part.lower() for word in ['use the following', 'given the context', 'answer the question']):
                        max_length = len(part)
                        best_content = part
            
            if best_content:
                # Clean up the content
                content = best_content.strip()
                # Remove page numbers and excessive whitespace
                content = ' '.join(content.split())
                
                # # Limit to reasonable length
                # if len(content) > 500:
                #     content = content[:500] + "..."
                
                return f"Based on the document:\n\n{content}"
        
        # Fallback - just return the most substantial part of the prompt
        lines = [line.strip() for line in prompt.split('\n') if line.strip()]
        substantial_lines = [line for line in lines if len(line) > 30]
        
        if substantial_lines:
            return f"From the document: {substantial_lines[0][:300]}..."
        
        return "I found relevant information in the document but cannot provide a clear answer from the retrieved content."


class RAGSystem:
    """RAG (Retrieval Augmented Generation) system using LangChain and local embeddings."""
    
    def __init__(self, pdf_path: str, chunk_size: int = 500, chunk_overlap: int = 100):
        """Initialize the RAG system with a PDF document.
        
        Args:
            pdf_path: Path to the PDF document
            chunk_size: Size of text chunks for processing
            chunk_overlap: Overlap between chunks
        """
        self.pdf_path = pdf_path
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.vectorstore = None
        self.qa_chain = None
        
        # Initialize components
        self._load_and_process_document()
        self._setup_retrieval_chain()
    
    def _load_and_process_document(self):
        """Load PDF document and create vector embeddings."""
        print("Loading PDF document...")
        
        # Load PDF
        loader = PyPDFLoader(self.pdf_path)
        documents = loader.load()
        print(f"Loaded {len(documents)} pages from PDF")
        
        # Split text into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
        )
        
        texts = text_splitter.split_documents(documents)
        print(f"Split document into {len(texts)} chunks")
        
        # Create embeddings using local model
        print("Creating embeddings...")
        embeddings = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2",  # Small, fast embedding model
            model_kwargs={'device': 'cpu'}
        )
        
        # Create vector store
        print("Building vector database...")
        self.vectorstore = Chroma.from_documents(
            documents=texts,
            embedding=embeddings,
            persist_directory="./chroma_db"
        )
        
        print("Vector database created successfully!")
    
    def _setup_retrieval_chain(self):
        """Setup the retrieval QA chain."""
        if self.vectorstore is None:
            raise ValueError("Vector store not initialized. Call _load_and_process_document first.")
        
        # Create retriever
        retriever = self.vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 3}  # Retrieve top 3 most similar chunks
        )
        
        # Initialize local LLM
        llm = LocalLLM()
        
        # Create QA chain
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True,
            verbose=True
        )
        
        print("Retrieval chain setup complete!")
    
    def query(self, question: str) -> dict:
        """Query the RAG system with a question.
        
        Args:
            question: The question to ask
            
        Returns:
            Dictionary containing the answer and source documents
        """
        if self.qa_chain is None:
            raise ValueError("QA chain not initialized.")
        
        print(f"\nQuery: {question}")
        print("=" * 50)
        
        # Get answer from the QA chain
        result = self.qa_chain.invoke({"query": question})
        
        # Format response
        response = {
            "question": question,
            "answer": result["result"],
            "source_documents": [
                {
                    "content": doc.page_content,
                    "metadata": doc.metadata
                }
                for doc in result["source_documents"]
            ]
        }
        
        return response
    
    def get_similar_chunks(self, query: str, k: int = 5) -> List[dict]:
        """Get similar document chunks without generating an answer.
        
        Args:
            query: Search query
            k: Number of similar chunks to return
            
        Returns:
            List of similar document chunks with metadata
        """
        if self.vectorstore is None:
            raise ValueError("Vector store not initialized.")
        
        docs = self.vectorstore.similarity_search(query, k=k)
        
        return [
            {
                "content": doc.page_content,
                "metadata": doc.metadata,
                "similarity_rank": i + 1
            }
            for i, doc in enumerate(docs)
        ]
    
    def list_document_info(self) -> dict:
        """Get information about the loaded document.
        
        Returns:
            Dictionary with document statistics
        """
        if self.vectorstore is None:
            raise ValueError("Vector store not initialized.")
        
        # Get all documents from vectorstore
        collection = self.vectorstore._collection
        count = collection.count()
        
        return {
            "pdf_path": self.pdf_path,
            "total_chunks": count,
            "chunk_size": self.chunk_size,
            "chunk_overlap": self.chunk_overlap
        }


def main():
    """Example usage of the RAG system."""
    
    # Initialize RAG system with the PDF
    pdf_path = "honeywell-T-4-User-Manual.pdf"
    
    if not os.path.exists(pdf_path):
        print(f"Error: PDF file '{pdf_path}' not found!")
        return
    
    print("Initializing RAG system...")
    rag = RAGSystem(pdf_path)
    
    # Display document info
    doc_info = rag.list_document_info()
    print(f"\nDocument Info:")
    print(f"- File: {doc_info['pdf_path']}")
    print(f"- Total chunks: {doc_info['total_chunks']}")
    print(f"- Chunk size: {doc_info['chunk_size']}")
    
    # Example queries
    sample_queries = [
        "What is Python used for?",
        "How does machine learning work?",
        "What are the components of financial statements?",
        "What is CRISPR technology?",
        "What is the market size of artificial intelligence?"
    ]
    
    print("\n" + "="*60)
    print("SAMPLE QUERIES")
    print("="*60)
    
    for query in sample_queries:
        try:
            result = rag.query(query)
            print(f"\nQ: {result['question']}")
            print(f"A: {result['answer']}")
            print(f"Sources: {len(result['source_documents'])} document chunks")
            print("-" * 50)
        except Exception as e:
            print(f"Error processing query '{query}': {e}")
    
    print("\nRAG system demo completed!")


if __name__ == "__main__":
    main()