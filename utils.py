import yaml
import os
import logging

logging_str = "[%(asctime)s: %(levelname)s: %(module)s]: %(message)s"
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(filename=os.path.join(log_dir, "ekyc_logs.log"), level=logging.INFO, format=logging_str, filemode="a")

def read_yaml(path_to_yaml):
    try:
        with open(path_to_yaml, 'r') as yaml_file:
            content = yaml.safe_load(yaml_file)
        logging.info(f"YAML file {path_to_yaml} loaded successfully.")
        return content
    except Exception as e:
        logging.error(f"Error in read_yaml: {e}")
        return None

def create_dirs(dirs):
    try:
        for dir_path in dirs:
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
        logging.info(f"Directories {dirs} created successfully.")
    except Exception as e:
        logging.error(f"Error in create_dirs: {e}")

def file_exists(filepath):
    try:
        exists = os.path.exists(filepath)
        logging.info(f"File {filepath} exists: {exists}")
        return exists
    except Exception as e:
        logging.error(f"Error in file_exists: {e}")
        return False