###########################################################################################
###   Transformation des données du site de pôle emploi + insert dans une base No SQL   ###
###########################################################################################
from pprint import pprint
#import sys
from pymongo import MongoClient
import pandas as pd
import json
#from PE_extraction import dataPE

#---------------------------------------------------
# récupération des données de l'API
#---------------------------------------------------
with open("dataPE.json", "r") as file:
    # Charger le contenu du fichier JSON
    dataPE_content = file.read()
    # Charger le JSON en tant que liste d'objets
    dataPE_list = json.loads(dataPE_content)

#---------------------------------------------------
# création de la base NoSQL
#---------------------------------------------------

# Connexion à MongoDB
client = MongoClient(host="127.0.0.1", port = 27017)

#création de la DB
DB = client["DB_job"]
#Création et initialisation de la collection
c_PE = DB["PE"]
# RAZ de la collection
c_PE.drop()


#---------------------------------------------------
# alimentation de la base NoSQL
#---------------------------------------------------

data_collection = []
for job in dataPE_list:
    data_doc = {
    "accessibleTH": job.get("accessibleTH"),
    "alternance": job.get("alternance"),
    "appellationlibelle": job.get("appellationlibelle"),
    "codeNAF": job.get("codeNAF"),
    "competences": job.get("competences"),
    "contact": job.get("contact"),
    "dateActualisation": job.get("dateActualisation"),
    "dateCreation": job.get("dateCreation"),
    "deplacementCode": job.get("deplacementCode"),
    "deplacementLibelle": job.get("deplacementLibelle"),
    "description": job.get("description"),
    "dureeTravailLibelle": job.get("dureeTravailLibelle"),
    "dureeTravailLibelleConverti": job.get("dureeTravailLibelleConverti"),
    "entreprise": job.get("entreprise"),
    "experienceExige": job.get("experienceExige"),
    "experienceLibelle": job.get("experienceLibelle"),
    "formations": job.get("formations"),
    "id": job.get("id"),
    "intitule": job.get("intitule"),
    "lieuTravail": job.get("lieuTravail"),
    "natureContrat": job.get("natureContrat"),
    "qualificationCode": job.get("qualificationCode"),
    "qualificationLibelle": job.get("qualificationLibelle"),
    "romeCode": job.get("romeCode"),
    "romeLibelle": job.get("romeLibelle"),
    "salaire": job.get("salaire"),
    "secteurActivite": job.get("secteurActivite"),
    "secteurActiviteLibelle": job.get("secteurActiviteLibelle"),
    "typeContrat": job.get("typeContrat"),
    "typeContratLibelle": job.get("typeContratLibelle")
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
