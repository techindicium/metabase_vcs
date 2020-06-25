import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import ReportDashboard, ReportCard
from app.env import *

db_metabase_prod = get_env_var_or_fail("DB_NAME")

def update_dashboard(dashboard):
    dashboard_name = dashboard['name']

    engine = create_engine(
        f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_metabase_prod}",
    )

    Session = sessionmaker(bind=engine)
    session = Session()

    with open(f"dashboards/{dashboard_name}.json") as f:
        dash = json.loads(f.read())
        dash_cards = dash['report_dashboard_cards']
        
        for dash_card in dash_cards:
            if dash_card['card'] is not None:
                card = dash_card['card']
                instance = session.query(ReportCard).filter(ReportCard.id == card['id']).first()
                print(f"Reading {instance.name}")
                instance.update_from_json(json.dumps(card))


        session.commit()
        session.close()

with open("tracked_dashboards.json") as f:
    dashboards = json.load(f)

for dashboard in dashboards['dashboards']:
    update_dashboard(dashboard)
