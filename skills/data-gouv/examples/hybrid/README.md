# Exemples hybrides : Librairie Python + MCP officiel

Ce dossier contient des exemples qui montrent comment combiner notre librairie Python avec le MCP officiel data.gouv.fr pour obtenir le meilleur des deux mondes.

## Workflow recommandé

### Phase 1 : Exploration avec la librairie Python

Utilisez notre librairie pour découvrir et explorer les données rapidement :
```python
from datagouv import DataGouvAPI

api = DataGouvAPI()

# Recherche rapide
results = api.search_datasets("vaccination", organization="iqvia-france")

# Téléchargement et exploration
df = api.load_csv(url)
print(df.columns)
print(df.head())
print(df.describe())

# Analyse simple
vaccinations_par_region = df.groupby('region')['nb_doses'].sum()
print(vaccinations_par_region.sort_values(ascending=False).head())
```

**Avantages** :
- ✅ Rapide (cache local)
- ✅ Offline possible
- ✅ Contrôle total du code

---

### Phase 2 : Questions complexes avec le MCP

Une fois que vous avez exploré les données, utilisez le MCP pour des analyses avancées :

**Dans Claude Desktop avec le MCP configuré :**
```
Maintenant que j'ai exploré le dataset IQVIA vaccination 2025-2026, 
peux-tu faire une analyse SQL qui :

1. Compare les vaccinations par tranche d'âge entre toutes les régions
2. Identifie les départements où la progression est supérieure à +50%
3. Croise avec les données de l'année précédente
4. Présente les résultats dans un tableau

Utilise la base Hydra pour accéder à tous les datasets nécessaires.
```

**Avantages** :
- ✅ Requêtes SQL complexes automatiques
- ✅ Accès à toute la base Hydra
- ✅ Pas besoin de coder

---

### Phase 3 : Production avec la librairie Python

Transformez votre analyse en script automatisé :
```python
from datagouv import DataGouvAPI
import pandas as pd

def analyse_hebdomadaire():
    """
    Script qui tourne tous les lundis pour analyser
    les données de la semaine précédente
    """
    api = DataGouvAPI()
    
    # Télécharger avec cache
    df = api.load_csv(vaccination_url, cache=True)
    
    # Appliquer la logique découverte en phase 1 et 2
    df_filtered = df[df['region'] == '75']
    df_seniors = df_filtered[df_filtered['age'].str.contains('65')]
    
    total = df_seniors['nb_doses'].sum()
    
    # Générer le rapport
    rapport = generer_rapport(df_seniors)
    envoyer_email(rapport)
    
    return total

# Exécuter
if __name__ == "__main__":
    total = analyse_hebdomadaire()
    print(f"✅ Analyse terminée : {total:,} vaccinations")
```

**Avantages** :
- ✅ Robuste et prévisible
- ✅ Automatisable (cron)
- ✅ Fonctionne sans le MCP

---

## Scénarios concrets

### Scénario 1 : Rapport mensuel

**Besoin** : Rapport automatique le 1er de chaque mois

**Solution** :
1. **Exploration initiale** (librairie Python) : Comprendre les données
2. **Définir les KPIs** (MCP) : "Quels sont les meilleurs indicateurs à suivre ?"
3. **Automatisation** (librairie Python) : Script cron mensuel

---

### Scénario 2 : Analyse ad-hoc

**Besoin** : "Le directeur veut savoir pourquoi la région X a une baisse"

**Solution** :
1. **Téléchargement rapide** (librairie Python) : Avoir les données localement
2. **Analyse approfondie** (MCP) : "Compare la région X avec les régions similaires"
3. **Visualisation** (librairie Python) : Créer des graphiques pour la présentation

---

### Scénario 3 : Pipeline de données

**Besoin** : ETL quotidien vers data warehouse

**Solution** :
1. **Design du pipeline** (MCP) : "Quelles transformations sont nécessaires ?"
2. **Implémentation** (librairie Python) : Code robuste et testé
3. **Monitoring** (MCP) : "Détecte les anomalies dans les nouvelles données"

---

## Bonnes pratiques

### DO ✅

- Utilisez la librairie Python pour le développement local
- Utilisez le MCP pour les questions exploratoires
- Automatisez avec la librairie Python
- Documentez vos découvertes MCP pour les réutiliser en Python

### DON'T ❌

- Ne dépendez pas du MCP pour la production (serveur peut être down)
- Ne codez pas en Python ce que le MCP peut faire en 1 question
- N'utilisez pas le MCP pour des analyses simples (overhead inutile)
- Ne téléchargez pas manuellement ce que la lib Python peut cacher

---

## Checklist du workflow hybride

- [ ] **Phase Exploration** : Lib Python pour comprendre les données
- [ ] **Phase Analyse** : MCP pour questions complexes
- [ ] **Phase Documentation** : Noter les insights et requêtes utiles
- [ ] **Phase Implémentation** : Lib Python pour le code de prod
- [ ] **Phase Test** : Vérifier que le script fonctionne offline
- [ ] **Phase Déploiement** : Automatiser avec cron/scheduler
- [ ] **Phase Monitoring** : MCP pour détecter anomalies

---

## Résumé

**Librairie Python** : Votre outil quotidien  
**MCP officiel** : Votre expert consultant  

Utilisez les deux intelligemment pour un workflow optimal ! 🚀

---

**Version** : 2.0.0  
**Dernière mise à jour** : 2025-12-02
