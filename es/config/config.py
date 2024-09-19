import yaml

from dotenv import dotenv_values

credentials = dotenv_values(dotenv_path="es/config/.env", verbose=True)

def read_es_config(debug=False):
    """
    Read configuration parameters from elasticsearch.yml.
    """
    try:
        with open("es/config/elasticsearch.yml", 'r') as f:
            _config = yaml.safe_load(f)
            _config.update(
                {
                    "hosts": credentials["URL"],
                    "username": credentials["USERNAME"],
                    "password": credentials["PASSWORD"],
                }
            )
            if debug: print(_config)
    except FileNotFoundError:
        print("Error: File 'es/config/elasticsearch.yml' not found.")
    except IOError:
        print("Error: Unable to read the file 'es/config/elasticsearch.yml'.")
    except Exception as e:
        print("Error: An unexpected error occurred: ", str(e))
    return _config

configs = read_es_config()