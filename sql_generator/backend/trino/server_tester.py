# from mcp_server.utility.schema import get_all_tables, get_table_info
# from mcp_server.utility.table_relations import table_relations
# from mcp_server.utility.terminology import terminology

from trino_connection import (
    listing_assets,
    get_describe_asset,
    execute_sql_query,
    new_melody_client
)

if __name__ == "__main__":
    # tables = get_all_tables()
    # print(f"Table List: {tables}")
    #
    # table_info = get_table_info(['ccs-aquila-tahoe-customersdimension_latest'])
    # print(f"Table Information : {table_info}")
    #
    # relation = table_relations()
    # print(f"Table relation : {relation}")
    #
    # termin = terminology()
    # print(f"Table relation : {termin}")

    melody = new_melody_client().create()

    assets = listing_assets(melody, "pa-load")
    for asset in assets:
        print(asset)

    print(get_describe_asset(melody, "pa-load", "ccs-mira-tahoe-devicedimension_latest"))

    input_query = 'SELECT * FROM columnar."hybrid:pa-load"."ccs-mira-tahoe-devicedimension_latest" limit 10'
    print(execute_sql_query(melody, input_query))
