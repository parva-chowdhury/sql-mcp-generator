from pathlib import Path
import os
import json
from hpe.melody.sdk.business_intelligence import MelodyBusinessIntelligence
from hpe.melody.sdk.api.melody_query_api import MelodyQuery
from hpe.melody.sdk.harmony import HarmonyClient
from hpe.melody.sdk.harmony_conf import HarmonyConf
from hpe.melody.sdk.api.auth import Credentials
from pyhocon import ConfigFactory

def new_melody_client():
    conf_path = os.environ.get('APP_CONFIG_PATH',
                                 Path(__file__).parent / "application.conf")
    conf = ConfigFactory.parse_file(conf_path)
    hconf = HarmonyConf(
        harmony_endpoint=conf.get_string("harmony.sdk.endpoint"),
        region=conf.get_string("harmony.sdk.region"),
        well_known_url=conf.get_string("harmony.sdk.well-known-url"),
        auth_version=conf.get_string("harmony.sdk.auth-version"),
        default_provider=conf.get_string("harmony.sdk.default-provider"),
        default_domain=conf.get_string("harmony.default-domain"),
        data_endpoint=conf.get_string("harmony.sdk.data-endpoint"),
        credentials=Credentials(
            clientID=conf.get_string("harmony.sdk.credentials.client-id"),
            secret=conf.get_string("harmony.sdk.credentials.secret"),
            scope=conf.get_string("harmony.sdk.credentials.scope"),
        )
    )
    return HarmonyClient(conf=hconf)

def listing_assets(melody: HarmonyClient, schema: str):
    assets = melody.catalog.list(schema, "hybrid")
    return [
        asset.name
        for asset in assets
        if asset.name.endswith("_latest")
    ]

def get_describe_asset(melody: HarmonyClient, schema: str, table: str):
    fileset = melody.catalog.describe_asset(table, schema, "hybrid")

    # Extract Avro schema string
    avro_schema_raw = fileset.attributes.schemaInfo.schema
    avro_schema = json.loads(avro_schema_raw)

    fields = []

    for field in avro_schema.get("fields", []):
        name = field["name"]
        ftype = field["type"]

        # Normalize Avro types
        if isinstance(ftype, list):
            normalized = "|".join(
                t["type"] if isinstance(t, dict) else t
                for t in ftype
            )
        elif isinstance(ftype, dict):
            normalized = ftype.get("type")
        else:
            normalized = ftype

        fields.append({
            "name": name,
            "type": normalized
        })

    return {
        "table": fileset.name,
        "fields": fields
    }

def execute_sql_query(melody: HarmonyClient, sql_query: str):
    bi_client = MelodyBusinessIntelligence(melody)
    query: MelodyQuery = bi_client.query(sql_query)
    cursor = query.execute()

    # Extract column names
    columns = [col[0] for col in cursor.description]

    # Fetch all rows
    raw_rows = cursor.fetchall()

    # Convert rows into list of dicts
    rows = []
    for row in raw_rows:
        row_dict = {}
        for col, value in zip(columns, row):
            if hasattr(value, "isoformat"):   # datetime, date, time
                row_dict[col] = value.isoformat()
            else:
                row_dict[col] = value
        rows.append(row_dict)

    query_id = query.id()
    status = query.status()

    # Cleanup
    query.close()

    return {
        "query": sql_query,
        "query_id": query_id,
        "status": status,
        "columns": columns,
        "rows": rows
    }

