#!/usr/bin/env python3
import chromadb
from fastmcp import FastMCP

CHROMA_HOST = "18.201.177.111"
CHROMA_PORT = 8000
COLLECTION_NAME = "company-docs"

mcp = FastMCP("chromadb-server")

def get_chroma_client():
    return chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)

@mcp.tool()
def query_company_docs(query: str, n_results: int = 5) -> str:
    """Query the company-docs collection in ChromaDB
    
    Args:
        query: The query text to search for
        n_results: Number of results to return (default: 5)
    """
    try:
        client = get_chroma_client()
        collection = client.get_collection(name=COLLECTION_NAME)
        
        results = collection.query(
            query_texts=[query],
            n_results=n_results
        )
        
        response = f"Found {len(results['documents'][0])} results:\n\n"
        for i, (doc, metadata, distance) in enumerate(zip(
            results['documents'][0],
            results['metadatas'][0],
            results['distances'][0]
        )):
            response += f"Result {i+1} (distance: {distance:.4f}):\n"
            response += f"Document: {doc}\n"
            response += f"Metadata: {metadata}\n\n"
        
        return response
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def get_all_company_docs(limit: int = 100) -> str:
    """Get all documents from the company-docs collection
    
    Args:
        limit: Maximum number of documents to return (default: 100)
    """
    try:
        client = get_chroma_client()
        collection = client.get_collection(name=COLLECTION_NAME)
        
        results = collection.get(limit=limit)
        
        response = f"Retrieved {len(results['documents'])} documents:\n\n"
        for i, (doc_id, doc, metadata) in enumerate(zip(
            results['ids'],
            results['documents'],
            results['metadatas']
        )):
            response += f"Document {i+1} (ID: {doc_id}):\n"
            response += f"Content: {doc}\n"
            response += f"Metadata: {metadata}\n\n"
        
        return response
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def get_document_count() -> str:
    """Get the total number of documents in the company-docs collection"""
    try:
        client = get_chroma_client()
        collection = client.get_collection(name=COLLECTION_NAME)
        count = collection.count()
        return f"Total documents in {COLLECTION_NAME}: {count}"
    except Exception as e:
        return f"Error: {str(e)}"
