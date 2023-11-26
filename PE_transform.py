###########################################################################################
###   Transformation des données du site de pôle emploi + insert dans une base No SQL   ###
###########################################################################################
from pprint import pprint
#import sys
from pymongo import MongoClient
import pandas as pd
import numpy as np
import json
import re
#from PE_extraction import dataPE
import time


# on supprime la limite de l'affichage de l'ouput car on a beaucoup de colonne !
pd.set_option('display.max_rows', None)
# Enregistrez le temps de début
debut = time.time()

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
    "competences_nb" : len(job.get("competences", "")),
    #competences : mise à plat Cf ci-dessous
    "dateActualisation": job.get("dateActualisation", ""),
    "dateCreation": job.get("dateCreation", ""),
    "deplacementCode": job.get("deplacementCode", 1),           #intialisation à 1 = jamais de déplacement
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
    #"formations": job.get("formations", ""),                   #faible taux de complétion !
    "id": job.get("id", ""),
    "intitule": job.get("intitule", ""),
    "langues_nb" : len(job.get("langues", "")),
    #langues : mise à plat cf ci-dessous
    "lieuTravail_libelle": job.get("lieuTravail").get("libelle", ""),
    "lieuTravail_latitude": job.get("lieuTravail").get("latitude", ""),
    "lieuTravail_longitude": job.get("lieuTravail").get("longitude", ""),
    "lieuTravail_codepostal": job.get("lieuTravail").get("codepostal", ""),
    "lieuTravail_commune": job.get("lieuTravail").get("commune", ""),
    "natureContrat": job.get("natureContrat", ""),
    "origineOffre": job.get("origineOffre").get("origine", ""),
    "outilsBureautiques": job.get("outilsBureautiques", ""),    
    "permis_nb" : len(job.get("permis", "")),
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
                dict1= {f"competences{i+1:02d}_code" : f'{comp.get("code", "")}'}
                dict2 = {f"competences{i+1:02d}_libelle" : f'{comp.get("libelle", "")}'}
                dict3 = {f"competences{i+1:02d}_exigence" : f'{comp.get("exigence", "")}'}
                data_doc.update(dict1)
                data_doc.update(dict2)
                data_doc.update(dict3)


    if job.get("qualitesProfessionnelles") != None:
        for i, qualite in enumerate(job.get("qualitesProfessionnelles")):
                dict1= {f"qualitesProfessionnelles{i+1}_libelle" : f"{comp.get('libelle', '')}"}
                dict2 = {f"qualitesProfessionnelles{i+1}_description" : f"{comp.get('description', '')}"}
                data_doc.update(dict1)
                data_doc.update(dict2)

    data_aplat.append(data_doc)

df = pd.DataFrame(data_aplat)
df= df[sorted(df.columns)]
#df.to_csv("df.csv", index=False)

#---------------------------------------------------
# Transformation des données
#---------------------------------------------------
#print(df.head())

#transformation des Nan en "" => il n'existe que sur les 3 rubriques qu'on a aplanit au dessus
df = df.replace(np.nan, "")
#print(df.isnull().sum(axis = 0) )

# Suppression des doublons
df = df.drop_duplicates()
#print(df.duplicated().sum())
print(f"temps d'exécution {round((time.time()-debut)/60 ,2)} minutes")
#remplissage "accessibleTH" par son mode (false)
df["accessibleTH"] = df["accessibleTH"].replace("", df["accessibleTH"].mode()[0])
print(f"temps d'exécution {round((time.time()-debut)/60 ,2)} minutes")
#extraction de la durée horaire du libellé et transformation au format numérique 38H30 ==> 38.5
df["dureeTravailLibelle"] = df["dureeTravailLibelle"].apply(lambda x : x[:2]+"."+ (str(round(int(x.replace(" ", "")[3:5])/60*100 ,2)) if x.replace(" ", "")[3:4].isnumeric() else "00"))
print(f"temps d'exécution {round((time.time()-debut)/60 ,2)} minutes")
#extraction de la durée d'expérience souhaitée en années en fonction du formatage présent
for x, ligne in enumerate(df["experienceLibelle"]):
    #si la ligne contient " an"/" ans" et qu'il existe un nombre dans le libellé
    if  (" an" in ligne or  " ans" in ligne)  and re.search(r"\d+", ligne):
        df.loc[x, "experienceLibelle"] = re.search(r"\d+", ligne).group()
    #si la ligne contient "mois" et qu'il existe un nombre dans le libellé
    elif " mois" in ligne and re.search(r"\d+", ligne):
        df.loc[x, "experienceLibelle"]  = round(int(re.search(r"\d+", ligne).group())/12, 2)
    #Sinon, si le libellé est simplement formaté avec les 2 mots suivants, on fixera arbitrairement l'expérience requise à 3ans.
    elif "Expérience souhaitée" in ligne or "Expérience exigée" in ligne :
        df.loc[x, "experienceLibelle"]  = 3
    #Sinon, on sera dans le cas "Débutant accepté"
    else:
        df.loc[x, "experienceLibelle"]  = 0
print(f"temps d'exécution {round((time.time()-debut)/60 ,2)} minutes")       
#extraction du numéro de département et de la ville de la zone lieuTravail_libellé
#for ligne in df["lieuTravail_libelle"]
df["lieuTravail_libelle_num_dep"] = df["lieuTravail_libelle"].str.split("-", expand=True)[0]
df["lieuTravail_libelle_nom_ville"] = df["lieuTravail_libelle"].str.split("-", expand=True)[1]
print(f"temps d'exécution {round((time.time()-debut)/60 ,2)} minutes")
#extraction du salaire minimum et maximum

#df[["salaire_libelle_min", "salaire_libelle_max"]] = df["salaire_libelle"].str.split(" ", expand=True)

print("1--------------------------------------------------------")
print(df["experienceLibelle"].head(30))
print("2--------------------------------------------------------")
print(df["lieuTravail_libelle_num_dep"].head(30))
print("3--------------------------------------------------------")
print(df["lieuTravail_libelle_nom_ville"].head(30))

#df.to_csv("df.csv", index=False)
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





print(f"temps d'exécution {round((time.time()-debut)/60 ,2)} minutes")