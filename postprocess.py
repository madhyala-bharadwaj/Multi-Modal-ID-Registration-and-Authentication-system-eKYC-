import re
import logging
import os
from face_verification import get_face_embeddings
from utils import read_yaml
from datetime import datetime
import json

logging_str = "[%(asctime)s: %(levelname)s: %(module)s]: %(message)s"
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(filename=os.path.join(log_dir, "ekyc_logs.log"), level=logging.INFO, format=logging_str, filemode="a")

config_path = "config.yaml"
config = read_yaml(config_path)
locations = config['locations']
face_from_feed = locations['FACE_FROM_FEED']

def pan_extract_information(extracted_text):
    try:
        pan_info = {
            'ID': 'N/A',
            'Name': 'N/A',
            'DOB': 'N/A',
            'ID_type':'PAN',
            'Registered_time':'',
            'Photo_embeddings': 'N/A'
        }
        pan_pattern = r'Card\s([A-Z0-9]{10})'
        name_pattern = r'Name\s([A-Z]*\s[A-Z]*)'
        dob_pattern = r'(\d{2}/\d{2}/\d{4})'
 
        pan_match = re.search(pan_pattern, extracted_text)
        name_match = re.search(name_pattern, extracted_text)
        dob_match = re.search(dob_pattern, extracted_text)

        if pan_match:
            pan_info['ID'] = pan_match.group(0)[5:]
        else:
            logging.error('PAN ID not found in the extracted text')
        if name_match:
            pan_info['Name'] = name_match.group(0)[5:]
        else:
            logging.error('Name not found in the extracted text')
        if dob_match:
            pan_info['DOB'] = datetime.strptime(dob_match.group(0), "%d/%m/%Y").date().strftime("%Y-%m-%d")
        else:
            logging.error('DOB not found in the extracted text')
        pan_info['Photo_embeddings'] = json.dumps(get_face_embeddings(face_from_feed))
        logging.info(f"PAN information extracted: {pan_info}")
        return pan_info
    except Exception as e:
        logging.error(f"Error in pan_extract_information: {e}")
        return None

def aadhar_extract_information(extracted_text):
    try:
        aadhar_info = {
            'ID': 'N/A',
            'Name': 'N/A',
            'DOB': 'N/A',
            'ID_type': 'Aadhar',
            'Registered_time': 'N/A',
            'Photo_embeddings': 'N/A'
        }
        aadhar_pattern = r'\d{4}\s\d{4}\s\d{4}'
        name_pattern = r'([A-Z]{1}[a-z]*\s[A-Z]{1}[a-z]*)'
        dob_pattern = r'(\d{2}/\d{2}/\d{4})'

        aadhar_match = re.search(aadhar_pattern, extracted_text)
        name_match = re.search(name_pattern, extracted_text)
        dob_match = re.search(dob_pattern, extracted_text)

        if aadhar_match:
            aadhar_info['ID'] = aadhar_match.group(0)
        else:
            logging.error('Aadhar ID not found in the extracted text')

        if name_match:
            aadhar_info['Name'] = name_match.group(0)
        else:
            logging.error('Name not found in the extracted text')

        if dob_match:
            aadhar_info['DOB'] = datetime.strptime(dob_match.group(0), "%d/%m/%Y").strftime("%Y/%m/%d")
        else:
            logging.error('DOB not found in the extracted text')
        aadhar_info['Photo_embeddings'] = json.dumps(get_face_embeddings(face_from_feed))
        logging.info(f"Aadhar information extracted")
        return aadhar_info
    except Exception as e:
        logging.error(f"Error in aadhar_extract_information: {e}")
        return None