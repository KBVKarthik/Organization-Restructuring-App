import React from 'react';
import { Container, Typography, Box, Button, CircularProgress, Alert } from '@mui/material';
import { organizationAPI, healthCheck } from '../api/client';

const LoadOrganization = ({ onOrganizationLoaded }) => {
  const [loading, setLoading] = React.useState(false);
  const [error, setError] = React.useState(null);
  const [apiConnected, setApiConnected] = React.useState(null);

  React.useEffect(() => {
    checkAPI();
  }, []);

  const checkAPI = async () => {
    try {
      await healthCheck();
      setApiConnected(true);
    } catch (err) {
      setApiConnected(false);
      setError('Unable to connect to backend API. Make sure the Flask server is running on port 5000.');
    }
  };

  const handleLoadMock = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await organizationAPI.loadMock();
      onOrganizationLoaded(response.data);
    } catch (err) {
      setError('Failed to load mock organization. ' + (err.message || ''));
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="sm">
      <Box
        sx={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          minHeight: '60vh',
          gap: 3,
        }}
      >
        <Typography variant="h3" component="h1" gutterBottom align="center">
          Organization Restructuring Tool
        </Typography>

        <Typography variant="body1" align="center" color="textSecondary">
          Welcome to the Organization Restructuring Planning Application. This tool helps you analyze your organization, identify critical employees, optimize layoff strategies, and generate restructuring recommendations.
        </Typography>

        {apiConnected === null && (
          <CircularProgress />
        )}

        {apiConnected === false && (
          <Alert severity="error">
            {error}
          </Alert>
        )}

        {apiConnected === true && (
          <>
            <Alert severity="info">
              Click below to load a sample organization with mock data
            </Alert>
            <Button
              variant="contained"
              size="large"
              onClick={handleLoadMock}
              disabled={loading}
            >
              {loading ? <CircularProgress size={24} /> : 'Load Mock Organization'}
            </Button>
          </>
        )}

        {error && apiConnected && (
          <Alert severity="error">{error}</Alert>
        )}
      </Box>
    </Container>
  );
};

export default LoadOrganization;
