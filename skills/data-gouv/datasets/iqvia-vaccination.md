# IQVIA France - Suivi des vaccinations anti-grippales

## Vue d'ensemble

Organisation : **IQVIA France**  
Mise à jour : **Hebdomadaire** (pendant la campagne de vaccination)  
Format : **CSV, XLSX**  
Licence : **Licence Ouverte 2.0**

## Description

Données de suivi de la vaccination anti-grippale en France métropolitaine et dans les DROM, collectées par IQVIA France. Les données sont mises à jour chaque semaine pendant la campagne de vaccination (octobre à mars).

## Datasets disponibles

### Campagne 2025-2026
- **ID**: `suivi-de-la-vaccination-anti-grippale-campagne-2025-2026`
- **Ressources**: CSV hebdomadaire, données cumulatives
- **Période**: Octobre 2025 - Mars 2026

### Campagnes précédentes
- Campagne 2024-2025
- Campagne 2023-2024
- Historique disponible depuis 2019

## Structure des données

### Colonnes principales

| Colonne | Type | Description |
|---------|------|-------------|
| `semaine_injection` | Date | Semaine de l'injection (format ISO: YYYY-Www) |
| `code_region` | String | Code INSEE de la région |
| `libelle_region` | String | Nom de la région |
| `code_departement` | String | Code du département (2 chiffres) |
| `libelle_departement` | String | Nom du département |
| `age` | String | Tranche d'âge (ex: "65 ans et plus", "50-64 ans") |
| `type_site` | String | Type de site de vaccination |
| `nb_doses` | Integer | Nombre de doses administrées |
| `nb_doses_cumulees` | Integer | Cumul depuis le début de la campagne |

### Types de sites

- `Pharmacie` : Pharmacies d'officine
- `Cabinet médical` : Cabinets de médecins généralistes/spécialistes
- `Cabinet infirmier` : Cabinets d'infirmiers libéraux
- `Centre de vaccination` : Centres dédiés
- `Autres` : Autres lieux de vaccination

### Tranches d'âge

- `0-17 ans`
- `18-49 ans`
- `50-64 ans`
- `65-74 ans`
- `75 ans et plus`
- `Âge non renseigné`

## Codes géographiques

### Régions de Nouvelle-Aquitaine
- **Code région**: `75`
- **Départements**: 
  - `16` : Charente
  - `17` : Charente-Maritime
  - `19` : Corrèze
  - `23` : Creuse
  - `24` : Dordogne
  - `33` : Gironde
  - `40` : Landes
  - `47` : Lot-et-Garonne
  - `64` : Pyrénées-Atlantiques
  - `79` : Deux-Sèvres
  - `86` : Vienne
  - `87` : Haute-Vienne

## Exemples d'utilisation

### Exemple 1 : Charger les données de la campagne actuelle

```python
from lib.datagouv import DataGouvAPI

api = DataGouvAPI()

# Rechercher le dataset
results = api.search_datasets("vaccination grippe 2025-2026", organization="iqvia-france")
dataset_id = results['data'][0]['id']

# Charger le CSV le plus récent
resource = api.get_latest_resource(dataset_id, format='csv')
df = api.load_csv(resource['url'])

print(f"Données chargées: {len(df)} lignes")
print(f"Dernière semaine: {df['semaine_injection'].max()}")
```

### Exemple 2 : Filtrer par région

```python
# Charger les données
df = api.load_csv(resource_url)

# Filtrer pour la Nouvelle-Aquitaine
df_na = df[df['code_region'] == '75']

# Ou par département (Charente-Maritime)
df_cm = df[df['code_departement'] == '17']

print(f"Vaccinations en Charente-Maritime: {df_cm['nb_doses'].sum():,}")
```

### Exemple 3 : Analyser par tranche d'âge

```python
# Grouper par âge
vaccinations_par_age = df.groupby('age')['nb_doses'].sum().sort_values(ascending=False)

print("Vaccinations par tranche d'âge:")
print(vaccinations_par_age)
```

### Exemple 4 : Comparer avec la campagne précédente

```python
# Charger campagne 2025-2026
df_2025 = api.load_csv(url_2025)

# Charger campagne 2024-2025
df_2024 = api.load_csv(url_2024)

# Comparer les totaux à même date
total_2025 = df_2025['nb_doses'].sum()
total_2024 = df_2024['nb_doses'].sum()

evolution = ((total_2025 - total_2024) / total_2024) * 100
print(f"Évolution: {evolution:+.1f}%")
```

### Exemple 5 : Visualisation de l'évolution hebdomadaire

```python
import matplotlib.pyplot as plt

# Préparer les données
weekly = df.groupby('semaine_injection')['nb_doses'].sum().reset_index()
weekly['semaine_injection'] = pd.to_datetime(weekly['semaine_injection'] + '-1', format='%Y-W%W-%w')

# Créer le graphique
plt.figure(figsize=(12, 6))
plt.plot(weekly['semaine_injection'], weekly['nb_doses'], marker='o')
plt.title('Évolution hebdomadaire des vaccinations anti-grippales')
plt.xlabel('Semaine')
plt.ylabel('Nombre de doses')
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('vaccinations_hebdo.png', dpi=150)
```

## Cas d'usage typiques

### Questions fréquentes

**Q: Combien de vaccinations ont été réalisées cette semaine ?**
```python
df_cette_semaine = df[df['semaine_injection'] == df['semaine_injection'].max()]
total = df_cette_semaine['nb_doses'].sum()
```

**Q: Quel département vaccine le plus ?**
```python
par_departement = df.groupby('libelle_departement')['nb_doses'].sum().sort_values(ascending=False)
print(par_departement.head(10))
```

**Q: Quelle proportion des vaccinations a lieu en pharmacie ?**
```python
par_site = df.groupby('type_site')['nb_doses'].sum()
pct_pharmacie = (par_site['Pharmacie'] / par_site.sum()) * 100
print(f"Pharmacies: {pct_pharmacie:.1f}%")
```

**Q: Combien de vaccinations pour les 65 ans et plus ?**
```python
seniors = df[df['age'].str.contains('65 ans et plus|75 ans et plus')]
total_seniors = seniors['nb_doses'].sum()
```

## Notes importantes

### Données manquantes
- Certaines semaines peuvent avoir des retards de publication
- Les données sont validées avant publication (délai de quelques jours)

### Interprétation
- Les données représentent les actes remboursés, pas nécessairement la date d'injection exacte
- Un léger décalage peut exister entre l'injection et l'enregistrement

### Mise à jour
- Publication : généralement le jeudi après-midi
- Période : mi-octobre à fin mars

## Ressources externes

- [Site officiel IQVIA France](https://www.iqvia.com/fr-fr)
- [Page du dataset sur data.gouv.fr](https://www.data.gouv.fr/fr/organizations/iqvia-france/)
- [Santé Publique France - Vaccination](https://www.santepubliquefrance.fr/)

## Dernière mise à jour

**Date** : 2025-11-24  
**Version** : 1.0.0
