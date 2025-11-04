import json
import time
import random
from kafka import KafkaProducer
from datetime import datetime

# Configuration Kafka
producer = KafkaProducer(bootstrap_servers='localhost:9092',
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

# Fonction pour générer une vente simulée
def generate_vente():
    produits = ['Ordinateur', 'Smartphone', 'Tablette', 'Écouteurs', 'Clavier']
    pays = ['France', 'Allemagne', 'Italie', 'Espagne', 'UK']
    segments = ['Particulier', 'Entreprise', 'Éducation']
    
    return {
        'id_vente': random.randint(1000, 9999),
        'produit': random.choice(produits),
        'quantite': random.randint(1, 10),
        'prix_unitaire': round(random.uniform(50, 1000), 2),
        'pays': random.choice(pays),
        'segment': random.choice(segments),
        'timestamp': datetime.now().isoformat()
    }

# Boucle d'envoi
while True:
    vente = generate_vente()
    producer.send('ventes_stream', vente)
    print(f"Vente envoyée : {vente}")
    time.sleep(2)