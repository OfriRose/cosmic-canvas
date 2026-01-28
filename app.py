"""
Cosmic Canvas: JWST & Hubble Gallery
A Streamlit application for browsing and comparing deep-space images from
the James Webb Space Telescope and Hubble Space Telescope.
"""

import streamlit as st
import pandas as pd
from typing import Optional
import os

# Import utility modules
from backend.apod_api import get_apod
from backend.mast_api import (
    get_telescope_images,
    get_preview_url,
    format_metadata,
    COMPARISON_PAIRS
)

# Try to import streamlit-image-comparison, fallback if not available
try:
    from streamlit_image_comparison import image_comparison
    HAS_IMAGE_COMPARISON = True
except ImportError:
    HAS_IMAGE_COMPARISON = False


# Page configuration
st.set_page_config(
    page_title="Cosmic Canvas: JWST & Hubble Gallery",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
    }
    .subheader {
        text-align: center;
        color: #888;
        margin-bottom: 2rem;
    }
    .apod-container {
        background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
    }
    .image-card {
        border: 2px solid #f0f0f0;
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1rem;
        transition: transform 0.2s;
    }
    .image-card:hover {
        transform: scale(1.02);
        border-color: #667eea;
    }
    .metadata-label {
        font-weight: bold;
        color: #667eea;
    }
</style>
""", unsafe_allow_html=True)


def display_apod_section(api_key: str):
    """Display the Astronomy Picture of the Day section."""
    st.markdown('<div class="apod-container">', unsafe_allow_html=True)
    st.markdown("### 🌟 Today's Astronomy Picture of the Day")
    
    try:
        apod_data = get_apod(api_key)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            if apod_data["media_type"] == "image":
                st.image(apod_data["url"], use_container_width=True)
            elif apod_data["media_type"] == "video":
                st.video(apod_data["url"])
            else:
                st.warning("Unsupported media type for today's APOD.")
        
        with col2:
            st.markdown(f"**{apod_data['title']}**")
            st.caption(f"📅 {apod_data['date']} | © {apod_data['copyright']}")
            st.write(apod_data["explanation"])
            
            if apod_data.get("hdurl"):
                st.markdown(f"[🔗 View HD Version]({apod_data['hdurl']})")
    
    except Exception as e:
        st.error(f"Failed to load APOD: {e}")
    
    st.markdown('</div>', unsafe_allow_html=True)


def display_image_gallery(telescope: str, object_filter: Optional[str], limit: int = 50):
    """Display the image gallery for the selected telescope."""
    st.markdown(f"### 🔭 {telescope} Image Gallery")
    
    with st.spinner(f"Loading {telescope} observations..."):
        try:
            df = get_telescope_images(telescope, limit=limit, object_name=object_filter)
            
            if df.empty:
                st.info(f"No observations found for {telescope}" + 
                       (f" matching '{object_filter}'" if object_filter else ""))
                return
            
            st.caption(f"Showing {len(df)} observations")
            
            # Display images in a grid (3 columns)
            cols_per_row = 3
            rows = len(df) // cols_per_row + (1 if len(df) % cols_per_row > 0 else 0)
            
            for row_idx in range(rows):
                cols = st.columns(cols_per_row)
                
                for col_idx in range(cols_per_row):
                    obs_idx = row_idx * cols_per_row + col_idx
                    
                    if obs_idx >= len(df):
                        break
                    
                    obs = df.iloc[obs_idx]
                    
                    with cols[col_idx]:
                        # Display target name
                        target_name = obs.get('target_name', 'Unknown Target')
                        st.markdown(f"**{target_name}**")
                        
                        # Try to get preview image
                        preview_url = None
                        
                        # FAST PATH: Use jpegURL from main query if available
                        if 'jpegURL' in obs and pd.notna(obs['jpegURL']):
                            uri = obs['jpegURL']
                            if uri.startswith('http'):
                                preview_url = uri
                            else:
                                preview_url = f"https://mast.stsci.edu/api/v0.1/Download/file?uri={uri}"
                        
                        # SLOW PATH: Fallback to querying products (only if needed)
                        if not preview_url:
                             # Prefer numeric obsid if available to avoid DB type errors
                            obs_identifier = obs.get('obsid') if 'obsid' in obs and pd.notna(obs.get('obsid')) else obs['obs_id']
                            preview_url = get_preview_url(obs_identifier)
                        
                        if preview_url:
                            st.image(preview_url, use_container_width=True)
                        else:
                            st.info("Preview not available")
                        
                        # Metadata in expander
                        with st.expander("📊 View Details"):
                            metadata = format_metadata(obs)
                            for key, value in metadata.items():
                                st.markdown(f"**{key}:** {value}")
        
        except Exception as e:
            st.error(f"Failed to load {telescope} images: {e}")


def display_comparison_section():
    """Display the image comparison section."""
    st.markdown("### 🔄 Compare JWST & Hubble Images")
    st.info("Select a famous object to see how JWST and Hubble captured it differently.")
    
    # Selection box for comparison pairs
    selected_object = st.selectbox(
        "Choose an object:",
        options=list(COMPARISON_PAIRS.keys())
    )
    
    if selected_object:
        pair = COMPARISON_PAIRS[selected_object]
        
        st.markdown(f"#### Comparing: {selected_object}")
        
        # Use streamlit-image-comparison if available
        if HAS_IMAGE_COMPARISON:
            try:
                image_comparison(
                    img1=pair["jwst"],
                    img2=pair["hst"],
                    label1="JWST",
                    label2="Hubble",
                    width=700,
                    starting_position=50,
                    show_labels=True,
                    make_responsive=True,
                )
            except Exception as e:
                st.warning(f"Image comparison widget failed: {e}. Using side-by-side view.")
                # Fallback to columns
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**JWST**")
                    st.image(pair["jwst"], use_container_width=True)
                with col2:
                    st.markdown("**Hubble**")
                    st.image(pair["hst"], use_container_width=True)
        else:
            # Fallback to side-by-side columns
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**🌌 James Webb Space Telescope**")
                st.image(pair["jwst"], use_container_width=True)
                st.caption("Infrared imaging reveals hidden details")
            with col2:
                st.markdown("**🔭 Hubble Space Telescope**")
                st.image(pair["hst"], use_container_width=True)
                st.caption("Visible light captures stunning colors")


def main():
    """Main application function."""
    
    # Header
    st.markdown('<h1 class="main-header">🌌 Cosmic Canvas</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subheader">Explore the Universe through JWST & Hubble</p>', 
                unsafe_allow_html=True)
    
    # Sidebar configuration
    st.sidebar.title("⚙️ Settings")
    
    # API Key configuration
    api_key = os.getenv("NASA_API_KEY", "DEMO_KEY")
    
    # Check for Streamlit secrets (gracefully handle missing secrets file)
    try:
        api_key = st.secrets.get("NASA_API_KEY", api_key)
    except (FileNotFoundError, KeyError):
        # No secrets file or NASA_API_KEY not in secrets, use env var or default
        pass

    
    with st.sidebar.expander("🔑 API Configuration"):
        st.caption(f"Current API Key: {api_key[:4]}...{api_key[-4:] if len(api_key) > 8 else ''}")
        st.caption("Configure via `.streamlit/secrets.toml` or environment variable")
    
    # Telescope selection
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔭 Telescope Selection")
    telescope = st.sidebar.radio(
        "Choose telescope:",
        options=["JWST", "HST"],
        format_func=lambda x: "James Webb Space Telescope" if x == "JWST" else "Hubble Space Telescope"
    )
    
    # Object search filter
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔍 Search Filter")
    object_filter = st.sidebar.text_input(
        "Object name (optional):",
        placeholder="e.g., Andromeda, Orion Nebula",
        help="Filter observations by target name"
    )
    
    # Image limit
    image_limit = st.sidebar.slider(
        "Max images to display:",
        min_value=10,
        max_value=100,
        value=30,
        step=10
    )
    
    # Comparison mode toggle
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔄 Comparison Mode")
    show_comparison = st.sidebar.checkbox(
        "Show Image Comparison",
        help="Compare famous objects as seen by both telescopes"
    )
    
    # About section
    st.sidebar.markdown("---")
    with st.sidebar.expander("ℹ️ About"):
        st.markdown("""
        **Cosmic Canvas** brings together stunning imagery from:
        - 🛰️ James Webb Space Telescope (JWST)
        - 🔭 Hubble Space Telescope (HST)
        - 🌟 NASA APOD
        
        Data sourced from [MAST Archive](https://mast.stsci.edu) 
        and [NASA APIs](https://api.nasa.gov).
        
        Built with ❤️ using Streamlit and astroquery.
        """)
    
    # Main content
    # Featured APOD section
    display_apod_section(api_key)
    
    st.markdown("---")
    
    # Comparison section (if enabled)
    if show_comparison:
        display_comparison_section()
        st.markdown("---")
    
    # Image gallery
    display_image_gallery(
        telescope=telescope,
        object_filter=object_filter if object_filter else None,
        limit=image_limit
    )
    
    # Footer
    st.markdown("---")
    st.markdown(
        '<p style="text-align: center; color: #888;">Built with Streamlit | '
        'Data from MAST & NASA APIs | © 2026</p>',
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
