import pandas as pd
import pymongo
from pymongo import MongoClient
from sklearn.preprocessing import LabelEncoder

leHall = LabelEncoder()
leDishes = LabelEncoder()
leStations = LabelEncoder()

menu = pd.read_excel("SH9 - Dining Halls Menu.xlsx")

leHall.fit(menu["Hall"])
leDishes.fit(menu["Dish"])
leStations.fit(menu["Station"])

hall_list = list(leHall.classes_)
dish_list = list(leDishes.classes_)
station_list = list(leStations.classes_)

menu["hall_id"]=leHall.transform(menu["Hall"])
menu["station_id"]=leStations.transform(menu["Station"])
menu["dish_id"]=leDishes.transform(menu["Dish"])

uri = "mongodb+srv://cluster0.zrljcr1.mongodb.net/?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority"
mongoDBClient = MongoClient(uri,
                     tls=True,
                     tlsCertificateKeyFile="X509-cert-6349946631379972350.pem")

db = mongoDBClient['spartan_eats']
stations = db["stations"]
dishes = db["dishes"]
halls = db["halls"]

#stations.insert_one({"name":menu['Station'][1]})

for i in station_list:
    station = {
        "station_id":station_list.index(i),
        "station_name":i,
        "hall_id":int(menu["hall_id"][menu["station_id"]==station_list.index(i)].iloc[0])
    }
    print(station)
    #stations.insert_one(station)

for i in dish_list:
    dish = {
        "dish_id":dish_list.index(i),
        "dish_name":i,
        "station_id": int(menu["station_id"][menu["dish_id"]==dish_list.index(i)].iloc[0]),
        "hall_id":int(menu["hall_id"][menu["dish_id"]==dish_list.index(i)].iloc[0]),
        "meal_cat": str(menu["Meal"][menu["dish_id"]==dish_list.index(i)].iloc[0])
    }
    print(dish)
    #dishes.insert_one(dish)

