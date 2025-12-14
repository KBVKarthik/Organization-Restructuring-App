import React from 'react';
import {
  Container,
  Grid,
  Paper,
  Typography,
  Box,
  Card,
  CardContent,
  CardHeader,
  CircularProgress,
  Alert,
} from '@mui/material';
import {
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  LineChart,
  Line,
} from 'recharts';
import { organizationAPI, analysisAPI } from '../api/client';

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8', '#82CA9D'];

const Dashboard = ({ organization }) => {
  const [overview, setOverview] = React.useState(null);
  const [critical, setCritical] = React.useState(null);
  const [layoffAnalysis, setLayoffAnalysis] = React.useState(null);
  const [kpiAnalysis, setKpiAnalysis] = React.useState(null);
  const [loading, setLoading] = React.useState(true);
  const [error, setError] = React.useState(null);

  React.useEffect(() => {
    fetchDashboardData();
  }, [organization]);

  const fetchDashboardData = async () => {
    setLoading(true);
    setError(null);
    try {
      const [overviewRes, criticalRes, layoffRes, kpiRes] = await Promise.all([
        organizationAPI.getOverview(),
        analysisAPI.getCriticalEmployees(),
        analysisAPI.getLayoffAnalysis(),
        analysisAPI.getKPIAnalysis(),
      ]);

      setOverview(overviewRes.data);
      setCritical(criticalRes.data);
      setLayoffAnalysis(layoffRes.data);
      setKpiAnalysis(kpiRes.data);
    } catch (err) {
      setError('Failed to load dashboard data');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}>
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return <Alert severity="error">{error}</Alert>;
  }

  // Prepare department distribution data
  const deptData = overview
    ? Object.entries(overview.department_distribution).map(([dept, count]) => ({
      name: dept,
      value: count,
    }))
    : [];

  // Prepare salary by department data
  const salaryData = overview
    ? Object.entries(overview.department_salaries).map(([dept, salary]) => ({
      name: dept,
      salary: salary / 1000, // Convert to thousands
    }))
    : [];

  // Prepare KPI performance data
  const kpiPerformanceData = kpiAnalysis
    ? kpiAnalysis.kpi_analyses
      .reduce((acc, kpi) => {
        const deptKpi = acc.find((item) => item.department === kpi.department);
        if (deptKpi) {
          deptKpi.gaps = (deptKpi.gaps || 0) + Math.abs(kpi.gap);
        } else {
          acc.push({ department: kpi.department, gaps: Math.abs(kpi.gap) });
        }
        return acc;
      }, [])
      .map((item) => ({
        ...item,
        gaps: Math.round(item.gaps * 10) / 10,
      }))
    : [];

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Typography variant="h4" gutterBottom sx={{ mb: 4 }}>
        Organization Overview Dashboard
      </Typography>

      {/* Key Metrics */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Total Headcount
              </Typography>
              <Typography variant="h5">{overview?.total_headcount || 0}</Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Total Payroll
              </Typography>
              <Typography variant="h5">
                ${(overview?.total_payroll / 1000000).toFixed(2)}M
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Average Salary
              </Typography>
              <Typography variant="h5">
                ${(overview?.average_salary / 1000).toFixed(0)}K
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Departments
              </Typography>
              <Typography variant="h5">{overview?.departments?.length || 0}</Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Critical Employees Alert */}
      {critical && critical.critical_count > 0 && (
        <Alert severity="warning" sx={{ mb: 4 }}>
          <strong>{critical.critical_count} Critical Employees</strong> identified with retention costs of
          <strong>${(critical.total_retention_cost / 1000).toFixed(0)}K</strong>
        </Alert>
      )}

      {/* Layoff Impact */}
      {layoffAnalysis && (
        <Alert severity="info" sx={{ mb: 4 }}>
          <strong>Potential Savings:</strong> ${(layoffAnalysis.net_savings / 1000).toFixed(0)}K from {layoffAnalysis.candidate_count}
          potential layoffs (considering ${(layoffAnalysis.total_layoff_cost / 1000).toFixed(0)}K in severance)
        </Alert>
      )}

      {/* Charts */}
      <Grid container spacing={3}>
        {/* Department Distribution */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Headcount by Department
            </Typography>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={deptData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, value }) => `${name}: ${value}`}
                  outerRadius={100}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {deptData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>

        {/* Salary by Department */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Payroll by Department ($K)
            </Typography>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={salaryData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" angle={-45} textAnchor="end" height={100} />
                <YAxis />
                <Tooltip />
                <Bar dataKey="salary" fill="#8884d8" />
              </BarChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>

        {/* KPI Performance */}
        {kpiPerformanceData.length > 0 && (
          <Grid item xs={12} md={6}>
            <Paper sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom>
                KPI Gaps by Department
              </Typography>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={kpiPerformanceData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="department" angle={-45} textAnchor="end" height={100} />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="gaps" fill="#82ca9d" />
                </BarChart>
              </ResponsiveContainer>
            </Paper>
          </Grid>
        )}

        {/* Critical Employees Table */}
        {critical && Array.isArray(critical.critical_employees) && critical.critical_employees.length > 0 && (
          <Grid item xs={12} md={6}>
            <Paper sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom>
                Top Critical Employees
              </Typography>
              <Box sx={{ overflowX: 'auto' }}>
                <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                  <thead>
                    <tr style={{ borderBottom: '2px solid #ddd' }}>
                      <th style={{ padding: '8px', textAlign: 'left' }}>Name</th>
                      <th style={{ padding: '8px', textAlign: 'left' }}>Department</th>
                      <th style={{ padding: '8px', textAlign: 'right' }}>Score</th>
                    </tr>
                  </thead>
                  <tbody>
                    {critical.critical_employees.slice(0, 5).map((emp, idx) => {
                      // Support both API shapes: array of objects or array-of-arrays
                      let id = null;
                      let name = '';
                      let dept = '';
                      let score = '';
                      if (Array.isArray(emp)) {
                        id = emp[0];
                        name = emp[1];
                        dept = emp[2];
                        score = emp[3];
                      } else if (emp && typeof emp === 'object') {
                        id = emp.id || `emp-${idx}`;
                        name = emp.name || emp.full_name || '';
                        dept = emp.department || emp.dept || '';
                        score = emp.criticality_score ?? emp.score ?? emp[3] ?? '';
                      }

                      return (
                        <tr key={id || idx} style={{ borderBottom: '1px solid #eee' }}>
                          <td style={{ padding: '8px' }}>{name}</td>
                          <td style={{ padding: '8px' }}>{dept}</td>
                          <td style={{ padding: '8px', textAlign: 'right', fontWeight: 'bold' }}>
                            {score}
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </Box>
            </Paper>
          </Grid>
        )}
      </Grid>
    </Container>
  );
};

export default Dashboard;
