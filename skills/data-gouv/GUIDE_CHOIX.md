# Guide de choix : Librairie Python vs MCP officiel

## TL;DR - Aide-mémoire rapide

**Question simple** : "Je veux juste télécharger et analyser des données"  
→ **Utilisez notre librairie Python** 🐍

**Question complexe** : "Je veux faire des requêtes SQL sur toute la base data.gouv.fr"  
→ **Utilisez le MCP officiel** 🚀

---

## Arbre de décision
```
Vous voulez...
│
├─ Télécharger un CSV et l'analyser ?
│  └─→ Librairie Python ✅
│
├─ Travailler offline / avec cache ?
│  └─→ Librairie Python ✅
│
├─ Faire un script automatisé simple ?
│  └─→ Librairie Python ✅
│
├─ Requête SQL complexe sur plusieurs datasets ?
│  └─→ MCP officiel ✅
│
├─ Créer/modifier des datasets sur data.gouv.fr ?
│  └─→ MCP officiel ✅
│
└─ Poser des questions en langage naturel ?
   └─→ MCP officiel ✅
```

---

## Cas d'usage par approche

### Librairie Python

#### ✅ Parfait pour :

**1. Analyse hebdomadaire automatisée**
```python
# Cron job tous les lundis
from datagouv import DataGouvAPI

api = DataGouvAPI()
df = api.load_csv(url, cache=True)
df_region = df[df['region'] == '75']
send_report(df_region)
```

**2. Développement local**
```python
# Itération rapide
df = api.load_csv(url)
print(df.columns)
df.groupby('age')['doses'].sum()
```

**3. Notebooks Jupyter**
```python
# Exploration interactive
api = DataGouvAPI()
df = api.load_csv(url)
df.plot()
```

**4. Scripts portables**
```python
# Fonctionne partout : laptop, serveur, CI/CD
# Pas de dépendances lourdes
```

**5. Formation / Pédagogie**
```python
# Code simple et clair
# Facile à comprendre et modifier
```

---

### MCP officiel

#### ✅ Parfait pour :

**1. Questions ad-hoc complexes**
```
"Trouve tous les départements où le taux de vaccination 
des 65+ a augmenté de plus de 30% par rapport à l'année dernière"
```

**2. Recherche multi-datasets**
```
"Compare la qualité de l'eau et les taux de vaccination 
dans les communes de plus de 50 000 habitants"
```

**3. Création de datasets**
```
"Crée un nouveau dataset avec les données agrégées 
que je viens de calculer"
```

**4. Intégration dans des éditeurs**
```
# Utilisez directement dans Claude Desktop, Cursor
# Pas besoin de coder
```

**5. Requêtes en langage naturel**
```
"Quelle commune a la meilleure qualité d'eau 
en Charente-Maritime ?"
```

---

## Comparaison détaillée

### Installation

**Librairie Python**
```bash
pip install pandas requests openpyxl
# C'est tout !
```

**MCP officiel**
```bash
git clone https://github.com/datagouv/datagouv-mcp
cd datagouv-mcp
# + installer Docker
# + configurer Hydra (PostgreSQL)
# + configurer le client MCP
# + démarrer le serveur
```

**Gagnant** : 🐍 Librairie Python (10x plus simple)

---

### Performance

**Librairie Python**
- Téléchargement : ~10-20 sec pour un CSV moyen
- Cache : 0 sec si déjà téléchargé
- Offline : Fonctionne sans Internet

**MCP officiel**
- Requête SQL : ~1-5 sec (données indexées)
- Pas de cache local
- Nécessite connexion permanente

**Gagnant** : ⚖️ Égalité (dépend du cas d'usage)

---

### Flexibilité

**Librairie Python**
```python
# Contrôle total du code
df = api.load_csv(url)
df['custom_column'] = df['col1'] * 2
df.to_csv('result.csv')
```

**MCP officiel**
```
# Questions en langage naturel
# Moins de contrôle précis
```

**Gagnant** : 🐍 Librairie Python (pour les développeurs)

---

### Puissance

**Librairie Python**
- Téléchargement et analyse de datasets individuels
- Pas de requêtes SQL complexes
- Pas de recherche multi-datasets

**MCP officiel**
- Requêtes SQL sur toute la base Hydra
- Recherche dans tous les datasets
- Création de nouveaux datasets

**Gagnant** : 🚀 MCP officiel (pour requêtes complexes)

---

## Scénarios réels

### Scénario 1 : Rapport hebdomadaire

**Besoin** : Envoyer un rapport tous les lundis sur les vaccinations en Nouvelle-Aquitaine

**Solution** : 🐍 Librairie Python

**Pourquoi** :
- Simple
- Cache local (pas de re-téléchargement)
- Fonctionne même si data.gouv.fr est down
- Facile à automatiser (cron)
```python
# script_hebdo.py
from datagouv import DataGouvAPI

api = DataGouvAPI()
df = api.load_csv(url, cache=True)
df_na = df[df['region'] == '75']
send_email(generate_report(df_na))
```

---

### Scénario 2 : Question ponctuelle complexe

**Besoin** : "Quelles sont les 10 communes avec le meilleur taux de vaccination ET la meilleure qualité d'eau ?"

**Solution** : 🚀 MCP officiel

**Pourquoi** :
- Nécessite de croiser 2 datasets
- Requête SQL complexe
- Pas besoin de coder
```
"Croise les données de vaccination IQVIA et de qualité de l'eau 
pour trouver les 10 communes avec les meilleurs scores sur les deux"
```

---

### Scénario 3 : Pipeline de données

**Besoin** : ETL quotidien qui télécharge, nettoie, transforme et stocke les données

**Solution** : 🐍 Librairie Python

**Pourquoi** :
- Contrôle total du pipeline
- Peut tourner sur un serveur sans interface
- Robuste et prévisible
```python
# etl_pipeline.py
from datagouv import DataGouvAPI

api = DataGouvAPI()
df = api.load_csv(url)
df_clean = clean_data(df)
df_transform = transform(df_clean)
df_transform.to_sql('vaccinations', engine)
```

---

### Scénario 4 : Exploration interactive

**Besoin** : Explorer les données pour comprendre leur structure

**Solution** : 🐍 Librairie Python (+ Jupyter)

**Pourquoi** :
- Itération rapide
- Visualisations inline
- Pas besoin de serveur
```python
# Dans Jupyter
from datagouv import DataGouvAPI

api = DataGouvAPI()
df = api.load_csv(url)

# Explorer
df.head()
df.describe()
df.plot()
```

---

### Scénario 5 : Recherche dans toute la base

**Besoin** : "Trouve tous les datasets qui mentionnent 'vaccination' ET qui ont des données pour 2025"

**Solution** : 🚀 MCP officiel

**Pourquoi** :
- Recherche dans toute la base Hydra
- Pas besoin de connaître les datasets à l'avance
```
"Recherche tous les datasets liés à la vaccination 
qui contiennent des données pour 2025"
```

---

## Workflow hybride recommandé

### Phase 1 : Exploration (Librairie Python)
```python
from datagouv import DataGouvAPI

api = DataGouvAPI()

# Explorer les datasets disponibles
results = api.search_datasets("vaccination")
for ds in results['data']:
    print(ds['title'])

# Télécharger et explorer
df = api.load_csv(url)
print(df.columns)
print(df.describe())
```

### Phase 2 : Questions complexes (MCP)
```
"Maintenant que j'ai exploré, peux-tu me faire une analyse SQL 
qui compare les vaccinations par tranche d'âge entre toutes les régions ?"
```

### Phase 3 : Production (Librairie Python)
```python
# Script final automatisé
from datagouv import DataGouvAPI

def daily_analysis():
    api = DataGouvAPI()
    df = api.load_csv(url, cache=True)
    # ... logique métier ...
    save_results(df)

# Cron : tous les jours à 8h
```

---

## Matrice de décision

| Critère | Lib Python | MCP officiel |
|---------|------------|--------------|
| **Simplicité** | 🟢🟢🟢 | 🔴 |
| **Setup rapide** | 🟢🟢🟢 | 🔴 |
| **Offline** | 🟢🟢🟢 | 🔴🔴🔴 |
| **Cache local** | 🟢🟢🟢 | 🔴🔴🔴 |
| **Requêtes SQL** | 🔴🔴🔴 | 🟢🟢🟢 |
| **Multi-datasets** | 🔴🔴 | 🟢🟢🟢 |
| **Création datasets** | 🔴🔴🔴 | 🟢🟢🟢 |
| **Portabilité** | 🟢🟢🟢 | 🔴 |
| **Automatisation** | 🟢🟢🟢 | 🔴 |
| **Pédagogie** | 🟢🟢🟢 | 🔴🔴 |

---

## Conclusion

**Utilisez les DEUX selon vos besoins !**

- **80% du temps** : Librairie Python (simple, rapide, portable)
- **20% du temps** : MCP officiel (requêtes complexes, création)

**La v2.0.0 du skill vous donne accès aux deux approches** avec une documentation claire pour choisir la bonne méthode au bon moment.

---

**Version** : 2.0.0  
**Dernière mise à jour** : 2025-12-02
