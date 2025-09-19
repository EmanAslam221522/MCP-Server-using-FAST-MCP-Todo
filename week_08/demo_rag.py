#!/usr/bin/env python3
"""
Interactive RAG System Demo

This script provides an interactive interface to query the RAG system
built with LangChain. You can ask questions and get answers based on 
the synthetic PDF document.
"""

import os
import sys
from rag_system import RAGSystem


def display_banner():
    """Display welcome banner."""
    print("=" * 70)
    print("🤖 RAG SYSTEM DEMO - Interactive Query Interface")
    print("=" * 70)
    print("This system can answer questions about the Honeywell T4 Pro Thermostat.")
    print("Ask anything about operation, programming, troubleshooting, or features.")
    print("\nType 'quit', 'exit', or 'q' to exit the program.")
    print("-" * 70)


def format_response(result: dict):
    """Format and display query response."""
    print(f"\n❓ QUESTION: {result['question']}")
    print("=" * 60)
    
    print("💡 ANSWER:")
    print(result['answer'])
    
    if result['source_documents']:
        print(f"\n📄 SOURCES ({len(result['source_documents'])} document chunks):")
        print("-" * 40)
        
        for i, doc in enumerate(result['source_documents'], 1):
            # Show first 100 characters of source content
            content_preview = doc['content'][:100] + "..." if len(doc['content']) > 100 else doc['content']
            page = doc['metadata'].get('page', 'Unknown')
            
            print(f"Source {i} (Page {page}): {content_preview}")
    
    print("\n" + "=" * 60)


def run_interactive_demo():
    """Run the interactive RAG demo."""
    
    # Check if PDF exists
    pdf_path = "honeywell-T-4-User-Manual.pdf"
    if not os.path.exists(pdf_path):
        print(f"❌ Error: PDF file '{pdf_path}' not found!")
        print("Please run the PDF creation script first.")
        return
    
    display_banner()
    
    try:
        print("🔄 Initializing RAG system...")
        rag = RAGSystem(pdf_path)
        
        # Display document info
        doc_info = rag.list_document_info()
        print(f"✅ System ready! Loaded {doc_info['total_chunks']} document chunks.")
        
        # Interactive loop
        while True:
            try:
                print(f"\n{'='*70}")
                query = input("🔍 Enter your question: ").strip()
                
                # Check for exit commands
                if query.lower() in ['quit', 'exit', 'q', '']:
                    print("\n👋 Thanks for using the RAG system! Goodbye!")
                    break
                
                # Special commands
                if query.lower() == 'help':
                    print("Ask any question about the Honeywell T4 Pro Thermostat.")
                    print("Examples: operation, programming, troubleshooting, features, etc.")
                    continue
                
                if query.lower() == 'info':
                    print(f"\n📊 DOCUMENT INFO:")
                    print(f"File: {doc_info['pdf_path']}")
                    print(f"Chunks: {doc_info['total_chunks']}")
                    print(f"Chunk size: {doc_info['chunk_size']}")
                    continue
                
                # Process query
                print("🤔 Processing your question...")
                result = rag.query(query)
                format_response(result)
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error processing query: {e}")
                continue
    
    except Exception as e:
        print(f"❌ Failed to initialize RAG system: {e}")
        return


def run_batch_demo():
    """Run a simple test to verify the system works."""
    
    pdf_path = "honeywell-T-4-User-Manual.pdf"
    if not os.path.exists(pdf_path):
        print(f"❌ Error: PDF file '{pdf_path}' not found!")
        return
    
    print("🚀 Testing RAG system with thermostat manual...")
    
    rag = RAGSystem(pdf_path)
    doc_info = rag.list_document_info()
    
    print(f"✅ System initialized successfully!")
    print(f"📄 Document: {doc_info['pdf_path']}")
    print(f"📊 Total chunks: {doc_info['total_chunks']}")
    print(f"🔧 Ready to answer questions about the Honeywell T4 Pro Thermostat.")


def main():
    """Main entry point."""
    
    if len(sys.argv) > 1 and sys.argv[1] == 'batch':
        run_batch_demo()
    else:
        run_interactive_demo()


if __name__ == "__main__":
    main()