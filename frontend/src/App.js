import React from 'react';
import {
  AppBar,
  Toolbar,
  Typography,
  Container,
  Box,
  Button,
  Drawer,
  List,
  ListItem,
  ListItemButton,
  ListItemText,
  Divider,
} from '@mui/material';
import MenuIcon from '@mui/icons-material/Menu';
import DashboardIcon from '@mui/icons-material/Dashboard';
import AnalyticsIcon from '@mui/icons-material/Analytics';
import BuildIcon from '@mui/icons-material/Build';
import LoadOrganization from './LoadOrganization';
import Dashboard from './Dashboard';
import AnalysisPage from './AnalysisPage';
import RestructuringPlans from './RestructuringPlans';

function App() {
  const [currentPage, setCurrentPage] = React.useState('load');
  const [organization, setOrganization] = React.useState(null);
  const [drawerOpen, setDrawerOpen] = React.useState(false);

  const handleOrganizationLoaded = (data) => {
    setOrganization(data);
    setCurrentPage('dashboard');
  };

  const handleDrawerToggle = () => {
    setDrawerOpen(!drawerOpen);
  };

  const handleNavigation = (page) => {
    setCurrentPage(page);
    setDrawerOpen(false);
  };

  const navigationItems = organization
    ? [
      { label: 'Dashboard', icon: '📊', id: 'dashboard' },
      { label: 'Analysis', icon: '📈', id: 'analysis' },
      { label: 'Restructuring Plans', icon: '🔨', id: 'plans' },
    ]
    : [];

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      <AppBar position="sticky">
        <Toolbar>
          {organization && (
            <Button
              color="inherit"
              onClick={handleDrawerToggle}
              sx={{ mr: 2, minWidth: 'auto' }}
            >
              <MenuIcon />
            </Button>
          )}
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            Organization Restructuring Tool
          </Typography>
          {organization && (
            <Typography variant="body2" sx={{ opacity: 0.8 }}>
              {organization.organization.name}
            </Typography>
          )}
        </Toolbar>
      </AppBar>

      {organization && (
        <Drawer anchor="left" open={drawerOpen} onClose={handleDrawerToggle}>
          <Box sx={{ width: 250, pt: 2 }}>
            <List>
              {navigationItems.map((item) => (
                <ListItem key={item.id} disablePadding>
                  <ListItemButton
                    selected={currentPage === item.id}
                    onClick={() => handleNavigation(item.id)}
                  >
                    <ListItemText primary={`${item.icon} ${item.label}`} />
                  </ListItemButton>
                </ListItem>
              ))}
            </List>
            <Divider />
            <List>
              <ListItem disablePadding>
                <ListItemButton onClick={() => { setOrganization(null); setCurrentPage('load'); setDrawerOpen(false); }}>
                  <ListItemText primary="🔄 Load New Organization" />
                </ListItemButton>
              </ListItem>
            </List>
          </Box>
        </Drawer>
      )}

      <Box component="main" sx={{ flexGrow: 1, width: '100%' }}>
        {!organization ? (
          <LoadOrganization onOrganizationLoaded={handleOrganizationLoaded} />
        ) : currentPage === 'dashboard' ? (
          <Dashboard organization={organization} />
        ) : currentPage === 'analysis' ? (
          <AnalysisPage organization={organization} />
        ) : currentPage === 'plans' ? (
          <RestructuringPlans organization={organization} />
        ) : null}
      </Box>
    </Box>
  );
}

export default App;
