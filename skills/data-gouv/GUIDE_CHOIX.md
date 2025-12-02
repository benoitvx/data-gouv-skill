# Accéder aux données data.gouv.fr

Ce document présente les différentes méthodes pour accéder aux données publiques françaises via data.gouv.fr.

---

## Deux approches disponibles

### 1. Téléchargement direct (librairie Python)

Une librairie Python pour télécharger et analyser les fichiers CSV/Excel de data.gouv.fr.

**Principe** : Télécharge les fichiers depuis data.gouv.fr et les charge dans pandas DataFrames.

**Avantages** :
- Installation simple (`pip install pandas requests`)
- Fonctionne offline une fois les données téléchargées
- Cache local pour éviter les re-téléchargements
- Contrôle total du code

**Cas d'usage** :
- Scripts automatisés (cron jobs)
- Développement local et exploration
- Analyse offline
- Notebooks Jupyter
- Pipelines de données

**Documentation** : [lib/datagouv.py](lib/datagouv.py)

**Exemple** :
```python
from datagouv import DataGouvAPI

api = DataGouvAPI()
df = api.load_csv(url, cache=True)
df.groupby('region')['value'].sum()
```

---

### 2. MCP officiel data.gouv.fr

Un serveur MCP (Model Context Protocol) maintenu par l'équipe data.gouv.fr pour interagir avec les données via Claude Desktop, Cursor et autres clients compatibles MCP.

**Principe** : Serveur qui expose des outils pour rechercher et requêter les données via Hydra (base PostgreSQL).

**Avantages** :
- Requêtes SQL complexes automatiques
- Questions en langage naturel
- Accès à toute la base Hydra
- Création de datasets (avec clé API)

**Cas d'usage** :
- Questions ad-hoc complexes
- Recherche dans plusieurs datasets
- Analyses exploratoires en langage naturel
- Création/modification de datasets

**Documentation officielle** : https://github.com/datagouv/datagouv-mcp

**Exemple** :
```
"Dans le dataset IQVIA vaccination, trouve les départements 
où le nombre de doses a augmenté de plus de 50%"
```

---

## Comparaison technique

| Critère | Librairie Python | MCP officiel |
|---------|------------------|--------------|
| **Installation** | `pip install` | Docker + config |
| **Requêtes** | Code Python | Langage naturel |
| **Offline** | Oui (avec cache) | Non |
| **SQL complexe** | Non | Oui (via Hydra) |
| **Création datasets** | Non | Oui (avec API key) |
| **Portabilité** | Excellente | Nécessite serveur |

---

## Choisir selon vos besoins

### Vous voulez télécharger des fichiers et les analyser ?
→ **Librairie Python**

### Vous voulez poser des questions complexes en langage naturel ?
→ **MCP officiel**

### Vous développez des scripts automatisés ?
→ **Librairie Python**

### Vous voulez créer ou modifier des datasets ?
→ **MCP officiel**

### Vous travaillez avec Claude Desktop ou Cursor ?
→ **MCP officiel** (intégration native)

### Vous travaillez en ligne de commande ou dans des notebooks ?
→ **Librairie Python**

---

## Utilisation combinée

Les deux approches ne sont pas exclusives. Vous pouvez :

1. **Explorer** avec la librairie Python (rapide, local)
2. **Approfondir** avec le MCP (requêtes complexes)
3. **Produire** avec la librairie Python (scripts robustes)

**Exemple de workflow** :
```python
# Phase 1 : Exploration locale
api = DataGouvAPI()
df = api.load_csv(url)
print(df.columns)  # Comprendre la structure

# Phase 2 : Question complexe via MCP
"Analyse SQL détaillée de ce dataset..."

# Phase 3 : Script de production
def analyse_quotidienne():
    df = api.load_csv(url, cache=True)
    # ... logique métier ...
```

---

## Ressources

### API data.gouv.fr
- Documentation API : https://www.data.gouv.fr/fr/apidoc/
- Catalogue datasets : https://www.data.gouv.fr/fr/datasets/

### Librairie Python (ce repo)
- Code source : [lib/datagouv.py](lib/datagouv.py)
- Exemples : [examples/](examples/)
- Datasets documentés : [datasets/](datasets/)

### MCP officiel
- Repository : https://github.com/datagouv/datagouv-mcp
- Issues : https://github.com/datagouv/datagouv-mcp/issues

---

**Version** : 2.1.0  
**Dernière mise à jour** : 2025-12-02
