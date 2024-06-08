import streamlit as st
from utils import read_yaml,file_exists
import os
import cv2
import logging

logging_str = "[%(asctime)s: %(levelname)s: %(module)s]: %(message)s"
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(filename=os.path.join(log_dir, "ekyc_logs.log"), level=logging.INFO, format=logging_str, filemode="a")

config_path = "config.yaml"
config = read_yaml(config_path)

locations = config['locations']
live_feed_image = locations['LIVE_FEED_IMAGE']

def capture_image_from_camera():
    if 'camera_started' not in st.session_state:
        st.session_state.camera_started = False
    if st.button("Start Camera", key='start_camera'):
        st.session_state.camera_started = True
        
    if st.session_state.camera_started:
        cap = cv2.VideoCapture(0)
        logging.info('Camera started')
        FRAME_WINDOW = st.image([])

        if st.button("Capture Frame", key='capture_image'):
            ret, frame = cap.read()
            if ret:
                if file_exists(live_feed_image):
                    os.remove(live_feed_image)
                cv2.imwrite(live_feed_image, frame)
                st.success('Image Captured successfully')
                st.session_state.camera_started = False
                return True
            else:
                st.error('Failed to capture image')
                    
        while st.session_state.camera_started:
            ret, frame = cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                FRAME_WINDOW.image(frame, caption="Live Feed")
            else:
                st.warning("Failed to read from camera.")

        cap.release()
        logging.info('Camera started')
    else:
        st.warning("Click 'Start Camera' to proceed for authentication.")