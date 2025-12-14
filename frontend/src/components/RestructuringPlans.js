import React from 'react';
import {
  Container,
  Paper,
  Typography,
  Box,
  Button,
  CircularProgress,
  Alert,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
} from '@mui/material';
import { restructuringAPI, analysisAPI } from '../api/client';

const RestructuringPlans = ({ organization }) => {
  const [scenarios, setScenarios] = React.useState([]);
  const [loading, setLoading] = React.useState(false);
  const [error, setError] = React.useState(null);
  const [selectedPlan, setSelectedPlan] = React.useState(null);

  const handleGenerateScenarios = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await restructuringAPI.createScenarios();
      setScenarios(response.data.scenarios);
    } catch (err) {
      setError('Failed to generate scenarios');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const getStatus = (value) => {
    if (value > 50) return 'error';
    if (value > 20) return 'warning';
    return 'success';
  };

  if (loading && scenarios.length === 0) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Typography variant="h4" gutterBottom sx={{ mb: 4 }}>
        Restructuring Plans & Scenarios
      </Typography>

      {error && <Alert severity="error" sx={{ mb: 3 }}>{error}</Alert>}

      {scenarios.length === 0 ? (
        <Paper sx={{ p: 4, textAlign: 'center' }}>
          <Typography variant="body1" color="textSecondary" sx={{ mb: 3 }}>
            Generate multiple restructuring scenarios to compare different strategies
          </Typography>
          <Button
            variant="contained"
            size="large"
            onClick={handleGenerateScenarios}
            disabled={loading}
          >
            {loading ? <CircularProgress size={24} /> : 'Generate Scenarios'}
          </Button>
        </Paper>
      ) : (
        <Box>
          {/* Scenario Summary Cards */}
          <Box sx={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: 3, mb: 4 }}>
            {scenarios.map((scenario, idx) => (
              <Paper
                key={idx}
                sx={{
                  p: 3,
                  cursor: 'pointer',
                  border: selectedPlan === idx ? '2px solid #1976d2' : '1px solid #ddd',
                  transition: 'all 0.3s',
                  '&:hover': { boxShadow: 3 },
                }}
                onClick={() => setSelectedPlan(idx)}
              >
                <Typography variant="h6" gutterBottom>
                  {scenario.scenario_name}
                </Typography>
                <Typography variant="body2" color="textSecondary" sx={{ mb: 2 }}>
                  {scenario.description}
                </Typography>
                <Box sx={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 2 }}>
                  <Box>
                    <Typography variant="caption" color="textSecondary">
                      Headcount Reduction
                    </Typography>
                    <Typography variant="h6">
                      {scenario.headcount_reduction}
                      <Typography component="span" variant="body2" color="textSecondary">
                        {' '}({((scenario.headcount_reduction / scenario.current_headcount) * 100).toFixed(1)}%)
                      </Typography>
                    </Typography>
                  </Box>
                  <Box>
                    <Typography variant="caption" color="textSecondary">
                      Annual Savings
                    </Typography>
                    <Typography variant="h6">
                      ${(scenario.annual_savings / 1000).toFixed(0)}K
                    </Typography>
                  </Box>
                  <Box>
                    <Typography variant="caption" color="textSecondary">
                      Implementation Cost
                    </Typography>
                    <Typography variant="body2">
                      ${(scenario.total_cost / 1000).toFixed(0)}K
                    </Typography>
                  </Box>
                  <Box>
                    <Typography variant="caption" color="textSecondary">
                      ROI (Months)
                    </Typography>
                    <Typography variant="body2">
                      {scenario.roi_months.toFixed(1)}m
                    </Typography>
                  </Box>
                </Box>
              </Paper>
            ))}
          </Box>

          {/* Selected Plan Details */}
          {selectedPlan !== null && scenarios[selectedPlan] && (
            <Box sx={{ mt: 4 }}>
              <Typography variant="h5" gutterBottom sx={{ mb: 3 }}>
                {scenarios[selectedPlan].scenario_name} - Detailed Analysis
              </Typography>

              {/* Key Metrics */}
              <Paper sx={{ p: 3, mb: 3 }}>
                <Typography variant="h6" gutterBottom>
                  Key Metrics
                </Typography>
                <Box sx={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: 2 }}>
                  <Box>
                    <Typography variant="caption" color="textSecondary">
                      Current Headcount
                    </Typography>
                    <Typography variant="h6">{scenarios[selectedPlan].current_headcount}</Typography>
                  </Box>
                  <Box>
                    <Typography variant="caption" color="textSecondary">
                      Target Headcount
                    </Typography>
                    <Typography variant="h6">{scenarios[selectedPlan].target_headcount}</Typography>
                  </Box>
                  <Box>
                    <Typography variant="caption" color="textSecondary">
                      Retention Bonuses
                    </Typography>
                    <Typography variant="h6">
                      ${(scenarios[selectedPlan].retention_cost / 1000).toFixed(0)}K
                    </Typography>
                  </Box>
                  <Box>
                    <Typography variant="caption" color="textSecondary">
                      Severance Costs
                    </Typography>
                    <Typography variant="h6">
                      ${(scenarios[selectedPlan].layoff_cost / 1000).toFixed(0)}K
                    </Typography>
                  </Box>
                </Box>
              </Paper>

              {/* Critical Employees */}
              {scenarios[selectedPlan].critical_details.length > 0 && (
                <Paper sx={{ p: 3, mb: 3 }}>
                  <Typography variant="h6" gutterBottom>
                    Critical Employees for Retention ({scenarios[selectedPlan].critical_count})
                  </Typography>
                  <TableContainer>
                    <Table size="small">
                      <TableHead>
                        <TableRow sx={{ backgroundColor: '#f5f5f5' }}>
                          <TableCell>Name</TableCell>
                          <TableCell>Department</TableCell>
                          <TableCell align="right">Criticality Score</TableCell>
                        </TableRow>
                      </TableHead>
                      <TableBody>
                        {scenarios[selectedPlan].critical_details.map((emp) => (
                          <TableRow key={emp[0]}>
                            <TableCell>{emp[1]}</TableCell>
                            <TableCell>{emp[2]}</TableCell>
                            <TableCell align="right">
                              <Chip label={emp[3]} color="primary" variant="outlined" size="small" />
                            </TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  </TableContainer>
                </Paper>
              )}

              {/* Layoff Candidates */}
              {scenarios[selectedPlan].layoffs.length > 0 && (
                <Paper sx={{ p: 3, mb: 3 }}>
                  <Typography variant="h6" gutterBottom>
                    Recommended Layoffs ({scenarios[selectedPlan].layoffs.length})
                  </Typography>
                  <Alert severity="warning" sx={{ mb: 2 }}>
                    These are candidates for layoff based on minimal impact to operations and criticality analysis
                  </Alert>
                  <Typography variant="body2" color="textSecondary">
                    IDs: {scenarios[selectedPlan].layoffs.join(', ')}
                  </Typography>
                </Paper>
              )}

              {/* Recommendations */}
              {scenarios[selectedPlan].recommendations.length > 0 && (
                <Paper sx={{ p: 3, mb: 3 }}>
                  <Typography variant="h6" gutterBottom>
                    Top Recommendations
                  </Typography>
                  <Box>
                    {scenarios[selectedPlan].recommendations.slice(0, 10).map((rec, idx) => (
                      <Box
                        key={idx}
                        sx={{
                          p: 2,
                          mb: 1,
                          backgroundColor: '#f9f9f9',
                          borderLeft: '4px solid #1976d2',
                          borderRadius: '4px',
                        }}
                      >
                        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start' }}>
                          <Box>
                            <Typography variant="body2" sx={{ fontWeight: 'bold' }}>
                              {rec.action}
                            </Typography>
                            <Typography variant="caption" color="textSecondary">
                              {rec.rationale}
                            </Typography>
                          </Box>
                          <Chip
                            label={`P${rec.priority}`}
                            size="small"
                            variant={rec.priority <= 2 ? 'filled' : 'outlined'}
                            color={rec.priority <= 2 ? 'error' : rec.priority <= 3 ? 'warning' : 'default'}
                          />
                        </Box>
                      </Box>
                    ))}
                  </Box>
                </Paper>
              )}

              {/* KPI Analysis */}
              {scenarios[selectedPlan].kpi_analysis.length > 0 && (
                <Paper sx={{ p: 3 }}>
                  <Typography variant="h6" gutterBottom>
                    KPI Analysis
                  </Typography>
                  <TableContainer>
                    <Table size="small">
                      <TableHead>
                        <TableRow sx={{ backgroundColor: '#f5f5f5' }}>
                          <TableCell>KPI</TableCell>
                          <TableCell>Department</TableCell>
                          <TableCell align="right">Current</TableCell>
                          <TableCell align="right">Target</TableCell>
                          <TableCell align="right">Gap</TableCell>
                        </TableRow>
                      </TableHead>
                      <TableBody>
                        {scenarios[selectedPlan].kpi_analysis.map((kpi, idx) => (
                          <TableRow key={idx}>
                            <TableCell>{kpi.kpi_name}</TableCell>
                            <TableCell>{kpi.department}</TableCell>
                            <TableCell align="right">{kpi.current_value}</TableCell>
                            <TableCell align="right">{kpi.target_value}</TableCell>
                            <TableCell align="right">
                              <Chip
                                label={kpi.gap.toFixed(1)}
                                size="small"
                                color={Math.abs(kpi.gap) > 5 ? 'error' : 'success'}
                                variant="outlined"
                              />
                            </TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  </TableContainer>
                </Paper>
              )}
            </Box>
          )}

          {scenarios.length > 0 && (
            <Box sx={{ mt: 4, textAlign: 'center' }}>
              <Button
                variant="outlined"
                onClick={handleGenerateScenarios}
                disabled={loading}
              >
                Regenerate Scenarios
              </Button>
            </Box>
          )}
        </Box>
      )}
    </Container>
  );
};

export default RestructuringPlans;
