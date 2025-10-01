# Error handling tests for AI Summarizer API
# Tests edge cases and validates error responses

import requests

BASE_URL = "http://127.0.0.1:8000"

def test_empty_text():
    """Test with empty text"""
    print("\n" + "="*70)
    print("🧪 TEST: Empty Text")
    print("="*70)
    
    payload = {
        "text": "",
        "summary_type": "standard"
    }
    
    response = requests.post(f"{BASE_URL}/summarize", json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    if response.status_code == 400:
        print("✅ PASS: Correctly rejected empty text")
    else:
        print("❌ FAIL: Should reject empty text with 400 error")

def test_text_too_long():
    """Test with text exceeding limit"""
    print("\n" + "="*70)
    print("🧪 TEST: Text Too Long (>10,000 chars)")
    print("="*70)
    
    # Create text over 10,000 characters
    long_text = "This is a test sentence. " * 500  # ~12,500 chars
    
    payload = {
        "text": long_text,
        "summary_type": "standard"
    }
    
    response = requests.post(f"{BASE_URL}/summarize", json=payload)
    print(f"Text length: {len(long_text)} chars")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    if response.status_code == 400:
        print("✅ PASS: Correctly rejected text over limit")
    else:
        print("❌ FAIL: Should reject text over 10,000 chars")

def test_invalid_summary_type():
    """Test with invalid summary type"""
    print("\n" + "="*70)
    print("🧪 TEST: Invalid Summary Type")
    print("="*70)
    
    payload = {
        "text": "This is a test document.",
        "summary_type": "invalid_type"
    }
    
    response = requests.post(f"{BASE_URL}/summarize", json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    if response.status_code == 422:
        print("✅ PASS: Correctly rejected invalid summary type")
    else:
        print("❌ FAIL: Should reject invalid type with 422 error")

def test_missing_fields():
    """Test with missing required fields"""
    print("\n" + "="*70)
    print("🧪 TEST: Missing Required Fields")
    print("="*70)
    
    payload = {
        "summary_type": "standard"
        # Missing "text" field
    }
    
    response = requests.post(f"{BASE_URL}/summarize", json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    if response.status_code == 422:
        print("✅ PASS: Correctly rejected missing required field")
    else:
        print("❌ FAIL: Should reject missing fields with 422 error")

def test_very_short_text():
    """Test with very short text"""
    print("\n" + "="*70)
    print("🧪 TEST: Very Short Text (Edge Case)")
    print("="*70)
    
    payload = {
        "text": "Revenue increased.",
        "summary_type": "executive"
    }
    
    response = requests.post(f"{BASE_URL}/summarize", json=payload)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ SUCCESS: Handled short text")
        print(f"Summary: {result['summary']}")
        print(f"Processing time: {result['metadata']['processing_time_seconds']}s")
    else:
        print(f"Response: {response.json()}")

def test_special_characters():
    """Test with special characters and formatting"""
    print("\n" + "="*70)
    print("🧪 TEST: Special Characters & Formatting")
    print("="*70)
    
    payload = {
        "text": "Revenue: $2.5M (↑35%). Key metrics—EBITDA @$500K, CAC:$125, LTV:$1,200. Q4'24 outlook: Strong! 🚀",
        "summary_type": "financial"
    }
    
    response = requests.post(f"{BASE_URL}/summarize", json=payload)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ SUCCESS: Handled special characters")
        print(f"Summary: {result['summary']}")
    else:
        print(f"Response: {response.json()}")

def run_all_error_tests():
    """Run complete error test suite"""
    print("\n🧪 AI SUMMARIZER API - ERROR HANDLING TEST SUITE")
    print("="*70)
    
    # Check if API is running
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"✅ API Status: {response.json()['status']}\n")
    except:
        print("❌ API is not running. Start it with: uvicorn summarizer_api:app --reload")
        return
    
    # Run all tests
    test_empty_text()
    test_text_too_long()
    test_invalid_summary_type()
    test_missing_fields()
    test_very_short_text()
    test_special_characters()
    
    print("\n" + "="*70)
    print("✅ ERROR HANDLING TESTS COMPLETED")
    print("="*70)

if __name__ == "__main__":
    run_all_error_tests()