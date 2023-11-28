import matplotlib.pyplot as plt
import json
# Les données JSON 
with open('ExemplePE.json', 'r') as file:
    data = json.load(file)


# Extraire les libellés de secteur d'activité et le nombre d'offres pour chaque secteur
secteurs = [offer["secteurActiviteLibelle"] for offer in data]
nombre_offres = [1 for _ in data]  # Chaque offre compte pour une

# Créer le graphique en barres
plt.bar(secteurs, nombre_offres, color='blue')
plt.xlabel('Secteur d\'activité')
plt.ylabel('Nombre d\'offres')
plt.title('Nombre d\'offres par secteur d\'activité')
plt.xticks(rotation=45, ha='right')  # Rotation des libellés pour une meilleure lisibilité
plt.tight_layout()

# Afficher le graphique
plt.show()
