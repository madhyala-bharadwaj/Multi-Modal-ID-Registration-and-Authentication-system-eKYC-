import os
import logging
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Setting up logging
logging_str = "[%(asctime)s: %(levelname)s: %(module)s]: %(message)s"
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(filename=os.path.join(log_dir, "ekyc_logs.log"), level=logging.INFO, format=logging_str, filemode="a")

# Connecting to the database
DATABASE_URL = "mysql+pymysql://root:@localhost/ekyc"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

def insert_records(records):
    try:
        session = Session()
        session.execute(
            text('INSERT INTO users (ID, Name, DOB, ID_type, Registered_time, Photo_embeddings) VALUES (:ID, :Name, :DOB, :ID_type, :Registered_time, :Photo_embeddings);'),
            {
                'ID': records['ID'],
                'Name': records['Name'],
                'DOB': records['DOB'],
                'ID_type': records['ID_type'],
                'Registered_time': records['Registered_time'],
                'Photo_embeddings': records['Photo_embeddings']
            }
        )
        session.commit()
        logging.info("Data Inserted successfully")
        st.success('Data Inserted Successfully')
    except Exception as e:
        st.error('Failed to Insert Data')
        logging.error(f"Error in insert_records: {e}")
        session.rollback()
    finally:
        session.close()

def fetch_records(col,value):
    try:
        session = Session()
        result = session.execute(text(f'SELECT * FROM users WHERE {col} = :value'), {'value': value})
        df = pd.DataFrame(result.fetchall(), columns=result.keys())[['ID','Name','DOB','ID_type','Registered_time']]
        session.close()
        return df
    except Exception as e:
        logging.error(f"Error in fetch_records: {e}")
        return None

def check_duplicacy(id):
    df = fetch_records('ID',id)
    return not df.empty