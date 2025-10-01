# Test file for AI Summarizer API
# Demonstrates all summary types with real-world examples

import requests
import json

# API endpoint
BASE_URL = "http://127.0.0.1:8000"

# Test documents for different industries
TEST_DOCUMENTS = {
    "business": """
    The quarterly financial report shows that our company achieved record revenue of $2.5 million, 
    representing a 35% increase from the previous quarter. Sales were particularly strong in the 
    enterprise software division, which contributed 60% of total revenue. However, marketing 
    expenses increased by 40% due to expanded digital advertising campaigns. The engineering 
    team hired 15 new developers, increasing operational costs but positioning us for future 
    product launches. Customer satisfaction scores improved to 4.2 out of 5.0, up from 3.8 
    last quarter. Looking forward, we expect continued growth but will need to optimize 
    marketing spend efficiency.
    """,
    
    "legal": """
    This Software License Agreement is entered into between TechCorp Inc. ("Licensor") 
    and Client Company LLC ("Licensee") effective January 1, 2024. The Licensor grants 
    Licensee a non-exclusive, non-transferable license to use the software for internal 
    business operations only. The license fee is $50,000 annually, payable in quarterly 
    installments of $12,500 by the first day of each quarter. Licensee may not reverse 
    engineer, modify, or redistribute the software without prior written consent. This 
    Agreement automatically terminates if Licensee breaches any material terms. Upon 
    termination, Licensee must cease all use and destroy all copies within 30 days. 
    Licensor provides the software "as is" without warranties and limits liability to 
    the total license fees paid in the preceding 12 months.
    """,
    
    "technical": """
    The system performance analysis reveals that database query response times have 
    increased by 200% over the past month, averaging 1.5 seconds per query. The primary 
    bottleneck is identified in the user authentication module, which processes 10,000 
    requests per minute during peak hours. Memory usage has reached 85% of available 
    capacity on the primary server, causing occasional timeouts. Network latency between 
    the application and database servers averages 45ms. We recommend implementing Redis 
    caching for frequently accessed queries, upgrading to NVMe SSD storage for 40% faster 
    disk I/O, and adding two additional server instances behind a load balancer. These 
    improvements should reduce response times by 60% and handle the projected 50% traffic 
    growth over the next quarter.
    """
}

def test_summary_type(doc_type, text, summary_type):
    """Test a specific summary type"""
    print(f"\n{'='*70}")
    print(f"📄 Testing: {doc_type.upper()} document with {summary_type.upper()} summary")
    print(f"{'='*70}")
    
    payload = {
        "text": text,
        "summary_type": summary_type
    }
    
    try:
        response = requests.post(f"{BASE_URL}/summarize", json=payload)
        
        if response.status_code == 200:
            result = response.json()
            print(f"\n✅ SUCCESS")
            print(f"\n📝 Summary ({result['metadata']['summary_type']}):")
            print(f"{result['summary']}")
            print(f"\n📊 Metrics:")
            print(f"  • Original length: {result['metadata']['original_length']} chars")
            print(f"  • Summary length: {result['metadata']['summary_length']} chars")
            print(f"  • Compression: {result['metadata']['compression_ratio']}")
            print(f"  • Processing time: {result['metadata']['processing_time_seconds']}s")
        else:
            print(f"❌ ERROR: {response.status_code}")
            print(response.json())
            
    except Exception as e:
        print(f"❌ Request failed: {e}")

def test_all_combinations():
    """Test all document types with all summary types"""
    
    print("\n🚀 AI SUMMARIZER API - COMPREHENSIVE TEST SUITE")
    print("Testing all summary types across different document types\n")
    
    # Test health endpoint
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"✅ API Status: {response.json()['status']}")
    except:
        print("❌ API is not running. Start it with: uvicorn summarizer_api:app --reload")
        return
    
    # Test business document with all summary types
    print("\n" + "="*70)
    print("BUSINESS DOCUMENT TESTS")
    print("="*70)
    for summary_type in ["standard", "executive", "financial"]:
        test_summary_type("business", TEST_DOCUMENTS["business"], summary_type)
    
    # Test legal document
    print("\n" + "="*70)
    print("LEGAL DOCUMENT TESTS")
    print("="*70)
    test_summary_type("legal", TEST_DOCUMENTS["legal"], "legal")
    test_summary_type("legal", TEST_DOCUMENTS["legal"], "standard")
    
    # Test technical document
    print("\n" + "="*70)
    print("TECHNICAL DOCUMENT TESTS")
    print("="*70)
    test_summary_type("technical", TEST_DOCUMENTS["technical"], "technical")
    test_summary_type("technical", TEST_DOCUMENTS["technical"], "standard")
    
    print("\n" + "="*70)
    print("✅ ALL TESTS COMPLETED")
    print("="*70)

if __name__ == "__main__":
    test_all_combinations()