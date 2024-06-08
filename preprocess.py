import cv2
import numpy as np
import logging
import os
from utils import read_yaml

logging_str = "[%(asctime)s: %(levelname)s: %(module)s]: %(message)s"
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(filename=os.path.join(log_dir, "ekyc_logs.log"), level=logging.INFO, format=logging_str, filemode="a")

config_path = "config.yaml"
config = read_yaml(config_path)
locations = config['locations']
id_card_path = locations['ID_FILE']

def read_image(image_path):
    try:
        image = np.fromstring(image_path.read(), np.uint8)
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        logging.info(f'Image read from {image_path}')
        return image
    except Exception as e:
        logging.error(f"Error in read_image: {e}")
        return None

def extract_id_card(img):
    try:
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        canny_output = cv2.Canny(gray_img, 100, 200)
        contours, _ = cv2.findContours(canny_output, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) == 0:
            logging.error("No contours found in the image.")
            return None
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)
        id_card = img[y:y+h, x:x+w]
        # id_card = img
        cv2.imwrite(id_card_path, id_card)
        logging.info(f'Extracted ID image saved at {id_card_path}')
        return id_card
    except Exception as e:
        logging.error(f"Error in extract_id_card: {e}")
        return None

def save_image(image, filename, path=""):
    try:
        if path and not os.path.exists(path):
            os.makedirs(path)
        file_path = os.path.join(path, filename)
        cv2.imwrite(file_path, image)
        logging.info(f"Image saved at {file_path}")
        return file_path
    except Exception as e:
        logging.error(f"Error in save_image: {e}")
        return None