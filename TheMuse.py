##################################################
###     Recuperation jobs sur The Muse         ###
##################################################
import os 
import requests
from pprint import pprint


apikey = '5f9cc4bfebe2d4db2b369267fbfdc98fbc499ecbc0c35dbdc259066e93acf4c1'
url = 'https://www.themuse.com/api/public/jobs'
headers = {'api_key' : apikey}
params = {
    "page": "0",  # numero de la page
#    "location":"France" 
}

req = requests.get(url, headers=headers, params = params)

pprint(req.json())