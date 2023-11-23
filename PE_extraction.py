##################################################
###     Webscraping du site de pôle emploi     ###
##################################################
import os 
import requests
import sys
import json


ID_CLIENT= "PAR_datascientest_98cd282e8a1a1386298c211358d8af06dfa5ab10edb133a40c513453375fcabb"
KEY= "37a59304f2c51b9cf9009fa731771b578468964e70c10d4782e1a9ae852f7b24"

#récupération de la clé github ?
API_KEY = os.environ.get('API_PE_KEY')
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
    "qualification": 0,  # Niveau de qualification demandé
    "typeContrat":"CDI",
    "tempsPlein" : "true", #"true"/"false"
    "origineOffre":1,    #"1 : Pole emploi ; 2 : Partenaires
    "departement":67
    #"motsCles": "informatique",  # Recherche par mot clé
    #"commune": "67482",  # Exemple de codes INSEE de communes

    #"distance" : 10 # rayon en km; 0 pour spécifier uniquement les offres de la ville
}


#Fonctions du programme
def maj_param_appel():
    param_range = params["range"].split("-")
    param_range = [int(i) + 150 for i in param_range]
    params["range"] = str(param_range[0])+"-"+ str(param_range[1])
    

def appel_API():
    r_req = requests.get(url_req, params=params, headers=authorization)
    return r_req

def gestion_rc(reponse, seq_appel, params):
    #gestion des codes retour
    if reponse.status_code == 200 :
        print("Récupération de la liste des jobs : OK")
    elif reponse.status_code == 206:
        if seq_appel == 20:
            print("Récupération partielle de la liste des jobs : plus de 3000 jobs !")
        else:
            return True
    elif reponse.status_code == 204 :
        if seq_appel == 1:
            print("Aucun résultat trouvé pour les critères de sélection !")
            return False
        else:
            print("Récupération de la liste des jobs : OK")
            return False
    elif reponse.status_code == 400 :
        print(f"Aucun résultat trouvé pour les paramètres suivantes : \n {params} - {reponse.json()['message']}")
        return False
    else:
        print(f"paramètre en d'appel : {params}")
        print(f"Séquence d'appel n°{seq_appel}")    
        sys.exit(f"Erreur lors de l'appel à l'API de récupération des jobs, code retour {reponse.status_code} - {reponse.json()['message']}")
    

def print_csv(type_écriture:str):
    # écriture en CSV pour contrôle soit en "w" (Write), soit en "a" (append)
    with open("dataPE.json", type_écriture) as fichier:
        json.dump(dataPE, fichier, indent=4)
    with open("r_req.json", type_écriture) as fichier:
        fichier.write(r_req.text)

#----------------------------------
#traitement principal
#----------------------------------

dataPE = []
#récupération des réponses des annonces Pôle emploi ainsi que des fournisseurs autres
for qualification in [0,9]:
    params.update({"qualification": qualification})
    for type_contrat in ["CDI", "CDD"]:
        params.update({"typeContrat": type_contrat})
        for departement in [f"{i:02d}" for i in range(1,96)]:
            params.update({"departement": departement})
            for origine_offre in [1,2]:
                params.update({"range" : "0-149", "origineOffre": origine_offre})
                print("len(dataPE) 0 ",len(dataPE))
                print(params)
                seq_appel = 1 
                r_req = appel_API()
                if gestion_rc(r_req, seq_appel, params):
                    for offre in r_req.json()["resultats"]:
                        dataPE.append(offre)
                # -- on boucle si on n'a pas récupéré toutes les réponses lors du 1er appel  -- limitation technique fixée à 19 séquence d'appel par l'API
                while r_req.status_code == 206 and seq_appel < 20:
                    seq_appel += 1 
                    maj_param_appel()
                    r_req = appel_API()
                    if gestion_rc(r_req, seq_appel, params):
                        for offre in r_req.json()["resultats"]:
                            dataPE.append(offre)

#écriture d'un fichier externe pour visualisation du json de réponse
print("len(dataPE) 5 ",len(dataPE))
print_csv("w")



