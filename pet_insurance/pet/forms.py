from django import forms

# class PetInsuranceForm(forms.Form):
#     race = forms.CharField(label="Race")
#     age = forms.IntegerField(label="Âge")
#     sexe = forms.ChoiceField(choices=[("M", "Mâle"), ("F", "Femelle")])
#     sterilise = forms.IntegerField(label="Stérilisé (0/1)")
#     poids = forms.FloatField(label="Poids (kg)")
#     region = forms.CharField(label="Région")


RACES = [
    ("Chihuahua", "Chihuahua"),
    ("Bouledogue français", "Bouledogue français"),
    ("Labrador", "Labrador"),
    ("Golden Retriever", "Golden Retriever"),
    ("Berger Allemand", "Berger Allemand"),
    ("Caniche", "Caniche"),
    ("Yorkshire", "Yorkshire"),
    ("Beagle", "Beagle"),
    ("Rottweiler", "Rottweiler"),
    ("Husky", "Husky"),
    ("Teckel", "Teckel"),
    ("Croisé", "Croisé"),
]

REGIONS = [
    ("Île-de-France", "Île-de-France"),
    ("Auvergne-Rhône-Alpes", "Auvergne-Rhône-Alpes"),
    ("Occitanie", "Occitanie"),
    ("Nouvelle-Aquitaine", "Nouvelle-Aquitaine"),
    ("Hauts-de-France", "Hauts-de-France"),
    ("Autres", "Autres"),
]

class PetInsuranceForm(forms.Form):
    race = forms.ChoiceField(
        choices=RACES,
        label="Race du chien"
    )

    age = forms.IntegerField(
        label="Âge du chien (années)",
        min_value=0
    )

    sexe = forms.ChoiceField(
        choices=[("M", "Mâle"), ("F", "Femelle")],
        label="Sexe"
    )

    sterilise = forms.ChoiceField(
        choices=[(1, "Oui"), (0, "Non")],
        label="Chien stérilisé ?"
    )

    poids = forms.FloatField(
        label="Poids du chien (kg)",
        min_value=0
    )

    region = forms.ChoiceField(
        choices=REGIONS,
        label="Région de résidence"
    )
