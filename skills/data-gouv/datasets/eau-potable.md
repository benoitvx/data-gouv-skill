# Résultats du contrôle sanitaire de l'eau distribuée

## Vue d'ensemble

Organisation : **Ministère de la Santé et de la Prévention**  
Mise à jour : **Mensuelle** (m+1)  
Format : **CSV** (fichiers volumineux ~200MB)  
Licence : **Licence Ouverte 2.0**

## Description

Résultats complets des analyses réalisées dans le cadre du contrôle sanitaire de l'eau potable du robinet. Plus de 300,000 prélèvements par an analysés par des laboratoires agréés pour le compte des Agences Régionales de Santé (ARS).

## Dataset

- **ID**: `resultats-du-controle-sanitaire-de-leau-distribuee-commune-par-commune`
- **Couverture**: France métropolitaine + DROM
- **Période**: Depuis 2016
- **Fréquence**: Mise à jour mensuelle pour l'année en cours, annuelle pour les années antérieures

## Structure des données

### Fichiers disponibles

1. **PLV_{ANNEE}.csv** : Prélèvements  
   Liste des prélèvements effectués avec métadonnées

2. **RESULT_{ANNEE}.csv** : Résultats d'analyses  
   Résultats détaillés pour chaque paramètre testé

3. **UDI_COM_{ANNEE}.csv** : Lien communes/UDI  
   Correspondance entre communes et unités de distribution

### PLV - Prélèvements

| Colonne | Type | Description |
|---------|------|-------------|
| `referenceprel` | String | Référence unique du prélèvement |
| `cdreseau` | String | Code SISE de l'unité de distribution (UDI) |
| `nomreseau` | String | Nom de l'UDI |
| `dateprel` | Date | Date du prélèvement |
| `typeprel` | String | Type de prélèvement (D=Distribution, P=Production, etc.) |
| `nbranalyses` | Integer | Nombre d'analyses dans le prélèvement |

### RESULT - Résultats

| Colonne | Type | Description |
|---------|------|-------------|
| `referenceprel` | String | Référence du prélèvement (clé étrangère) |
| `cdparametre` | Integer | Code du paramètre analysé |
| `libelleparametre` | String | Nom du paramètre (ex: "Escherichia coli") |
| `resultanaly` | String/Float | Résultat de l'analyse |
| `unitemesure` | String | Unité de mesure (mg/L, UFC/100mL, etc.) |
| `conforme` | String | Conformité (O=Oui, N=Non, S=Sans objet) |
| `limitequalite` | Float | Limite de qualité réglementaire |

### UDI_COM - Correspondance

| Colonne | Type | Description |
|---------|------|-------------|
| `cdreseau` | String | Code SISE de l'UDI |
| `nomreseau` | String | Nom de l'UDI |
| `codecommune` | String | Code INSEE de la commune (5 chiffres) |
| `nomcommune` | String | Nom de la commune |

## Paramètres analysés

### Microbiologie
- **Escherichia coli** (UFC/100mL) : Limite = 0
- **Entérocoques** (UFC/100mL) : Limite = 0
- **Bactéries coliformes** (UFC/100mL) : Limite = 0

### Chimie
- **Nitrates** (mg/L) : Limite = 50
- **Pesticides totaux** (μg/L) : Limite = 0.5
- **Plomb** (μg/L) : Limite = 10
- **Arsenic** (μg/L) : Limite = 10
- **Fluorures** (mg/L) : Limite = 1.5

### Physico-chimie
- **Turbidité** (NFU) : Limite variable
- **pH** : 6.5 ≤ pH ≤ 9
- **Conductivité** (μS/cm) : 200-1100

## Codes géographiques

### La Rochelle et environs

**La Rochelle**
- Code commune : `17300`
- Département : `17` (Charente-Maritime)
- Région : `75` (Nouvelle-Aquitaine)

**Communes proches**
- Sainte-Marie-de-Ré : `17369`
- Aytré : `17028`
- Périgny : `17274`
- Lagord : `17200`

## Exemples d'utilisation

### Exemple 1 : Charger les données pour une commune

```python
from lib.datagouv import DataGouvAPI
import pandas as pd

api = DataGouvAPI()

# Charger le fichier de correspondance UDI/Communes
dataset_id = "resultats-du-controle-sanitaire-de-leau-distribuee-commune-par-commune"
dataset = api.get_dataset(dataset_id)

# Trouver les fichiers pour 2025
udi_com_resource = [r for r in dataset['resources'] if 'UDI_COM_2025' in r['title']][0]
udi_com = api.load_csv(udi_com_resource['url'])

# Filtrer pour La Rochelle
udi_larochelle = udi_com[udi_com['codecommune'] == '17300']
print(f"UDI pour La Rochelle: {udi_larochelle['cdreseau'].unique()}")
```

### Exemple 2 : Analyser la conformité de l'eau

```python
# Charger les résultats
result_resource = [r for r in dataset['resources'] if 'RESULT_2025' in r['title']][0]
results = api.load_csv(result_resource['url'])

# Charger les prélèvements
plv_resource = [r for r in dataset['resources'] if 'PLV_2025' in r['title']][0]
prelevements = api.load_csv(plv_resource['url'])

# Joindre avec les UDI de La Rochelle
udi_codes = udi_larochelle['cdreseau'].unique()
plv_larochelle = prelevements[prelevements['cdreseau'].isin(udi_codes)]

# Obtenir les résultats pour ces prélèvements
ref_prel = plv_larochelle['referenceprel'].unique()
results_larochelle = results[results['referenceprel'].isin(ref_prel)]

# Analyser la conformité
conformite = results_larochelle['conforme'].value_counts()
taux_conformite = (conformite.get('O', 0) / len(results_larochelle)) * 100

print(f"Taux de conformité: {taux_conformite:.1f}%")
```

### Exemple 3 : Paramètres critiques

```python
# Analyser les paramètres microbiologiques
params_micro = ['Escherichia coli', 'Entérocoques', 'Bactéries coliformes']
micro = results_larochelle[results_larochelle['libelleparametre'].isin(params_micro)]

# Vérifier les non-conformités
non_conformes = micro[micro['conforme'] == 'N']

if len(non_conformes) > 0:
    print(f"⚠️ {len(non_conformes)} non-conformités détectées:")
    print(non_conformes[['dateprel', 'libelleparametre', 'resultanaly']])
else:
    print("✅ Tous les paramètres microbiologiques sont conformes")
```

### Exemple 4 : Évolution de la qualité

```python
# Charger plusieurs années
years = [2023, 2024, 2025]
all_results = []

for year in years:
    result_resource = [r for r in dataset['resources'] if f'RESULT_{year}' in r['title']][0]
    df = api.load_csv(result_resource['url'])
    df['annee'] = year
    all_results.append(df)

combined = pd.concat(all_results, ignore_index=True)

# Calculer le taux de conformité par an
conformite_annuelle = combined.groupby('annee').apply(
    lambda x: (x['conforme'] == 'O').sum() / len(x) * 100
)

print("Évolution de la conformité:")
print(conformite_annuelle)
```

### Exemple 5 : Comparer plusieurs communes

```python
# Communes à comparer
communes = {
    'La Rochelle': '17300',
    'Royan': '17306',
    'Saintes': '17415'
}

comparison = []

for nom, code in communes.items():
    # Obtenir les UDI
    udi = udi_com[udi_com['codecommune'] == code]['cdreseau'].unique()
    
    # Obtenir les prélèvements
    plv = prelevements[prelevements['cdreseau'].isin(udi)]
    
    # Obtenir les résultats
    res = results[results['referenceprel'].isin(plv['referenceprel'])]
    
    # Calculer conformité
    taux = (res['conforme'] == 'O').sum() / len(res) * 100
    
    comparison.append({
        'Commune': nom,
        'Nb prélèvements': len(plv),
        'Nb analyses': len(res),
        'Taux conformité': taux
    })

df_comp = pd.DataFrame(comparison)
print(df_comp)
```

## Optimisation des performances

### Fichiers volumineux

Les fichiers peuvent être très volumineux (>200 MB). Stratégies d'optimisation :

```python
# 1. Charger avec des chunks
chunks = []
for chunk in pd.read_csv(url, chunksize=10000, sep=';', encoding='utf-8'):
    # Filtrer immédiatement
    chunk_filtered = chunk[chunk['codecommune'] == '17300']
    chunks.append(chunk_filtered)

df = pd.concat(chunks, ignore_index=True)

# 2. Sélectionner seulement les colonnes nécessaires
usecols = ['referenceprel', 'cdparametre', 'libelleparametre', 'resultanaly', 'conforme']
df = pd.read_csv(url, sep=';', encoding='utf-8', usecols=usecols)

# 3. Utiliser des types de données optimisés
dtypes = {
    'codecommune': 'category',
    'conforme': 'category',
    'libelleparametre': 'category'
}
df = pd.read_csv(url, sep=';', encoding='utf-8', dtype=dtypes)
```

## Cas d'usage typiques

### Questions fréquentes

**Q: L'eau est-elle potable dans ma commune ?**
```python
# Obtenir le taux de conformité récent (3 derniers mois)
recent = results_commune[results_commune['dateprel'] > (datetime.now() - timedelta(days=90))]
taux = (recent['conforme'] == 'O').sum() / len(recent) * 100
print(f"Conformité sur 3 mois: {taux:.1f}%")
```

**Q: Y a-t-il des problèmes de nitrates ?**
```python
nitrates = results_commune[results_commune['libelleparametre'] == 'Nitrates']
depassements = nitrates[nitrates['resultanaly'].astype(float) > 50]
print(f"Dépassements nitrates: {len(depassements)}")
```

**Q: Date du dernier contrôle ?**
```python
dernier = prelevements_commune['dateprel'].max()
print(f"Dernier contrôle: {dernier}")
```

## Notes importantes

### Interprétation des résultats
- `conforme='O'` : Conforme aux limites réglementaires
- `conforme='N'` : Non-conforme (dépassement de limite)
- `conforme='S'` : Sans objet (pas de limite applicable)

### Unités de Distribution (UDI)
- Une commune peut avoir plusieurs UDI
- Plusieurs communes peuvent partager une UDI
- Utiliser le fichier UDI_COM pour faire la correspondance

### Limitations
- Données validées avec délai de publication (m+1)
- Tous les prélèvements ne testent pas tous les paramètres
- Focus sur les paramètres réglementaires

## Ressources externes

- [Site officiel eaupotable.sante.gouv.fr](https://eaupotable.sante.gouv.fr/)
- [ANSES - Eau potable](https://www.anses.fr/fr/content/la-qualit%C3%A9-de-l%E2%80%99eau-potable)
- [SISE-Eaux](https://solidarites-sante.gouv.fr/)

## Dernière mise à jour

**Date** : 2025-11-24  
**Version** : 1.0.0
