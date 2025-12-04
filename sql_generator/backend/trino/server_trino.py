from mcp.server.fastmcp import FastMCP
from trino_connection import (
    listing_assets,
    get_describe_asset,
    execute_sql_query,
    new_melody_client
)

# Initialize MCP
mcp = FastMCP("PATrinoConnection")

# ============================================================
# Tool 1: list_assets(schema)
# ============================================================
# @mcp.tool()
# async def list_assets(schema: str) -> str:
#     """
#     List dataset assets for given schema.
#     """
#     try:
#         melody = new_melody_client().create()
#         assets = listing_assets(melody, schema)
#         return {"assets": assets}
#     except Exception as e:
#         return {"error": str(e)}


# ============================================================
# Tool 2: describe_asset(schema, table)
# ============================================================
# @mcp.tool()
# async def describe_asset(schema: str, table: str) -> str:
#     """
#     Describe a specific asset (return fields & types).
#     """
#     try:
#         melody = new_melody_client().create()
#         result = get_describe_asset(melody, schema, table)
#         return result
#     except Exception as e:
#         return {"error": str(e)}


# ============================================================
# Tool 3: execute_sql(sql_query)
# ============================================================
@mcp.tool()
async def execute_sql(sql_query: str) -> str:
    """
    Execute SQL query using Melody BI engine.
    sample query : SELECT * FROM columnar."hybrid:pa-load"."ccs-mira-tahoe-devicedimension_latest" limit 10
    """
    try:
        melody = new_melody_client().create()
        result = execute_sql_query(melody, sql_query)
        return result
    except Exception as e:
        return {"error": str(e)}


# ============================================================
# Server entry point (MCP stdio)
# ============================================================
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    return f"Hello, {name}! How can I assist you with Trino Connection?"

if __name__ == "__main__":
    mcp.run()
