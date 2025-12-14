# Organization Restructuring App

A comprehensive application for planning organization restructuring with intelligent analytics, KPI-based recommendations, and beautiful visualizations.

## Features

### Core Capabilities

- **Critical Employee Analysis**: Identifies critical employees based on performance, project criticality, tenure, market value, and direct reports
- **Layoff Optimization**: Intelligently recommends layoff candidates while minimizing operational impact
- **Hierarchy Restructuring**: Analyzes organizational structure and suggests consolidations and span of control optimizations
- **KPI-Based Analysis**: Evaluates departmental KPIs (performance, productivity, cost efficiency, etc.) and provides recommendations
- **Multiple Scenarios**: Generate conservative, moderate, and aggressive restructuring plans
- **Cost Analysis**: Calculates retention bonuses, severance costs, and estimated savings with ROI calculations

### Visualizations

- Headcount distribution by department (pie chart)
- Payroll analysis by department (bar chart)
- KPI performance gaps (bar chart)
- Critical employees table
- Detailed analysis dashboards with filterable data

### User Interface

- Intuitive Material-UI design
- Responsive layout for all devices
- Multi-page navigation (Dashboard, Analysis, Restructuring Plans)
- Real-time data loading and analysis

## Technology Stack

### Backend

- **Framework**: Flask (Python)
- **Analysis**: Pandas, NumPy, SciPy, Scikit-learn
- **Visualization**: Matplotlib
- **Server**: Python 3.8+

### Frontend

- **Framework**: React 18
- **UI Library**: Material-UI (MUI) v5
- **Charting**: Recharts
- **HTTP Client**: Axios
- **Styling**: Emotion (MUI's built-in styling)

## Project Structure

```
Organization-Restructuring-App/
├── backend/
│   ├── app.py                 # Flask application entry point
│   ├── analytics.py           # Core analysis algorithms
│   ├── data_models.py         # Data structures and models
│   ├── mock_data.py           # Mock organization data
│   └── requirements.txt       # Python dependencies
│
└── frontend/
    ├── public/
    │   └── index.html         # HTML template
    ├── src/
    │   ├── api/
    │   │   └── client.js      # API client
    │   ├── components/
    │   │   ├── App.js         # Main app component
    │   │   ├── Dashboard.js   # Dashboard page
    │   │   ├── AnalysisPage.js # Detailed analysis
    │   │   ├── RestructuringPlans.js # Plans & scenarios
    │   │   └── LoadOrganization.js  # Data loading
    │   ├── index.js           # React entry point
    │   └── App.js             # App routing
    └── package.json           # Node dependencies
```

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- Node.js 14 or higher
- npm or yarn package manager

### Backend Setup

1. Navigate to the backend directory:

   ```bash
   cd backend
   ```

2. Create a virtual environment:

   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the Flask server:
   ```bash
   python app.py
   ```

The backend will start on `http://localhost:5000`

### Frontend Setup

1. Navigate to the frontend directory:

   ```bash
   cd frontend
   ```

2. Install dependencies:

   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

The frontend will open in your browser at `http://localhost:3000`

## Usage

1. **Load Organization Data**: Click "Load Mock Organization" to load sample data
2. **View Dashboard**: See organization overview, headcount distribution, and payroll analysis
3. **Analyze**:
   - View critical employees for retention
   - Review layoff candidates
   - Check organizational hierarchy recommendations
   - Review KPI analysis by department
4. **Generate Plans**: Create multiple restructuring scenarios (Conservative, Moderate, Aggressive)
5. **Compare Scenarios**: View detailed analysis and recommendations for each scenario

## API Endpoints

### Organization

- `GET /api/health` - Health check
- `POST /api/organization/load-mock` - Load mock data
- `GET /api/organization/overview` - Get organization statistics

### Employees

- `GET /api/employees` - List all employees
- `GET /api/employees/<id>` - Get specific employee

### Analysis

- `GET /api/analysis/critical-employees` - Identify critical employees
- `GET /api/analysis/layoff-analysis` - Analyze layoff candidates
- `GET /api/analysis/hierarchy` - Review hierarchy
- `GET /api/analysis/kpis` - KPI analysis by department
- `GET /api/department-stats/<department>` - Department statistics

### Restructuring

- `POST /api/restructuring/plan` - Create custom restructuring plan
- `POST /api/restructuring/scenarios` - Generate multiple scenarios

## Mock Data

The application comes with comprehensive mock data including:

- **26 Employees** across 6 departments (Engineering, Sales, Marketing, HR, Finance, Operations)
- **Performance Metrics**: Performance scores (0-100), tenure, market value
- **Organization Roles**: Various levels from coordinators to VPs
- **Department Distribution**: Realistic distribution across functions

## Analysis Algorithms

### Critical Employee Scoring

Weighted formula considering:

- Performance score (25%)
- Project criticality (30%)
- Tenure (15%)
- Market value (20%)
- Direct reports (10%)

### Layoff Impact Scoring

Evaluates organizational impact of potential layoffs based on:

- Direct reports managed
- Project criticality
- Performance level
- Tenure and experience

### KPI Analysis

Department-specific KPIs evaluated:

- **Engineering**: Code quality, productivity, stability, cost efficiency
- **Sales**: Performance, experience, cost efficiency
- **Marketing**: Performance, creativity, cost efficiency
- **Finance**: Accuracy, experience, cost efficiency
- **HR**: Performance, experience, cost efficiency
- **Operations**: Efficiency, experience, cost efficiency

## Example Scenarios

### Conservative Plan

- 5% headcount reduction
- Focus on retention of critical talent
- Minimal organizational disruption
- Quick ROI

### Moderate Plan

- 10% headcount reduction
- Balanced approach with selective layoffs
- Hierarchy optimizations
- Reasonable implementation costs

### Aggressive Plan

- 20% headcount reduction
- Significant restructuring
- Maximum cost savings
- Longer ROI period

## Customization

### Adding New Mock Data

Edit `backend/mock_data.py` to add employees or modify organization structure.

### Modifying Analysis Weights

Adjust weights in `backend/analytics.py`:

- `CriticalEmployeeAnalyzer.calculate_criticality_score()`
- `LayoffOptimizer.calculate_layoff_impact_score()`

### Customizing Dashboard

Edit React components in `frontend/src/components/` to modify visualizations and layouts.

## Output Examples

The app generates:

- Employee lists with criticality scores
- Layoff recommendations with severance costs
- Retention bonus calculations
- Restructuring recommendations with priority levels
- ROI calculations (months to break even)
- KPI gap analysis with recommendations

## Troubleshooting

### Backend Connection Issues

- Ensure Flask server is running on port 5000
- Check firewall settings
- Verify CORS is enabled in Flask app

### Data Not Loading

- Clear browser cache
- Restart both backend and frontend servers
- Check browser console for errors

### Charts Not Displaying

- Ensure Recharts is installed: `npm install recharts`
- Check that data is being returned from API

## Future Enhancements

- [ ] Custom organization data upload (CSV/Excel)
- [ ] Salary adjustment recommendations
- [ ] Skills gap analysis
- [ ] Succession planning
- [ ] Department-specific benchmarking
- [ ] Export reports to PDF
- [ ] Real-time what-if analysis
- [ ] Integration with HR systems
- [ ] Multi-year planning scenarios
- [ ] Advanced risk analysis

## License

This project is provided as-is for organizational planning purposes.

## Support

For issues or questions, please check the console logs and API responses for debugging information.
