# Changelog

Toutes les modifications notables de ce projet seront documentées dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet adhère au [Semantic Versioning](https://semver.org/lang/fr/).

---

## [2.0.0] - 2025-12-02

### 🆕 Ajouté

- **Support du MCP officiel data.gouv.fr** : Documentation complète du MCP officiel en complément de notre librairie Python
- **Guide de choix** (`GUIDE_CHOIX.md`) : Aide à choisir entre la librairie Python et le MCP selon le cas d'usage
- **Documentation MCP** (`mcp/MCP_OFFICIEL.md`) : Installation, configuration et exemples d'utilisation du MCP officiel
- **Exemples hybrides** : Guide pour combiner les deux approches (`examples/hybrid/README.md`)
- **CHANGELOG.md** : Suivi des versions et modifications

### 📝 Modifié

- **SKILL.md** : Mise à jour pour la v2.0.0 avec documentation des deux approches
- **README.md** : Ajout d'une section "Nouveau en v2.0.0" et badge version
- Structure du projet élargie pour supporter les deux méthodes d'accès aux données

### 📚 Documentation

- Clarification des cas d'usage pour chaque approche (80% lib Python, 20% MCP)
- Ajout de scénarios concrets et d'un arbre de décision
- Documentation des workflows hybrides recommandés

---

## [1.0.0] - 2025-11-24

### 🎉 Version initiale

- **Librairie Python complète** (`datagouv.py`) : 350+ lignes
  - Recherche de datasets via l'API data.gouv.fr
  - Téléchargement automatique avec cache intelligent
  - Parsing avancé des formats français (CSV `;`, dates DD/MM/YYYY, décimales `,`)
  - Auto-détection encodage (utf-8, latin-1, cp1252) et séparateurs
  - Chargement direct dans pandas DataFrames
  
- **Documentation datasets** :
  - IQVIA Vaccinations anti-grippales : Structure, codes géographiques, 5 exemples
  - Qualité de l'eau potable : 3 fichiers, paramètres, optimisations
  
- **Exemples de code** :
  - `vaccination_analysis.py` : Analyse complète avec visualisations (150+ lignes)
  
- **Scripts utilitaires** :
  - `update-metadata.py` : Synchronisation des métadonnées datasets
  
- **Documentation** :
  - README.md professionnel (3,000+ mots)
  - SKILL.md complet (5,500+ mots)
  - LICENSE.md : Licence Ouverte 2.0
  
- **Configuration** :
  - `.claude-plugin/` : Support Claude Code
  - `.gitignore` : Configuration Git
  - Structure professionnelle pour GitHub

---

## Types de changements

- `Ajouté` : Nouvelles fonctionnalités
- `Modifié` : Changements dans les fonctionnalités existantes
- `Déprécié` : Fonctionnalités bientôt supprimées
- `Supprimé` : Fonctionnalités supprimées
- `Corrigé` : Corrections de bugs
- `Sécurité` : Correctifs de sécurité

---

**Auteur** : Benoit Vinceneux  
**Repository** : https://github.com/benoitvx/data-gouv-skill
