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

# Charger le contenu du JSON en tant que liste d'objets
with open("dataPE.json", "r") as file:
    dataPE_list = json.loads(file.read())


#---------------------------------------------------
# Création du Dataframe de données
#---------------------------------------------------
comp = []

data_aplat = []
for job in dataPE_list:
    #print(job.get("id"), job.get("permis")) if job.get("permis") != None else ""

    data_doc = {
    "accessibleTH": job.get("accessibleTH", ""),
    "alternance": job.get("alternance", ""),
    "appellationlibelle": job.get("appellationlibelle", ""),
    "codeNAF": job.get("codeNAF", ""),
    "competences_nb" : len(job.get("competences", "0")),
    #competences : mise à plat Cf ci-dessous
    "contact": job.get("contact", ""),
    "dateActualisation": job.get("dateActualisation", ""),
    "dateCreation": job.get("dateCreation", ""),
    "deplacementCode": job.get("deplacementCode", ""),
    "deplacementLibelle": job.get("deplacementLibelle", ""),
    "description": job.get("description", ""),
    "dureeTravailLibelle": job.get("dureeTravailLibelle", ""),
    "dureeTravailLibelleConverti": job.get("dureeTravailLibelleConverti", ""),
    "entreprise_nom": job.get("entreprise").get("nom", ""),
    "entreprise_description": job.get("entreprise").get("description", ""),
    "entreprise_logo": job.get("entreprise").get("logo", ""),
    "entreprise_url": job.get("entreprise").get("url", ""),
    "entreprise_adaptee": job.get("entreprise").get("entrepriseAdaptee", ""),
    "experienceExige": job.get("experienceExige", ""),
    "experienceLibelle": job.get("experienceLibelle", ""),
    "formations": job.get("formations", ""),
    "id": job.get("id", ""),
    "intitule": job.get("intitule", ""),
    "langues_nb" : len(job.get("langues", "0")),
    #langues : mise à plat cf ci-dessous
    "lieuTravail_libelle": job.get("lieuTravail").get("libelle", ""),
    "lieuTravail_latitude": job.get("lieuTravail").get("latitude", ""),
    "lieuTravail_longitude": job.get("lieuTravail").get("longitude", ""),
    "lieuTravail_codepostal": job.get("lieuTravail").get("codepostal", ""),
    "lieuTravail_commune": job.get("lieuTravail").get("commune", ""),
    "natureContrat": job.get("natureContrat", ""),
    "origineOffre": job.get("origineOffre").get("origine", ""),
    "outilsBureautiques": job.get("outilsBureautiques", ""),    
    "permis_nb" : len(job.get("permis", "0")),
    #permis : mise à plat Cf ci-dessous
    "qualificationCode": job.get("qualificationCode", ""),
    "qualificationLibelle": job.get("qualificationLibelle", ""),
    "romeCode": job.get("romeCode", ""),
    "romeLibelle": job.get("romeLibelle", ""),
    "salaireMin": job.get("salaireMin",""),
    "salaire_libelle": job.get("salaire").get("libelle", ""),
    "salaire_commentaire": job.get("salaire").get("commentaire", ""),
    "salaire_complement1": job.get("salaire").get("complement1", ""),
    "salaire_complement2": job.get("salaire").get("complement2", ""),
    "secteurActivite": job.get("secteurActivite", ""),
    "secteurActiviteLibelle": job.get("secteurActiviteLibelle", ""),
    "typeContrat": job.get("typeContrat", ""),
    "typeContratLibelle": job.get("typeContratLibelle", "")
    }

    if job.get("langues") != None :
        for i, langue in enumerate(job.get("langues")):
                dict1= {f"langues{i+1}_libelle" : f"{comp.get('libelle', '')}"}
                dict2 = {f"langues{i+1}_exigence" : f"{comp.get('exigence', '')}"}
                data_doc.update(dict1)
                data_doc.update(dict2)

    if job.get("permis") != None :
        for i, type_permis in enumerate(job.get("permis")):
                dict1= {f"permis{i+1}_libelle" : f"{comp.get('libelle', '')}"}
                dict2 = {f"permis{i+1}_exigence" : f"{comp.get('exigence', '')}"}
                data_doc.update(dict1)
                data_doc.update(dict2)


    if job.get("competences") != None:
        for i, comp in enumerate(job.get("competences")):
                dict1= {f"competences_code{i+1}" : f"{comp.get('code', '')}"}
                dict2 = {f"competences_libelle{i+1}" : f"{comp.get('libelle', '')}"}
                dict3 = {f"competences_exigence{i+1}" : f"{comp.get('exigence', '')}"}
                data_doc.update(dict1)
                data_doc.update(dict2)
                data_doc.update(dict3)


    if job.get("qualitesProfessionnelles") != None:
        for i, qualite in enumerate(job.get("qualitesProfessionnelles")):
                dict1= {f"qualitesProfessionnelles{i+1}" : f"{comp.get('libelle', '')}"}
                dict2 = {f"qualitesProfessionnelles-{i+1}" : f"{comp.get('description', '')}"}
                data_doc.update(dict1)
                data_doc.update(dict2)

    data_aplat.append(data_doc)

df = pd.DataFrame(data_aplat)
df.columns = sorted(df.columns)
df.to_csv("df.csv", index=False)
#---------------------------------------------------
# Transformation des données
#---------------------------------------------------

#transformation des Nan en 
#print(df.columns[df.isna().any()][60:])





"""
from statistics import median,mean
import numpy as np
comp.sort(reverse=True)   
print(np.median(comp))
print(np.mean(comp))
print(np.percentile(comp, 96))
print(np.percentile(comp, 97))
print(np.percentile(comp, 98))
print(np.percentile(comp, 99))"""


"""print(type(data_collection))
print(data_collection[11])
print(data_collection[12])
print(data_collection[13])"""


"""#---------------------------------------------------
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

c_PE.insert_many(data_collection)
pprint(c_PE.count_documents({}))

df3 = pd.DataFrame(list(c_PE.find()))["id"].drop_duplicates()
print("réel :", df3.value_counts().sum())
#print dans un fichier
df3.to_csv('df3.csv', index=False)


cle_dataPE = []
#  on met toutes les clé dans la même liste
for i in dataPE_list:
    cle_dataPE.extend(list(i.keys()))

df = pd.DataFrame({"cle" : cle_dataPE})
# on supprime les duplicates keys
df2 = df["cle"].drop_duplicates().tolist()
pprint(df2) 
"""