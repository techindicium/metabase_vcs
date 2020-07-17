import json
from metabase_vcs.models.models import ReportDashboard, ReportDashboardcard, ReportCard, MetabaseDatabase, MetabaseTable, MetabaseField, Collection, CoreUser
from metabase_vcs.serde.utils import *

def serialize_user(user_id, session, tracked_dir):
    user = session.query(CoreUser).filter(CoreUser.id == user_id).first()
    
    with open(f"{tracked_dir}/users/{user_id}.json", 'w', encoding='utf-8') as f:
        json_str = json.loads(user.to_json(max_nesting=4))
        f.write(json.dumps(json_str, indent=4, sort_keys=True))


def serialize_collection(collection_id, session, tracked_dir):
    coll_from_db = session.query(Collection).filter(Collection.id == collection_id).first()
    
    with open(f"{tracked_dir}/collections/{collection_id}.json", 'w', encoding='utf-8') as f:
        json_str = json.loads(coll_from_db.to_json(max_nesting=4))
        f.write(json.dumps(json_str, indent=4, sort_keys=True))


def serialize_dashboard(dashboard, session, tracked_dir):
    '''
        Serializes a given dashboard and returns a list of
        required table for this dashboard to work
    '''
    
    dashboard_id = dashboard['id']
    dashboard_name = dashboard['name']
    
    dash = session.query(ReportDashboard).filter(ReportDashboard.id == dashboard_id).first()
    serialize_collection(dash.collection_id, session, tracked_dir)
    serialize_user(dash.creator_id, session, tracked_dir)

    for report_card in dash.report_dashboard_cards:
        if report_card.card is not None and report_card.card.collection_id is not None:
            serialize_collection(report_card.card.collection_id, session, tracked_dir)

    with open(f"{tracked_dir}/dashboards/{dashboard_name}.json", 'w', encoding='utf-8') as f:
        json_str = json.loads(dash.to_json(max_nesting=4))
        f.write(json.dumps(json_str, indent=4, sort_keys=True))
    

def serialize_database(database, session, tracked_dir, extra_tables=None):
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
        if 'regex_list' in database: 
            if match_regex_list(database['regex_list'], table.name):
                json_tables.append(json.loads(table.to_json(max_nesting=4)))
        else:
            # no regex list
            json_tables.append(json.loads(table.to_json(max_nesting=4)))

        count += 1
        print('Done table: ' + str(table.name))
        print('finished {} of {}'.format(count, total_tables))
    
    for table in extra_tables:
        extra = json.loads(table.to_json(max_nesting=4))
        extra['_from_dashboar_dep'] = True
        json_tables.append(extra)
    
    database_obj['tables'] = dedup_by_id(json_tables)
    
    with open(f"{tracked_dir}/databases/{database_name}.json", 'w', encoding='utf-8') as f:
        f.write(json.dumps(database_obj, indent=4, sort_keys=True))

def dedup_by_id(input):
    already_id = []
    return_list = []

    for i in input:
        if i['id'] in already_id:
            continue
        else:
            return_list.append(i)
            already_id.append(i['id'])
    return return_list