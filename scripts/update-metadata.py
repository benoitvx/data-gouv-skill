#!/usr/bin/env python3
"""
Sync Dataset Metadata
=====================

This script synchronizes metadata from data.gouv.fr for documented datasets
and updates their documentation files.

Usage:
    python scripts/update-metadata.py
    python scripts/update-metadata.py --dataset iqvia-vaccination
"""

import requests
import json
import argparse
from pathlib import Path
from datetime import datetime

# Configuration
DATASETS = {
    'iqvia-vaccination': {
        'search_query': 'vaccination grippe campagne',
        'organization': 'iqvia-france',
        'doc_file': 'skills/data-gouv/datasets/iqvia-vaccination.md'
    },
    'eau-potable': {
        'dataset_id': 'resultats-du-controle-sanitaire-de-leau-distribuee-commune-par-commune',
        'doc_file': 'skills/data-gouv/datasets/eau-potable.md'
    }
}

API_BASE = "https://www.data.gouv.fr/api/1"


def get_dataset_info(dataset_key):
    """Fetch dataset information from data.gouv.fr API"""
    config = DATASETS[dataset_key]
    
    if 'dataset_id' in config:
        # Direct dataset ID
        url = f"{API_BASE}/datasets/{config['dataset_id']}/"
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response.json()
    else:
        # Search query
        url = f"{API_BASE}/datasets/"
        params = {
            'q': config['search_query'],
            'page_size': 5
        }
        if 'organization' in config:
            params['organization'] = config['organization']
        
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        results = response.json()
        
        if results['data']:
            return results['data'][0]
        else:
            raise ValueError(f"No dataset found for {dataset_key}")


def update_doc_metadata(dataset_key, dataset_info):
    """Update the documentation file with fresh metadata"""
    config = DATASETS[dataset_key]
    doc_path = Path(config['doc_file'])
    
    if not doc_path.exists():
        print(f"⚠️  Documentation file not found: {doc_path}")
        return
    
    content = doc_path.read_text(encoding='utf-8')
    
    # Extract metadata to update
    title = dataset_info.get('title', 'N/A')
    last_modified = dataset_info.get('last_modified', 'N/A')[:10]
    organization = dataset_info.get('organization', {}).get('name', 'N/A')
    num_resources = len(dataset_info.get('resources', []))
    
    # Update the "Dernière mise à jour" section at the end
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Simple replacement (could be made more sophisticated)
    if "## Dernière mise à jour" in content:
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if line.startswith("**Date**"):
                lines[i] = f"**Date** : {today}"
            if "Dataset ID:" in content and line.startswith("- **ID**"):
                lines[i] = f"- **ID**: `{dataset_info.get('id', 'N/A')}`"
        
        content = '\n'.join(lines)
        doc_path.write_text(content, encoding='utf-8')
        
        print(f"✅ Updated {dataset_key}")
        print(f"   Title: {title}")
        print(f"   Last modified: {last_modified}")
        print(f"   Resources: {num_resources}")
    else:
        print(f"⚠️  Could not find update section in {dataset_key}")


def main():
    parser = argparse.ArgumentParser(description='Sync dataset metadata from data.gouv.fr')
    parser.add_argument('--dataset', help='Specific dataset to sync (omit to sync all)')
    args = parser.parse_args()
    
    datasets_to_sync = [args.dataset] if args.dataset else DATASETS.keys()
    
    print("🔄 Syncing dataset metadata from data.gouv.fr...\n")
    
    for dataset_key in datasets_to_sync:
        if dataset_key not in DATASETS:
            print(f"❌ Unknown dataset: {dataset_key}")
            continue
        
        try:
            print(f"📊 Fetching {dataset_key}...")
            dataset_info = get_dataset_info(dataset_key)
            update_doc_metadata(dataset_key, dataset_info)
            print()
        except Exception as e:
            print(f"❌ Error syncing {dataset_key}: {e}\n")
    
    print("✅ Sync complete!")


if __name__ == "__main__":
    main()
