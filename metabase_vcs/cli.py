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
    from metabase_vcs.models.export_tracked_dashs import serialize_dashboard
    from metabase_vcs.models.env import db_host, db_user, db_password, db_port, db_metabase_dev

    engine = create_engine(
        f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_metabase_dev}",
        isolation_level="READ UNCOMMITTED"
    )
    Session = sessionmaker(bind=engine)
    session = Session()

    with open("tracked_dashboards.json") as f:
        dashboards = json.load(f)

    for dashboard in dashboards['dashboards']:
        serialize_dashboard(dashboard, session)

    session.close()

if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
