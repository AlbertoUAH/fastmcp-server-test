# chroma_mcp.py
from __future__ import annotations
from typing import Any, Dict, List, Optional
from dataclasses import dataclass
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from mcp.server.fastmcp import FastMCP, Context
import chromadb

# Try modern API (0.5.x) first; fallback to REST settings (0.4.x)
try:
    from chromadb import HttpClient  # 0.5.x
    HAS_HTTP = True
except Exception:
    HAS_HTTP = False
    from chromadb.config import Settings  # 0.4.x

COLLECTION_NAME = "company-docs"
CHROMA_HOST = "18.201.177.111"
CHROMA_PORT = 8000

@dataclass
class AppCtx:
    client: Any
    collection: Any

def build_client():
    if HAS_HTTP:
        return HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)  # type: ignore
    return chromadb.Client(Settings(  # type: ignore
        chroma_api_impl="rest",
        chroma_server_host=CHROMA_HOST,
        chroma_server_http_port=CHROMA_PORT,
    ))

@asynccontextmanager
async def lifespan(server: FastMCP) -> AsyncIterator[AppCtx]:
    client = build_client()
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
    res = app.collection.get(
        include=include,
        limit=limit,
        offset=offset,
        where=where,
        where_document=where_document,
    )
    return {
        "pagination": {"limit": limit, "offset": offset},
        "count": len(res.get("ids", [])),
        "include": include,
        "data": res,
    }

@mcp.tool(description="Cuenta los elementos en la colección 'company-docs'.")
def count_company_docs(ctx: Context) -> int:
    app: AppCtx = ctx.request_context.lifespan_context
    return int(app.collection.count())

if __name__ == "__main__":
    mcp.run()
