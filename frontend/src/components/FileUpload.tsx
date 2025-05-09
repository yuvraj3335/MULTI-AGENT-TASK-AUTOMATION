import React, { useState, useCallback } from 'react';
import { Box, Button, CircularProgress, Typography, Alert } from '@mui/material';
import { CloudUpload as CloudUploadIcon } from '@mui/icons-material';
import api from '../services/api';

interface FileUploadProps {
  onUploadSuccess: (fileId: string) => void;
}

const FileUpload: React.FC<FileUploadProps> = ({ onUploadSuccess }) => {
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleFileUpload = useCallback(async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    setUploading(true);
    setError(null);

    try {
      const response = await api.uploadFile(file);
      if (response.error) {
        throw new Error(response.error);
      }
      onUploadSuccess(response.file_id);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to upload file');
    } finally {
      setUploading(false);
    }
  }, [onUploadSuccess]);

  return (
    <Box sx={{ textAlign: 'center', p: 3 }}>
      <input
        accept=".pdf,.mp3,.mp4,.wav"
        style={{ display: 'none' }}
        id="file-upload"
        type="file"
        onChange={handleFileUpload}
        disabled={uploading}
      />
      <label htmlFor="file-upload">
        <Button
          variant="contained"
          component="span"
          disabled={uploading}
          startIcon={uploading ? <CircularProgress size={20} /> : <CloudUploadIcon />}
          sx={{ mb: 2 }}
        >
          {uploading ? 'Uploading...' : 'Upload File'}
        </Button>
      </label>
      
      <Typography variant="body2" color="textSecondary" sx={{ mt: 1 }}>
        Supported formats: PDF, MP3, MP4, WAV
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mt: 2 }}>
          {error}
        </Alert>
      )}
    </Box>
  );
};

export default FileUpload; 