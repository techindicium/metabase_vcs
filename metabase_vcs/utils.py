from dotenv import load_dotenv
import os

load_dotenv()

def get_env_var_or_fail(envvar):
    envvar_value = os.getenv(envvar)
    if envvar_value is None:
        raise Exception(f"{envvar} not set")
    return envvar_value