# Organization Restructuring App - START HERE

Welcome to the Organization Restructuring Planning Application!

This is a comprehensive tool for analyzing your organization and planning restructuring with data-driven recommendations.

## Quick Navigation

### For First-Time Users

👉 **[GETTING_STARTED.md](GETTING_STARTED.md)** - Complete setup and usage guide

### For Detailed Information

📖 **[README.md](README.md)** - Full feature documentation

### For Project Overview

📋 **[COMPLETION_SUMMARY.md](COMPLETION_SUMMARY.md)** - What's been built
📋 **[PROJECT_MANIFEST.md](PROJECT_MANIFEST.md)** - Complete file directory

## 60-Second Quick Start

### What You Need

- Python 3.8+
- Node.js 14+
- A terminal/command prompt

### Run It

**Terminal 1 (Backend Server):**

```bash
cd backend
python app.py
```

**Terminal 2 (Frontend App):**

```bash
cd frontend
npm start
```

Then visit: **http://localhost:3000**

## What This App Does

### 1. Analyzes Your Organization

- Loads employee data
- Evaluates performance and criticality
- Identifies organizational structure

### 2. Identifies Critical Talent

- Scores employees on multiple factors
- Calculates retention bonuses
- Prioritizes key talent retention

### 3. Recommends Cost Savings

- Identifies layoff candidates
- Minimizes operational impact
- Calculates exact savings

### 4. Provides KPI Analysis

- Evaluates 19 department KPIs
- Identifies performance gaps
- Suggests improvements

### 5. Generates Multiple Scenarios

- Conservative (5% reduction)
- Moderate (10% reduction)
- Aggressive (20% reduction)

### 6. Shows Beautiful Visualizations

- Department distribution charts
- Payroll analysis
- KPI performance metrics
- Recommendation tables

## Sample Results (Included Mock Data)

**Critical Employees:**

- Grace Lee (Sales): 87.9/100 - Retention bonus: \$24K
- Samuel Brown (Finance): 87.7/100 - Retention bonus: \$42K
- Leo Anderson (Marketing): 82.5/100 - Retention bonus: \$33K

**Layoff Optimization (10% reduction):**

- 3 candidates identified
- Severance cost: \$170,096
- Annual savings: \$700,000
- Net savings: \$529,904

**Restructuring Plans:**

- Conservative: 5% reduction, 20.3 month ROI
- Moderate: 10% reduction, 11.5 month ROI
- Aggressive: 20% reduction, 7.3 month ROI

## Key Features

✓ Critical Employee Analysis - Identify and retain top talent  
✓ Layoff Optimization - Minimize impact while reducing costs  
✓ KPI-Based Analysis - Evaluate department performance  
✓ Hierarchy Review - Optimize organizational structure  
✓ Multiple Scenarios - Compare different strategies  
✓ Beautiful UI - Professional Material-UI design  
✓ Real-time Analysis - See results instantly

## Technology Stack

**Backend:**

- Python/Flask REST API
- Pandas, NumPy for data analysis
- scikit-learn for algorithms

**Frontend:**

- React 18 application
- Material-UI components
- Recharts for visualizations
- Axios for API calls

## Files Overview

```
📁 Organization-Restructuring-App/
├── README.md                 ← Full documentation
├── GETTING_STARTED.md        ← Quick start guide
├── COMPLETION_SUMMARY.md     ← Project details
├── PROJECT_MANIFEST.md       ← File directory
├── SETUP.py                  ← Setup validation
├── test_api.py              ← Run API tests
├── demo_api_responses.py    ← See API examples
│
├── 📁 backend/              ← Python Flask API
│   ├── app.py              - REST API server
│   ├── analytics.py        - Core algorithms
│   ├── data_models.py      - Data structures
│   ├── mock_data.py        - Sample data
│   └── requirements.txt    - Dependencies
│
└── 📁 frontend/             ← React application
    ├── package.json
    ├── public/
    └── src/
        ├── App.js
        ├── components/     - Dashboard, Analysis, Plans
        └── api/           - API client
```

## Installation (First Time)

### 1. Check Prerequisites

```bash
python --version      # Should be 3.8+
node --version        # Should be 14+
```

### 2. Install Dependencies

**Backend:**

```bash
cd backend
pip install -r requirements.txt
```

**Frontend:**

```bash
cd frontend
npm install
```

### 3. Run Setup Validation

```bash
python SETUP.py
```

## Common Tasks

### Start Everything

```bash
# Terminal 1
cd backend && python app.py

# Terminal 2
cd frontend && npm start

# Then open http://localhost:3000
```

### Run Tests

```bash
# Backend tests
cd backend && python test_backend.py

# API tests (requires backend running)
python test_api.py

# See API response examples
python demo_api_responses.py
```

### Use Your Own Data

Edit `backend/mock_data.py` with your employees, then restart the backend.

### Customize Analysis

Edit `backend/analytics.py` to change algorithm weights or KPI targets.

## API Reference

The backend provides 11 REST endpoints:

```
GET  /api/health
GET  /api/organization/overview
GET  /api/employees
GET  /api/analysis/critical-employees
GET  /api/analysis/layoff-analysis
GET  /api/analysis/hierarchy
GET  /api/analysis/kpis
GET  /api/department-stats/<department>
POST /api/restructuring/plan
POST /api/restructuring/scenarios
```

See [README.md](README.md) for full API documentation.

## Troubleshooting

**Backend won't start?**

```bash
pip install -r backend/requirements.txt
```

**Frontend won't start?**

```bash
cd frontend
npm cache clean --force
rm -rf node_modules
npm install
npm start
```

**Connection error?**

- Make sure backend is running on http://localhost:5000
- Check ports 5000 and 3000 are available

For more help, see [GETTING_STARTED.md](GETTING_STARTED.md)

## Next: Dive Deeper

1. **Run the app** (follow Quick Start above)
2. **Load mock data** by clicking the button
3. **Explore the dashboard** - see overview and metrics
4. **View analysis** - check critical employees and layoffs
5. **Compare scenarios** - see restructuring options
6. **Customize** - add your own organization data

## Learn More

- **[README.md](README.md)** - All features and detailed usage
- **[GETTING_STARTED.md](GETTING_STARTED.md)** - Setup guide with examples
- **[COMPLETION_SUMMARY.md](COMPLETION_SUMMARY.md)** - What's implemented

## Questions?

Check the documentation files:

- [GETTING_STARTED.md](GETTING_STARTED.md) - Setup and troubleshooting
- [README.md](README.md) - Features and customization
- [COMPLETION_SUMMARY.md](COMPLETION_SUMMARY.md) - Technical details

---

**Ready to get started?** → [GETTING_STARTED.md](GETTING_STARTED.md)

**Status:** ✓ Production Ready | **Version:** 1.0.0 | **Last Updated:** December 14, 2025
