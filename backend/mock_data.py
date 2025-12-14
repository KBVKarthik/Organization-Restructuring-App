"""Mock data for the application."""

from data_models import Employee, Position, Organization, Department

# Mock employees
MOCK_EMPLOYEES = [
    # Engineering Department
    Employee(
        id="E001", name="Alice Johnson", department="Engineering", role="Engineering Manager",
        salary=180000, tenure_years=8, performance_score=95, 
        skills=["Python", "Leadership", "System Design"], direct_reports=5, 
        project_criticality=95, market_value=1.3
    ),
    Employee(
        id="E002", name="Bob Smith", department="Engineering", role="Senior Software Engineer",
        salary=160000, tenure_years=6, performance_score=88,
        skills=["Python", "React", "AWS"], direct_reports=0,
        project_criticality=90, market_value=1.4
    ),
    Employee(
        id="E003", name="Carol Davis", department="Engineering", role="Software Engineer",
        salary=120000, tenure_years=2, performance_score=75,
        skills=["JavaScript", "React"], direct_reports=0,
        project_criticality=60, market_value=0.9
    ),
    Employee(
        id="E004", name="David Wilson", department="Engineering", role="Software Engineer",
        salary=118000, tenure_years=1, performance_score=70,
        skills=["Java", "Spring Boot"], direct_reports=0,
        project_criticality=50, market_value=0.8
    ),
    Employee(
        id="E005", name="Emma Brown", department="Engineering", role="DevOps Engineer",
        salary=140000, tenure_years=4, performance_score=92,
        skills=["AWS", "Kubernetes", "Docker"], direct_reports=0,
        project_criticality=88, market_value=1.5
    ),
    Employee(
        id="E006", name="Frank Garcia", department="Engineering", role="QA Engineer",
        salary=105000, tenure_years=3, performance_score=65,
        skills=["Testing", "Automation", "Python"], direct_reports=0,
        project_criticality=45, market_value=0.7
    ),
    
    # Sales Department
    Employee(
        id="S001", name="Grace Lee", department="Sales", role="Sales Director",
        salary=200000, tenure_years=10, performance_score=94,
        skills=["Sales Strategy", "Leadership", "Negotiation"], direct_reports=8,
        project_criticality=98, market_value=1.2
    ),
    Employee(
        id="S002", name="Henry Martinez", department="Sales", role="Senior Account Executive",
        salary=140000, tenure_years=5, performance_score=85,
        skills=["Enterprise Sales", "Negotiation"], direct_reports=0,
        project_criticality=75, market_value=1.1
    ),
    Employee(
        id="S003", name="Iris Chen", department="Sales", role="Account Executive",
        salary=100000, tenure_years=1, performance_score=72,
        skills=["Sales", "Communication"], direct_reports=0,
        project_criticality=40, market_value=0.6
    ),
    Employee(
        id="S004", name="Jack Robinson", department="Sales", role="Account Executive",
        salary=98000, tenure_years=1, performance_score=68,
        skills=["Sales", "Prospecting"], direct_reports=0,
        project_criticality=35, market_value=0.5
    ),
    Employee(
        id="S005", name="Karen White", department="Sales", role="Sales Operations Manager",
        salary=110000, tenure_years=4, performance_score=80,
        skills=["Sales Ops", "Analytics", "Process"], direct_reports=2,
        project_criticality=70, market_value=0.9
    ),
    
    # Marketing Department
    Employee(
        id="M001", name="Leo Anderson", department="Marketing", role="VP Marketing",
        salary=220000, tenure_years=9, performance_score=91,
        skills=["Marketing Strategy", "Leadership", "Analytics"], direct_reports=6,
        project_criticality=96, market_value=1.15
    ),
    Employee(
        id="M002", name="Maya Patel", department="Marketing", role="Senior Marketing Manager",
        salary=130000, tenure_years=4, performance_score=87,
        skills=["Content Marketing", "SEO", "Analytics"], direct_reports=2,
        project_criticality=72, market_value=1.0
    ),
    Employee(
        id="M003", name="Nathan Scott", department="Marketing", role="Digital Marketing Specialist",
        salary=85000, tenure_years=2, performance_score=73,
        skills=["Digital Marketing", "Social Media"], direct_reports=0,
        project_criticality=50, market_value=0.7
    ),
    Employee(
        id="M004", name="Olivia King", department="Marketing", role="Content Writer",
        salary=75000, tenure_years=1, performance_score=65,
        skills=["Content Writing", "Copywriting"], direct_reports=0,
        project_criticality=30, market_value=0.5
    ),
    
    # HR Department
    Employee(
        id="H001", name="Patricia Taylor", department="HR", role="HR Manager",
        salary=110000, tenure_years=7, performance_score=88,
        skills=["Recruitment", "People Management", "Compliance"], direct_reports=2,
        project_criticality=85, market_value=0.95
    ),
    Employee(
        id="H002", name="Quinn Davis", department="HR", role="Recruiter",
        salary=85000, tenure_years=2, performance_score=76,
        skills=["Recruitment", "Sourcing"], direct_reports=0,
        project_criticality=55, market_value=0.75
    ),
    Employee(
        id="H003", name="Rachel Green", department="HR", role="HR Coordinator",
        salary=65000, tenure_years=1, performance_score=70,
        skills=["HR Administration", "Data Entry"], direct_reports=0,
        project_criticality=25, market_value=0.5
    ),
    
    # Finance Department
    Employee(
        id="F001", name="Samuel Brown", department="Finance", role="CFO",
        salary=280000, tenure_years=12, performance_score=96,
        skills=["Financial Strategy", "Leadership", "Analytics"], direct_reports=5,
        project_criticality=99, market_value=1.4
    ),
    Employee(
        id="F002", name="Tina Lopez", department="Finance", role="Senior Accountant",
        salary=120000, tenure_years=5, performance_score=84,
        skills=["Accounting", "Finance", "Reporting"], direct_reports=1,
        project_criticality=75, market_value=0.95
    ),
    Employee(
        id="F003", name="Uma Singh", department="Finance", role="Financial Analyst",
        salary=95000, tenure_years=2, performance_score=78,
        skills=["Financial Analysis", "Excel", "Forecasting"], direct_reports=0,
        project_criticality=60, market_value=0.85
    ),
    
    # Operations Department
    Employee(
        id="O001", name="Victor Chang", department="Operations", role="VP Operations",
        salary=200000, tenure_years=8, performance_score=90,
        skills=["Operations Strategy", "Leadership", "Process Improvement"], direct_reports=4,
        project_criticality=94, market_value=1.25
    ),
    Employee(
        id="O002", name="Wendy Hall", department="Operations", role="Operations Manager",
        salary=115000, tenure_years=4, performance_score=82,
        skills=["Operations", "Process Management"], direct_reports=3,
        project_criticality=70, market_value=0.9
    ),
    Employee(
        id="O003", name="Xander Turner", department="Operations", role="Operations Analyst",
        salary=80000, tenure_years=1, performance_score=68,
        skills=["Data Analysis", "Operations"], direct_reports=0,
        project_criticality=40, market_value=0.65
    ),
]

# Mock positions
MOCK_POSITIONS = [
    Position(id="P001", title="Engineering Manager", department="Engineering", salary_band=180000, critical=True, headcount=2, filled_by=["E001"]),
    Position(id="P002", title="Senior Software Engineer", department="Engineering", salary_band=160000, critical=True, headcount=3, filled_by=["E002"]),
    Position(id="P003", title="Software Engineer", department="Engineering", salary_band=120000, critical=False, headcount=5, filled_by=["E003", "E004"]),
    Position(id="P004", title="DevOps Engineer", department="Engineering", salary_band=140000, critical=True, headcount=2, filled_by=["E005"]),
    Position(id="P005", title="QA Engineer", department="Engineering", salary_band=105000, critical=False, headcount=3, filled_by=["E006"]),
    
    Position(id="P006", title="Sales Director", department="Sales", salary_band=200000, critical=True, headcount=1, filled_by=["S001"]),
    Position(id="P007", title="Senior Account Executive", department="Sales", salary_band=140000, critical=True, headcount=2, filled_by=["S002"]),
    Position(id="P008", title="Account Executive", department="Sales", salary_band=100000, critical=False, headcount=5, filled_by=["S003", "S004"]),
    Position(id="P009", title="Sales Operations Manager", department="Sales", salary_band=110000, critical=False, headcount=1, filled_by=["S005"]),
    
    Position(id="P010", title="VP Marketing", department="Marketing", salary_band=220000, critical=True, headcount=1, filled_by=["M001"]),
    Position(id="P011", title="Senior Marketing Manager", department="Marketing", salary_band=130000, critical=False, headcount=2, filled_by=["M002"]),
    Position(id="P012", title="Digital Marketing Specialist", department="Marketing", salary_band=85000, critical=False, headcount=3, filled_by=["M003"]),
    Position(id="P013", title="Content Writer", department="Marketing", salary_band=75000, critical=False, headcount=2, filled_by=["M004"]),
    
    Position(id="P014", title="HR Manager", department="HR", salary_band=110000, critical=False, headcount=1, filled_by=["H001"]),
    Position(id="P015", title="Recruiter", department="HR", salary_band=85000, critical=False, headcount=2, filled_by=["H002"]),
    Position(id="P016", title="HR Coordinator", department="HR", salary_band=65000, critical=False, headcount=1, filled_by=["H003"]),
    
    Position(id="P017", title="CFO", department="Finance", salary_band=280000, critical=True, headcount=1, filled_by=["F001"]),
    Position(id="P018", title="Senior Accountant", department="Finance", salary_band=120000, critical=False, headcount=2, filled_by=["F002"]),
    Position(id="P019", title="Financial Analyst", department="Finance", salary_band=95000, critical=False, headcount=2, filled_by=["F003"]),
    
    Position(id="P020", title="VP Operations", department="Operations", salary_band=200000, critical=True, headcount=1, filled_by=["O001"]),
    Position(id="P021", title="Operations Manager", department="Operations", salary_band=115000, critical=False, headcount=2, filled_by=["O002"]),
    Position(id="P022", title="Operations Analyst", department="Operations", salary_band=80000, critical=False, headcount=3, filled_by=["O003"]),
]


def get_mock_organization():
    """Get mock organization data."""
    return Organization(
        name="Tech Corp Inc.",
        employees=MOCK_EMPLOYEES,
        positions=MOCK_POSITIONS,
        departments=[dept.value for dept in Department]
    )
