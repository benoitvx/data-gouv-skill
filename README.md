# 🇫🇷 data.gouv.fr Skill pour Claude Code

[![License](https://img.shields.io/badge/License-Licence_Ouverte_2.0-blue.svg)](LICENSE.md)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Claude Code](https://img.shields.io/badge/Claude-Code-purple.svg)](https://claude.ai/)
[![Version](https://img.shields.io/badge/Version-2.0.0-green.svg)](https://github.com/benoitvx/data-gouv-skill/releases)

> Skill professionnel pour Claude Code permettant d'accéder, télécharger et analyser les données ouvertes françaises via [data.gouv.fr](https://www.data.gouv.fr/)

## 📖 À propos

Ce repository fournit une **documentation complète** et une **librairie Python** pour travailler avec les données publiques françaises de data.gouv.fr.

**⚠️ Important** : Ce n'est **PAS un plugin avec des commandes slash interactives**, mais plutôt :
- 📚 Une documentation détaillée de l'API data.gouv.fr et des datasets
- 🐍 Une librairie Python réutilisable (`datagouv.py`)
- 📊 Des datasets documentés (IQVIA vaccinations, qualité de l'eau, etc.)
- 💡 Des exemples de code prêts à l'emploi
- 🔗 Des liens vers le MCP officiel data.gouv.fr

**Pour des commandes interactives dans Claude Code** (requêtes SQL, langage naturel), utilisez le [MCP officiel data.gouv.fr](https://github.com/datagouv/datagouv-mcp).

---
## ✨ Fonctionnalités

- 🆕 **Support du MCP officiel data.gouv.fr** (v2.1.0)
- 🔍 **Recherche intelligente** de datasets via l'API officielle
- 📥 **Téléchargement automatique** avec mise en cache
- 🧹 **Parsing avancé** des formats français (CSV `;`, dates DD/MM/YYYY, décimales `,`)
- 📊 **Chargement direct** dans pandas DataFrames
- 📚 **Documentation complète** des datasets les plus utilisés
- 🐍 **Librairie Python** réutilisable et testée
- 💡 **Exemples pratiques** pour chaque cas d'usage

## 🚀 Accès à la documentation

### Consulter en ligne

Parcourez la documentation directement sur GitHub :
- [SKILL.md](skills/data-gouv/SKILL.md) - Documentation principale
- [GUIDE_CHOIX.md](skills/data-gouv/GUIDE_CHOIX.md) - Choisir entre lib Python et MCP
- [Datasets](skills/data-gouv/datasets/) - Documentation détaillée des datasets

### Cloner localement
```bash
# Pour consulter la documentation et utiliser la librairie Python
git clone https://github.com/benoitvx/data-gouv-skill.git
cd data-gouv-skill
```

### Installer la librairie Python
```bash
pip install pandas requests openpyxl
# La librairie est dans skills/data-gouv/lib/datagouv.py
```

## 🆕 Nouveau en v2.1.0

Cette version ajoute le support du **MCP officiel data.gouv.fr** en complément de notre librairie Python !

### Deux approches au choix

**Notre librairie Python** (simple & rapide)
```python
from data-gouv.lib.datagouv import DataGouvAPI
api = DataGouvAPI()
df = api.load_csv(url)  # Cache, offline, portable
```

**MCP officiel** (requêtes SQL avancées)
```
"Dans le dataset IQVIA, trouve les départements où
les vaccinations ont augmenté de plus de 50%"
```

### Comment choisir ?

- **80% des cas** : Utilisez notre librairie Python (simple, rapide, offline)
- **20% des cas** : Utilisez le MCP (requêtes SQL, création datasets, langage naturel)

📖 **Guide complet** : [GUIDE_CHOIX.md](skills/data-gouv/GUIDE_CHOIX.md)
📚 **Documentation MCP** : [mcp/MCP_OFFICIEL.md](skills/data-gouv/mcp/MCP_OFFICIEL.md)

## 📖 Exemple d'utilisation

```python
from data-gouv.lib.datagouv import DataGouvAPI

# Initialiser l'API
api = DataGouvAPI()

# Rechercher des datasets
results = api.search_datasets("vaccination", organization="iqvia-france")
for dataset in results['data']:
    print(f"📊 {dataset['title']}")

# Charger directement un CSV
df = api.load_csv("https://www.data.gouv.fr/fr/datasets/r/resource-id")
print(f"✅ Chargé : {len(df)} lignes")

# Obtenir la dernière ressource d'un dataset
resource = api.get_latest_resource("dataset-id", format="csv")
df = api.load_csv(resource['url'])
```

## 📊 Datasets documentés

Le skill inclut une documentation détaillée pour les datasets les plus utilisés :

### Santé

#### [IQVIA - Vaccinations anti-grippales](skills/data-gouv/datasets/iqvia-vaccination.md)
- Suivi hebdomadaire des campagnes de vaccination
- Détails par région, département, âge et type de site
- Données depuis 2019

#### [Qualité de l'eau potable](skills/data-gouv/datasets/eau-potable.md)
- Résultats des contrôles sanitaires commune par commune
- Plus de 300,000 analyses par an
- Paramètres microbiologiques, chimiques et physico-chimiques

### Administration
- Calendrier scolaire par zone académique
- Code Officiel Géographique (INSEE)
- Population légale des communes

### Environnement
- Qualité de l'air
- Production d'énergie renouvelable
- Stations de recharge électrique

## 🎯 Cas d'usage

### Analyser les vaccinations par région

```python
from data-gouv.lib.datagouv import DataGouvAPI
import pandas as pd

api = DataGouvAPI()

# Charger les données de vaccination
results = api.search_datasets("vaccination grippe 2025-2026", organization="iqvia-france")
dataset_id = results['data'][0]['id']
resource = api.get_latest_resource(dataset_id, format='csv')
df = api.load_csv(resource['url'])

# Filtrer par région
df_na = df[df['code_region'] == '75']  # Nouvelle-Aquitaine
total = df_na['nb_doses'].sum()
print(f"💉 Total vaccinations en Nouvelle-Aquitaine : {total:,}")
```

### Vérifier la qualité de l'eau

```python
# Charger les données
dataset_id = "resultats-du-controle-sanitaire-de-leau-distribuee-commune-par-commune"
dataset = api.get_dataset(dataset_id)

# Obtenir les données pour La Rochelle (17300)
# ... (voir documentation complète dans skills/data-gouv/datasets/eau-potable.md)

# Calculer le taux de conformité
taux = (results['conforme'] == 'O').sum() / len(results) * 100
print(f"✅ Taux de conformité : {taux:.1f}%")
```

### Comparer des campagnes de vaccination

```python
# Charger 2 campagnes
df_2025 = api.load_csv(url_2025)
df_2024 = api.load_csv(url_2024)

# Comparer
evolution = ((df_2025['nb_doses'].sum() - df_2024['nb_doses'].sum()) / df_2024['nb_doses'].sum()) * 100
print(f"📈 Évolution : {evolution:+.1f}%")
```

## 🏗️ Structure du projet

```
data-gouv-skill/
├── .claude-plugin/
│   ├── plugin.json              # Métadonnées du plugin
│   └── marketplace.json         # Configuration marketplace
│
├── skills/data-gouv/
│   ├── SKILL.md                 # Documentation principale (point d'entrée)
│   │
│   ├── lib/
│   │   └── datagouv.py         # Librairie Python
│   │
│   ├── datasets/                # Documentation détaillée
│   │   ├── iqvia-vaccination.md
│   │   ├── eau-potable.md
│   │   └── ...
│   │
│   └── examples/                # Exemples de code
│       ├── vaccination_analysis.py
│       ├── water_quality.py
│       └── ...
│
├── scripts/
│   ├── sync-datasets.sh         # Synchroniser les métadonnées
│   └── update-metadata.py       # Mettre à jour la documentation
│
├── README.md                    # Ce fichier
└── LICENSE.md                   # Licence Ouverte 2.0
```

## 🔧 API Reference

### Classe DataGouvAPI

```python
class DataGouvAPI:
    def __init__(self, cache_dir: Optional[str] = None)

    def search_datasets(
        self, query: str,
        organization: Optional[str] = None,
        tag: Optional[str] = None,
        page_size: int = 20
    ) -> Dict[str, Any]

    def get_dataset(self, dataset_id: str) -> Optional[Dict[str, Any]]

    def get_latest_resource(
        self, dataset_id: str,
        format: str = 'csv'
    ) -> Optional[Dict[str, Any]]

    def download_resource(
        self, resource_url: str,
        cache: bool = True
    ) -> Optional[bytes]

    def load_csv(
        self, resource_url: str,
        sep: Optional[str] = None,
        encoding: Optional[str] = None,
        decimal: str = ','
    ) -> Optional[pd.DataFrame]
```

### Fonctions utilitaires

```python
def quick_search(query: str, limit: int = 5) -> List[Dict[str, Any]]
def load_dataset_csv(dataset_id: str, resource_index: int = 0) -> Optional[pd.DataFrame]
```

## 💡 Bonnes pratiques

### 1. Utiliser le cache

```python
api = DataGouvAPI(cache_dir="~/.cache/datagouv")
df = api.load_csv(url)  # cache automatique
```

### 2. Gérer les gros fichiers

```python
# Charger par chunks
chunks = []
for chunk in pd.read_csv(url, chunksize=10000, sep=';'):
    chunk_filtered = chunk[chunk['region'] == 'Nouvelle-Aquitaine']
    chunks.append(chunk_filtered)
df = pd.concat(chunks)
```

### 3. Valider les données

```python
df = api.load_csv(url)
if df is not None:
    print(f"✓ {len(df)} lignes, {len(df.columns)} colonnes")
else:
    print("✗ Erreur de chargement")
```

## 🤝 Contribution

Les contributions sont les bienvenues !

### Ajouter un nouveau dataset documenté

1. Créer `skills/data-gouv/datasets/nom-dataset.md`
2. Suivre le modèle des datasets existants
3. Inclure des exemples de code concrets
4. Soumettre une pull request

### Guidelines

- Utiliser le format markdown
- Inclure des exemples de code testés
- Documenter les colonnes importantes
- Ajouter des cas d'usage pratiques

## 📚 Ressources

### Documentation officielle
- [data.gouv.fr](https://www.data.gouv.fr/)
- [API documentation](https://www.data.gouv.fr/fr/apidoc/)
- [Guide des producteurs](https://guides.data.gouv.fr/)

### Organisations principales sur data.gouv.fr
- **INSEE** : Statistiques, population, économie
- **Ministère de la Santé** : Santé publique, qualité de l'eau
- **IQVIA France** : Campagnes de vaccination
- **Santé Publique France** : Surveillance sanitaire
- **Ministère de l'Éducation** : Données scolaires

## 📄 Licence

Ce projet est publié sous [Licence Ouverte 2.0](LICENSE.md) (compatible Creative Commons BY).

**Vous êtes libre de :**
- ✅ Réutiliser les données et le code
- ✅ Modifier et adapter
- ✅ Usage commercial autorisé

**Sous condition de :**
- 📝 Mentionner la paternité (source + date)

## 🙏 Remerciements

- [data.gouv.fr](https://www.data.gouv.fr/) pour l'API et les données ouvertes
- [Etalab](https://www.etalab.gouv.fr/) pour la plateforme et la Licence Ouverte
- La communauté des producteurs de données publiques
- [Claude Code](https://claude.ai/) par Anthropic

## 📞 Support

- 🐛 **Bug reports** : [GitHub Issues](https://github.com/benoitvx/data-gouv-skill/issues)
- 💡 **Feature requests** : [GitHub Discussions](https://github.com/benoitvx/data-gouv-skill/discussions)
- 📧 **Contact** : [benoitvinceneux@gmail.com]

---

**Auteur** : [Benoit Vinceneux](https://www.linkedin.com/in/votre-profil/)
**Version** : 2.0.0
**Dernière mise à jour** : 2025-12-02

⭐ Si ce projet vous est utile, n'hésitez pas à mettre une étoile sur GitHub !
