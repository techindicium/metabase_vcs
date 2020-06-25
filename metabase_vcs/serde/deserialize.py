import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from metabase_vcs.models.models import ReportDashboard, ReportCard
from metabase_vcs.env import *

db_metabase_prod = get_env_var_or_fail("DB_NAME")

def update_dashboard(dashboard, dashboards_dir, session):
    dashboard_name = dashboard['name']

    with open(f"{dashboards_dir}/{dashboard_name}.json") as f:
        dash = json.loads(f.read())
        dash_cards = dash['report_dashboard_cards']
        
        for dash_card in dash_cards:
            if dash_card['card'] is not None:
                card = dash_card['card']
                instance = session.query(ReportCard).filter(ReportCard.id == card['id']).first()
                print(f"Reading {instance.name}")
                instance.update_from_json(json.dumps(card))
        
        del dash['report_dashboard_cards']
        dash_db = session.query(ReportDashboard).filter(ReportDashboard.id == dash['id']).first()
        dash_db.update_from_json(json.dumps(dash))