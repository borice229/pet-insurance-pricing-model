#%%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#%%
data = pd.read_csv("data/pet_insurance.csv",encoding="latin1",decimal=".")
data.head(10)

# %%
data.describe()

# %%
data.describe(include='object')

# %%
data.info()

# %%
data['race'].value_counts(dropna=False)

# %%
data['sexe'].value_counts(dropna=False)

# %%
data['region'].value_counts(dropna=False)

# Vérification des valeurs manquantes

# %%
data.isna().sum()

# Visualisation

# %%
plt.hist(data["freq_soins"], bins=10, edgecolor="black")
plt.xlabel("Fréquence des soins (visites/an)")
plt.ylabel("Nombre de chiens")
plt.title("Distribution de la fréquence des soins")
plt.show()

# %%
plt.hist(data["cout_moyen"], bins=10, edgecolor="black")
plt.xlabel("Coût moyen annuel des soins (€)")
plt.ylabel("Nombre de chiens")
plt.title("Distribution du coût moyen annuel")

# %%
sns.boxplot(x=pd.cut(data["age"], bins=[0,2,7,15]),
            y=data["freq_soins"])
plt.xlabel("Classe d'âge")
plt.ylabel("Fréquence des soins")
plt.show()

"""
Commentaire : On constate que plus l'age est au dela de 7 ans la fréquance des soins
est supérieur

"""
# %%
sns.boxplot(x="region", y="cout_moyen", data=data)
plt.xticks(rotation=45)
plt.show()

"""
Commentaire : On constate que le coût est legerement plus élévé en ile-de-france

"""

# %%
top_races = data["race"].value_counts().index[:10]
sns.boxplot(x="race", y="cout_moyen",
            data=data[data["race"].isin(top_races)])
plt.xticks(rotation=45)
plt.show()

# %%
data.groupby("region")[["freq_soins", "cout_moyen"]].mean()



# %%
data.groupby("race")[["freq_soins", "cout_moyen"]].mean()

#%%
X = data[["race", "age", "sexe", "sterilise", "poids", "region"]]
y_freq = data["freq_soins"]
y_cost = data["cout_moyen"]

# %%
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline

cat_features = ["race", "sexe", "region"]
num_features = ["age", "poids", "sterilise"]

preprocessor = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(drop="first"), cat_features),
        ("num", "passthrough", num_features)
    ]
)

# %%
## GLM
from sklearn.linear_model import PoissonRegressor
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y_freq, test_size=0.2, random_state=42
)

model_freq = Pipeline(steps=[
    ("preprocess", preprocessor),
    ("model", PoissonRegressor(alpha=0.1, max_iter=1000))
])

model_freq.fit(X_train, y_train)

# %%
### Evaluation modele
from sklearn.metrics import mean_poisson_deviance

y_pred = model_freq.predict(X_test)

mean_poisson_deviance(y_test, y_pred)

# %%
feature_names = model_freq.named_steps["preprocess"].get_feature_names_out()
coeffs = model_freq.named_steps["model"].coef_

pd.DataFrame({
    "feature": feature_names,
    "coef": coeffs
}).sort_values("coef", ascending=False).head(10)


# %%
facteurs_formule = {
    "Essentielle": 1.10,
    "Confort": 1.25,
    "Premium": 1.45
}

def calcul_prime(freq_pred, cost_pred, formule):
    """
    Calcule la prime annuelle estimée d'assurance santé chien.

    Paramètres
    ----------
    freq_pred : float
        Fréquence annuelle prédite des soins
    cost_pred : float
        Coût moyen annuel des soins (€)
    formule : str
        Formule d'assurance ("Essentielle", "Confort", "Premium")

    Retour
    ------
    float
        Prime annuelle estimée (€)
    """
    if formule not in facteurs_formule:
        raise ValueError("Formule inconnue")

    prime_pure = freq_pred * cost_pred
    facteur = facteurs_formule[formule]
    prime_finale = prime_pure * facteur

    return round(prime_finale, 2)


# %%
calcul_prime(
    freq_pred=3.2,
    cost_pred=180,
    formule="Confort"
)

# %%
