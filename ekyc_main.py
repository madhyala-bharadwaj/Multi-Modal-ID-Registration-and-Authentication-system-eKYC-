import streamlit as st
import cv2
from db_operations import insert_records, fetch_records, check_duplicacy
from livefeed import capture_image_from_camera
from preprocess import read_image,extract_id_card
from face_verification import detect_and_extract_face
from face_verification import face_comparison
from ocr_engine import extract_text
from postprocess import aadhar_extract_information,pan_extract_information
from utils import read_yaml
from datetime import datetime
import logging
from dateutil import parser
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

st.set_page_config(layout="wide")

# Setting up Logging
logging_str = "[%(asctime)s: %(levelname)s: %(module)s]: %(message)s"
logging.basicConfig(filename='logs\ekyc_logs.log', level=logging.INFO, format=logging_str, filemode="a")

# Connect to Database
DATABASE_URL = "mysql+pymysql://root:@localhost/ekyc"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

# Configuration Settings
config_path = "config.yaml"
config = read_yaml(config_path)
locations = config['locations']
id_file = locations['ID_FILE']
live_feed_image = locations['LIVE_FEED_IMAGE']
face_from_feed = locations['FACE_FROM_FEED']
face_from_id = locations['FACE_FROM_ID']


st.markdown("""
    <style>
    .main {
        background-color: #1e1e1e;
        color: #ffffff;
        font-family: 'Arial', sans-serif;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 3rem;
        padding-right: 3rem;
    }
    .css-18e3th9 {
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 3rem;
        padding-right: 3rem;
    }
    h1 {
        color: #4B72FA;
    }
    h2, h3 {
        color: #DDDDDD;
    }
    .stButton>button {
        background-color: #4B72FA;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
    }
    .stButton>button:hover {
        background-color: #3959D0;
        color: white;
    }
    .stSidebar .stSelectbox {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .stTextInput input {
        color: #ffffff;
        background-color: #333333;
    }
    .stTextArea textarea {
        color: #ffffff;
        background-color: #333333;
    }
    .stSlider .stSliderBar {
        background-color: #4B72FA;
    }
    .stSlider .stSliderHandle {
        background-color: #4B72FA;
    }
    .css-1offfwp e1ewe7hr1 {
        color: #ffffff;
        background-color: #333333;
    }
    .css-1siy2j7 {
        color: #ffffff;
    }
    </style>
    """, unsafe_allow_html=True)


st.title("eKYC System")
st.markdown("## Efficient and Secure KYC Verification")

# Global Variables
id_details = {}
st.session_state.authenticated = False

def main():
    st.sidebar.title("Navigation")
    option = st.sidebar.selectbox("Choose an option", ["Home", "Authentication", "Verify Details", "Enrol Data", "Fetch Records"])
    # option = st.sidebar.radio('Navigation',["Home", "Authentication", "Verify Details", "Enrol Data", "Fetch Records"])

    if option == "Home":
        st.header("Welcome to the eKYC System")
        st.write("""
            This system provides a streamlined and secure way to verify customer identities using face recognition and OCR technologies.
        """)

    if option == "Authentication":
        if not st.session_state.authenticated:
            id_type = st.selectbox("Select ID Type", ["PAN Card","Aadhar"],index=0)
            st.title(f'Registration using {id_type}')
            model_name = st.radio("Select Face Comparison Model", ["deepface", "facerecognition"], index=0,horizontal=True,key='face_recognition_model')
            st.write("Upload ID Card and Capture Image for Face Authentication")
            uploaded_file = st.file_uploader("Upload an ID card image", type=["jpg", "jpeg", "png"])
            if uploaded_file is not None:
                logging.info('ID card uploaded')
                st.image(uploaded_file, caption="Uploaded ID Card", width=400)
                extracted_id_img = read_image(uploaded_file)
                logging.info('ID Image read successfully')
                try:
                    processed_id_img = extract_id_card(extracted_id_img)
                    logging.info('Extracted ID Card')
                except:
                    logging.error('Error in Extracting id image')
                    st.error('Error in Extracting id image')

                if capture_image_from_camera():
                    logging.info('Image Captured from camera')
                    st.image(live_feed_image, caption="Captured Image", width=400)
                    logging.info('Authentication started')
                    st.write('Authentication Started')

                    # Extracting Face from ID
                    try:
                        detect_and_extract_face(processed_id_img,file_name=face_from_id)
                        logging.info('Face extracted from ID')
                    except:
                        logging.error('Error in extracting face from ID.')
                        st.error('Error in extracting face from ID.')

                    # Extract Face from Face Image
                    try:
                        face_img = cv2.imread(live_feed_image)
                        try:
                            detect_and_extract_face(face_img,file_name=face_from_feed)
                            logging.info('Extracted face from camera image')
                        except:
                            logging.error('Error in extracting face from camera image')
                            st.error('Error in extracting face from camera image')
                    except:
                        logging.error('Error in reading face image')
                        st.error('Error in reading face image')
                    
                    # Authentication
                    if face_comparison(face_from_id, face_from_feed,model_name):
                        st.success("Face Authentication successful")
                        st.session_state.authenticated = True
                        logging.info('Face Authenticated')
                    else:
                        logging.error("Face Authentication failed")
                        st.error("Face Authentication failed")
                        st.session_state.authenticated = False
                    if st.session_state.authenticated:
                        extracted_text = extract_text(id_file)
                        logging.info('Extracted text:',extracted_text)
                        if id_type=='Aadhar':
                            id_details = aadhar_extract_information(extracted_text)
                        else:
                            id_details = pan_extract_information(extracted_text)
                        if id_details:
                            st.session_state.id_details = id_details
                            st.success('Details extracted from ID. Proceed for Verification.')
                        else:
                            st.error('Failed to extract details from ID')
        else:
            st.success('Already Authenticated')

    if option == "Verify Details":
        st.header("Details Verification")
        if st.session_state.get('id_details', {}):
            st.subheader("Edit the extracted details below if necessary")

            id_details = st.session_state.get('id_details', {})
            if id_details:
                id_info = {
                    "ID": st.text_input("ID", value=id_details.get('ID', '')),
                    "Name": st.text_input("Name", value=id_details.get('Name', '')),
                    "DOB": st.date_input("DOB", value=parser.parse(id_details.get('DOB', '')) if id_details.get('DOB') else datetime.now()),
                    "ID_type": st.text_input("ID_type", value=id_details.get('ID_type', ''))
                }
                if st.button("Confirm"):
                    if id_info['ID']=='':
                        logging.error('Empty ID')
                        st.error("Cannot submit. Please fill in the ID")
                    else:
                        id_info['Photo_embeddings'] = id_details.get('Photo_embeddings', '')
                        id_info['Registered_time'] = datetime.now()
                        st.session_state.id_info = id_info
                        st.session_state.info_confirmed = True
                        st.success("Information Verified")
                        logging.info('Information Verified')
            else:
                st.warning('Details not Fetched. Try uploading different ID image')
        else:
            st.warning("Authentication need to be successful to verify details")

    if option == 'Enrol Data':
        st.header('Insert Data')
        if st.session_state.get('id_info'):
            st.write(st.session_state.id_info)
            if st.button("Insert Data"):
                if check_duplicacy(st.session_state.id_info['ID']):
                    st.warning(f"User already exists with ID {st.session_state.id_info['ID']}")
                    st.dataframe(fetch_records('ID',st.session_state.id_info['ID'])[['ID','Name','DOB','ID_type','Registered_time']])
                    logging.info('User already exists')
                else: 
                    insert_records(st.session_state.id_info)
        else:
            st.warning("Verify and confirm the extracted details before inserting data")

    if option == "Fetch Records":
        st.subheader("Fetch Records")
        col = st.selectbox("Choose the column", ["ID", "Name","DOB","ID_type"])
        if col in ['ID','Name']:
            value = st.text_input(f"Enter {col} to fetch records")
        elif col=='DOB':
            value = st.date_input('Date of Birth')
        elif col=='ID_type':
            value = st.radio('Select ID Type:', ('PAN', 'Aadhar'))
        if st.button("Fetch"):
            records = fetch_records(col,value)
            if not records.empty and records.shape[0]>0:
                st.dataframe(records)
            else:
                st.warning("No records found")

if __name__ == "__main__":
    main()