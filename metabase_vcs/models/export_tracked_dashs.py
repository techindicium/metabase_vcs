import json
from metabase_vcs.app.models import ReportDashboard, ReportDashboardcard, ReportCard 
from metabase_vcs.app.env import *

def serialize_dashboard(dashboard, session):
    dashboard_id = dashboard['id']
    dashboard_name = dashboard['name']
    
    dash = session.query(ReportDashboard).filter(ReportDashboard.id == dashboard_id).first()

    with open(f"dashboards/{dashboard_name}.json", 'w', encoding='utf-8') as f:
        json_str = json.loads(dash.to_json(max_nesting=4))
        f.write(json.dumps(json_str, indent=4, sort_keys=True))
