#!/usr/bin/env python
"""
Quick API test for Organization Restructuring App
"""

import requests
import json
import sys
import time

BASE_URL = "http://localhost:5000/api"

def test_api():
    print("\n" + "=" * 70)
    print("TESTING ORGANIZATION RESTRUCTURING APP API")
    print("=" * 70)
    
    # Wait for server
    time.sleep(2)
    
    tests_passed = 0
    tests_failed = 0
    
    try:
        # Test 1: Health check
        print("\n[1] Testing health check...")
        resp = requests.get(f"{BASE_URL}/health", timeout=5)
        if resp.status_code == 200:
            print("   ✓ Health check passed")
            tests_passed += 1
        else:
            print(f"   ✗ Health check failed: {resp.status_code}")
            tests_failed += 1
        
        # Test 2: Load mock org
        print("\n[2] Loading mock organization...")
        resp = requests.post(f"{BASE_URL}/organization/load-mock", timeout=5)
        if resp.status_code == 200:
            org_data = resp.json()
            print(f"   ✓ Loaded: {org_data['organization']['total_employees']} employees")
            tests_passed += 1
        else:
            print(f"   ✗ Failed to load: {resp.status_code}")
            tests_failed += 1
            return
        
        # Test 3: Overview
        print("\n[3] Getting organization overview...")
        resp = requests.get(f"{BASE_URL}/organization/overview", timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            print(f"   ✓ Headcount: {data['total_headcount']}")
            print(f"   ✓ Total Payroll: ${data['total_payroll']:,.2f}")
            print(f"   ✓ Departments: {len(data['departments'])}")
            tests_passed += 1
        else:
            print(f"   ✗ Failed: {resp.status_code}")
            tests_failed += 1
        
        # Test 4: Critical employees
        print("\n[4] Analyzing critical employees...")
        resp = requests.get(f"{BASE_URL}/analysis/critical-employees", timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            print(f"   ✓ Found {data['critical_count']} critical employees")
            print(f"   ✓ Retention cost: ${data['total_retention_cost']:,.2f}")
            tests_passed += 1
        else:
            print(f"   ✗ Failed: {resp.status_code}")
            tests_failed += 1
        
        # Test 5: Layoff analysis
        print("\n[5] Analyzing layoff options...")
        resp = requests.get(f"{BASE_URL}/analysis/layoff-analysis?reduction_percent=10", timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            print(f"   ✓ Candidates: {data['candidate_count']}")
            print(f"   ✓ Severance cost: ${data['total_layoff_cost']:,.2f}")
            print(f"   ✓ Net savings: ${data['net_savings']:,.2f}")
            tests_passed += 1
        else:
            print(f"   ✗ Failed: {resp.status_code}")
            tests_failed += 1
        
        # Test 6: KPI analysis
        print("\n[6] Running KPI analysis...")
        resp = requests.get(f"{BASE_URL}/analysis/kpis", timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            print(f"   ✓ Analyzed {data['total_kpis']} KPIs")
            tests_passed += 1
        else:
            print(f"   ✗ Failed: {resp.status_code}")
            tests_failed += 1
        
        # Test 7: Create scenarios
        print("\n[7] Creating restructuring scenarios...")
        resp = requests.post(f"{BASE_URL}/restructuring/scenarios", timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            print(f"   ✓ Created {data['scenario_count']} scenarios")
            for scenario in data['scenarios']:
                print(f"     - {scenario['scenario_name']}: {scenario['headcount_reduction']} layoffs, ${scenario['annual_savings']:,.0f} savings")
            tests_passed += 1
        else:
            print(f"   ✗ Failed: {resp.status_code}")
            tests_failed += 1
        
    except requests.exceptions.ConnectionError:
        print("\n✗ ERROR: Cannot connect to backend on port 5000")
        print("  Make sure Flask server is running:")
        print("  cd backend")
        print("  python app.py")
        return 1
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        return 1
    
    # Summary
    print("\n" + "=" * 70)
    print(f"RESULTS: {tests_passed} passed, {tests_failed} failed")
    print("=" * 70)
    
    if tests_failed == 0:
        print("\n✓ All tests passed! The app is ready.")
        print("\nNext steps:")
        print("1. Backend is running on http://localhost:5000")
        print("2. Start frontend: cd frontend && npm start")
        print("3. Open http://localhost:3000 in your browser")
        return 0
    else:
        return 1

if __name__ == '__main__':
    sys.exit(test_api())
