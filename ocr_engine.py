import easyocr
import logging
import os

logging_str = "[%(asctime)s: %(levelname)s: %(module)s]: %(message)s"
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(filename=os.path.join(log_dir, "ekyc_logs.log"), level=logging.INFO, format=logging_str, filemode="a")

reader = easyocr.Reader(['en'])

def extract_text(img_path):
    try:
        if not os.path.exists(img_path):
            raise FileNotFoundError(f"Image file not found: {img_path}")
        result = reader.readtext(img_path)
        extracted_text = " ".join([text[1] for text in result])
        logging.info(f"Text extracted from image: {extracted_text}")
        return extracted_text
    except Exception as e:
        logging.error(f"Error in extract_text: {e}")
        return ""