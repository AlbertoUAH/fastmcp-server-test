#!/usr/bin/env python3
import json
import chromadb
from fastmcp import FastMCP

CHROMA_HOST = "18.201.177.111"
CHROMA_PORT = 8000
COLLECTION_NAME = "company-docs"

mcp = FastMCP("chromadb-server")

_collection = None

def get_chroma_collection():
    global _collection
    if _collection is None:
        client = chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)
        _collection = client.get_or_create_collection(name=COLLECTION_NAME)
    return _collection

@mcp.tool()
def query_company_docs(query: str, n_results: int = 5) -> str:
    """Query the company-docs collection in ChromaDB
    
    Args:
        query: The query text to search for
        n_results: Number of results to return (default: 5)
    """
    try:
        collection = get_chroma_collection()
        
        results = collection.query(
            query_texts=[query],
            n_results=n_results
        )
        
        if not results.get('documents') or not results['documents'][0]:
            return "No results found."
        
        response = f"Found {len(results['documents'][0])} results:\n\n"
        for i in range(len(results['documents'][0])):
            doc = results['documents'][0][i]
            distance = results['distances'][0][i] if results.get('distances') else 0
            metadata = results['metadatas'][0][i] if results.get('metadatas') else {}
            
            clean_metadata = {k: v for k, v in metadata.items() if not k.startswith('_')} if metadata else {}
            
            response += f"Result {i+1} (distance: {distance:.4f}):\n"
            response += f"Document: {doc}\n"
            if clean_metadata:
                response += f"Metadata: {json.dumps(clean_metadata, indent=2)}\n"
            response += "\n"
        
        return response
    except Exception as e:
        import traceback
        return f"Error: {str(e)}\n{traceback.format_exc()}"

@mcp.tool()
def get_all_company_docs(limit: int = 100) -> str:
    """Get all documents from the company-docs collection
    
    Args:
        limit: Maximum number of documents to return (default: 100)
    """
    try:
        collection = get_chroma_collection()
        
        results = collection.get(limit=limit)
        
        if not results.get('documents'):
            return "No documents found."
        
        response = f"Retrieved {len(results['documents'])} documents:\n\n"
        for i in range(len(results['documents'])):
            doc_id = results['ids'][i] if results.get('ids') else f"doc_{i}"
            doc = results['documents'][i]
            metadata = results['metadatas'][i] if results.get('metadatas') else {}
            
            clean_metadata = {k: v for k, v in metadata.items() if not k.startswith('_')} if metadata else {}
            
            response += f"Document {i+1} (ID: {doc_id}):\n"
            response += f"Content: {doc[:500]}{'...' if len(doc) > 500 else ''}\n"
            if clean_metadata:
                response += f"Metadata: {json.dumps(clean_metadata, indent=2)}\n"
            response += "\n"
        
        return response
    except Exception as e:
        import traceback
        return f"Error: {str(e)}\n{traceback.format_exc()}"

@mcp.tool()
def get_document_count() -> str:
    """Get the total number of documents in the company-docs collection"""
    try:
        collection = get_chroma_collection()
        count = collection.count()
        return f"Total documents in {COLLECTION_NAME}: {count}"
    except Exception as e:
        import traceback
        return f"Error: {str(e)}\n{traceback.format_exc()}"
