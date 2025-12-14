"""
Demonstration of API responses from the Organization Restructuring App
This script shows example JSON output from the API endpoints
"""

import json
from pathlib import Path
import sys

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / 'backend'))

from mock_data import get_mock_organization
from analytics import (
    CriticalEmployeeAnalyzer,
    LayoffOptimizer,
    KPIAnalyzer,
    RecommendationEngine,
    RestructuringPlanner,
)

def demo():
    print("\n" + "=" * 80)
    print("ORGANIZATION RESTRUCTURING APP - API RESPONSE EXAMPLES")
    print("=" * 80)
    
    # Load organization
    org = get_mock_organization()
    
    # 1. Organization Overview
    print("\n1. GET /api/organization/overview")
    print("-" * 80)
    dept_distribution = {}
    dept_salaries = {}
    for emp in org.employees:
        if emp.department not in dept_distribution:
            dept_distribution[emp.department] = 0
            dept_salaries[emp.department] = 0
        dept_distribution[emp.department] += 1
        dept_salaries[emp.department] += emp.salary
    
    overview = {
        "organization_name": org.name,
        "total_headcount": len(org.employees),
        "total_payroll": sum(emp.salary for emp in org.employees),
        "average_salary": sum(emp.salary for emp in org.employees) / len(org.employees),
        "departments": org.departments,
        "department_distribution": dept_distribution,
        "total_positions": len(org.positions)
    }
    print(json.dumps(overview, indent=2))
    
    # 2. Critical Employees
    print("\n2. GET /api/analysis/critical-employees")
    print("-" * 80)
    critical = CriticalEmployeeAnalyzer.identify_critical_employees(org.employees, threshold=75)
    retention_costs = CriticalEmployeeAnalyzer.calculate_retention_cost([emp for emp, _ in critical])
    
    critical_response = {
        "critical_employees": [
            {
                "id": emp.id,
                "name": emp.name,
                "department": emp.department,
                "role": emp.role,
                "salary": emp.salary,
                "criticality_score": round(score, 2),
                "performance_score": emp.performance_score
            }
            for emp, score in critical[:3]
        ],
        "critical_count": len(critical),
        "total_retention_cost": round(sum(retention_costs.values()), 2)
    }
    print(json.dumps(critical_response, indent=2))
    
    # 3. Layoff Analysis
    print("\n3. GET /api/analysis/layoff-analysis")
    print("-" * 80)
    layoff_ids = LayoffOptimizer.optimize_layoffs(org.employees, target_reduction=0.10)
    layoff_costs = LayoffOptimizer.calculate_layoff_cost(
        [emp for emp in org.employees if emp.id in layoff_ids]
    )
    salary_savings = sum(emp.salary for emp in org.employees if emp.id in layoff_ids)
    
    layoff_candidates = []
    for emp_id in layoff_ids[:2]:
        emp = next((e for e in org.employees if e.id == emp_id), None)
        if emp:
            layoff_candidates.append({
                "id": emp.id,
                "name": emp.name,
                "department": emp.department,
                "role": emp.role,
                "salary": emp.salary,
                "severance_cost": round(layoff_costs.get(emp_id, 0), 2)
            })
    
    layoff_response = {
        "layoff_candidates": layoff_candidates,
        "candidate_count": len(layoff_ids),
        "total_layoff_cost": round(sum(layoff_costs.values()), 2),
        "estimated_salary_savings": round(salary_savings, 2),
        "net_savings": round(salary_savings - sum(layoff_costs.values()), 2)
    }
    print(json.dumps(layoff_response, indent=2))
    
    # 4. KPI Analysis
    print("\n4. GET /api/analysis/kpis (sample)")
    print("-" * 80)
    kpi_analyses = KPIAnalyzer.analyze_all_kpis(org.employees)
    kpi_sample = [
        {
            "kpi_name": kpi.kpi_name,
            "department": kpi.department,
            "current_value": kpi.current_value,
            "target_value": kpi.target_value,
            "gap": kpi.gap,
            "recommendations": kpi.recommendations[:1] if kpi.recommendations else []
        }
        for kpi in kpi_analyses[:4]
    ]
    print(json.dumps({"kpi_analyses": kpi_sample, "total_kpis": len(kpi_analyses)}, indent=2))
    
    # 5. Restructuring Scenarios
    print("\n5. POST /api/restructuring/scenarios")
    print("-" * 80)
    scenarios_data = []
    for scenario_name, reduction in [("Conservative", 0.05), ("Moderate", 0.10)]:
        plan = RestructuringPlanner.create_plan(
            org,
            plan_name=f"{scenario_name} Plan",
            scenario_name=scenario_name,
            target_reduction_percentage=reduction
        )
        scenarios_data.append({
            "scenario_name": plan["scenario_name"],
            "headcount_reduction": plan["headcount_reduction"],
            "estimated_savings": plan["estimated_savings"],
            "total_cost": plan["total_cost"],
            "roi_months": plan["roi_months"],
            "critical_count": plan["critical_count"]
        })
    
    print(json.dumps({
        "scenarios": scenarios_data,
        "scenario_count": len(scenarios_data)
    }, indent=2))
    
    print("\n" + "=" * 80)
    print("END OF API RESPONSE EXAMPLES")
    print("=" * 80)
    print("\nFor complete API documentation, see README.md")

if __name__ == '__main__':
    demo()
