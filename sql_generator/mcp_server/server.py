import json
import os

# Load schema and business logic
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCHEMA_PATH = os.path.join(BASE_DIR, "schema.json")
BUSINESS_LOGIC_PATH = os.path.join(BASE_DIR, "business_logic.md")

def load_schema():
    with open(SCHEMA_PATH, "r") as f:
        return json.load(f)

def load_business_logic():
    with open(BUSINESS_LOGIC_PATH, "r") as f:
        return f.read()

def get_schema() -> str:
    """Returns the database schema in JSON format."""
    schema = load_schema()
    return json.dumps(schema, indent=2)

def get_business_logic() -> str:
    """Returns the business logic rules and definitions."""
    return load_business_logic()

def list_tables() -> list[str]:
    """Returns a list of all table names in the database."""
    schema = load_schema()
    return [table["name"] for table in schema.get("tables", [])]

def get_table_schema(table_name: str) -> str:
    """Returns the schema for a specific table."""
    schema = load_schema()
    for table in schema.get("tables", []):
        if table["name"] == table_name:
            return json.dumps(table, indent=2)
    return f"Table '{table_name}' not found."
