# 🌌 Cosmic Canvas: JWST & Hubble Gallery

An interactive Streamlit application for browsing, filtering, and comparing stunning deep-space images from the James Webb Space Telescope (JWST) and Hubble Space Telescope (HST), featuring NASA's Astronomy Picture of the Day.

![JWST & Hubble](https://img.shields.io/badge/JWST%20%26%20Hubble-Gallery-blue)
![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-red.svg)

## ✨ Features

- **📸 Featured APOD**: Display NASA's Astronomy Picture of the Day with full details
- **🔭 Telescope Selection**: Browse images from JWST or Hubble Space Telescope
- **🔍 Smart Filtering**: Search for specific celestial objects by name
- **🖼️ Interactive Gallery**: Grid layout with thumbnails and detailed metadata
- **🔄 Image Comparison**: Side-by-side viewing of the same objects captured by both telescopes
- **⚡ Performance**: Intelligent caching for fast loading and reduced API calls
- **🎨 Modern UI**: Beautiful gradient design with smooth animations

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- pip package manager

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd JamesWebb
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API Key** (Optional - Skip to Step 4 if you want to use the default):
   
   The app works out-of-the-box with NASA's `DEMO_KEY` (30 requests/hour). For higher limits, get a free NASA API key from [api.nasa.gov](https://api.nasa.gov/) and configure it:
   
   **Option A: Using Streamlit Secrets** (Recommended for Streamlit Cloud):
   ```bash
   mkdir -p .streamlit
   cp .streamlit/secrets.toml.example .streamlit/secrets.toml
   # Edit .streamlit/secrets.toml and add your API key
   ```
   
   **Option B: Using Environment Variable**:
   ```bash
   export NASA_API_KEY="your_api_key_here"
   ```
   
   **Note**: If you skip this step, the app will automatically use `DEMO_KEY`.

4. **Run the application**:
   ```bash
   streamlit run app.py
   ```

5. **Open in browser**: The app will automatically open at `http://localhost:8501`

## 📖 Usage

### Browsing Images

1. Use the **sidebar** to select between JWST and Hubble telescopes
2. Enter an object name (e.g., "Andromeda", "Orion Nebula") to filter results
3. Adjust the image limit slider to control how many images are displayed
4. Click on **"View Details"** under any image to see full metadata

### Comparing Images

1. Enable **"Show Image Comparison"** in the sidebar
2. Select a famous celestial object from the dropdown
3. Use the interactive slider (if available) or view side-by-side comparison

### APOD Section

The Astronomy Picture of the Day is always displayed at the top of the page, featuring:
- High-resolution image or video
- Title and publication date
- Detailed explanation
- Copyright information
- Link to HD version

## 🏗️ Architecture

```
JamesWebb/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── utils/
│   ├── __init__.py            # Package initialization
│   ├── apod_api.py            # NASA APOD API client
│   └── mast_api.py            # MAST API client for JWST/HST
└── .streamlit/
    └── secrets.toml.example   # Example secrets configuration
```

### Key Components

- **`utils/apod_api.py`**: Handles NASA APOD API requests with caching and error handling
- **`utils/mast_api.py`**: Queries MAST archive using `astroquery.mast` for telescope observations
- **`app.py`**: Main UI with sidebar controls, image gallery, and comparison features

### Data Sources

- **MAST API**: [Mikulski Archive for Space Telescopes](https://mast.stsci.edu)
- **NASA APOD API**: [Astronomy Picture of the Day](https://api.nasa.gov/planetary/apod)

## ⚙️ Configuration

### API Rate Limits

- **DEMO_KEY**: 30 requests/hour, 50 requests/day
- **Personal API Key**: 1,000 requests/hour

The application uses `@st.cache_data` with 1-hour TTL to minimize API calls.

### Image Limits

Adjust the number of displayed images using the sidebar slider (10-100 images).

## 🛠️ Development

### Running Tests

The application includes comprehensive error handling and graceful fallbacks. To test:

```bash
# Test with demo key
streamlit run app.py

# Test with your API key
NASA_API_KEY="your_key" streamlit run app.py
```

### Adding New Comparison Pairs

Edit `utils/mast_api.py` and add entries to `COMPARISON_PAIRS`:

```python
COMPARISON_PAIRS = {
    "Your Object": {
        "jwst": "url_to_jwst_image",
        "hst": "url_to_hst_image"
    }
}
```

## 📦 Dependencies

- **streamlit**: Web application framework
- **pandas**: Data manipulation and analysis
- **requests**: HTTP library for API calls
- **astroquery**: Astronomy data query library
- **Pillow**: Image processing
- **plotly**: Interactive visualizations (future use)
- **streamlit-image-comparison**: Side-by-side image comparison widget

## 🚢 Deployment

### Streamlit Cloud

1. Push your code to GitHub
2. Sign in to [Streamlit Cloud](https://streamlit.io/cloud)
3. Create a new app and point it to your repository
4. Add your `NASA_API_KEY` in the Secrets section
5. Deploy!

### Local Production

```bash
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

## 🔮 Future Enhancements

- [ ] Add download functionality for full-resolution images
- [ ] Implement advanced filters (instrument, wavelength, exposure time)
- [ ] Create data visualizations showing observation statistics
- [ ] Add favorites/bookmarking system
- [ ] Integration with more space telescope archives
- [ ] Multi-image comparison (3+ telescopes)
- [ ] Timeline view of observations

## 📄 License

This project uses data from NASA and STScI, which are publicly available. Please respect their usage guidelines and provide appropriate attribution.

## 🙏 Credits

- **NASA**: For the APOD API and stunning imagery
- **STScI (Space Telescope Science Institute)**: For MAST archive and both telescopes
- **Streamlit**: For the amazing framework
- **astroquery**: For simplifying astronomical data access

## 🐛 Troubleshooting

### "Rate limit exceeded" error

Switch from `DEMO_KEY` to your personal NASA API key.

### "No preview available" for images

Some observations don't have JPEG/PNG previews in MAST. The app gracefully handles this.

### Images not loading

- Check your internet connection
- Verify API key is configured correctly
- Try reducing the image limit slider

### Import errors

Ensure all dependencies are installed:
```bash
pip install -r requirements.txt --upgrade
```

## 📧 Support

For issues or questions:
- Check the [MAST API documentation](https://mast.stsci.edu/api/v0/)
- Review [NASA API documentation](https://api.nasa.gov/)
- Open an issue on GitHub

---

**Built with ❤️ for space enthusiasts | Data from MAST & NASA APIs**
