"""
NASA Astronomy Picture of the Day (APOD) API client.

This module provides functions to fetch the daily astronomy picture
and its metadata from NASA's APOD API.
"""

import requests
from typing import Optional, Dict, Any
from datetime import datetime
import streamlit as st


@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_apod(api_key: str = "DEMO_KEY", date: Optional[str] = None) -> Dict[str, Any]:
    """
    Fetch the Astronomy Picture of the Day from NASA's APOD API.
    
    Args:
        api_key: NASA API key (default: DEMO_KEY with rate limits)
        date: Optional date in YYYY-MM-DD format. If None, returns today's APOD.
    
    Returns:
        Dictionary containing:
            - title: Image title
            - explanation: Description of the image
            - url: URL to the full-resolution image
            - hdurl: URL to the HD version (if available)
            - media_type: "image" or "video"
            - copyright: Copyright information (if available)
            - date: Date of the APOD
    
    Raises:
        Exception: If the API request fails
    """
    base_url = "https://api.nasa.gov/planetary/apod"
    
    params = {
        "api_key": api_key,
    }
    
    if date:
        params["date"] = date
    
    try:
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Ensure all expected fields exist
        result = {
            "title": data.get("title", "Unknown"),
            "explanation": data.get("explanation", "No description available."),
            "url": data.get("url", ""),
            "hdurl": data.get("hdurl", data.get("url", "")),
            "media_type": data.get("media_type", "image"),
            "copyright": data.get("copyright", "Public Domain"),
            "date": data.get("date", datetime.now().strftime("%Y-%m-%d"))
        }
        
        return result
        
    except requests.exceptions.Timeout:
        raise Exception("NASA APOD API request timed out. Please try again.")
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 429:
            raise Exception("NASA APOD API rate limit exceeded. Please try again later or use your own API key.")
        elif e.response.status_code == 403:
            raise Exception("Invalid NASA API key. Please check your configuration.")
        else:
            raise Exception(f"NASA APOD API error: {e}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to fetch APOD: {e}")
    except ValueError as e:
        raise Exception(f"Invalid JSON response from NASA APOD API: {e}")


def validate_date(date_str: str) -> bool:
    """
    Validate date format for APOD API.
    
    Args:
        date_str: Date string to validate
    
    Returns:
        True if valid YYYY-MM-DD format, False otherwise
    """
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False
