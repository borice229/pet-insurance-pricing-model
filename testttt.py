import os

# chemin relatif depuis ce script
MODEL_FREQ_PATH = os.path.join("models", "model_freq.joblib")
MODEL_COST_PATH = os.path.join("models", "model_cost.joblib")


from rest_framework import serializers

class SimulationSerializer(serializers.Serializer):
    race = serializers.CharField()
    age = serializers.IntegerField()
    sexe = serializers.CharField()
    sterilise = serializers.BooleanField()
    poids = serializers.FloatField()
    region = serializers.CharField()
    formule = serializers.ChoiceField(
        choices=["Essentielle", "Confort", "Premium"]
    )


################
from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from core.models_ml import model_freq, model_cost
from core.pricing import calcul_prime
from .serializers import SimulationSerializer
import pandas as pd

class SimulationView(APIView):
    def post(self, request):
        serializer = SimulationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        X = pd.DataFrame([serializer.validated_data]).drop(columns=["formule"])

        freq_pred = model_freq.predict(X)[0]
        cost_pred = model_cost.predict(X)[0]

        prime = calcul_prime(
            freq_pred,
            cost_pred,
            serializer.validated_data["formule"]
        )

        return Response({
            "prime_annuelle": prime,
            "frequence_predite": round(freq_pred, 2),
            "cout_moyen_predit": round(cost_pred, 2)
        })
######

FACTEURS_FORMULE = {
    "Essentielle": 1.10,
    "Confort": 1.25,
    "Premium": 1.45
}

def calcul_prime(freq_pred, cost_pred, formule):
    if formule not in FACTEURS_FORMULE:
        raise ValueError("Formule inconnue")

    prime_pure = freq_pred * cost_pred
    prime_finale = prime_pure * FACTEURS_FORMULE[formule]

    return round(prime_finale, 2)