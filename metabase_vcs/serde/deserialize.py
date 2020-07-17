import json
import copy

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from metabase_vcs.models.models import ReportDashboard, ReportCard, ReportDashboardcard, Collection, CoreUser
from datetime import datetime


def update_colletion(collection_file, colletions_dir, session):
    with open(f"{colletions_dir}/{collection_file}") as f:
        collection = json.loads(f.read())
        collection_instance = session.query(Collection).filter(Collection.id == collection['id']).first()
        
        if collection_instance is not None:
            print(f"Updating Collection {collection_instance.id}")
            collection_instance.update_from_json(json.dumps(collection))
        else:
            print(f"Creating new DashboardCards")
            new_collection = Collection()
            new_collection = new_collection.new_from_json(json.dumps(collection))
         
            session.add(new_collection)


def update_user(user_file, users_dir, session):
    with open(f"{users_dir}/{user_file}") as f:
        user = json.loads(f.read())
        user_instance = session.query(CoreUser).filter(CoreUser.id == user['id']).first()
        
        if user_instance is not None:
            print(f"Updating User {user_instance.id}")
            user_instance.update_from_json(json.dumps(user))
        else:
            print(f"Creating new User")
            new_user = CoreUser()
            new_user = new_user.new_from_json(json.dumps(user))
         
            session.add(new_user)


def update_dashboard(dashboard, dashboards_dir, session):

    dash_cards = dashboard['report_dashboard_cards']
    del dashboard['report_dashboard_cards']
    save_dashboard(dashboard, session)
    
    for dash_card in dash_cards:
        
        dash_report_card_instance = session.query(ReportDashboardcard) \
            .filter(ReportDashboardcard.id == dash_card['id']) \
            .first()
        
        dash_card_without_questions = copy.copy(dash_card)
        del dash_card_without_questions['card']

        if dash_card['card'] is not None:
            card = dash_card['card']
            instance = session.query(ReportCard).filter(ReportCard.id == card['id']).first()
            if instance is not None:
                print(f"Reading {instance.name}")
                instance.update_from_json(json.dumps(card))
            else:
                print(f"Creating new Cards")
                report_card = ReportCard()
                report_card = report_card.new_from_json(json.dumps(card))
                report_card.created_at = datetime.now().isoformat()
                report_card.updated_at = datetime.now().isoformat()
                session.add(report_card)
        
        if dash_report_card_instance is not None:
            print(f"Updating DashBoardCard{dash_report_card_instance.id}")
            dash_report_card_instance.update_from_json(json.dumps(dash_card_without_questions))
        else:
            print(f"Creating new DashboardCards")
            report_dash_card = ReportDashboardcard()
            report_dash_card = report_dash_card.new_from_json(json.dumps(dash_card_without_questions))
            report_dash_card.created_at = datetime.now().isoformat()
            report_dash_card.updated_at = datetime.now().isoformat()
            session.add(report_dash_card)


def save_dashboard(dash, session):
    dashboard_instance = session.query(ReportDashboard).filter(ReportDashboard.id == dash['id']).first()

    if dashboard_instance is not None:
        dashboard_instance.update_from_json(json.dumps(dash))
    else:
        new_dash = ReportDashboard()
        new_dash = new_dash.new_from_json(json.dumps(dash))
        new_dash.created_at = datetime.now().isoformat()
        new_dash.updated_at = datetime.now().isoformat()
        session.add(new_dash)


def update_entity_from_json(entity_json, entity_model, session, delete_keys = []):
    if 'name' in entity_json:
        print(entity_json['name'])
    entity_instance = session.query(entity_model).filter(entity_model.id == entity_json['id']).first()
    entity_json_copy = copy.copy(entity_json)
    for key in delete_keys:
        del entity_json_copy[key]
    
    if '_from_dashboar_dep' in entity_json_copy:
        del entity_json_copy['_from_dashboar_dep'] # removing metadata not useful for metabase

    if entity_instance is not None:
        print(f"Updating {str(entity_model)} {entity_instance.id}")
        entity_instance.update_from_json(json.dumps(entity_json_copy))
    else:
        print(f"Creating new {str(entity_model)}")
        new_entity = entity_model()
        new_entity = new_entity.new_from_json(json.dumps(entity_json_copy))
        
        session.add(new_entity)