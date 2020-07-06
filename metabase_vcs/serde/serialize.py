import json
from metabase_vcs.models.models import ReportDashboard, ReportDashboardcard, ReportCard, MetabaseDatabase, MetabaseTable
from metabase_vcs.env import *

def serialize_dashboard(dashboard, session):
    dashboard_id = dashboard['id']
    dashboard_name = dashboard['name']
    
    dash = session.query(ReportDashboard).filter(ReportDashboard.id == dashboard_id).first()
    
    with open(f"dashboards/{dashboard_name}.json", 'w', encoding='utf-8') as f:
        json_str = json.loads(dash.to_json(max_nesting=4))
        f.write(json.dumps(json_str, indent=4, sort_keys=True))


def serialize_database(database, session):
    database_id = database['id']
    database_name = database['name']
    
    database_from_db = session.query(MetabaseDatabase).filter(MetabaseDatabase.id == database_id).first()
    
    if 'schemas' not in database:
        raise Exception("An array of schemas must be provided")

    schemas = database['schemas']

    tables = session.query(MetabaseTable) \
        .filter(MetabaseTable.db_id == database_id) \
        .filter(MetabaseTable.schema.in_(schemas)).all()

    database_obj = json.loads(database_from_db.to_json(max_nesting=1))
    json_tables = []
    
    total_tables = len(tables)
    count = 0
    for table in tables:
        json_tables.append(json.loads(table.to_json(max_nesting=4)))
        count += 1
        print('Done table: ' + str(table.name))
        print('finished {} of {}'.format(count, total_tables))
    
    database_obj['tables'] = json_tables
    
    with open(f"databases/{database_name}.json", 'w', encoding='utf-8') as f:
        f.write(json.dumps(database_obj, indent=4, sort_keys=True))
