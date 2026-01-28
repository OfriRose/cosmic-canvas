"""
MAST (Mikulski Archive for Space Telescopes) API client.

This module provides functions to query and retrieve observation data
from the James Webb Space Telescope (JWST) and Hubble Space Telescope (HST).
"""

import pandas as pd
from typing import Optional, List, Dict, Any, Union
import streamlit as st
from astroquery.mast import Observations
import warnings

# Suppress astroquery warnings
warnings.filterwarnings('ignore', category=UserWarning, module='astroquery')


@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_telescope_images(
    telescope: str,
    limit: int = 50,
    object_name: Optional[str] = None
) -> pd.DataFrame:
    """
    Query MAST for recent observations from the specified telescope.
    
    Args:
        telescope: Either "JWST" or "HST"
        limit: Maximum number of observations to return
        object_name: Optional target name to filter by (e.g., "Andromeda", "Orion Nebula")
    
    Returns:
        DataFrame with columns:
            - target_name: Name of the observed target
            - obs_id: Observation ID (string)
            - obsid: Observation ID (numeric)
            - instrument_name: Instrument used
            - filters: Filters used in observation
            - t_obs_release: Observation release date
            - proposal_id: Proposal ID
            - dataproduct_type: Type of data product
            - obs_collection: Telescope collection (JWST/HST)
    
    Raises:
        Exception: If the query fails
    """
    try:
        # Build query parameters
        query_params = {
            "obs_collection": telescope,
            "dataproduct_type": "image",
        }
        
        # Add object name filter if provided
        if object_name:
            query_params["target_name"] = f"*{object_name}*"
        
        # Query MAST
        observations = Observations.query_criteria(**query_params)
        
        if len(observations) == 0:
            # Return empty DataFrame with expected columns
            return pd.DataFrame(columns=[
                "target_name", "obs_id", "obsid", "instrument_name", "filters",
                "t_obs_release", "proposal_id", "dataproduct_type", "obs_collection",
                "jpegURL"
            ])
        
        # Convert to pandas DataFrame and sort by observation date
        df = observations.to_pandas()
        
        # Sort by observation release date (most recent first)
        if 't_obs_release' in df.columns:
            df = df.sort_values('t_obs_release', ascending=False)
        
        # Limit results
        df = df.head(limit)
        
        # Select and rename relevant columns
        columns_to_keep = [
            "target_name", "obs_id", "obsid", "instrument_name", "filters",
            "t_obs_release", "proposal_id", "dataproduct_type", "obs_collection",
            "jpegURL"
        ]
        
        # Only keep columns that exist
        available_columns = [col for col in columns_to_keep if col in df.columns]
        df = df[available_columns]
        
        return df
        
    except Exception as e:
        raise Exception(f"Failed to query MAST for {telescope} observations: {e}")


@st.cache_data(ttl=3600)
def get_observation_products(obs_id: Union[str, int]) -> List[Dict[str, Any]]:
    """
    Get data products (including preview images) for a specific observation.
    
    Args:
        obs_id: Observation ID (numeric ID preferred, strictly required for some queries)
    
    Returns:
        List of dictionaries containing product information
    """
    try:
        # Get products for this observation
        products = Observations.get_product_list(obs_id)
        
        if len(products) == 0:
            return []
        
        # Convert to list of dicts
        products_df = products.to_pandas()
        
        # Filter for preview images (JPEG, PNG)
        preview_products = products_df[
            (products_df['productType'] == 'PREVIEW') |
            (products_df['dataURI'].str.contains('.jpg|.jpeg|.png', case=False, na=False))
        ]
        
        return preview_products.to_dict('records')
        
    except Exception as e:
        st.warning(f"Could not fetch products for {obs_id}: {e}")
        return []


def get_preview_url(obs_id: Union[str, int]) -> Optional[str]:
    """
    Get the preview image URL for an observation.
    
    Args:
        obs_id: Observation ID
    
    Returns:
        URL to the preview image, or None if not available
    """
    products = get_observation_products(obs_id)
    
    if not products:
        return None
    
    # Find the first JPEG or PNG preview
    for product in products:
        data_uri = product.get('dataURI', '')
        if data_uri and ('.jpg' in data_uri.lower() or '.jpeg' in data_uri.lower() or '.png' in data_uri.lower()):
            # Construct full URL
            if not data_uri.startswith('http'):
                data_uri = f"https://mast.stsci.edu/api/v0.1/Download/file?uri={data_uri}"
            return data_uri
    
    return None


def format_metadata(obs_row: pd.Series) -> Dict[str, str]:
    """
    Format observation metadata for display.
    
    Args:
        obs_row: A row from the observations DataFrame
    
    Returns:
        Dictionary with formatted metadata
    """
    metadata = {}
    
    # Target name
    if 'target_name' in obs_row:
        metadata['Target'] = str(obs_row['target_name'])
    
    # Instrument
    if 'instrument_name' in obs_row:
        metadata['Instrument'] = str(obs_row['instrument_name'])
    
    # Filters
    if 'filters' in obs_row and pd.notna(obs_row['filters']):
        metadata['Filters'] = str(obs_row['filters'])
    
    # Observation date
    if 't_obs_release' in obs_row and pd.notna(obs_row['t_obs_release']):
        metadata['Released'] = str(obs_row['t_obs_release'])[:10]  # Just the date part
    
    # Proposal ID
    if 'proposal_id' in obs_row and pd.notna(obs_row['proposal_id']):
        metadata['Proposal ID'] = str(obs_row['proposal_id'])
    
    # Observation ID
    if 'obs_id' in obs_row:
        metadata['Observation ID'] = str(obs_row['obs_id'])
    
    return metadata


# Sample comparison pairs for demo (famous objects observed by both telescopes)
COMPARISON_PAIRS = {
    "Pillars of Creation": {
        "jwst": "https://stsci-opo.org/STScI-01GA76Q01D09HFEV174Z5ZJW5J.png",
        "hst": "https://stsci-opo.org/STScI-01EVT1Z0Z2VQK8308JZ85E6EEM.png"
    },
    "Carina Nebula": {
        "jwst": "https://stsci-opo.org/STScI-01G7HDGS4743HQX7K9PVGQHXJT.png",
        "hst": "https://stsci-opo.org/STScI-01G7HDGS27Q61ZJHPXN2R1JR8H.png"
    },
    "Southern Ring Nebula": {
        "jwst": "https://stsci-opo.org/STScI-01G70BTB8SYYQ8QN8JYJX3QE26.png",
        "hst": "https://cdn.esahubble.org/archives/images/screen/heic1518a.jpg"
    }
}
