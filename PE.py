# Webscraping du site de pôle emploi

import os 
import requests

KEY = "37a59304f2c51b9cf9009fa731771b578468964e70c10d4782e1a9ae852f7b24"
#KEY = os.getenv("37a59304f2c51b9cf9009fa731771b578468964e70c10d4782e1a9ae852f7b24")
p = requests.post("https://entreprise.pole-emploi.fr/connexion/oauth2/{}".format(KEY))
r = requests.get(
    url="https://api.pole-emploi.io/partenaire/offresdemploi/v2/offres/search?qualification=0&motsCles=informatique&commune=51069,76322,46083,12172,28117&origineOffre=2"

    )

data = r.json()

print(data)




