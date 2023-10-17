from bs4 import BeautifulSoup
import requests
import pandas as pd
from pprint import pprint

app_key = "d16d75c7"
app_id ="829a6fd7e4f2031025c36a92918ed1c1"


#emplois par page
job_ads=[]
for i in range (1,2):
  url1= f"https://api.adzuna.com/v1/api/jobs/fr/search/{i}?app_id=d16d75c7&app_key=829a6fd7e4f2031025c36a92918ed1c1"
  reponse1 = requests.get (url1)
rep = reponse1.json()["results"]
pprint(reponse1.json()["results"])

cles = []
for i in rep:
    cles.extend(i.keys())  # Utilisez extend() pour ajouter les clés à la liste au lieu de append()

# Créez un DataFrame à partir de la liste de clés
df = pd.DataFrame({'Cle': cles})

# Supprimez les doublons des clés
cles_sans_doublons = df['Cle'].drop_duplicates().tolist()

# Affichez les clés sans doublons
pprint(cles_sans_doublons)
