import json
from metabase_vcs.models.models import ReportDashboard, ReportDashboardcard, ReportCard, MetabaseDatabase, MetabaseTable, MetabaseField
from collections import OrderedDict
import re


def match_regex_list(regex_list, text):
    for regex_str in regex_list:
        print(regex_str, text)
        match = re.search(regex_str, text)
        print(match)
        if match:
            return True
    return False


def group_by_tables_by_db(input):
    res = {}
    for table in input:
        if table.db_id in res: 
            res[table.db_id].append(table)
        else: 
            res[table.db_id] = [table]
    return res
    
def extract_required_tables_dashboard(dashboard, session):
    dashboard_id = dashboard['id']
    dash = session.query(ReportDashboard).filter(ReportDashboard.id == dashboard_id).first()
 
    ## get from dashboard_cards
    fields = []
    for dashboardcard in dash.report_dashboard_cards:
        fields += extract_required_tables_dashboardcard(dashboardcard)
    
    required_fields = set(fields) # unique
    
    required_fields_from_db = session.query(MetabaseField.table_id) \
        .filter(MetabaseField.id.in_(required_fields)) \
        .distinct() \
        .all()

    required_table_ids = [field[0] for field in required_fields_from_db]
    
    required_tables = session.query(MetabaseTable) \
        .filter(MetabaseTable.id.in_(required_table_ids)) \
        .all()

    return group_by_tables_by_db(required_tables)

def extract_required_tables_dashboardcard(dashboardcard):
    ## dashboardcard fields that might have table_fields: parameter_mappings, visualization_settings
    dashcard_parametner_fields = get_fields_from_parameter_mappings(dashboardcard.parameter_mappings)
    dashcard_visualization_fields = get_fields_from_visualization_settings(dashboardcard.visualization_settings)
    
    if dashboardcard.card is not None:
        card_visua_settings = dashboardcard.card.visualization_settings
        card_visualiztion_fields = get_fields_from_visualization_settings(card_visua_settings)
    else:
        card_visualiztion_fields = []
    
    return dashcard_visualization_fields + \
           dashcard_parametner_fields + \
           card_visualiztion_fields
    

def traverse(item):
    if isinstance(item, list) and item[0] == 'field-id':
        yield item[1]
    else:
        for i in item:
            if isinstance(i, list) and i[0] == 'field-id':
                yield i[1]
            if isinstance(i, list) and i[0] != 'field-id':
                for j in traverse(i):
                    yield j

def get_maybe_field(json_list):
    if isinstance(json_list, list):
        lis = [k for k in traverse(json_list)]
    else:
        lis = []

    return lis

def get_fields_from_parameter_mappings(json_str):
    if 'field-id' not in json_str:
        # dont even parse if the string doesnt contains field-id
        return []
    
    json_obj = json.loads(json_str)
    
    fields = []
    for l in json_obj:
        if 'target' in l:
            target = l['target']
            if len(target) > 1:
                fields += get_maybe_field(target[1])

    return fields


def get_fields_from_visualization_settings(json_str):
    def extract_col_settings(col_settings):
        for key in col_settings.keys():
            if key is not None and key != '':
                ref_list = json.loads(key)
                return get_maybe_field(ref_list)
            else:
                return []
    
    def extract_table_columns(cols): 
        if cols is None:
            return []
        fields = []
        for col in cols:
            if 'fieldRef' in col:
                field_ref = col['fieldRef']
                if len(field_ref) > 0 and field_ref[0] != 'field-id':
                    field = get_maybe_field(field_ref[1])
                else:
                    field = get_maybe_field(field_ref)
                fields += field
        return fields

    if 'field-id' not in json_str:
        # dont even parse if the string doesnt contains field-id
        return []
    
    json_obj = json.loads(json_str)
    
    fields = []
    if 'column_settings' in json_obj:
        fields += extract_col_settings(json_obj['column_settings'])
    
    if 'table.columns' in json_obj:
        fields += extract_table_columns(json_obj['table.columns'])

    return fields

            

if __name__ == "__main__":
    #lst = [{'parameter_id': '2135a716', 'card_id': 90, 'target': ['dimension', ['field-id', 56074]]}, {'parameter_id': 'f96b26dc', 'card_id': 90, 'target': ['dimension', ['fk->', ['field-id', 56080], ['field-id', 55465]]]}, {'parameter_id': '68434bf7', 'card_id': 90, 'target': ['dimension', ['field-id', 56084]]}, {'parameter_id': '88055e1a', 'card_id': 90, 'target': ['dimension', ['fk->', ['field-id', 56076], ['field-id', 56701]]]}]
    #get_fields_from_parameter_mappings(lst)

    # stra = "{\"table.pivot_column\":\"CD_EMPRESA\",\"table.cell_column\":\"CD_GRUPOEMPRESA\",\"table.columns\":[{\"name\":\"DT_SALDO\",\"fieldRef\":[\"datetime-field\",[\"field-id\",55565],\"default\"],\"enabled\":true},{\"name\":\"CD_EMPRESA\",\"fieldRef\":[\"field-id\",55568],\"enabled\":true},{\"name\":\"CD_GRUPOEMPRESA\",\"fieldRef\":[\"field-id\",55570],\"enabled\":false},{\"name\":\"CD_OPERADOR\",\"fieldRef\":[\"field-id\",55569],\"enabled\":false},{\"name\":\"CD_SALDO\",\"fieldRef\":[\"field-id\",55572],\"enabled\":true},{\"name\":\"CD_PRODUTO\",\"fieldRef\":[\"field-id\",55571],\"enabled\":true},{\"name\":\"DT_CADASTRO\",\"fieldRef\":[\"datetime-field\",[\"field-id\",55567],\"default\"],\"enabled\":false},{\"name\":\"QT_SALDO\",\"fieldRef\":[\"field-id\",55566],\"enabled\":true}],\"column_settings\":{\"[\\\"ref\\\",[\\\"field-id\\\",55565]]\":{\"time_enabled\":null,\"date_style\":\"D/M/YYYY\"}},\"card.description\":\"Filtrado apenas por Empresa e Produto\"}"
    # stra = "{\"table.pivot_column\":\"CD_EMPRESA\",\"table.cell_column\":\"CD_GRUPOEMPRESA\",\"table.columns\":[{\"name\":\"DT_SALDO\",\"fieldRef\":[\"datetime-field\",[\"field-id\",55565],\"default\"],\"enabled\":true},{\"name\":\"CD_EMPRESA\",\"fieldRef\":[\"field-id\",55568],\"enabled\":true},{\"name\":\"CD_GRUPOEMPRESA\",\"fieldRef\":[\"field-id\",55570],\"enabled\":false},{\"name\":\"CD_OPERADOR\",\"fieldRef\":[\"field-id\",55569],\"enabled\":false},{\"name\":\"CD_SALDO\",\"fieldRef\":[\"field-id\",55572],\"enabled\":true},{\"name\":\"CD_PRODUTO\",\"fieldRef\":[\"field-id\",55571],\"enabled\":true},{\"name\":\"DT_CADASTRO\",\"fieldRef\":[\"datetime-field\",[\"field-id\",55567],\"default\"],\"enabled\":false},{\"name\":\"QT_SALDO\",\"fieldRef\":[\"field-id\",55566],\"enabled\":true}],\"column_settings\":{\"[\\\"ref\\\",[\\\"field-id\\\",55565]]\":{\"time_enabled\":null,\"date_style\":\"D/M/YYYY\"}}}"

    # get_fields_from_visualization_settings(stra)
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker, joinedload
    from metabase_vcs.serde.serialize import serialize_dashboard, serialize_database
    from metabase_vcs.env import db_host, db_user, db_password, db_port, db_metabase_dev

    engine = create_engine(
        f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_metabase_dev}",
        isolation_level="READ UNCOMMITTED"
    )
    Session = sessionmaker(bind=engine)
    session = Session()

    x = extract_required_tables_dashboard(
        {
            "name": "materia_prima",
            "id": 17
        }
    )
    print(x)
    session.close()