import React, { useState, useEffect } from 'react';
import {
  Box,
  Paper,
  Typography,
  CircularProgress,
  List,
  ListItem,
  ListItemText,
  Checkbox,
  Button,
  Alert,
} from '@mui/material';
import { Description as DescriptionIcon } from '@mui/icons-material';
import api, { FileResponse } from '../services/api';

interface FileViewerProps {
  fileId: string;
  onCreateBRD: (selectedPoints: string[]) => void;
}

const FileViewer: React.FC<FileViewerProps> = ({ fileId, onCreateBRD }) => {
  const [fileData, setFileData] = useState<FileResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedPoints, setSelectedPoints] = useState<string[]>([]);

  useEffect(() => {
    const fetchFile = async () => {
      try {
        setLoading(true);
        setError(null);
        const response = await api.getFile(fileId);
        if (response.error) {
          throw new Error(response.error);
        }
        setFileData(response);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load file');
      } finally {
        setLoading(false);
      }
    };

    const pollFile = async () => {
      try {
        const response = await api.getFile(fileId);
        if (response.error) {
          throw new Error(response.error);
        }
        setFileData(response);
        if (response.status === 'done') {
          return true;
        }
        return false;
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load file');
        return true;
      }
    };

    const startPolling = async () => {
      while (true) {
        const isDone = await pollFile();
        if (isDone) break;
        await new Promise(resolve => setTimeout(resolve, 2000));
      }
    };

    fetchFile();
    if (!fileData || fileData.status === 'uploading' || fileData.status === 'transcribing') {
      startPolling();
    }
  }, [fileId]);

  const handlePointToggle = (point: string) => {
    setSelectedPoints(prev => {
      if (prev.includes(point)) {
        return prev.filter(p => p !== point);
      }
      return [...prev, point];
    });
  };

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', p: 3 }}>
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Alert severity="error" sx={{ m: 2 }}>
        {error}
      </Alert>
    );
  }

  if (!fileData) {
    return (
      <Alert severity="info" sx={{ m: 2 }}>
        No file data available
      </Alert>
    );
  }

  return (
    <Box sx={{ p: 2 }}>
      <Paper sx={{ p: 2, mb: 2 }}>
        <Typography variant="h6" gutterBottom>
          <DescriptionIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
          File Status: {fileData.status}
        </Typography>
        
        {fileData.transcription && (
          <>
            <Typography variant="subtitle1" gutterBottom sx={{ mt: 2 }}>
              Transcription:
            </Typography>
            <Paper variant="outlined" sx={{ p: 2, mb: 2, maxHeight: '200px', overflow: 'auto' }}>
              <Typography variant="body2">
                {fileData.transcription.text}
              </Typography>
            </Paper>

            <Typography variant="subtitle1" gutterBottom>
              Key Points:
            </Typography>
            <List>
              {fileData.transcription.key_points.map((point, index) => (
                <ListItem
                  key={index}
                  dense
                  onClick={() => handlePointToggle(point.text)}
                  sx={{ cursor: 'pointer' }}
                >
                  <Checkbox
                    edge="start"
                    checked={selectedPoints.includes(point.text)}
                    tabIndex={-1}
                    disableRipple
                  />
                  <ListItemText primary={point.text} />
                </ListItem>
              ))}
            </List>

            <Button
              variant="contained"
              color="primary"
              disabled={selectedPoints.length === 0}
              onClick={() => onCreateBRD(selectedPoints)}
              sx={{ mt: 2 }}
            >
              Create BRD
            </Button>
          </>
        )}
      </Paper>
    </Box>
  );
};

export default FileViewer; 