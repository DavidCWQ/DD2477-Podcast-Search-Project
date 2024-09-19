import yaml

from es.config.config import configs as _

def read_app_config():
    """
    Read configuration parameters from settings.yml.
    """
    try:
        with open("backend/config/settings.yml", 'r') as f:
            _config = yaml.safe_load(f)
        _config.update(_)
    except FileNotFoundError:
        print("Error: File 'backend/config/settings.yml' not found.")
    except IOError:
        print("Error: Unable to read the file 'backend/config/settings.yml'.")
    except Exception as e:
        print("Error: An unexpected error occurred: ", str(e))

    return _config

configs = read_app_config()