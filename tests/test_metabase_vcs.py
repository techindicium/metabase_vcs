#!/usr/bin/env python

"""Tests for `metabase_vcs` package."""

import pytest
import os

from click.testing import CliRunner

from metabase_vcs import cli
from metabase_vcs.models.models import ReportDashboard, ReportCard

from subprocess import Popen, PIPE
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

test_db_user = 'postgres'
test_db_name = 'postgres'
test_db_password = 'mvcs'
test_db_port = '5555'
test_db_host = 'localhost'

def set_test_env_vars():
    os.environ['DB_USER'] = test_db_user
    os.environ['DB_PASSWORD'] = test_db_password
    os.environ['DB_HOST'] = test_db_host
    os.environ['DB_NAME_DEV'] = test_db_name
    os.environ['DB_PORT'] = test_db_port


@pytest.fixture
def prepare_db():
    process = Popen(['bash', 'tests/resources/reset_test_postgres.sh'], stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    
    while process.poll() is None:
        print(stdout)
        time.sleep(2)

    engine = create_engine(
        f"postgresql+psycopg2://{test_db_user}:{test_db_password}@{test_db_host}:{test_db_port}/{test_db_name}",
    )

    Session = sessionmaker(bind=engine)
    session = Session()
    return {'exit_code': process.returncode, 'session': session}


def test_dashboard_changes(prepare_db):
    """Test that dashboard information changes."""
   
    assert prepare_db['exit_code'] == 0
    session = prepare_db['session']
    dash = session.query(ReportDashboard).filter(ReportDashboard.id == 147).first()

    assert dash.name == 'CRM - Unique'
    
    set_test_env_vars()
    runner = CliRunner()
    result = runner.invoke(cli.import_from_file, [
        '-d', 'tests/resources/test_dashboards_files/', 
        '-f', 'tests/resources/test_dashboards.json'
    ])
    
    session.refresh(dash)
    assert dash.name == 'CRM - Duplique'
    assert result.exit_code == 0

    session.close()


def test_dashboard_card_changes(prepare_db):
    """Test cards that belongs to a dashboard changes."""
   
    assert prepare_db['exit_code'] == 0
    session = prepare_db['session']
    card = session.query(ReportCard).filter(ReportCard.id == 437).first()

    assert card.name == 'Leads'
    
    set_test_env_vars()
    runner = CliRunner()
    result = runner.invoke(cli.import_from_file, [
        '-d', 'tests/resources/test_dashboards_files/', 
        '-f', 'tests/resources/test_dashboards.json'
    ])
    
    session.refresh(card)
    assert card.name == 'LeadsBad'
    assert result.exit_code == 0

    session.close()