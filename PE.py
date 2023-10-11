##################################################
###     Webscraping du site de pôle emploi     ###
##################################################
import os 
import requests
from pprint import pprint

ID_CLIENT= "PAR_datascientest_98cd282e8a1a1386298c211358d8af06dfa5ab10edb133a40c513453375fcabb"
KEY= "37a59304f2c51b9cf9009fa731771b578468964e70c10d4782e1a9ae852f7b24"
REALM= "Datascientest"
API_KEY = os.environ.get("API_KEY")

print(f"API_KEY : {API_KEY}")
# URL de point d'accès
url_token = "https://entreprise.pole-emploi.fr/connexion/oauth2/access_token?realm=%2Fpartenaire"
# En-tête de la requête du point d'accès
headers_token = { "Content-Type": "application/x-www-form-urlencoded"}
# Corps de la requête du point d'accès
data_token = {
    "grant_type": "client_credentials"
   , "client_id": ID_CLIENT
   , "client_secret": KEY
   , "scope": "api_offresdemploiv2 o2dsoffre"
}
# Effectuer la requête POST
r_token = requests.post(url_token, headers=headers_token, data=data_token)
#récupération de la réponse et transformation en Json
print(r_token)
rep_token = r_token.json()
pprint(rep_token)

access_token_bearer = rep_token["access_token"]
# URL de la requête
url_req = "https://api.pole-emploi.io/partenaire/offresdemploi/v2/offres/search?"
#Autorisation de rêquete
authorization = {"Authorization": f"Bearer {access_token_bearer}"}
# Paramètres de la requête
params = {
    "qualification": "0",  # Niveau de qualification demandé
    "motsCles": "informatique",  # Recherche par mot clé
    "commune": "67482",  # Exemple de codes INSEE de communes
}
# Effectuer la requête GET
r_req = requests.get(url_req, params=params, headers=authorization)


data = r_req.json()
print(r_req )
#pprint(r_req.json())


