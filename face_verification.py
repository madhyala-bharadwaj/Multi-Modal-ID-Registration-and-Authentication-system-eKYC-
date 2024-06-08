import face_recognition
from deepface import DeepFace
import numpy as np
import cv2
import os
import logging
from utils import file_exists, read_yaml

# Setting up logging
logging_str = "[%(asctime)s: %(levelname)s: %(module)s]: %(message)s"
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(filename=os.path.join(log_dir, "ekyc_logs.log"), level=logging.INFO, format=logging_str, filemode="a")

# Configuration Setting
config_path = "config.yaml"
config = read_yaml(config_path)
locations = config['locations']
cascade_path = locations['HAARCASCADE_PATH']

def detect_and_extract_face(img,file_name):
    try:
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier(cascade_path)
        faces = face_cascade.detectMultiScale(gray_img, scaleFactor=1.1, minNeighbors=5)
        max_area = 0
        largest_face = None
        for (x, y, w, h) in faces:
            area = w * h
            if area > max_area:
                max_area = area
                largest_face = (x, y, w, h)
        if largest_face is not None:
            (x, y, w, h) = largest_face
            new_w = int(w * 1.50)
            new_h = int(h * 1.50)
            new_x = max(0, x - int((new_w - w) / 2))
            new_y = max(0, y - int((new_h - h) / 2))
            extracted_face = img[new_y:new_y + new_h, new_x:new_x + new_w]
            if os.path.exists(file_name):
                os.remove(file_name)
            cv2.imwrite(file_name, extracted_face)
            logging.info(f"Extracted face saved at: {file_name}")
            return file_name
        else:
            logging.info("No face detected in the image.")
            return None
    except Exception as e:
        logging.error(f"Error in detect_and_extract_face: {e}")
        return None

def face_recog_face_comparison(image1_path, image2_path):
    try:
        img1_exists = file_exists(image1_path)
        img2_exists = file_exists(image2_path)
        if not (img1_exists or img2_exists):
            logging.error("Check the path for the images provided")
            return False
        image1 = face_recognition.load_image_file(image1_path)
        image2 = face_recognition.load_image_file(image2_path)
        face_encodings1 = face_recognition.face_encodings(image1)
        face_encodings2 = face_recognition.face_encodings(image2)
        if len(face_encodings1) == 0 or len(face_encodings2) == 0:
            logging.error("No faces detected in one or both images.")
            return False
        matches = face_recognition.compare_faces(np.array(face_encodings1), np.array(face_encodings2))
        if matches[0]:
            logging.info("Faces are verified")
            return True
        else:
            logging.info("Faces are not verified")
            return False
    except Exception as e:
        logging.error(f"Error in face_recog_face_comparison: {e}")
        return False

def deepface_face_comparison(image1_path, image2_path):
    try:
        img1_exists = file_exists(image1_path)
        img2_exists = file_exists(image2_path)
        if not (img1_exists or img2_exists):
            logging.error("Check the path for the images provided")
            return False
        verification = DeepFace.verify(img1_path=image1_path, img2_path=image2_path)
        if len(verification) > 0 and verification['verified']:
            logging.info("Faces are verified")
            return True
        else:
            logging.info("Faces are not verified")
            return False
    except Exception as e:
        logging.error(f"Error in deepface_face_comparison: {e}")
        return False

def face_comparison(image1_path, image2_path, model_name='deepface'):
    try:
        is_verified = False
        if model_name == 'deepface':
            is_verified = deepface_face_comparison(image1_path, image2_path)
        elif model_name == 'facerecognition':
            is_verified = face_recog_face_comparison(image1_path, image2_path)
        else:
            logging.error("Error reading face recognition method.")
        return is_verified
    except Exception as e:
        logging.error(f"Error in face_comparison: {e}")
        return False

def get_face_embeddings(image_path):
    try:
        img_exists = file_exists(image_path)
        if not img_exists:
            logging.error("Check the path for the images provided")
            return None
        embedding_objs = DeepFace.represent(img_path=image_path, model_name="Facenet")
        embedding = embedding_objs[0]["embedding"]
        if len(embedding) > 0:
            return embedding
        return None
    except Exception as e:
        logging.error(f"Error in get_face_embeddings: {e}")
        return None