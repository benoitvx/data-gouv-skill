#!/usr/bin/env python3
"""
data.gouv.fr Python Library
===========================

Professional Python library for accessing and manipulating French open data
from data.gouv.fr.

Author: Benoit Vinceneux
License: Licence Ouverte 2.0
Repository: https://github.com/benoitvx/data-gouv-skill
"""

import requests
import pandas as pd
from typing import Optional, Dict, List, Any, Union
from datetime import datetime
import json
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataGouvAPI:
    """Main class for interacting with data.gouv.fr API"""
    
    BASE_URL = "https://www.data.gouv.fr/api/1"
    
    def __init__(self, cache_dir: Optional[str] = None):
        """
        Initialize the DataGouvAPI client
        
        Args:
            cache_dir: Optional directory for caching downloaded files
        """
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'data-gouv-skill/1.0.0 (Python)'
        })
        self.cache_dir = Path(cache_dir) if cache_dir else Path.home() / '.cache' / 'datagouv'
        self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def search_datasets(
        self,
        query: str,
        organization: Optional[str] = None,
        tag: Optional[str] = None,
        page_size: int = 20,
        page: int = 1
    ) -> Dict[str, Any]:
        """
        Search for datasets in the data.gouv.fr catalog
        
        Args:
            query: Search query string
            organization: Filter by organization slug or ID
            tag: Filter by tag
            page_size: Number of results per page (max 100)
            page: Page number
            
        Returns:
            Dictionary containing search results
            
        Example:
            >>> api = DataGouvAPI()
            >>> results = api.search_datasets("vaccination", organization="iqvia-france")
            >>> print(f"Found {results['total']} datasets")
        """
        params = {
            'q': query,
            'page_size': min(page_size, 100),
            'page': page
        }
        
        if organization:
            params['organization'] = organization
        if tag:
            params['tag'] = tag
        
        try:
            response = self.session.get(f"{self.BASE_URL}/datasets/", params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error searching datasets: {e}")
            return {'data': [], 'total': 0}
    
    def get_dataset(self, dataset_id: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed information about a specific dataset
        
        Args:
            dataset_id: Dataset ID or slug
            
        Returns:
            Dictionary with dataset information or None if not found
            
        Example:
            >>> api = DataGouvAPI()
            >>> dataset = api.get_dataset("5e7e104ace2080d9162b61d8")
            >>> print(dataset['title'])
        """
        try:
            response = self.session.get(f"{self.BASE_URL}/datasets/{dataset_id}/", timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching dataset: {e}")
            return None
    
    def get_latest_resource(
        self,
        dataset_id: str,
        format: str = 'csv',
        title_contains: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Get the most recent resource of a given format from a dataset
        
        Args:
            dataset_id: Dataset ID or slug
            format: Resource format (csv, json, xlsx, etc.)
            title_contains: Optional filter on resource title
            
        Returns:
            Resource dictionary or None
            
        Example:
            >>> api = DataGouvAPI()
            >>> resource = api.get_latest_resource("vaccination-dataset", format="csv")
            >>> print(resource['url'])
        """
        dataset = self.get_dataset(dataset_id)
        if not dataset:
            return None
        
        # Filter resources
        resources = [
            r for r in dataset.get('resources', [])
            if r.get('format', '').lower() == format.lower()
        ]
        
        # Additional filter by title if provided
        if title_contains:
            resources = [
                r for r in resources
                if title_contains.lower() in r.get('title', '').lower()
            ]
        
        if not resources:
            logger.warning(f"No {format} resources found in dataset {dataset_id}")
            return None
        
        # Sort by last_modified date
        resources.sort(key=lambda x: x.get('last_modified', ''), reverse=True)
        
        return resources[0]
    
    def download_resource(
        self,
        resource_url: str,
        cache: bool = True
    ) -> Optional[bytes]:
        """
        Download a resource file
        
        Args:
            resource_url: URL of the resource to download
            cache: Whether to use/save cache
            
        Returns:
            File content as bytes or None
            
        Example:
            >>> api = DataGouvAPI()
            >>> content = api.download_resource("https://www.data.gouv.fr/fr/datasets/r/abc123")
        """
        # Check cache
        if cache:
            cache_key = resource_url.split('/')[-1]
            cache_file = self.cache_dir / cache_key
            if cache_file.exists():
                logger.info(f"Loading from cache: {cache_file}")
                return cache_file.read_bytes()
        
        try:
            logger.info(f"Downloading: {resource_url}")
            response = self.session.get(resource_url, timeout=60)
            response.raise_for_status()
            
            content = response.content
            
            # Save to cache
            if cache:
                cache_file.write_bytes(content)
                logger.info(f"Saved to cache: {cache_file}")
            
            return content
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error downloading resource: {e}")
            return None
    
    def load_csv(
        self,
        resource_url: str,
        sep: Optional[str] = None,
        encoding: Optional[str] = None,
        decimal: str = ',',
        cache: bool = True,
        **pandas_kwargs
    ) -> Optional[pd.DataFrame]:
        """
        Load a CSV resource into a pandas DataFrame with automatic format detection
        
        Args:
            resource_url: URL of the CSV resource
            sep: Column separator (auto-detected if None)
            encoding: File encoding (auto-detected if None)
            decimal: Decimal separator (default: ',')
            cache: Whether to use cache
            **pandas_kwargs: Additional arguments for pd.read_csv
            
        Returns:
            pandas DataFrame or None
            
        Example:
            >>> api = DataGouvAPI()
            >>> df = api.load_csv("https://www.data.gouv.fr/fr/datasets/r/abc123")
            >>> print(df.head())
        """
        content = self.download_resource(resource_url, cache=cache)
        if content is None:
            return None
        
        # Try different encodings and separators
        encodings_to_try = [encoding] if encoding else ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
        separators_to_try = [sep] if sep else [';', ',', '\t', '|']
        
        for enc in encodings_to_try:
            for separator in separators_to_try:
                try:
                    df = pd.read_csv(
                        pd.io.common.BytesIO(content),
                        sep=separator,
                        encoding=enc,
                        decimal=decimal,
                        **pandas_kwargs
                    )
                    
                    # Check if parsing was successful (more than 1 column)
                    if len(df.columns) > 1:
                        logger.info(f"Successfully parsed with encoding={enc}, separator={repr(separator)}")
                        return self._clean_dataframe(df)
                        
                except Exception as e:
                    continue
        
        logger.error("Failed to parse CSV with all attempted encodings/separators")
        return None
    
    def _clean_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean a DataFrame (parse dates, fix decimal formats, etc.)
        
        Args:
            df: Input DataFrame
            
        Returns:
            Cleaned DataFrame
        """
        # Try to parse date columns
        for col in df.columns:
            if df[col].dtype == 'object':
                # Check if column looks like dates
                sample = df[col].dropna().astype(str).iloc[0] if len(df[col].dropna()) > 0 else None
                
                if sample and ('/' in sample or '-' in sample) and len(sample) <= 20:
                    # Try common French date formats
                    for date_format in ['%d/%m/%Y', '%d-%m-%Y', '%Y-%m-%d', '%d/%m/%Y %H:%M:%S']:
                        try:
                            df[col] = pd.to_datetime(df[col], format=date_format, errors='coerce')
                            if df[col].notna().sum() / len(df) > 0.5:
                                logger.info(f"Parsed dates in column '{col}'")
                                break
                        except:
                            continue
        
        return df


# Convenience functions for common use cases

def quick_search(query: str, limit: int = 5) -> List[Dict[str, Any]]:
    """
    Quick search for datasets
    
    Example:
        >>> datasets = quick_search("vaccination")
        >>> for ds in datasets:
        ...     print(ds['title'])
    """
    api = DataGouvAPI()
    results = api.search_datasets(query, page_size=limit)
    return results.get('data', [])


def load_dataset_csv(dataset_id: str, resource_index: int = 0) -> Optional[pd.DataFrame]:
    """
    Quick load of a CSV from a dataset
    
    Example:
        >>> df = load_dataset_csv("5e7e104ace2080d9162b61d8")
        >>> print(df.head())
    """
    api = DataGouvAPI()
    dataset = api.get_dataset(dataset_id)
    if not dataset:
        return None
    
    csv_resources = [r for r in dataset.get('resources', []) if r.get('format', '').lower() == 'csv']
    if not csv_resources or resource_index >= len(csv_resources):
        return None
    
    return api.load_csv(csv_resources[resource_index]['url'])


# Main execution for testing
if __name__ == "__main__":
    # Example usage
    api = DataGouvAPI()
    
    # Search for vaccination datasets
    print("Searching for vaccination datasets...")
    results = api.search_datasets("vaccination", organization="iqvia-france", page_size=3)
    
    print(f"\nFound {results['total']} datasets:")
    for dataset in results['data']:
        print(f"  - {dataset['title']}")
        print(f"    ID: {dataset['id']}")
        print(f"    Last modified: {dataset.get('last_modified', 'Unknown')[:10]}")
        print()
