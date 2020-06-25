from dotenv import load_dotenv
import os

load_dotenv()

def get_env_var_or_fail(envvar):
    envvar_value = os.getenv(envvar)
    if envvar_value is None:
        raise Exception(f"{envvar} not set")
    return envvar_value

db_user = get_env_var_or_fail('DB_USER')
db_password = get_env_var_or_fail('DB_PASSWORD')
db_host = get_env_var_or_fail('DB_HOST')
db_metabase_dev = get_env_var_or_fail('DB_NAME_DEV')

db_port = os.environ.get("DB_PORT", 5566)

