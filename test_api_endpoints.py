#!/usr/bin/env python3
"""
Test script to check all API endpoints
Usage: python test_api_endpoints.py
"""
import requests
import json
from urllib.parse import urljoin

# Your backend URL
BASE_URL = "https://chemical-equipment-parameter-visualizer-1.onrender.com"
API_BASE = f"{BASE_URL}/api"

# Colors for output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'

def test_endpoint(method, endpoint, data=None, headers=None, description=""):
    """Test a single endpoint"""
    url = urljoin(API_BASE + "/", endpoint.lstrip("/"))
    
    try:
        if method == "GET":
            response = requests.get(url, headers=headers, timeout=60)
        elif method == "POST":
            response = requests.post(url, json=data, headers=headers, timeout=60)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers, timeout=60)
        else:
            return False, f"Unsupported method: {method}"
        
        status_ok = 200 <= response.status_code < 400
        status_color = GREEN if status_ok else RED
        
        result = {
            "status": response.status_code,
            "ok": status_ok,
            "response": response.text[:200] if response.text else "No response body"
        }
        
        try:
            result["json"] = response.json()
        except:
            pass
        
        return status_ok, result
        
    except requests.exceptions.RequestException as e:
        return False, {"error": str(e)}

def print_result(name, success, result):
    """Print test result"""
    status_icon = "[PASS]" if success else "[FAIL]"
    status_color = GREEN if success else RED
    
    print(f"{status_color}{status_icon}{RESET} {name}")
    if isinstance(result, dict):
        if "error" in result:
            print(f"   {RED}Error: {result['error']}{RESET}")
        else:
            print(f"   Status: {result.get('status', 'N/A')}")
            if "json" in result:
                print(f"   Response: {json.dumps(result['json'], indent=2)[:200]}")
    print()

def main():
    print(f"\n{'='*60}")
    print(f"Testing API Endpoints: {BASE_URL}")
    print(f"{'='*60}\n")
    
    results = []
    
    # 1. Health Check (No auth required)
    print("1. Testing Health Check...")
    success, result = test_endpoint("GET", "/health/", description="Health check endpoint")
    print_result("Health Check", success, result)
    results.append(("Health Check", success))
    
    # 2. CSRF Token (No auth required)
    print("2. Testing CSRF Token...")
    success, result = test_endpoint("GET", "/auth/csrf/", description="Get CSRF token")
    print_result("CSRF Token", success, result)
    csrf_token = result.get("json", {}).get("csrfToken", "") if isinstance(result, dict) and "json" in result else ""
    results.append(("CSRF Token", success))
    
    # 3. Register (No auth required)
    print("3. Testing User Registration...")
    register_data = {
        "username": f"testuser_{hash(BASE_URL) % 10000}",
        "password": "testpass123",
        "password_confirm": "testpass123",
        "email": "test@example.com"
    }
    success, result = test_endpoint("POST", "/auth/register/", data=register_data, description="User registration")
    print_result("User Registration", success, result)
    results.append(("User Registration", success))
    
    # 4. Login (No auth required)
    print("4. Testing User Login...")
    login_data = {
        "username": register_data["username"],
        "password": register_data["password"]
    }
    success, result = test_endpoint("POST", "/auth/login/", data=login_data, description="User login")
    print_result("User Login", success, result)
    
    # Get session cookie for authenticated requests
    session_cookie = None
    if success and isinstance(result, dict):
        # Try to get cookies from a real request
        try:
            response = requests.post(
                urljoin(API_BASE + "/", "auth/login/"),
                json=login_data,
                timeout=10
            )
            if response.status_code == 200:
                session_cookie = response.cookies.get('sessionid')
        except Exception as e:
            print(f"   Note: Could not get session cookie: {e}")
            pass
    
    results.append(("User Login", success))
    
    # 5. Current User (Requires auth)
    print("5. Testing Current User (requires auth)...")
    headers = {}
    if session_cookie:
        headers['Cookie'] = f'sessionid={session_cookie}'
    success, result = test_endpoint("GET", "/auth/me/", headers=headers, description="Get current user")
    print_result("Current User", success, result)
    results.append(("Current User", success))
    
    # 6. Equipment List (Requires auth)
    print("6. Testing Equipment List (requires auth)...")
    success, result = test_endpoint("GET", "/equipment/", headers=headers, description="List equipment")
    print_result("Equipment List", success, result)
    results.append(("Equipment List", success))
    
    # 7. Equipment Types (Requires auth)
    print("7. Testing Equipment Types (requires auth)...")
    success, result = test_endpoint("GET", "/equipment/types/", headers=headers, description="Get equipment types")
    print_result("Equipment Types", success, result)
    results.append(("Equipment Types", success))
    
    # 8. CSV Uploads List (Requires auth)
    print("8. Testing CSV Uploads List (requires auth)...")
    success, result = test_endpoint("GET", "/uploads/", headers=headers, description="List CSV uploads")
    print_result("CSV Uploads List", success, result)
    results.append(("CSV Uploads List", success))
    
    # 9. Dashboard Summary (Requires auth)
    print("9. Testing Dashboard Summary (requires auth)...")
    success, result = test_endpoint("GET", "/dashboard/summary/", headers=headers, description="Dashboard summary")
    print_result("Dashboard Summary", success, result)
    results.append(("Dashboard Summary", success))
    
    # 10. Flowrate Chart Data (Requires auth)
    print("10. Testing Flowrate Chart Data (requires auth)...")
    success, result = test_endpoint("GET", "/dashboard/flowrate-chart/", headers=headers, description="Flowrate chart data")
    print_result("Flowrate Chart Data", success, result)
    results.append(("Flowrate Chart Data", success))
    
    # 11. Type Distribution Data (Requires auth)
    print("11. Testing Type Distribution Data (requires auth)...")
    success, result = test_endpoint("GET", "/dashboard/type-distribution/", headers=headers, description="Type distribution data")
    print_result("Type Distribution Data", success, result)
    results.append(("Type Distribution Data", success))
    
    # 12. Swagger Documentation
    print("12. Testing Swagger Documentation...")
    try:
        response = requests.get(f"{BASE_URL}/swagger/", timeout=60)
        success = response.status_code == 200
        print_result("Swagger Documentation", success, {"status": response.status_code})
        results.append(("Swagger Documentation", success))
    except Exception as e:
        print_result("Swagger Documentation", False, {"error": str(e)})
        results.append(("Swagger Documentation", False))
    
    # Summary
    print(f"\n{'='*60}")
    print("TEST SUMMARY")
    print(f"{'='*60}\n")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for name, success in results:
        status = f"{GREEN}[PASS]{RESET}" if success else f"{RED}[FAIL]{RESET}"
        print(f"{status} {name}")
    
    print(f"\n{'='*60}")
    print(f"Total: {passed}/{total} endpoints working")
    print(f"{'='*60}\n")
    
    if passed == total:
        print(f"{GREEN}[SUCCESS] All endpoints are working!{RESET}")
    elif passed > 0:
        print(f"{YELLOW}[WARNING] Some endpoints need attention{RESET}")
    else:
        print(f"{RED}[ERROR] No endpoints are working. Check your deployment.{RESET}")

if __name__ == "__main__":
    main()

