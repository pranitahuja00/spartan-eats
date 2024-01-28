import streamlit as st
import pymongo
from pymongo import MongoClient

# Connecting to my mongodb localhost service
cert_string = st.secrets["DB_ROOT_CERT"]
cert_path = "mongo_cert.pem"
with open(cert_path, "w") as cert_file:
    cert_file.write(cert_string)
uri = "mongodb+srv://cluster0.zrljcr1.mongodb.net/?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority"
mongoDBClient = MongoClient(uri,
                     tls=True,
                     tlsCertificateKeyFile=cert_path)

db = mongoDBClient['spartan_eats']
db_col = db['people']


but = st.button("Click to update db")
if(but):
    data = {'ID':'99999',
        'Name':'test name',
        'meal_passes':100,
        'Role':'admin'}

    db_col.insert_one(data)