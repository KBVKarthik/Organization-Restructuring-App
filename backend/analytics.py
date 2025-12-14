"""Analytics and algorithms for organization restructuring."""

import math
from typing import List, Dict, Tuple
from data_models import Employee, Position, Organization, RestructuringRecommendation, KPIAnalysis, EmploymentStatus
import pandas as pd
import numpy as np


class CriticalEmployeeAnalyzer:
    """Analyze and identify critical employees for retention."""
    
    @staticmethod
    def calculate_criticality_score(employee: Employee) -> float:
        """Calculate overall criticality score for an employee (0-100)."""
        weights = {
            'performance': 0.25,
            'project_criticality': 0.30,
            'tenure': 0.15,
            'market_value': 0.20,
            'direct_reports': 0.10
        }
        
        # Normalize metrics
        performance_norm = employee.performance_score
        criticality_norm = employee.project_criticality
        tenure_norm = min(employee.tenure_years * 10, 100)  # Cap at 100
        market_norm = min(employee.market_value * 50, 100)  # Normalize to 0-100
        reports_norm = min(employee.direct_reports * 10, 100)  # Cap at 100
        
        score = (
            weights['performance'] * performance_norm +
            weights['project_criticality'] * criticality_norm +
            weights['tenure'] * tenure_norm +
            weights['market_value'] * market_norm +
            weights['direct_reports'] * reports_norm
        )
        
        return min(score, 100)
    
    @staticmethod
    def identify_critical_employees(employees: List[Employee], threshold: float = 75.0) -> List[Tuple[Employee, float]]:
        """Identify critical employees above threshold."""
        employee_scores = [
            (emp, CriticalEmployeeAnalyzer.calculate_criticality_score(emp))
            for emp in employees
        ]
        critical = [(emp, score) for emp, score in employee_scores if score >= threshold]
        return sorted(critical, key=lambda x: x[1], reverse=True)
    
    @staticmethod
    def calculate_retention_cost(employees: List[Employee]) -> Dict[str, float]:
        """Calculate retention costs (bonuses, equity grants)."""
        costs = {}
        for emp in employees:
            # Retention bonus: 10-30% of salary based on criticality
            score = CriticalEmployeeAnalyzer.calculate_criticality_score(emp)
            bonus_percentage = 0.10 + (score - 50) * 0.004  # 10% to 30%
            retention_bonus = emp.salary * bonus_percentage
            costs[emp.id] = retention_bonus
        return costs


class LayoffOptimizer:
    """Optimize layoff strategy while minimizing operational impact."""
    
    @staticmethod
    def calculate_layoff_impact_score(employee: Employee) -> float:
        """Calculate impact of laying off employee (higher = worse impact)."""
        weights = {
            'direct_reports': 0.25,
            'project_criticality': 0.35,
            'performance': 0.25,
            'tenure': 0.15
        }
        
        # Normalize metrics
        reports_impact = min(employee.direct_reports * 10, 100)
        criticality_impact = employee.project_criticality
        performance_impact = employee.performance_score
        tenure_impact = min(employee.tenure_years * 8, 100)
        
        impact = (
            weights['direct_reports'] * reports_impact +
            weights['project_criticality'] * criticality_impact +
            weights['performance'] * performance_impact +
            weights['tenure'] * tenure_impact
        )
        
        return min(impact, 100)
    
    @staticmethod
    def calculate_layoff_cost(employees: List[Employee]) -> Dict[str, float]:
        """Calculate severance and other layoff costs."""
        costs = {}
        for emp in employees:
            # Severance: 1 week per year of tenure + 4 weeks minimum
            weeks = max(4, emp.tenure_years)
            weekly_pay = emp.salary / 52
            severance = weekly_pay * weeks
            
            # Add benefits continuation (30 days)
            benefits = weekly_pay * 4.3 * 0.5  # 50% of salary for benefits
            
            costs[emp.id] = severance + benefits
        return costs
    
    @staticmethod
    def optimize_layoffs(employees: List[Employee], target_reduction: float = 0.15) -> List[str]:
        """
        Optimize which employees to lay off.
        
        Args:
            employees: List of employees
            target_reduction: Target percentage reduction (0.15 = 15%)
        
        Returns:
            List of employee IDs to lay off
        """
        target_count = math.ceil(len(employees) * target_reduction)
        
        # Score employees by combination of low impact, low criticality, and low cost
        candidates = []
        for emp in employees:
            impact_score = LayoffOptimizer.calculate_layoff_impact_score(emp)
            criticality_score = CriticalEmployeeAnalyzer.calculate_criticality_score(emp)
            
            # Combine: prefer high impact to organizational structure (low score)
            # and low criticality
            layoff_worthiness = 100 - impact_score + (100 - criticality_score) * 0.5
            candidates.append((emp.id, layoff_worthiness, impact_score, emp.salary))
        
        # Sort by layoff worthiness (descending) and take bottom N
        candidates.sort(key=lambda x: x[1])
        layoff_ids = [emp_id for emp_id, _, _, _ in candidates[:target_count]]
        
        return layoff_ids


class HierarchyRestructurer:
    """Handle organizational hierarchy restructuring."""
    
    @staticmethod
    def optimize_hierarchy(employees: List[Employee], positions: List[Position]) -> Dict:
        """
        Optimize hierarchy to eliminate redundancies.
        Returns mapping of employees to optimized roles.
        """
        # Analyze span of control
        max_direct_reports = max([emp.direct_reports for emp in employees] or [0])
        avg_direct_reports = np.mean([emp.direct_reports for emp in employees])
        
        recommendations = {
            'consolidations': [],
            'promotions': [],
            'restructurings': []
        }
        
        # Identify managers with very few reports for consolidation
        for emp in employees:
            if 0 < emp.direct_reports < 3:
                # Could consolidate with another manager
                if emp.performance_score < 80:
                    recommendations['consolidations'].append({
                        'employee_id': emp.id,
                        'employee_name': emp.name,
                        'current_reports': emp.direct_reports,
                        'recommendation': 'Consolidate team with another manager'
                    })
            elif emp.direct_reports > 8:
                # Could split team
                recommendations['consolidations'].append({
                    'employee_id': emp.id,
                    'employee_name': emp.name,
                    'current_reports': emp.direct_reports,
                    'recommendation': 'Split team - hire another manager'
                })
        
        return recommendations


class KPIAnalyzer:
    """Analyze organization against KPIs and suggest restructuring."""
    
    DEPARTMENTAL_KPIS = {
        'Engineering': {
            'code_quality': {'metric': 'performance_score', 'target': 85, 'weight': 0.3},
            'productivity': {'metric': 'direct_reports', 'target': 5, 'weight': 0.3},
            'stability': {'metric': 'tenure_years', 'target': 4, 'weight': 0.2},
            'cost_efficiency': {'metric': 'salary', 'target': 130000, 'weight': 0.2}
        },
        'Sales': {
            'performance': {'metric': 'performance_score', 'target': 80, 'weight': 0.4},
            'experience': {'metric': 'tenure_years', 'target': 3, 'weight': 0.3},
            'cost_efficiency': {'metric': 'salary', 'target': 120000, 'weight': 0.3}
        },
        'Marketing': {
            'performance': {'metric': 'performance_score', 'target': 80, 'weight': 0.4},
            'creativity': {'metric': 'skills_count', 'target': 3, 'weight': 0.3},
            'cost_efficiency': {'metric': 'salary', 'target': 110000, 'weight': 0.3}
        },
        'Finance': {
            'accuracy': {'metric': 'performance_score', 'target': 85, 'weight': 0.4},
            'experience': {'metric': 'tenure_years', 'target': 4, 'weight': 0.3},
            'cost_efficiency': {'metric': 'salary', 'target': 125000, 'weight': 0.3}
        },
        'HR': {
            'performance': {'metric': 'performance_score', 'target': 80, 'weight': 0.4},
            'experience': {'metric': 'tenure_years', 'target': 3, 'weight': 0.3},
            'cost_efficiency': {'metric': 'salary', 'target': 90000, 'weight': 0.3}
        },
        'Operations': {
            'efficiency': {'metric': 'performance_score', 'target': 80, 'weight': 0.4},
            'experience': {'metric': 'tenure_years', 'target': 3, 'weight': 0.3},
            'cost_efficiency': {'metric': 'salary', 'target': 110000, 'weight': 0.3}
        }
    }
    
    @staticmethod
    def analyze_department_kpis(employees: List[Employee], department: str) -> List[KPIAnalysis]:
        """Analyze KPIs for a specific department."""
        dept_employees = [e for e in employees if e.department == department]
        
        if not dept_employees:
            return []
        
        kpi_results = []
        kpis = KPIAnalyzer.DEPARTMENTAL_KPIS.get(department, {})
        
        for kpi_name, kpi_config in kpis.items():
            metric = kpi_config['metric']
            target = kpi_config['target']
            
            # Calculate current average
            if metric == 'salary':
                current = np.mean([e.salary for e in dept_employees])
            elif metric == 'performance_score':
                current = np.mean([e.performance_score for e in dept_employees])
            elif metric == 'tenure_years':
                current = np.mean([e.tenure_years for e in dept_employees])
            elif metric == 'direct_reports':
                current = np.mean([e.direct_reports for e in dept_employees]) if dept_employees else 0
            elif metric == 'skills_count':
                current = np.mean([len(e.skills) for e in dept_employees])
            else:
                current = 0
            
            gap = target - current
            
            # Generate recommendations
            recommendations = []
            if gap > 10:
                if metric == 'performance_score':
                    recommendations.append("Implement training and development programs")
                    recommendations.append("Consider performance improvement plans")
                elif metric == 'salary':
                    recommendations.append("Review compensation structure")
                    recommendations.append("Consider consolidating roles to reduce headcount")
                elif metric == 'tenure_years':
                    recommendations.append("Implement retention programs")
                    recommendations.append("Improve employee engagement")
            elif gap < -10:
                if metric == 'salary':
                    recommendations.append("Current compensation is above target - optimize spend")
                elif metric == 'performance_score':
                    recommendations.append("Excellent performance - maintain current staffing")
            
            # Calculate required headcount adjustments
            required_headcount = None
            if metric == 'salary' and gap > 0:
                required_headcount = int(len(dept_employees) * 0.9)  # Reduce by 10%
            
            kpi_results.append(KPIAnalysis(
                kpi_name=kpi_name,
                current_value=round(current, 2),
                target_value=float(target),
                gap=round(gap, 2),
                department=department,
                recommendations=recommendations,
                required_headcount=required_headcount
            ))
        
        return kpi_results
    
    @staticmethod
    def analyze_all_kpis(employees: List[Employee]) -> List[KPIAnalysis]:
        """Analyze KPIs across all departments."""
        all_kpis = []
        departments = set(e.department for e in employees)
        
        for dept in departments:
            all_kpis.extend(KPIAnalyzer.analyze_department_kpis(employees, dept))
        
        return all_kpis


class RecommendationEngine:
    """Generate comprehensive restructuring recommendations."""
    
    @staticmethod
    def generate_recommendations(
        organization: Organization,
        critical_employees: List[Tuple[Employee, float]],
        layoff_candidates: List[str],
        kpi_analyses: List[KPIAnalysis]
    ) -> List[RestructuringRecommendation]:
        """Generate restructuring recommendations."""
        recommendations = []
        
        # 1. Retention incentives for critical employees
        for emp, score in critical_employees[:5]:  # Top 5 critical
            if emp.performance_score >= 85:
                retention_cost = emp.salary * 0.15  # 15% bonus
                rec = RestructuringRecommendation(
                    recommendation_type='retention_incentive',
                    employee_id=emp.id,
                    department=emp.department,
                    action=f'Offer {int(retention_cost):,} retention bonus to {emp.name}',
                    rationale=f'Critical employee with {score:.1f}/100 criticality score. Retaining this talent is essential.',
                    impact_score=0.8,
                    cost_impact=retention_cost,
                    priority=1
                )
                recommendations.append(rec)
        
        # 2. Layoff recommendations
        layoff_cost_map = LayoffOptimizer.calculate_layoff_cost(organization.employees)
        for emp_id in layoff_candidates[:3]:  # Top 3 candidates
            emp = next((e for e in organization.employees if e.id == emp_id), None)
            if emp:
                impact = LayoffOptimizer.calculate_layoff_impact_score(emp)
                cost = layoff_cost_map.get(emp_id, 0)
                rec = RestructuringRecommendation(
                    recommendation_type='layoff',
                    employee_id=emp_id,
                    department=emp.department,
                    action=f'Consider layoff of {emp.name} ({emp.role})',
                    rationale=f'Low organizational impact ({impact:.1f}/100). Minimal disruption expected.',
                    impact_score=-0.5,
                    cost_impact=-cost,
                    priority=3
                )
                recommendations.append(rec)
        
        # 3. Hierarchy restructuring
        hierarchy_recs = HierarchyRestructurer.optimize_hierarchy(organization.employees, organization.positions)
        for consolidation in hierarchy_recs['consolidations']:
            emp = next((e for e in organization.employees if e.id == consolidation['employee_id']), None)
            if emp:
                rec = RestructuringRecommendation(
                    recommendation_type='restructure',
                    employee_id=emp.id,
                    department=emp.department,
                    action=consolidation['recommendation'],
                    rationale=f"{emp.name} has {consolidation['current_reports']} direct reports. Span of control adjustment needed.",
                    impact_score=0.2,
                    cost_impact=0,
                    priority=5
                )
                recommendations.append(rec)
        
        # 4. KPI-based recommendations
        for kpi in kpi_analyses:
            if kpi.recommendations:
                for rec_text in kpi.recommendations[:1]:  # Top recommendation per KPI
                    rec = RestructuringRecommendation(
                        recommendation_type='optimization',
                        employee_id=None,
                        department=kpi.department,
                        action=rec_text,
                        rationale=f"KPI '{kpi.kpi_name}' gap: {kpi.gap:.1f} from target",
                        impact_score=0.3 if 'training' in rec_text.lower() else 0.5,
                        cost_impact=5000 if 'training' in rec_text.lower() else 0,
                        priority=4
                    )
                    recommendations.append(rec)
        
        # Sort by priority
        recommendations.sort(key=lambda x: x.priority)
        
        return recommendations


class RestructuringPlanner:
    """Create comprehensive restructuring plans."""
    
    @staticmethod
    def create_plan(
        organization: Organization,
        plan_name: str = "Restructuring Plan",
        scenario_name: str = "Conservative",
        target_reduction_percentage: float = 0.10
    ) -> Dict:
        """Create a comprehensive restructuring plan."""
        
        # 1. Identify critical employees
        critical = CriticalEmployeeAnalyzer.identify_critical_employees(
            organization.employees,
            threshold=75.0
        )
        critical_ids = [emp.id for emp, _ in critical]
        
        # 2. Optimize layoffs
        layoff_ids = LayoffOptimizer.optimize_layoffs(
            organization.employees,
            target_reduction=target_reduction_percentage
        )
        
        # 3. Analyze KPIs
        kpi_analyses = KPIAnalyzer.analyze_all_kpis(organization.employees)
        
        # 4. Generate recommendations
        recommendations = RecommendationEngine.generate_recommendations(
            organization,
            critical,
            layoff_ids,
            kpi_analyses
        )
        
        # 5. Calculate costs and savings
        retention_costs = CriticalEmployeeAnalyzer.calculate_retention_cost(
            [emp for emp, _ in critical]
        )
        layoff_costs = LayoffOptimizer.calculate_layoff_cost(
            [emp for emp in organization.employees if emp.id in layoff_ids]
        )
        
        total_retention_cost = sum(retention_costs.values())
        total_layoff_cost = sum(layoff_costs.values())
        
        # Salary savings from layoffs
        salary_savings = sum(
            emp.salary for emp in organization.employees
            if emp.id in layoff_ids
        )
        
        # Annual savings
        annual_savings = salary_savings - total_retention_cost
        
        # Implementation cost
        implementation_cost = total_retention_cost + total_layoff_cost
        
        # ROI
        roi_months = (implementation_cost / annual_savings * 12) if annual_savings > 0 else 0
        
        retained_ids = [
            emp.id for emp in organization.employees
            if emp.id not in layoff_ids
        ]
        
        return {
            'plan_name': plan_name,
            'scenario_name': scenario_name,
            'current_headcount': len(organization.employees),
            'target_headcount': len(retained_ids),
            'headcount_reduction': len(layoff_ids),
            'estimated_savings': round(annual_savings, 2),
            'retained_employees': retained_ids,
            'critical_employees': critical_ids,
            'layoffs': layoff_ids,
            'recommendations': [r.to_dict() for r in recommendations],
            'kpi_analysis': [k.to_dict() for k in kpi_analyses],
            'total_cost': round(implementation_cost, 2),
            'retention_cost': round(total_retention_cost, 2),
            'layoff_cost': round(total_layoff_cost, 2),
            'annual_savings': round(annual_savings, 2),
            'roi_months': round(roi_months, 1),
            'critical_count': len(critical_ids),
            'critical_details': [(emp.id, emp.name, emp.department, round(score, 1)) for emp, score in critical]
        }
