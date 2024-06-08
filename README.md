# eKYC System

![Screenshot (252)](https://github.com/madhyala-bharadwaj/Multi-Modal-ID-Registration-and-Authentication-system-eKYC-/assets/142684967/6b2fa37a-5cb9-4466-b7c5-11c2c467b674)

This project is an Electronic Know Your Customer (eKYC) system that uses facial recognition and OCR (Optical Character Recognition) to verify user identity. The system is built with Streamlit for the interactive web interface, OpenCV for image processing, SQLAlchemy for database operations, and various libraries for face recognition and OCR.

## Files and Directories

### `ekyc_main.py`
The main file for the eKYC application, utilizing Streamlit to create an interactive web interface.

#### Key Sections:
- **Imports**: Necessary libraries and modules are imported, including Streamlit, OpenCV, SQLAlchemy, and custom modules.
- **Logging Setup**: Logging is configured for capturing application logs.
- **Database Connection**: Establishes a connection to a MySQL database using SQLAlchemy.
- **Configuration Settings**: Loads application settings from a YAML configuration file.
- **Streamlit Interface Customization**: Applies custom CSS to style the Streamlit interface.
- **Main Application Logic**: Manages the application flow using a sidebar with different options (Home, Authentication, Verify Details, Enrol Data, Fetch Records).

#### Core Functions:
- **Home**: Displays an introduction to the eKYC system.
- **Authentication**: Handles the upload of an ID card image, captures a live image from the camera, and performs face authentication.
- **Verify Details**: Allows users to verify and edit the extracted details from the ID card.
- **Enrol Data**: Inserts the verified details into the database.
- **Fetch Records**: Fetches records from the database based on user input.

### `db_operations.py`
Functions for database operations such as inserting and fetching records.

#### Key Functions:
- **insert_records**: Inserts user data into the database.
- **fetch_records**: Retrieves records from the database based on specified column and value.
- **check_duplicacy**: Checks if a user already exists in the database by their ID.

### `face_verification.py`
Handles face detection, extraction, and comparison using different models.

#### Key Functions:
- **detect_and_extract_face**: Detects faces in an image and extracts the largest face detected.
- **face_recog_face_comparison**: Compares two faces using the `face_recognition` library.
- **deepface_face_comparison**: Compares two faces using the `DeepFace` library.
- **face_comparison**: Selects the appropriate model for face comparison based on input.
- **get_face_embeddings**: Generates face embeddings using the `DeepFace` library for further processing.

### `livefeed.py`
Captures images from a live camera feed using OpenCV.

#### Key Functions:
- **capture_image_from_camera**: Starts the camera, displays the live feed in the Streamlit interface, and captures an image when a button is clicked.

### `ocr_engine.py`
Performs OCR on ID card images to extract text information.

#### Key Functions:
- **extract_text**: Uses the `easyocr` library to extract text from an image.

### `postprocess.py`
Processes the extracted text from the OCR engine to retrieve specific details based on the type of ID card (PAN or Aadhar).

#### Key Functions:
- **pan_extract_information**: Extracts details like ID, Name, and DOB from the text of a PAN card.
- **aadhar_extract_information**: Extracts details like ID, Name, and DOB from the text of an Aadhar card.

### `preprocess.py`
Handles preprocessing of images such as reading and extracting the ID card area from the image.

#### Key Functions:
- **read_image**: Reads an image from a file-like object.
- **extract_id_card**: Extracts the ID card area from an image using contour detection.
- **save_image**: Saves an image to a specified file path.

### `utils.py`
Provides utility functions that are used across various other modules.

#### Key Functions:
- **read_yaml**: Reads a YAML configuration file.
- **file_exists**: Checks if a file exists at a given path.

### `config.yaml`
Configuration file containing various settings and paths used throughout the application.

#### Key Sections:
- **locations**: Defines paths for saving images and other resources.
- **database**: Contains database connection settings.
- **logging**: Specifies logging configuration.

## Summary
This eKYC project is a comprehensive system designed for efficient and secure customer identity verification. The main application leverages Streamlit for the interface, OpenCV for image processing, various face recognition libraries for authentication, and easyOCR for text extraction. It also integrates with a MySQL database for storing and retrieving user data. Each file in the project serves a specific purpose, working together to provide a seamless user experience.
