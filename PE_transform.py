###########################################################################################
###   Transformation des données du site de pôle emploi + insert dans une base No SQL   ###
###########################################################################################
from pprint import pprint
#import sys
from pymongo import MongoClient
import pandas as pd
#import json
from PE_extraction import dataPE


#---------------------------------------------------
# gestion des données issues de l"API
#---------------------------------------------------

# Connexion à MongoDB
client = MongoClient(host="127.0.0.1", port = 27017)

#création de la DB
DB = client["DB_job"]
#Création et initialisation de la collection
c_PE = DB["PE"]
c_PE.drop()


#alimentation de la collection c_PE de la DB
data_collection = []
for doc in dataPE:
    data_doc = {
    "accessibleTH": doc.get("accessibleTH"),
    "alternance": doc.get("alternance"),
    "appellationlibelle": doc.get("appellationlibelle"),
    "codeNAF": doc.get("codeNAF"),
    "competences": doc.get("competences"),
    "contact": doc.get("contact"),
    "dateActualisation": doc.get("dateActualisation"),
    "dateCreation": doc.get("dateCreation"),
    "deplacementCode": doc.get("deplacementCode"),
    "deplacementLibelle": doc.get("deplacementLibelle"),
    "description": doc.get("description"),
    "dureeTravailLibelle": doc.get("dureeTravailLibelle"),
    "dureeTravailLibelleConverti": doc.get("dureeTravailLibelleConverti"),
    "entreprise": doc.get("entreprise"),
    "experienceExige": doc.get("experienceExige"),
    "experienceLibelle": doc.get("experienceLibelle"),
    "formations": doc.get("formations"),
    "id": doc.get("id"),
    "intitule": doc.get("intitule"),
    "lieuTravail": doc.get("lieuTravail"),
    "natureContrat": doc.get("natureContrat"),
    "qualificationCode": doc.get("qualificationCode"),
    "qualificationLibelle": doc.get("qualificationLibelle"),
    "romeCode": doc.get("romeCode"),
    "romeLibelle": doc.get("romeLibelle"),
    "salaire": doc.get("salaire"),
    "secteurActivite": doc.get("secteurActivite"),
    "secteurActiviteLibelle": doc.get("secteurActiviteLibelle"),
    "typeContrat": doc.get("typeContrat"),
    "typeContratLibelle": doc.get("typeContratLibelle")
    }
    data_collection.append(data_doc)      

c_PE.insert_many(data_collection)
pprint(c_PE.count_documents({}))

df3 = pd.DataFrame(list(c_PE.find()))["id"].drop_duplicates()
print("réel :", df3.value_counts().sum())
#print dans un fichier
df3.to_csv('df3.csv', index=False)


cle_dataPE = []
#  on met toutes les clé dans la même liste
for i in dataPE:
    cle_dataPE.extend(list(i.keys()))

df = pd.DataFrame({"cle" : cle_dataPE})
# on supprime les duplicates keys
df2 = df["cle"].drop_duplicates().tolist()
pprint(df2) 










