#!/usr/bin/env python
"""
Comprehensive testing script for Organization Restructuring App
Tests all major features and validates API endpoints
"""

import requests
import json
import sys
import time
from typing import Dict, Any

BASE_URL = "http://localhost:5000/api"

class APITester:
    def __init__(self):
        self.results = []
        self.passed = 0
        self.failed = 0
    
    def test_endpoint(self, method: str, endpoint: str, name: str, expected_status: int = 200, data: Dict = None) -> bool:
        """Test an API endpoint."""
        try:
            url = f"{BASE_URL}{endpoint}"
            if method == 'GET':
                response = requests.get(url, timeout=10)
            elif method == 'POST':
                response = requests.post(url, json=data, timeout=10)
            else:
                return False
            
            success = response.status_code == expected_status
            
            if success:
                self.passed += 1
                self.results.append((name, "✓ PASS", response.status_code))
                return True
            else:
                self.failed += 1
                self.results.append((name, "✗ FAIL", f"Status {response.status_code}"))
                return False
        except requests.exceptions.ConnectionError:
            self.failed += 1
            self.results.append((name, "✗ ERROR", "Connection refused - Backend not running?"))
            return False
        except Exception as e:
            self.failed += 1
            self.results.append((name, "✗ ERROR", str(e)))
            return False
    
    def print_results(self):
        """Print test results."""
        print("\n" + "=" * 70)
        print("TEST RESULTS")
        print("=" * 70)
        
        for test_name, status, details in self.results:
            print(f"{status:8} | {test_name:40} | {details}")
        
        print("\n" + "=" * 70)
        print(f"TOTAL: {self.passed + self.failed} tests | {self.passed} passed | {self.failed} failed")
        print("=" * 70)
        
        return self.failed == 0


def main():
    print("\n" + "=" * 70)
    print("ORGANIZATION RESTRUCTURING APP - API TEST SUITE")
    print("=" * 70)
    print("\nTesting API endpoints... (ensure backend is running on port 5000)")
    
    # Wait a moment for server to be ready
    time.sleep(1)
    
    tester = APITester()
    
    # Test 1: Health check
    print("\n[1/4] Testing Basic Endpoints...")
    tester.test_endpoint('GET', '/health', 'Health Check', 200)
    
    # Test 2: Load mock data
    print("\n[2/4] Testing Organization Loading...")
    tester.test_endpoint('POST', '/organization/load-mock', 'Load Mock Organization', 200)
    tester.test_endpoint('GET', '/organization/overview', 'Get Organization Overview', 200)
    tester.test_endpoint('GET', '/employees', 'Get All Employees', 200)
    
    # Test 3: Analysis endpoints
    print("\n[3/4] Testing Analysis Endpoints...")
    tester.test_endpoint('GET', '/analysis/critical-employees', 'Critical Employee Analysis', 200)
    tester.test_endpoint('GET', '/analysis/layoff-analysis', 'Layoff Analysis', 200)
    tester.test_endpoint('GET', '/analysis/hierarchy', 'Hierarchy Analysis', 200)
    tester.test_endpoint('GET', '/analysis/kpis', 'KPI Analysis', 200)
    tester.test_endpoint('GET', '/department-stats/Engineering', 'Department Statistics', 200)
    
    # Test 4: Restructuring endpoints
    print("\n[4/4] Testing Restructuring Endpoints...")
    tester.test_endpoint('POST', '/restructuring/plan', 'Create Restructuring Plan', 200, 
                        {'plan_name': 'Test Plan', 'scenario_name': 'Test', 'target_reduction_percent': 10})
    tester.test_endpoint('POST', '/restructuring/scenarios', 'Create Multiple Scenarios', 200)
    
    # Print summary
    success = tester.print_results()
    
    if success:
        print("\n✓ All API tests passed! The app is ready to use.")
        print("\nTo run the full application:")
        print("1. Backend is running on http://localhost:5000")
        print("2. Start frontend with: npm start (from frontend directory)")
        print("3. Open http://localhost:3000 in your browser")
        return 0
    else:
        print("\n✗ Some tests failed. Check the backend server.")
        return 1


if __name__ == '__main__':
    sys.exit(main())
