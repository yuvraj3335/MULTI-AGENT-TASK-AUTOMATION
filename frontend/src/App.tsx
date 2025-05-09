import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useNavigate } from 'react-router-dom';
import {
  AppBar,
  Toolbar,
  Typography,
  Container,
  Box,
  Button,
  CssBaseline,
  ThemeProvider,
  createTheme,
} from '@mui/material';
import FileUpload from './components/FileUpload';
import FileViewer from './components/FileViewer';
import BRDViewer from './components/BRDViewer';
import TicketManager from './components/TicketManager';
import api from './services/api';

const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
  },
});

function HomePage() {
  const navigate = useNavigate();

  const handleUploadSuccess = (fileId: string) => {
    navigate(`/files/${fileId}`);
  };

  return (
    <Box sx={{ mt: 4 }}>
      <Typography variant="h4" gutterBottom align="center">
        Multi-Agent Task Automation
      </Typography>
      <Typography variant="subtitle1" gutterBottom align="center" color="textSecondary">
        Upload a file to get started
      </Typography>
      <FileUpload onUploadSuccess={handleUploadSuccess} />
    </Box>
  );
}

function FileViewerPage() {
  const navigate = useNavigate();
  const fileId = window.location.pathname.split('/').pop() || '';

  const handleCreateBRD = async (selectedPoints: string[]) => {
    try {
      const response = await api.createBRD(fileId, selectedPoints);
      navigate(`/brds/${response.brd_id}`);
    } catch (error) {
      console.error('Failed to create BRD:', error);
    }
  };

  return <FileViewer fileId={fileId} onCreateBRD={handleCreateBRD} />;
}

function BRDViewerPage() {
  const brdId = window.location.pathname.split('/').pop() || '';
  return (
    <Box>
      <BRDViewer brdId={brdId} />
      <TicketManager brdId={brdId} />
    </Box>
  );
}

function TicketsPage() {
  return <TicketManager />;
}

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <Box sx={{ flexGrow: 1 }}>
          <AppBar position="static">
            <Toolbar>
              <Typography variant="h6" component={Link} to="/" sx={{ flexGrow: 1, textDecoration: 'none', color: 'inherit' }}>
                Task Automation
              </Typography>
              <Button color="inherit" component={Link} to="/tickets">
                Tickets
              </Button>
            </Toolbar>
          </AppBar>

          <Container maxWidth="lg">
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/files/:fileId" element={<FileViewerPage />} />
              <Route path="/brds/:brdId" element={<BRDViewerPage />} />
              <Route path="/tickets" element={<TicketsPage />} />
            </Routes>
          </Container>
        </Box>
      </Router>
    </ThemeProvider>
  );
}

export default App; 