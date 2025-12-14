"""Flask backend for Organization Restructuring App."""

from flask import Flask, request, jsonify
from flask_cors import CORS
from mock_data import get_mock_organization
from analytics import (
    CriticalEmployeeAnalyzer,
    LayoffOptimizer,
    KPIAnalyzer,
    RecommendationEngine,
    RestructuringPlanner,
    HierarchyRestructurer
)
from data_models import Organization, Employee, Position
import json

app = Flask(__name__)
CORS(app)

# Store organization in memory (for testing)
current_organization = None


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'ok', 'message': 'Organization Restructuring API is running'})


@app.route('/api/organization/load-mock', methods=['POST'])
def load_mock_organization():
    """Load mock organization data."""
    global current_organization
    current_organization = get_mock_organization()
    
    return jsonify({
        'success': True,
        'message': 'Mock organization loaded',
        'organization': {
            'name': current_organization.name,
            'total_employees': len(current_organization.employees),
            'departments': current_organization.departments,
            'total_positions': len(current_organization.positions)
        }
    })


@app.route('/api/organization/overview', methods=['GET'])
def get_organization_overview():
    """Get organization overview."""
    if not current_organization:
        return jsonify({'error': 'Organization not loaded'}), 400
    
    # Calculate department distribution
    dept_distribution = {}
    dept_salaries = {}
    for emp in current_organization.employees:
        if emp.department not in dept_distribution:
            dept_distribution[emp.department] = 0
            dept_salaries[emp.department] = 0
        dept_distribution[emp.department] += 1
        dept_salaries[emp.department] += emp.salary
    
    total_payroll = sum(emp.salary for emp in current_organization.employees)
    avg_salary = total_payroll / len(current_organization.employees)
    
    return jsonify({
        'organization_name': current_organization.name,
        'total_headcount': len(current_organization.employees),
        'total_payroll': round(total_payroll, 2),
        'average_salary': round(avg_salary, 2),
        'departments': current_organization.departments,
        'department_distribution': dept_distribution,
        'department_salaries': {k: round(v, 2) for k, v in dept_salaries.items()},
        'total_positions': len(current_organization.positions)
    })


@app.route('/api/employees', methods=['GET'])
def get_employees():
    """Get all employees."""
    if not current_organization:
        return jsonify({'error': 'Organization not loaded'}), 400
    
    return jsonify({
        'employees': [emp.to_dict() for emp in current_organization.employees]
    })


@app.route('/api/employees/<employee_id>', methods=['GET'])
def get_employee(employee_id):
    """Get specific employee."""
    if not current_organization:
        return jsonify({'error': 'Organization not loaded'}), 400
    
    emp = next((e for e in current_organization.employees if e.id == employee_id), None)
    if not emp:
        return jsonify({'error': 'Employee not found'}), 404
    
    return jsonify(emp.to_dict())


@app.route('/api/analysis/critical-employees', methods=['GET'])
def analyze_critical_employees():
    """Analyze and identify critical employees."""
    if not current_organization:
        return jsonify({'error': 'Organization not loaded'}), 400
    
    threshold = request.args.get('threshold', 75, type=float)
    
    critical = CriticalEmployeeAnalyzer.identify_critical_employees(
        current_organization.employees,
        threshold=threshold
    )
    
    critical_data = []
    for emp, score in critical:
        critical_data.append({
            'id': emp.id,
            'name': emp.name,
            'department': emp.department,
            'role': emp.role,
            'salary': emp.salary,
            'criticality_score': round(score, 2),
            'performance_score': emp.performance_score,
            'project_criticality': emp.project_criticality,
            'tenure_years': emp.tenure_years,
            'direct_reports': emp.direct_reports,
            'market_value': emp.market_value
        })
    
    retention_costs = CriticalEmployeeAnalyzer.calculate_retention_cost(
        [emp for emp, _ in critical]
    )
    
    total_retention_cost = sum(retention_costs.values())
    
    return jsonify({
        'critical_employees': critical_data,
        'critical_count': len(critical),
        'total_retention_cost': round(total_retention_cost, 2),
        'retention_costs': {emp_id: round(cost, 2) for emp_id, cost in retention_costs.items()}
    })


@app.route('/api/analysis/layoff-analysis', methods=['GET'])
def analyze_layoffs():
    """Analyze layoff scenarios."""
    if not current_organization:
        return jsonify({'error': 'Organization not loaded'}), 400
    
    target_reduction = request.args.get('reduction_percent', 10, type=float) / 100
    
    layoff_ids = LayoffOptimizer.optimize_layoffs(
        current_organization.employees,
        target_reduction=target_reduction
    )
    
    layoff_details = []
    layoff_cost_map = LayoffOptimizer.calculate_layoff_cost(
        [emp for emp in current_organization.employees if emp.id in layoff_ids]
    )
    
    for emp_id in layoff_ids:
        emp = next((e for e in current_organization.employees if e.id == emp_id), None)
        if emp:
            impact = LayoffOptimizer.calculate_layoff_impact_score(emp)
            layoff_details.append({
                'id': emp.id,
                'name': emp.name,
                'department': emp.department,
                'role': emp.role,
                'salary': emp.salary,
                'tenure_years': emp.tenure_years,
                'impact_score': round(impact, 2),
                'severance_cost': round(layoff_cost_map.get(emp_id, 0), 2),
                'performance_score': emp.performance_score,
                'direct_reports': emp.direct_reports
            })
    
    total_layoff_cost = sum(layoff_cost_map.values())
    salary_savings = sum(emp.salary for emp in current_organization.employees if emp.id in layoff_ids)
    
    return jsonify({
        'layoff_candidates': layoff_details,
        'candidate_count': len(layoff_details),
        'target_reduction_percent': target_reduction * 100,
        'total_layoff_cost': round(total_layoff_cost, 2),
        'estimated_salary_savings': round(salary_savings, 2),
        'net_savings': round(salary_savings - total_layoff_cost, 2)
    })


@app.route('/api/analysis/hierarchy', methods=['GET'])
def analyze_hierarchy():
    """Analyze organizational hierarchy."""
    if not current_organization:
        return jsonify({'error': 'Organization not loaded'}), 400
    
    hierarchy_recs = HierarchyRestructurer.optimize_hierarchy(
        current_organization.employees,
        current_organization.positions
    )
    
    return jsonify({
        'consolidations': hierarchy_recs['consolidations'],
        'promotions': hierarchy_recs['promotions'],
        'restructurings': hierarchy_recs['restructurings'],
        'total_recommendations': len(hierarchy_recs['consolidations']) + len(hierarchy_recs['promotions']) + len(hierarchy_recs['restructurings'])
    })


@app.route('/api/analysis/kpis', methods=['GET'])
def analyze_kpis():
    """Analyze KPIs by department."""
    if not current_organization:
        return jsonify({'error': 'Organization not loaded'}), 400
    
    kpi_analyses = KPIAnalyzer.analyze_all_kpis(current_organization.employees)
    
    kpi_data = []
    for kpi in kpi_analyses:
        kpi_data.append({
            'kpi_name': kpi.kpi_name,
            'department': kpi.department,
            'current_value': kpi.current_value,
            'target_value': kpi.target_value,
            'gap': kpi.gap,
            'status': 'on_track' if abs(kpi.gap) <= 5 else ('below_target' if kpi.gap > 0 else 'exceeds_target'),
            'recommendations': kpi.recommendations,
            'required_headcount': kpi.required_headcount
        })
    
    return jsonify({
        'kpi_analyses': kpi_data,
        'total_kpis': len(kpi_data)
    })


@app.route('/api/restructuring/plan', methods=['POST'])
def create_restructuring_plan():
    """Create a restructuring plan."""
    if not current_organization:
        return jsonify({'error': 'Organization not loaded'}), 400
    
    data = request.get_json()
    plan_name = data.get('plan_name', 'Restructuring Plan')
    scenario_name = data.get('scenario_name', 'Conservative')
    target_reduction = data.get('target_reduction_percent', 10) / 100
    
    plan = RestructuringPlanner.create_plan(
        current_organization,
        plan_name=plan_name,
        scenario_name=scenario_name,
        target_reduction_percentage=target_reduction
    )
    
    return jsonify(plan)


@app.route('/api/restructuring/scenarios', methods=['POST'])
def create_multiple_scenarios():
    """Create multiple restructuring scenarios."""
    if not current_organization:
        return jsonify({'error': 'Organization not loaded'}), 400
    
    scenarios = {
        'conservative': {
            'plan_name': 'Conservative Plan',
            'scenario_name': 'Conservative',
            'target_reduction': 0.05,  # 5%
            'description': 'Minimal restructuring with focus on critical employee retention'
        },
        'moderate': {
            'plan_name': 'Moderate Plan',
            'scenario_name': 'Moderate',
            'target_reduction': 0.10,  # 10%
            'description': 'Balanced approach with selective layoffs and restructuring'
        },
        'aggressive': {
            'plan_name': 'Aggressive Plan',
            'scenario_name': 'Aggressive',
            'target_reduction': 0.20,  # 20%
            'description': 'Significant restructuring for maximum cost reduction'
        }
    }
    
    plans = []
    for scenario_key, scenario_config in scenarios.items():
        plan = RestructuringPlanner.create_plan(
            current_organization,
            plan_name=scenario_config['plan_name'],
            scenario_name=scenario_config['scenario_name'],
            target_reduction_percentage=scenario_config['target_reduction']
        )
        plan['description'] = scenario_config['description']
        plans.append(plan)
    
    return jsonify({
        'scenarios': plans,
        'scenario_count': len(plans)
    })


@app.route('/api/department-stats/<department>', methods=['GET'])
def get_department_stats(department):
    """Get statistics for a specific department."""
    if not current_organization:
        return jsonify({'error': 'Organization not loaded'}), 400
    
    dept_employees = [e for e in current_organization.employees if e.department == department]
    
    if not dept_employees:
        return jsonify({'error': 'Department not found'}), 404
    
    total_salary = sum(e.salary for e in dept_employees)
    avg_salary = total_salary / len(dept_employees)
    avg_performance = sum(e.performance_score for e in dept_employees) / len(dept_employees)
    avg_tenure = sum(e.tenure_years for e in dept_employees) / len(dept_employees)
    total_reports = sum(e.direct_reports for e in dept_employees)
    
    return jsonify({
        'department': department,
        'headcount': len(dept_employees),
        'total_salary': round(total_salary, 2),
        'average_salary': round(avg_salary, 2),
        'average_performance': round(avg_performance, 2),
        'average_tenure': round(avg_tenure, 2),
        'total_direct_reports': total_reports,
        'employees': [
            {
                'id': e.id,
                'name': e.name,
                'role': e.role,
                'salary': e.salary,
                'performance_score': e.performance_score,
                'tenure_years': e.tenure_years
            }
            for e in dept_employees
        ]
    })


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    # Load mock data on startup
    current_organization = get_mock_organization()
    print(f"Loaded {len(current_organization.employees)} employees from mock data")
    
    # Run Flask app
    app.run(debug=False, port=5000, host='0.0.0.0', use_reloader=False)
