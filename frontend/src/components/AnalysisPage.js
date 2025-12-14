import React from 'react';
import {
  Container,
  Paper,
  Typography,
  Box,
  Tabs,
  Tab,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  CircularProgress,
  Alert,
  Chip,
} from '@mui/material';
import { analysisAPI } from '../api/client';

const AnalysisPage = ({ organization }) => {
  const [tabValue, setTabValue] = React.useState(0);
  const [criticalData, setCriticalData] = React.useState(null);
  const [layoffData, setLayoffData] = React.useState(null);
  const [hierarchyData, setHierarchyData] = React.useState(null);
  const [kpiData, setKpiData] = React.useState(null);
  const [loading, setLoading] = React.useState(true);
  const [error, setError] = React.useState(null);

  React.useEffect(() => {
    fetchAnalysisData();
  }, [organization]);

  const fetchAnalysisData = async () => {
    setLoading(true);
    setError(null);
    try {
      const [critical, layoff, hierarchy, kpi] = await Promise.all([
        analysisAPI.getCriticalEmployees(),
        analysisAPI.getLayoffAnalysis(),
        analysisAPI.getHierarchyAnalysis(),
        analysisAPI.getKPIAnalysis(),
      ]);

      setCriticalData(critical.data);
      setLayoffData(layoff.data);
      setHierarchyData(hierarchy.data);
      setKpiData(kpi.data);
    } catch (err) {
      setError('Failed to load analysis data');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
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

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Typography variant="h4" gutterBottom sx={{ mb: 4 }}>
        Detailed Analysis
      </Typography>

      <Paper>
        <Tabs value={tabValue} onChange={handleTabChange} variant="fullWidth">
          <Tab label="Critical Employees" />
          <Tab label="Layoff Candidates" />
          <Tab label="Hierarchy Review" />
          <Tab label="KPI Analysis" />
        </Tabs>

        <Box sx={{ p: 3 }}>
          {/* Critical Employees Tab */}
          {tabValue === 0 && criticalData && (
            <Box>
              <Alert severity="info" sx={{ mb: 3 }}>
                Retention Cost: <strong>${(criticalData.total_retention_cost / 1000).toFixed(0)}K</strong> for{' '}
                <strong>{criticalData.critical_count} critical employees</strong>
              </Alert>

              <TableContainer>
                <Table>
                  <TableHead>
                    <TableRow sx={{ backgroundColor: '#f5f5f5' }}>
                      <TableCell>Name</TableCell>
                      <TableCell>Department</TableCell>
                      <TableCell>Role</TableCell>
                      <TableCell align="right">Salary</TableCell>
                      <TableCell align="right">Criticality Score</TableCell>
                      <TableCell align="right">Performance</TableCell>
                      <TableCell align="right">Tenure (yrs)</TableCell>
                      <TableCell align="right">Retention Cost</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {criticalData.critical_employees.map((emp) => (
                      <TableRow key={emp.id}>
                        <TableCell sx={{ fontWeight: 'bold' }}>{emp.name}</TableCell>
                        <TableCell>{emp.department}</TableCell>
                        <TableCell>{emp.role}</TableCell>
                        <TableCell align="right">${(emp.salary / 1000).toFixed(0)}K</TableCell>
                        <TableCell align="right">
                          <Chip label={emp.criticality_score} color="primary" size="small" />
                        </TableCell>
                        <TableCell align="right">{emp.performance_score}</TableCell>
                        <TableCell align="right">{emp.tenure_years}</TableCell>
                        <TableCell align="right">
                          ${(criticalData.retention_costs[emp.id] / 1000).toFixed(0)}K
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            </Box>
          )}

          {/* Layoff Candidates Tab */}
          {tabValue === 1 && layoffData && (
            <Box>
              <Alert severity="warning" sx={{ mb: 3 }}>
                <strong>{layoffData.candidate_count}</strong> potential layoffs identified.
                <br />
                Layoff Cost: <strong>${(layoffData.total_layoff_cost / 1000).toFixed(0)}K</strong>
                <br />
                Estimated Net Savings: <strong>${(layoffData.net_savings / 1000).toFixed(0)}K</strong> annually
              </Alert>

              <TableContainer>
                <Table>
                  <TableHead>
                    <TableRow sx={{ backgroundColor: '#f5f5f5' }}>
                      <TableCell>Name</TableCell>
                      <TableCell>Department</TableCell>
                      <TableCell>Role</TableCell>
                      <TableCell align="right">Salary</TableCell>
                      <TableCell align="right">Impact Score</TableCell>
                      <TableCell align="right">Performance</TableCell>
                      <TableCell align="right">Reports</TableCell>
                      <TableCell align="right">Severance</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {layoffData.layoff_candidates.map((emp) => (
                      <TableRow key={emp.id}>
                        <TableCell sx={{ fontWeight: 'bold' }}>{emp.name}</TableCell>
                        <TableCell>{emp.department}</TableCell>
                        <TableCell>{emp.role}</TableCell>
                        <TableCell align="right">${(emp.salary / 1000).toFixed(0)}K</TableCell>
                        <TableCell align="right">
                          <Chip
                            label={emp.impact_score}
                            size="small"
                            color={emp.impact_score > 50 ? 'error' : 'success'}
                            variant="outlined"
                          />
                        </TableCell>
                        <TableCell align="right">{emp.performance_score}</TableCell>
                        <TableCell align="right">{emp.direct_reports}</TableCell>
                        <TableCell align="right">
                          ${(emp.severance_cost / 1000).toFixed(0)}K
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            </Box>
          )}

          {/* Hierarchy Review Tab */}
          {tabValue === 2 && hierarchyData && (
            <Box>
              <Typography variant="h6" sx={{ mb: 2 }}>
                Organization Consolidations ({hierarchyData.consolidations.length})
              </Typography>
              {hierarchyData.consolidations.length === 0 ? (
                <Typography color="textSecondary">No consolidations recommended</Typography>
              ) : (
                <Box>
                  {hierarchyData.consolidations.map((item, idx) => (
                    <Paper
                      key={idx}
                      sx={{
                        p: 2,
                        mb: 2,
                        backgroundColor: '#f9f9f9',
                        borderLeft: '4px solid #ff9800',
                      }}
                    >
                      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start' }}>
                        <Box>
                          <Typography variant="body2" sx={{ fontWeight: 'bold' }}>
                            {item.employee_name}
                          </Typography>
                          <Typography variant="caption" color="textSecondary">
                            Current Direct Reports: {item.current_reports}
                          </Typography>
                          <Typography variant="body2" sx={{ mt: 1 }}>
                            {item.recommendation}
                          </Typography>
                        </Box>
                      </Box>
                    </Paper>
                  ))}
                </Box>
              )}
            </Box>
          )}

          {/* KPI Analysis Tab */}
          {tabValue === 3 && kpiData && (
            <Box>
              <Alert severity="info" sx={{ mb: 3 }}>
                Analyzing {kpiData.total_kpis} KPIs across all departments
              </Alert>

              <TableContainer>
                <Table>
                  <TableHead>
                    <TableRow sx={{ backgroundColor: '#f5f5f5' }}>
                      <TableCell>KPI</TableCell>
                      <TableCell>Department</TableCell>
                      <TableCell align="right">Current</TableCell>
                      <TableCell align="right">Target</TableCell>
                      <TableCell align="right">Gap</TableCell>
                      <TableCell>Status</TableCell>
                      <TableCell>Recommendation</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {kpiData.kpi_analyses.map((kpi, idx) => (
                      <TableRow key={idx}>
                        <TableCell sx={{ fontWeight: 'bold' }}>{kpi.kpi_name}</TableCell>
                        <TableCell>{kpi.department}</TableCell>
                        <TableCell align="right">{kpi.current_value}</TableCell>
                        <TableCell align="right">{kpi.target_value}</TableCell>
                        <TableCell align="right">{kpi.gap.toFixed(1)}</TableCell>
                        <TableCell>
                          <Chip
                            label={kpi.status.replace('_', ' ').toUpperCase()}
                            size="small"
                            color={
                              kpi.status === 'on_track'
                                ? 'success'
                                : kpi.status === 'below_target'
                                  ? 'error'
                                  : 'default'
                            }
                            variant="outlined"
                          />
                        </TableCell>
                        <TableCell>
                          {kpi.recommendations.length > 0 ? (
                            <Typography variant="caption">{kpi.recommendations[0]}</Typography>
                          ) : (
                            <Typography variant="caption" color="textSecondary">
                              On track
                            </Typography>
                          )}
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            </Box>
          )}
        </Box>
      </Paper>
    </Container>
  );
};

export default AnalysisPage;
