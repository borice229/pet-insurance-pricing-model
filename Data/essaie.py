# ==========================================================
# 1. Imports
# ==========================================================
import os
import pickle
import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.linear_model import PoissonRegressor, GammaRegressor
from sklearn.metrics import mean_poisson_deviance, mean_squared_error


# ==========================================================
# 2. Chargement des données
# ==========================================================
data = pd.read_csv("pet_insurance.csv",encoding="latin1",decimal=".")

# ==========================================================
# 3. Sélection des variables
# ==========================================================
X = data[["race", "age", "sexe", "sterilise", "poids", "region"]]



y_freq = data["freq_soins"]
y_cost = data["cout_moyen"]




# ==========================================================
# 4. Préprocessing
# ==========================================================
cat_features = ["race", "sexe", "region"]
num_features = ["age", "poids", "sterilise"]

preprocessor = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(drop="first", handle_unknown="ignore"), cat_features),
        ("num", "passthrough", num_features),
    ]
)


# ==========================================================
# 5. Train / Test split
# ==========================================================
X_train, X_test, y_freq_train, y_freq_test = train_test_split(
    X, y_freq, test_size=0.2, random_state=42
)

_, _, y_cost_train, y_cost_test = train_test_split(
    X, y_cost, test_size=0.2, random_state=42
)


# ==========================================================
# 6. Modèle fréquence (Poisson)
# ==========================================================
model_freq = Pipeline(steps=[
    ("preprocess", preprocessor),
    ("model", PoissonRegressor(alpha=0.1, max_iter=1000))
])

model_freq.fit(X_train, y_freq_train)

freq_pred = model_freq.predict(X_test)
print("Poisson deviance (freq):",
      mean_poisson_deviance(y_freq_test, freq_pred))


# ==========================================================
# 7. Modèle coût (Gamma)
# ==========================================================
model_cost = Pipeline(steps=[
    ("preprocess", preprocessor),
    ("model", GammaRegressor(alpha=0.1, max_iter=1000))
])

model_cost.fit(X_train, y_cost_train)

cost_pred = model_cost.predict(X_test)
print("RMSE (cost):",
      np.sqrt(mean_squared_error(y_cost_test, cost_pred)))



# ==========================================================
# 8. Sauvegarde des modèles
# ==========================================================
os.makedirs("models", exist_ok=True)

pickle.dump(model_freq, open("model_freq.sav", "wb"))
pickle.dump(model_cost, open("model_cost.sav", "wb"))

print("✅ Modèles sauvegardés dans le dossier 'models/'")
