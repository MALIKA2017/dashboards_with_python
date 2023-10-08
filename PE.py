# Webscraping du site de pôle emploi

import os 
import requests

ID_CLIENT= "PAR_datascientest_98cd282e8a1a1386298c211358d8af06dfa5ab10edb133a40c513453375fcabb"
KEY= "37a59304f2c51b9cf9009fa731771b578468964e70c10d4782e1a9ae852f7b24"
REALM= "Datascientest"

# URL de point d'accès
url = "https://entreprise.pole-emploi.fr/connexion/oauth2/access_token?realm=%2Fpartenaire"

# En-tête de la requête
headers = { "Content-Type": "application/x-www-form-urlencoded"}

# Corps de la requête
data = {
    "grant_type": "client_credentials"
   , "client_id": ID_CLIENT
   , "client_secret": KEY
   , "scope": "job"
}

# Effectuer la requête POST
response = requests.post(url, headers=headers, data=data)

#KEY = os.getenv("37a59304f2c51b9cf9009fa731771b578468964e70c10d4782e1a9ae852f7b24")

"""r = requests.get(
    url="https://api.pole-emploi.io/partenaire/offresdemploi/v2/offres/search?qualification=0&motsCles=informatique&commune=51069,76322,46083,12172,28117&origineOffre=2"

    )"""



#data = r.json()
print(response)
print(response.json())

