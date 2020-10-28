"""Console script for metabase_vcs."""
import sys
import click
import json
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, joinedload
from metabase_vcs.utils import get_env_var_or_fail

NEGATE_ALL_REGEX = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX' # vveeeery weird vitor

@click.group()
def main(args=None):
    pass

@main.command()
@click.option('-f', '--dashboards-file', default='tracked.json')
@click.option('-d', '--dashboards-tracked-dir', default='.')
def export_metabase(dashboards_file, dashboards_tracked_dir):
    from metabase_vcs.serde.serialize import serialize_dashboard, serialize_database
    from metabase_vcs.serde.utils import extract_required_tables_dashboard
    from dotenv import load_dotenv
    load_dotenv()

    # Source envs for exporting
    db_user = get_env_var_or_fail('DB_USER')
    db_password = get_env_var_or_fail('DB_PASSWORD')
    db_host = get_env_var_or_fail('DB_HOST')
    db_metabase = get_env_var_or_fail('DB_NAME')
    db_port = get_env_var_or_fail("DB_PORT")

    engine = create_engine(
        f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_metabase}",
        isolation_level="READ UNCOMMITTED"
    )
    Session = sessionmaker(bind=engine)
    session = Session()

    with open(dashboards_file) as f:
        tracked = json.load(f)

    dashboard_dependent_tables = {}
    for dashboard in tracked['dashboards']:
        try:
            serialize_dashboard(dashboard, session, dashboards_tracked_dir)
        except Exception as e:
            print(str(e))
            raise Exception(f"Error serializing dashboard: {dashboard}")

        dependent_tables = extract_required_tables_dashboard(dashboard, session)
        dashboard_dependent_tables = combine_dicts(dashboard_dependent_tables, dependent_tables)
    
    for database in tracked['databases']:
        extra_tables = dashboard_dependent_tables.get(database['id'])
        serialize_database(database, session, dashboards_tracked_dir, database.get('regex_list', []), extra_tables)
    
    for database, tables in dashboard_dependent_tables.items():
        tracked_db_ids = [db['id'] for db in tracked['databases']]
        if database in tracked_db_ids:
            continue
        # required database not tracked
        serialize_database({'id': database, 'schemas': []}, session, dashboards_tracked_dir, NEGATE_ALL_REGEX, extra_tables=tables)

    session.close()


@main.command()
@click.option('-f', '--dashboards-file', default='tracked.json')
@click.option('-d', '--dashboards-tracked-dir', default='.')
def import_from_file(dashboards_file, dashboards_tracked_dir):
    from metabase_vcs.serde.deserialize import update_dashboard, update_colletion, update_user, update_entity_from_json
    from metabase_vcs.models.models import MetabaseDatabase, MetabaseTable, MetabaseField, Collection, CoreUser

    # Target envs for importing
    db_user_target = get_env_var_or_fail('DB_USER_TARGET')
    db_password_target = get_env_var_or_fail('DB_PASSWORD_TARGET')
    db_host_target = get_env_var_or_fail('DB_HOST_TARGET')
    db_metabase_target = get_env_var_or_fail('DB_NAME_TARGET')
    db_port_target = get_env_var_or_fail("DB_PORT_TARGET")

    engine = create_engine(
        f"postgresql+psycopg2://{db_user_target}:{db_password_target}@{db_host_target}:{db_port_target}/{db_metabase_target}",
        isolation_level="READ UNCOMMITTED"
    )
    
    with open(dashboards_file) as f:
        dashboards = json.load(f)

    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        
        databases_dir = 'databases'
        for database in os.listdir(dashboards_tracked_dir + "/" + databases_dir):
            with open(f'{dashboards_tracked_dir + "/" + databases_dir}/{database}') as f:
                database_json = json.loads(f.read())
        
            update_entity_from_json(
                database_json, 
                MetabaseDatabase,
                session,
                delete_keys=['tables']
            )

            tables = database_json['tables']
            for table in tables:
                update_entity_from_json(table, MetabaseTable, session, delete_keys=['metabase_table_fields']) 
                
                fields = table['metabase_table_fields']
                [
                    update_entity_from_json(f, MetabaseField, session) 
                    for f in fields
                ]

        collections_dir = 'collections'
        for collection in os.listdir(dashboards_tracked_dir + "/" + collections_dir):
            with open(f'{dashboards_tracked_dir + "/" + collections_dir}/{collection}') as f:
                collection_json = json.loads(f.read())
            update_entity_from_json(collection_json, Collection, session)

        users_dir = 'users'
        for user in os.listdir(dashboards_tracked_dir + "/" + users_dir):
            with open(f'{dashboards_tracked_dir + "/" + users_dir}/{user}') as f:
                user_json = json.loads(f.read())
            update_entity_from_json(user_json, CoreUser, session)
       
        dashboards_dir = 'dashboards'
        for dashboard in os.listdir(dashboards_tracked_dir + "/" + dashboards_dir):
            with open(f'{dashboards_tracked_dir + "/" + dashboards_dir}/{dashboard}') as f:
                dashboards_json = json.loads(f.read())
            update_dashboard(dashboards_json, dashboards_tracked_dir, session)
        
        session.commit()
    finally:
        session.close()


def combine_dicts(d1, d2):
    ds = [d1, d2]

    for key in d1.keys():
        if key not in d2:
            d2[key] = []

    for key in d2.keys():
        if key not in d1:
            d1[key] = []

    d = {}
    for k in d1.keys():
        items = []
        for d in ds:
            items += d[k]
        d[k] = set(items)
    return d

if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
