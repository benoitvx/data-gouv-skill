#!/usr/bin/env python3
"""
Exemple : Analyse complète des vaccinations anti-grippales

Ce script montre comment utiliser la librairie data.gouv.fr pour :
1. Rechercher et charger les données IQVIA
2. Filtrer par région/département
3. Analyser l'évolution temporelle
4. Comparer avec la campagne précédente
5. Créer des visualisations

Author: Benoit Vinceneux
License: Licence Ouverte 2.0
"""

import sys
from pathlib import Path

# Ajouter le chemin de la librairie
sys.path.insert(0, str(Path(__file__).parent.parent / 'skills' / 'data-gouv' / 'lib'))

from datagouv import DataGouvAPI
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime


def main():
    print("🇫🇷 Analyse des vaccinations anti-grippales\n")
    print("=" * 60)
    
    # Initialiser l'API
    api = DataGouvAPI()
    
    # 1. Rechercher le dataset de la campagne actuelle
    print("\n1️⃣  Recherche du dataset...\n")
    results = api.search_datasets(
        "vaccination grippe 2025-2026",
        organization="iqvia-france"
    )
    
    if not results['data']:
        print("❌ Aucun dataset trouvé")
        return
    
    dataset = results['data'][0]
    print(f"✅ Dataset trouvé : {dataset['title']}")
    print(f"   Organisation : {dataset['organization']['name']}")
    print(f"   Dernière MAJ : {dataset.get('last_modified', 'N/A')[:10]}")
    
    # 2. Charger les données
    print("\n2️⃣  Chargement des données...\n")
    resource = api.get_latest_resource(dataset['id'], format='csv')
    
    if not resource:
        print("❌ Aucune ressource CSV trouvée")
        return
    
    print(f"📄 Ressource : {resource['title']}")
    print(f"   Taille : {resource.get('filesize', 0) / 1024 / 1024:.1f} MB")
    
    df = api.load_csv(resource['url'])
    
    if df is None:
        print("❌ Erreur de chargement")
        return
    
    print(f"✅ Données chargées : {len(df):,} lignes, {len(df.columns)} colonnes")
    print(f"   Colonnes : {', '.join(df.columns.tolist()[:5])}...")
    
    # 3. Analyser les données
    print("\n3️⃣  Analyse des données...\n")
    
    # Total national
    total_national = df['nb_doses'].sum()
    print(f"💉 Total national : {total_national:,} doses")
    
    # Par région
    print("\n📊 Top 5 régions :")
    par_region = df.groupby('libelle_region')['nb_doses'].sum().sort_values(ascending=False)
    for i, (region, doses) in enumerate(par_region.head(5).items(), 1):
        print(f"   {i}. {region:30s} : {doses:>10,} doses")
    
    # Focus Nouvelle-Aquitaine
    print("\n🎯 Focus Nouvelle-Aquitaine :")
    df_na = df[df['code_region'] == '75']
    total_na = df_na['nb_doses'].sum()
    part_na = (total_na / total_national) * 100
    print(f"   Total : {total_na:,} doses ({part_na:.1f}% du national)")
    
    # Par département en Nouvelle-Aquitaine
    print("\n   Par département :")
    par_dept = df_na.groupby('libelle_departement')['nb_doses'].sum().sort_values(ascending=False)
    for dept, doses in par_dept.head(5).items():
        print(f"   • {dept:25s} : {doses:>10,} doses")
    
    # Par type de site
    print("\n📍 Par type de site (national) :")
    par_site = df.groupby('type_site')['nb_doses'].sum().sort_values(ascending=False)
    for site, doses in par_site.items():
        pct = (doses / total_national) * 100
        print(f"   • {site:25s} : {doses:>10,} doses ({pct:>5.1f}%)")
    
    # Par tranche d'âge
    print("\n👥 Par tranche d'âge (national) :")
    par_age = df.groupby('age')['nb_doses'].sum().sort_values(ascending=False)
    for age, doses in par_age.items():
        pct = (doses / total_national) * 100
        print(f"   • {age:25s} : {doses:>10,} doses ({pct:>5.1f}%)")
    
    # 4. Évolution temporelle
    print("\n4️⃣  Évolution temporelle...\n")
    
    # Convertir les semaines en dates
    df['date'] = pd.to_datetime(df['semaine_injection'] + '-1', format='%Y-W%W-%w', errors='coerce')
    
    # Grouper par semaine
    evolution = df.groupby('date')['nb_doses'].sum().sort_index()
    
    print("📅 Évolution hebdomadaire :")
    for date, doses in evolution.tail(5).items():
        print(f"   Semaine du {date.strftime('%d/%m/%Y')} : {doses:>10,} doses")
    
    # 5. Visualisations
    print("\n5️⃣  Création des visualisations...\n")
    
    # Graphique 1 : Évolution temporelle
    plt.figure(figsize=(14, 6))
    plt.subplot(1, 2, 1)
    evolution.plot(marker='o', linewidth=2)
    plt.title('Évolution hebdomadaire des vaccinations', fontsize=14, fontweight='bold')
    plt.xlabel('Semaine')
    plt.ylabel('Nombre de doses')
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    
    # Graphique 2 : Top départements Nouvelle-Aquitaine
    plt.subplot(1, 2, 2)
    par_dept.head(10).plot(kind='barh', color='steelblue')
    plt.title('Top 10 départements - Nouvelle-Aquitaine', fontsize=14, fontweight='bold')
    plt.xlabel('Nombre de doses')
    plt.grid(True, alpha=0.3, axis='x')
    
    plt.tight_layout()
    output_file = 'vaccination_analysis.png'
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    print(f"📊 Graphiques sauvegardés : {output_file}")
    
    # 6. Export des données
    print("\n6️⃣  Export des données...\n")
    
    # Export CSV Nouvelle-Aquitaine
    export_file = 'vaccinations_nouvelle_aquitaine.csv'
    df_na.to_csv(export_file, index=False, sep=';', encoding='utf-8')
    print(f"💾 Données exportées : {export_file}")
    print(f"   {len(df_na):,} lignes")
    
    # Résumé par département
    summary = df_na.groupby(['libelle_departement', 'code_departement']).agg({
        'nb_doses': 'sum',
        'semaine_injection': 'nunique'
    }).reset_index()
    summary.columns = ['Département', 'Code', 'Total doses', 'Nb semaines']
    summary = summary.sort_values('Total doses', ascending=False)
    
    summary_file = 'summary_departements.csv'
    summary.to_csv(summary_file, index=False, sep=';', encoding='utf-8')
    print(f"💾 Résumé exporté : {summary_file}")
    
    print("\n" + "=" * 60)
    print("✅ Analyse terminée !")
    print("\nFichiers générés :")
    print(f"  • {output_file}")
    print(f"  • {export_file}")
    print(f"  • {summary_file}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Analyse interrompue")
    except Exception as e:
        print(f"\n❌ Erreur : {e}")
        import traceback
        traceback.print_exc()
