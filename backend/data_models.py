"""Data models and structures for organization restructuring."""

from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
from enum import Enum
import json


class Department(str, Enum):
    """Department enumeration."""
    ENGINEERING = "Engineering"
    SALES = "Sales"
    MARKETING = "Marketing"
    HR = "HR"
    FINANCE = "Finance"
    OPERATIONS = "Operations"
    PRODUCT = "Product"


class EmploymentStatus(str, Enum):
    """Employment status enumeration."""
    ACTIVE = "Active"
    RETAINED = "Retained"
    LAID_OFF = "Laid Off"
    CRITICAL = "Critical"


@dataclass
class Employee:
    """Employee data model."""
    id: str
    name: str
    department: str
    role: str
    salary: float
    tenure_years: int
    performance_score: float  # 0-100
    skills: List[str]
    direct_reports: int
    project_criticality: float  # 0-100
    market_value: float  # relative to salary
    status: str = EmploymentStatus.ACTIVE.value

    def to_dict(self):
        return asdict(self)


@dataclass
class Position:
    """Position/Role data model."""
    id: str
    title: str
    department: str
    salary_band: float
    critical: bool
    headcount: int
    filled_by: List[str]  # employee IDs

    def to_dict(self):
        return asdict(self)


@dataclass
class Organization:
    """Organization data model."""
    name: str
    employees: List[Employee]
    positions: List[Position]
    departments: List[str]

    def to_dict(self):
        return {
            "name": self.name,
            "employees": [e.to_dict() for e in self.employees],
            "positions": [p.to_dict() for p in self.positions],
            "departments": self.departments
        }


@dataclass
class RestructuringRecommendation:
    """Restructuring recommendation."""
    recommendation_type: str  # "retention_incentive", "layoff", "promotion", "restructure"
    employee_id: Optional[str]
    department: str
    action: str
    rationale: str
    impact_score: float  # -1 to 1
    cost_impact: float
    priority: int  # 1-10

    def to_dict(self):
        return asdict(self)


@dataclass
class KPIAnalysis:
    """KPI-based analysis result."""
    kpi_name: str
    current_value: float
    target_value: float
    gap: float
    department: str
    recommendations: List[str]
    required_headcount: Optional[int]

    def to_dict(self):
        return asdict(self)


@dataclass
class RestructuringPlan:
    """Complete restructuring plan."""
    plan_name: str
    scenario_name: str
    current_headcount: int
    target_headcount: int
    estimated_savings: float
    retained_employees: List[str]
    critical_employees: List[str]
    layoffs: List[str]
    recommendations: List[RestructuringRecommendation]
    kpi_analysis: List[KPIAnalysis]
    total_cost: float
    roi_months: float

    def to_dict(self):
        return {
            "plan_name": self.plan_name,
            "scenario_name": self.scenario_name,
            "current_headcount": self.current_headcount,
            "target_headcount": self.target_headcount,
            "estimated_savings": self.estimated_savings,
            "retained_employees": self.retained_employees,
            "critical_employees": self.critical_employees,
            "layoffs": self.layoffs,
            "recommendations": [r.to_dict() for r in self.recommendations],
            "kpi_analysis": [k.to_dict() for k in self.kpi_analysis],
            "total_cost": self.total_cost,
            "roi_months": self.roi_months
        }
