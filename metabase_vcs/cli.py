"""Console script for metabase_vcs."""
import sys
import click
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, joinedload

@click.group()
def main(args=None):
    pass

@main.command()
def export_metabase(args=None):
    from metabase_vcs.serde.serialize import serialize_dashboard, serialize_database
    from metabase_vcs.env import db_host, db_user, db_password, db_port, db_metabase_dev

    engine = create_engine(
        f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_metabase_dev}",
        isolation_level="READ UNCOMMITTED"
    )
    Session = sessionmaker(bind=engine)
    session = Session()

    with open("tracked.json") as f:
        tracked = json.load(f)

    for database in tracked['databases']:
        serialize_database(database, session)

    for dashboard in tracked['dashboards']:
        serialize_dashboard(dashboard, session)


    session.close()


@main.command()
@click.option('-f', '--dashboards-file', default='tracked.json')
@click.option('-d', '--dashboards-dir', default='dashboards/')
def import_from_file(dashboards_file, dashboards_dir):
    from metabase_vcs.serde.deserialize import update_dashboard
    from metabase_vcs.env import db_host, db_user, db_password, db_port, db_metabase_dev

    engine = create_engine(
        f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_metabase_dev}",
        isolation_level="READ UNCOMMITTED"
    )
    
    with open(dashboards_file) as f:
        dashboards = json.load(f)

    try:
        Session = sessionmaker(bind=engine)
        session = Session()
    
        for dashboard in dashboards['dashboards']:
            update_dashboard(dashboard, dashboards_dir, session)
        
        session.commit()
    finally:
        session.close()


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
