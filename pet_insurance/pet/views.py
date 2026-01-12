from django.shortcuts import render
from .forms import PetInsuranceForm
import pickle
import pandas as pd
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

model_freq = pickle.load(
    open(os.path.join(BASE_DIR, "pet/ml_models/model_freq.sav"), "rb")
)

model_cost = pickle.load(
    open(os.path.join(BASE_DIR, "pet/ml_models/model_cost.sav"), "rb")
)

def home(request):
    return render(request, "pet/home.html")

def predict_insurance(request):
    result = None

    if request.method == "POST":
        form = PetInsuranceForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            X = pd.DataFrame([{
                "race": data["race"],
                "age": data["age"],
                "sexe": data["sexe"],
                "sterilise": data["sterilise"],
                "poids": data["poids"],
                "region": data["region"],
            }])

            freq = model_freq.predict(X)[0]
            cost = model_cost.predict(X)[0]

            result = {
                "freq": round(freq, 2),
                "cost": round(cost, 2),
                "prime_estimee": round(freq * cost, 2)
            }
    else:
        form = PetInsuranceForm()

    return render(request, "pet/predict.html", {
        "form": form,
        "result": result
    })
