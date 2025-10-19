#!/usr/bin/env python3
import asyncio
import chromadb
from mcp.server import Server
from mcp.types import Tool, TextContent
from mcp.server.stdio import stdio_server

CHROMA_HOST = "18.201.177.111"
CHROMA_PORT = 8000
COLLECTION_NAME = "company-docs"

app = Server("chromadb-server")

def get_chroma_client():
    return chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)

@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="query_company_docs",
            description="Query the company-docs collection in ChromaDB",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The query text to search for"
                    },
                    "n_results": {
                        "type": "integer",
                        "description": "Number of results to return (default: 5)",
                        "default": 5
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="get_all_company_docs",
            description="Get all documents from the company-docs collection",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of documents to return",
                        "default": 100
                    }
                }
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    try:
        client = get_chroma_client()
        collection = client.get_collection(name=COLLECTION_NAME)
        
        if name == "query_company_docs":
            query = arguments["query"]
            n_results = arguments.get("n_results", 5)
            
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
            
            return [TextContent(type="text", text=response)]
        
        elif name == "get_all_company_docs":
            limit = arguments.get("limit", 100)
            
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
            
            return [TextContent(type="text", text=response)]
        
        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]
            
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())
