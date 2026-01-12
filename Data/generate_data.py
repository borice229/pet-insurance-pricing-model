import numpy as np
import pandas as pd


np.random.seed(42)

N = 10000

races = {
    "Chihuahua": 3,
    "Bouledogue français": 12,
    "Labrador": 30,
    "Golden Retriever": 32,
    "Berger Allemand": 35,
    "Caniche": 10,
    "Yorkshire": 4,
    "Beagle": 15,
    "Rottweiler": 45,
    "Husky": 28,
    "Teckel": 8,
    "Croisé": 20
}

regions = {
    "Île-de-France": 1.3,
    "Auvergne-Rhône-Alpes": 1.15,
    "Occitanie": 1.1,
    "Nouvelle-Aquitaine": 1.05,
    "Hauts-de-France": 1.1,
    "Autres": 1.0
}

data = []

for _ in range(N):
    race = np.random.choice(list(races.keys()))
    age = np.round(np.random.uniform(0.5, 15), 1)
    sexe = np.random.choice(["M", "F"])
    sterilise = np.random.choice([0, 1], p=[0.4, 0.6])
    region = np.random.choice(list(regions.keys()))

    poids_moyen = races[race]
    poids = np.clip(np.random.normal(poids_moyen, poids_moyen * 0.15), 2, 70)

    # Lambda fréquence
    lambda_base = 1.2
    if age > 7:
        lambda_base += 1.0
    elif age < 2:
        lambda_base += 0.3

    if sterilise == 1:
        lambda_base -= 0.2

    freq_soins = np.random.poisson(max(lambda_base, 0.5))

    # Coût moyen
    base_cost = 120 + poids * 8
    base_cost *= regions[region]

    if age > 7:
        base_cost *= 1.3

    cout_moyen = np.random.gamma(shape=2, scale=base_cost / 2)

    data.append([
        race, age, sexe, sterilise, round(poids, 1),
        region, freq_soins, round(cout_moyen, 2)
    ])

columns = [
    "race", "age", "sexe", "sterilise",
    "poids", "region", "freq_soins", "cout_moyen"
]

df = pd.DataFrame(data, columns=columns)

# 2️⃣ Sauvegarder le fichier dedans
df.to_csv("data/pet_insurance.csv", index=False,encoding="latin1")

print("✅ Fichier enregistré dans data/pet_insurance.csv")
