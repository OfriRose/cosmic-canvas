"""
Simple test script to verify API integrations work correctly.
This is not a comprehensive test suite, but a quick verification.
"""

import sys
import os

# Add parent directory to path to import utils
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_apod_api():
    """Test NASA APOD API integration."""
    print("Testing NASA APOD API...")
    try:
        # Import without streamlit context
        import requests
        
        # Direct API call to test
        response = requests.get(
            "https://api.nasa.gov/planetary/apod",
            params={"api_key": "DEMO_KEY"},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✓ APOD API working! Today's title: {data.get('title', 'N/A')}")
            return True
        else:
            print(f"✗ APOD API returned status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ APOD API test failed: {e}")
        return False


def test_mast_api():
    """Test MAST API integration."""
    print("\nTesting MAST API (astroquery)...")
    try:
        from astroquery.mast import Observations
        
        # Simple query
        observations = Observations.query_criteria(
            obs_collection="JWST",
            dataproduct_type="image",
        )
        
        if len(observations) > 0:
            print(f"✓ MAST API working! Found {len(observations)} JWST observations")
            print(f"  First observation: {observations[0]['target_name']}")
            return True
        else:
            print("✗ MAST API returned no observations")
            return False
    except Exception as e:
        print(f"✗ MAST API test failed: {e}")
        return False


def test_imports():
    """Test that all required modules can be imported."""
    print("\nTesting imports...")
    modules = [
        'streamlit',
        'pandas',
        'requests',
        'astroquery',
        'PIL',
        'plotly'
    ]
    
    all_success = True
    for module in modules:
        try:
            __import__(module)
            print(f"✓ {module}")
        except ImportError as e:
            print(f"✗ {module}: {e}")
            all_success = False
    
    # Test optional module
    try:
        __import__('streamlit_image_comparison')
        print(f"✓ streamlit_image_comparison (optional)")
    except ImportError:
        print(f"⚠ streamlit_image_comparison (optional) - not installed, will use fallback")
    
    return all_success


def main():
    """Run all tests."""
    print("=" * 60)
    print("Cosmic Canvas - API Integration Tests")
    print("=" * 60)
    
    results = {
        "Imports": test_imports(),
        "APOD API": test_apod_api(),
        "MAST API": test_mast_api()
    }
    
    print("\n" + "=" * 60)
    print("Test Summary:")
    print("=" * 60)
    
    for test, passed in results.items():
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{test}: {status}")
    
    all_passed = all(results.values())
    
    if all_passed:
        print("\n🎉 All tests passed! The application is ready to run.")
        print("\nTo start the app, run:")
        print("  ./venv/bin/streamlit run app.py")
    else:
        print("\n⚠ Some tests failed. Please check the errors above.")
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
