# MCP data.gouv.fr officiel

## Vue d'ensemble

Le **MCP (Model Context Protocol) officiel de data.gouv.fr** est un serveur qui permet d'interagir avec data.gouv.fr via des outils avancés, notamment des requêtes SQL sur la base **Hydra**.

**Repository officiel** : https://github.com/datagouv/datagouv-mcp

---

## Quand utiliser le MCP officiel ?

**✅ Utilisez le MCP si :**
- Vous avez besoin de **requêtes SQL complexes** sur les données
- Vous voulez **créer ou modifier des datasets** sur data.gouv.fr
- Vous travaillez avec **Claude Desktop, Cursor, ou Codeium**
- Vous voulez des **données toujours à jour** (via Hydra)
- Vous posez des questions complexes nécessitant de la recherche multi-datasets

**❌ N'utilisez PAS le MCP si :**
- Vous voulez juste **télécharger un CSV** (utilisez notre lib)
- Vous travaillez **offline** (le MCP nécessite un serveur)
- Vous préférez la **simplicité** (notre lib est plus simple)
- Vous faites des **scripts automatisés** simples

---

## Fonctionnalités du MCP

### 1. `search_datasets`
Recherche de datasets par mots-clés.

**Exemple :**
```
"Recherche les datasets IQVIA sur la vaccination"
```

### 2. `query_dataset_data`
Requêtes SQL sur les données via Hydra.

**Exemple :**
```
"Dans le dataset de vaccination IQVIA, montre-moi les départements 
où le nombre de doses a augmenté de plus de 50% par rapport à l'année dernière"
```

### 3. `create_dataset`
Création de nouveaux datasets (nécessite une clé API).

**Exemple :**
```python
create_dataset(
    title="Mon dataset",
    description="...",
    organization="mon-org"
)
```

---

## Installation

### Prérequis

- Docker
- Python 3.11+
- `uv` (gestionnaire de packages Python)

### Étape 1 : Cloner le repo
```bash
git clone https://github.com/datagouv/datagouv-mcp.git
cd datagouv-mcp
```

### Étape 2 : Installer Hydra (base PostgreSQL)

Suivez les instructions du [repository Hydra](https://github.com/datagouv/hydra).

**Résumé rapide :**
```bash
# Hydra indexe tous les CSV de data.gouv.fr dans PostgreSQL
docker-compose up -d
```

### Étape 3 : Configurer l'environnement
```bash
cp .env.example .env
```

Éditez `.env` :
```bash
MCP_PORT=8007
DATAGOUV_API_ENV=prod  # ou "demo"
HYDRA_DB_HOST=127.0.0.1
HYDRA_DB_PORT=5434
```

### Étape 4 : Installer les dépendances
```bash
uv sync
```

### Étape 5 : Démarrer le serveur MCP
```bash
uv run main.py
```

Le serveur démarre sur `http://127.0.0.1:8007/mcp`

---

## Configuration des clients

### Claude Desktop

Éditez `~/Library/Application Support/Claude/claude_desktop_config.json` :
```json
{
  "mcpServers": {
    "data-gouv": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "http://127.0.0.1:8007/mcp",
        "--header",
        "Authorization: Bearer VOTRE_CLE_API"
      ]
    }
  }
}
```

### Claude Code

Pas encore de support MCP natif dans Claude Code CLI.

**Alternative** : Utilisez notre librairie Python ! 👍

### Cursor

Dans les settings de Cursor :
```json
{
  "mcpServers": {
    "data-gouv": {
      "url": "http://127.0.0.1:8007/mcp",
      "transport": "http",
      "headers": {
        "API_KEY": "VOTRE_CLE_API"
      }
    }
  }
}
```

---

## Obtenir une clé API

1. Allez sur https://www.data.gouv.fr/fr/admin/me/
2. Section "Clés d'API"
3. Créez une nouvelle clé
4. Copiez-la dans votre configuration

**Note** : La clé API est **uniquement nécessaire** pour créer/modifier des datasets. La lecture est publique.

---

## Exemples d'utilisation

### Exemple 1 : Recherche simple

**Dans Claude Desktop avec le MCP configuré :**
```
Recherche les datasets sur la vaccination anti-grippale
```

**Réponse** : Liste des datasets IQVIA avec métadonnées

---

### Exemple 2 : Requête SQL via Hydra
```
Dans le dataset IQVIA vaccination 2025-2026, montre-moi :
- Le nombre total de doses par région
- Trié par ordre décroissant
- Pour les personnes de 65 ans et plus
```

**Le MCP va** :
1. Trouver le dataset
2. Identifier les tables Hydra correspondantes
3. Exécuter la requête SQL
4. Retourner les résultats

---

### Exemple 3 : Comparaison multi-datasets
```
Compare le nombre de vaccinations entre la campagne 2024-2025 
et 2025-2026 pour la région Nouvelle-Aquitaine
```

**Le MCP va** :
1. Trouver les 2 datasets
2. Faire des requêtes SQL sur les 2 tables
3. Calculer l'évolution
4. Présenter les résultats

---

## Avantages du MCP

✅ **Requêtes complexes** - SQL automatique  
✅ **Données à jour** - Hydra synchronisé  
✅ **Multi-datasets** - Recherche dans toute la base  
✅ **Création** - Peut modifier data.gouv.fr  
✅ **Intégré** - Dans Claude Desktop, Cursor, etc.

---

## Limitations du MCP

❌ **Nécessite un serveur** - Doit tourner en permanence  
❌ **Complexe** - Docker + PostgreSQL + configuration  
❌ **Pas offline** - Nécessite connexion réseau  
❌ **Pas dans Claude Code CLI** - Support limité  
❌ **Ressources** - Hydra peut être lourd

---

## MCP vs Notre librairie Python

| Critère | MCP officiel | Notre lib |
|---------|--------------|-----------|
| **Setup** | Docker + config | `pip install` |
| **Requêtes SQL** | ✅ Oui | ❌ Non |
| **Offline** | ❌ Non | ✅ Oui |
| **Cache local** | ❌ Non | ✅ Oui |
| **Création datasets** | ✅ Oui | ❌ Non |
| **Simplicité** | 🔴 Complexe | 🟢 Simple |
| **Claude Code CLI** | ⚠️ Limité | ✅ Plein support |

---

## Recommandation

**Pour 80% des cas d'usage** : Utilisez notre librairie Python  
**Pour 20% des cas avancés** : Utilisez le MCP officiel

**Workflow hybride idéal** :
1. Développement et exploration → Notre lib
2. Questions complexes ad-hoc → MCP
3. Scripts automatisés → Notre lib
4. Création de datasets → MCP

---

## Ressources

- **MCP officiel** : https://github.com/datagouv/datagouv-mcp
- **Hydra** : https://github.com/datagouv/hydra
- **Documentation MCP** : https://modelcontextprotocol.io/
- **Notre librairie** : `skills/data-gouv/lib/datagouv.py`

---

**Version** : 2.0.0  
**Dernière mise à jour** : 2025-12-02
