# chroma_mcp.py
# MCP para consultar la colección "company-docs" en ChromaDB remota (18.201.177.111:8000)

from __future__ import annotations
from typing import Any, Dict, List, Optional
from dataclasses import dataclass
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from mcp.server.fastmcp import FastMCP, Context
import chromadb

COLLECTION_NAME = "company-docs"

@dataclass
class AppCtx:
    client: Any
    collection: Any

def _build_chroma_client() -> Any:
    # Cliente HTTP apuntando a tu instancia
    return chromadb.HttpClient(host="18.201.177.111", port=8000)

@asynccontextmanager
async def lifespan(server: FastMCP) -> AsyncIterator[AppCtx]:
    client = _build_chroma_client()
    collection = client.get_or_create_collection(COLLECTION_NAME)
    try:
        yield AppCtx(client=client, collection=collection)
    finally:
        pass

mcp = FastMCP("ChromaDB - company-docs", lifespan=lifespan)

@mcp.tool(description="Lista elementos de la colección 'company-docs'.")
def list_company_docs(
    ctx: Context, 
    limit: int = 100,
    offset: int = 0,
    include: Optional[List[str]] = None,
    where: Optional[Dict[str, Any]] = None,
    where_document: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    app: AppCtx = ctx.request_context.lifespan_context
    include = include or ["ids", "documents", "metadatas"]

    result = app.collection.get(
        include=include,
        limit=limit,
        offset=offset,
        where=where,
        where_document=where_document,
    )

    return {
        "pagination": {"limit": limit, "offset": offset},
        "count": len(result.get("ids", [])),
        "include": include,
        "data": result,
    }

@mcp.tool(description="Cuenta los elementos en la colección 'company-docs'.")
def count_company_docs(ctx: Context) -> int:
    app: AppCtx = ctx.request_context.lifespan_context
    return int(app.collection.count())

if __name__ == "__main__":
    mcp.run()
