"""
Simple RAG test to verify retrieval functionality
"""

from rag_system import RAGSystem


def test_retrieval():
    """Test the retrieval functionality directly."""
    
    print("Testing RAG retrieval system...")
    rag = RAGSystem("honeywell-T-4-User-Manual.pdf", chunk_size=10, chunk_overlap=1)
    
    test_queries = [
        "Python programming language",
        "machine learning algorithms", 
        "financial statements",
        "artificial intelligence market size",
        "SWOT analysis"
    ]
    
    print("\n" + "="*70)
    print("RETRIEVAL TEST RESULTS")
    print("="*70)
    
    for query in test_queries:
        print(f"\n🔍 Query: {query}")
        print("-" * 50)
        
        # Get similar chunks
        chunks = rag.get_similar_chunks(query, k=2)
        
        for i, chunk in enumerate(chunks, 1):
            print(f"\nChunk {i} (Page {chunk['metadata'].get('page', 'Unknown')}):")
            print(chunk['content'][:200] + "..." if len(chunk['content']) > 200 else chunk['content'])
        
        print("\n" + "="*70)


if __name__ == "__main__":
    test_retrieval()