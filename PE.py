##################################################
###     Webscraping du site de pôle emploi     ###
##################################################
import os 
import requests
from pprint import pprint
import sys
from pymongo import MongoClient
import pandas as pd
import json

ID_CLIENT= "PAR_datascientest_98cd282e8a1a1386298c211358d8af06dfa5ab10edb133a40c513453375fcabb"
KEY= "37a59304f2c51b9cf9009fa731771b578468964e70c10d4782e1a9ae852f7b24"

#récupération de la clé github ?
API_KEY = os.environ.get("API_PE_KEY")
print("***********", API_KEY, "*****************")

#############################################################
# Appel de l'API de génération du Token
#############################################################

# Paramètre du point d"accès (URL, entête et token)
url_token = "https://entreprise.pole-emploi.fr/connexion/oauth2/access_token?realm=%2Fpartenaire"
headers_token = { "Content-Type": "application/x-www-form-urlencoded"}
data_token = {
    "grant_type": "client_credentials"
   , "client_id": ID_CLIENT
   , "client_secret": KEY
   , "scope": "api_offresdemploiv2 o2dsoffre"
}
#récupération et gestion de la réponse 
r_token = requests.post(url_token, headers=headers_token, data=data_token)
if r_token.status_code == 200 :
    print("Récupération de la clé d'accès Pôle Emploi : OK")
    access_token_bearer = r_token.json()["access_token"]
else:
    sys.exit(f"Erreur lors de l'appel à l'API de génération du token de connection, code retour {r_token.status_code}")

#############################################################
# Appel de l'API de récupération des jobs Pôle Emploi
#############################################################

# Paramètre du point d"accès (URL, autorisation et paramètre)
seq_appel = 0
url_req = "https://api.pole-emploi.io/partenaire/offresdemploi/v2/offres/search?"
authorization = {"Authorization": f"Bearer {access_token_bearer}"}
params = {
    "range" : "0-149",
    "qualification": "0"  # Niveau de qualification demandé
    #"motsCles": "informatique",  # Recherche par mot clé
    #"commune": "67482",  # Exemple de codes INSEE de communes
}


#Fonctions du programme
def maj_param_appel():
    param_range = params["range"].split("-")
    param_range = [int(i) + 150 for i in param_range]
    params["range"] = str(param_range[0])+"-"+ str(param_range[1])
    

def appel_API():
    r_req = requests.get(url_req, params=params, headers=authorization)
    return r_req

#----------------------------------
#traitement principal
#----------------------------------

#récupération et transormation de la réponse en json
r_req = appel_API()
dataPE = r_req.json()["resultats"]

while (seq_appel == 0 or r_req.status_code == 206) and seq_appel < 19:
    maj_param_appel()
    r_req = appel_API()
    seq_appel += 1 
    dataPE = dataPE + r_req.json()["resultats"]

#gestion des codes retour
if r_req.status_code == 200:
    print("Récupération de la liste des jobs de Pôle Emploi : OK")
elif r_req.status_code == 206 and seq_appel == 19:
    print("Récupération partielle de la liste des jobs de Pôle Emploi : nombre de jobs dépassant les 3000 !")
else:
    print("/",seq_appel,"/")    
    print("/",r_req.status_code,"/")
    sys.exit(f"Erreur lors de l'appel à l'API de récupération des jobs, code retour {r_req.status_code}")
    

#écriture d'un fichier externe pour visualisation du json de réponse
"""with open("dataPE.json", "w") as fichier:
    json.dump(dataPE, fichier, indent=4)
with open("r_req.json", "w") as fichier:
    fichier.write(r_req.text)"""

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
#df3.to_csv('df3.csv', index=False)


cle_dataPE = []
#  on met toutes les clé dans la même liste
for i in dataPE:
    cle_dataPE.extend(list(i.keys()))

df = pd.DataFrame({"cle" : cle_dataPE})
# on supprime les duplicates keys
df2 = df["cle"].drop_duplicates().tolist()
pprint(df2) 










