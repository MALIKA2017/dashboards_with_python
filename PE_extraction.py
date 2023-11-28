##################################################
###     Webscraping du site de pôle emploi     ###
##################################################
import os 
import requests
import sys
import json
import time

# Enregistrez le temps de début
debut = time.time()

#############################################################
# Appel de l'API de génération du Token
#############################################################

#récupération de la clé github ?
API_KEY = os.environ.get('api_key')
API_ID_CLIENT = os.environ.get('api_id_client')
print("***********", API_KEY, "*****************")
print("***********", API_ID_CLIENT, "*****************")

# Paramètre du point d"accès (URL, entête et token)
url_token = "https://entreprise.pole-emploi.fr/connexion/oauth2/access_token?realm=%2Fpartenaire"
headers_token = { "Content-Type": "application/x-www-form-urlencoded"}
data_token = {
    "grant_type": "client_credentials"
   , "client_id": API_ID_CLIENT
   , "client_secret": API_KEY 
   , "scope": "api_offresdemploiv2 o2dsoffre"
}

def appel_API_token():
    r_token = requests.post(url_token, headers=headers_token, data=data_token)
    return r_token

def gestion_rc_token(reponse, params):
    #récupération et gestion de la réponse 
    if reponse.status_code == 200 :
        print("Récupération de la clé d'accès Pôle Emploi : OK")
        access_token_bearer = reponse.json()["access_token"]
        return access_token_bearer
    else:
        print(f"paramètres d'appel: {params} ") 
        sys.exit(f"Erreur lors de l'appel à l'API de génération du token de connection, code retour {reponse.status_code}, erreur : {reponse.json().get('error')}")

#############################################################
# Appel de l'API de récupération des jobs Pôle Emploi
#############################################################
seq_appel = 1

# Paramètre du point d"accès (URL et paramètres ; l'autorisation va être construite suite à un premier appel à l'API de génération du token)
url_offre = "https://api.pole-emploi.io/partenaire/offresdemploi/v2/offres/search?"
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

def appel_API_offres(access_token):
    authorisation = {"Authorization": f"Bearer {access_token}"}
    r_req = requests.get(url_offre, params=params, headers=authorisation)
    return r_req

def maj_param_appel(variable, valeur):
    #mise à jour spécique du range qui commence par un paramétrage "0-149" et qui augmente selon à pas de 150. 
    #le pas est paramétré selon le numéro de séquence d'appel qui commence à 1 et qui sera contenu dans la variable "valeur"
    if variable == "range":
        range_1 = "0-149"
        param_range = [int(i) + 150 * (valeur - 1) for i in range_1.split("-")]
        valeur = str(param_range[0])+"-"+ str(param_range[1])
    
    #Dans tous les cas, on va mettre à jour le paramétrage avec la valeur d'entrée ou calculée dans cette fonction
    params.update({variable: valeur})
    

def gestion_rc_offres(reponse, seq_appel, params):
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
        print(f"reponse {reponse}")    
        sys.exit(f"Erreur lors de l'appel à l'API de récupération des jobs, code retour {reponse.status_code} - {reponse.json()['message']}")
    

def print_csv(type_écriture:str):
    # écriture en CSV pour contrôle soit en "w" (Write), soit en "a" (append)
    with open("dataPE.json", type_écriture) as fichier:
        json.dump(dataPE, fichier, indent=4)
    with open("r_req.json", type_écriture) as fichier:
        fichier.write(r_req.text)

###############################################################################
# Appel de l'API de récupération des code Activité de Pôle Emploi (code Naf)  #
###############################################################################
url_naf ="https://api.pole-emploi.io/partenaire/stats-informations-territoire/v1/referentiel/activites/{code_type_activite}"

def appel_API_naf(access_token,code_type_activite):
    authorisation = {"Authorization": f"Bearer {access_token}"}
    r_req = requests.get(f"{url_naf}{}", params=params, headers=authorisation)
    return r_req
#----------------------------------
#traitement principal
#----------------------------------

dataPE = []
access_token = ""
#cinématique : étant donné que l'API nous limite à 3000 emplois par appel, nous allons démultiplier les appels en jouant sur les paramètres d'appel
#afin de récolte un panel de job le plus large possible.

#récupération des annonces pour chacun des départements français de métropole
for departement in [f"{i:02d}" for i in range(1,96)]:
    maj_param_appel("departement", departement)

    #(ré)initialisation du token d'accès tous les 10 départements afin de ne pas se faire jeter par l'API.
    if departement in [f"{i:02d}" for i in range(1,96,10)]:
        rep = appel_API_token()
        access_token = gestion_rc_token(rep, params)

    #récupération des annonces pour en fonction de la qualification du poste : non cadre (0) ou cadre (9)
    for qualification in [0,9]:
        maj_param_appel("qualification", qualification)

        #récupération des annonces pour en fonction du type de contrat
        for type_contrat in ["CDI", "CDD"]:
            maj_param_appel("typeContrat", type_contrat)

            #récupération des annonces Pôle emploi (1) ainsi que des fournisseurs autres (2) et on réinitialise le range à "0-149"
            for origine_offre in [1,2]:
                seq_appel = 1
                maj_param_appel("origineOffre", origine_offre)
                maj_param_appel("range", seq_appel)
                #récupération des offres 
                r_req = appel_API_offres(access_token)
                if gestion_rc_offres(r_req, seq_appel, params):
                    for offre in r_req.json()["resultats"]:
                        dataPE.append(offre)

                # -- on boucle si on n'a pas récupéré toutes les réponses lors du 1er appel  -- limitation technique fixée 3000 enreg soit à 19 séquences d'appel par l'API
                while r_req.status_code == 206 and seq_appel < 20:
                    seq_appel += 1 
                    maj_param_appel("range", seq_appel)
                    r_req = appel_API_offres(access_token)
                    if gestion_rc_offres(r_req, seq_appel, params):
                        for offre in r_req.json()["resultats"]:
                            dataPE.append(offre)
                    
#écriture d'un fichier externe pour visualisation du json de réponse
print("len(dataPE) 5 ",len(dataPE))
print_csv("w")


print(f"temps d'exécution {round((time.time()-debut)/60 ,2)} minutes")
