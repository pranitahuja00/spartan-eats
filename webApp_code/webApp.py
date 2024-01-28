
import pymongo
from pymongo import MongoClient


# Connecting to my mongodb localhost service
uri = "mongodb+srv://cluster0.zrljcr1.mongodb.net/?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority"
mongoDBClient = MongoClient(uri,
                     tls=True,
                     tlsCertificateKeyFile='X509-cert-6349946631379972350.pem')

db = mongoDBClient['spartan_eats']
db_col = db['people']
data = {'ID':'28392',
        'Name':'Vishal Kumar',
        'meal_passes':5,
        'Role':'student'}

db_col.insert_one(data)