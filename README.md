# Simulateur de prime d’assurance santé pour chiens

## 1. Contexte et objectif du projet

Ce projet vise à concevoir un **simulateur de prime d’assurance santé pour chiens**, destiné à un usage de **simulation tarifaire**.  
Il s’agit d’un **projet personnel à vocation pédagogique et professionnelle**, reproduisant les logiques **métier, data et actuarielles** utilisées dans le secteur de l’assurance.

Le simulateur permet à un utilisateur de renseigner des caractéristiques relatives à son chien et à son environnement afin d’obtenir une **estimation de prime annuelle**, selon plusieurs formules d’assurance.

Ce produit ne constitue **ni un devis contractuel**, **ni un avis médical**, mais un **outil de démonstration**.



## 2. Périmètre du produit (MVP)

- **Type d’assurance** : Assurance santé animale (chien)
- **Pays** : France
- **Animal couvert** : Chien uniquement
- **Usage** : Simulation de prime annuelle
- **Population cible** : Particuliers

### Exclusions
- Pas de gestion de remboursement réel
- Pas de suivi médical
- Pas de données personnelles réelles



## 3. Description des formules d’assurance

Le simulateur propose trois formules standards, représentatives du marché :

| Formule     | Taux de remboursement | Franchise annuelle | Plafond annuel |
|------------|-----------------------|-------------------|----------------|
| Essentielle | 70 %                  | 150 €             | 1 000 €        |
| Confort     | 80 %                  | 100 €             | 2 000 €        |
| Premium     | 90 %                  | 50 €              | 3 000 €        |

Ces paramètres interviennent directement dans le **calcul de la prime finale**.



## 4. Logique actuarielle et data

### 4.1 Principe général de tarification


La prime commerciale est ensuite ajustée en fonction :
- de la formule choisie
- de la franchise
- du plafond annuel
- d’un chargement (frais + marge)



## 5. Variables du modèle

### 5.1 Variables d’entrée (X)

Variables renseignées par l’utilisateur via le formulaire web :

| Variable   | Type         | Description |
|-----------|--------------|-------------|
| race      | Catégorielle | Race du chien |
| age       | Numérique    | Âge du chien (années) |
| sexe      | Catégorielle | Mâle / Femelle |
| sterilise | Binaire      | Stérilisé ou non |
| poids     | Numérique    | Poids du chien (kg) |
| region    | Catégorielle | Région ou zone géographique |

### 5.2 Variables cibles (Y)

Variables prédites par les modèles :

| Variable    | Description |
|------------|-------------|
| freq_soins | Nombre moyen de consultations vétérinaires par an |
| cout_moyen | Coût moyen annuel des soins vétérinaires (€) |



## 6. Règles métier de génération et d’interprétation

### 6.1 Effet de l’âge
- **Chiot (< 2 ans)** : fréquence modérée, coût modéré
- **Adulte (2–7 ans)** : fréquence stable, coût moyen
- **Senior (> 7 ans)** : fréquence élevée, coût élevé

### 6.2 Effet de la race
- **Races de grande taille**
  - Risque articulaire
  - Coûts de soins plus élevés
- **Races avec prédispositions génétiques connues**
  - Fréquence accrue
- **Races robustes**
  - Fréquence et coûts réduits

### 6.3 Effet du poids
- Poids élevé → coûts médicaux plus élevés
- Poids faible → coûts réduits

### 6.4 Effet de la stérilisation
- Chien stérilisé :
  - Réduction de certains risques
  - Fréquence légèrement plus faible

### 6.5 Effet de la région
- Zones urbaines :
  - Coût vétérinaire plus élevé
- Zones rurales :
  - Coût plus faible



## 7. Stratégie de données

### 7.1 Données synthétiques

Les données sont générées artificiellement à partir des règles métier ci-dessus, avec des distributions réalistes :

- `freq_soins` : distribution de **Poisson**
- `cout_moyen` : distribution **Gamma** ou **Log-Normale**

Cette approche est cohérente avec les pratiques de **prototypage en assurance**.



## 8. Modélisation

Deux modèles distincts sont entraînés :

1. **Modèle de fréquence**
   - Poisson GLM ou Random Forest
2. **Modèle de coût**
   - Gamma GLM ou Gradient Boosting

Les résultats sont combinés pour produire la **prime annuelle estimée**.



## 9. Architecture technique cible

- **Backend** : Django + Django REST Framework  
- **Modèles ML** : scikit-learn  
- **Sérialisation** : `pickle`  
- **Frontend** : HTML / CSS / Bootstrap  
- **Déploiement** : Render / Railway / Docker  


## 10. Livrables attendus

- Dataset synthétique documenté
- Notebooks d’exploration et de modélisation
- API de prédiction
- Interface web de simulation
- Documentation projet (README)



## 11. Critères de réussite

- Logique métier claire et justifiable
- Modèles interprétables
- Résultat de prime cohérent
- Application fonctionnelle déployée
- Projet présentable en entretien
