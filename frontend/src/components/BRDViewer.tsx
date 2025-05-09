import React, { useState, useEffect } from 'react';
import {
  Box,
  Paper,
  Typography,
  CircularProgress,
  Button,
  Alert,
  Rating,
  TextField,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
} from '@mui/material';
import { PictureAsPdf as PdfIcon } from '@mui/icons-material';
import api, { BRD } from '../services/api';

interface BRDViewerProps {
  brdId: string;
}

const BRDViewer: React.FC<BRDViewerProps> = ({ brdId }) => {
  const [brd, setBRD] = useState<BRD | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [feedbackOpen, setFeedbackOpen] = useState(false);
  const [rating, setRating] = useState<number | null>(null);
  const [comments, setComments] = useState('');
  const [submittingFeedback, setSubmittingFeedback] = useState(false);

  useEffect(() => {
    const fetchBRD = async () => {
      try {
        setLoading(true);
        setError(null);
        const response = await api.getBRD(brdId);
        setBRD(response);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load BRD');
      } finally {
        setLoading(false);
      }
    };

    fetchBRD();
  }, [brdId]);

  const handleViewPDF = () => {
    api.getBRDPDF(brdId);
  };

  const handleSubmitFeedback = async () => {
    if (!rating) return;

    try {
      setSubmittingFeedback(true);
      await api.submitFeedback(brdId, rating, comments);
      setFeedbackOpen(false);
      setRating(null);
      setComments('');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to submit feedback');
    } finally {
      setSubmittingFeedback(false);
    }
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

  if (!brd) {
    return (
      <Alert severity="info" sx={{ m: 2 }}>
        No BRD data available
      </Alert>
    );
  }

  return (
    <Box sx={{ p: 2 }}>
      <Paper sx={{ p: 2 }}>
        <Typography variant="h6" gutterBottom>
          Business Requirements Document
        </Typography>

        <Typography variant="subtitle1" gutterBottom sx={{ mt: 2 }}>
          Selected Key Points:
        </Typography>
        <Paper variant="outlined" sx={{ p: 2, mb: 2 }}>
          {brd.selected_key_points.map((point, index) => (
            <Typography key={index} variant="body2" paragraph>
              • {point}
            </Typography>
          ))}
        </Paper>

        <Typography variant="subtitle1" gutterBottom>
          Generated Content:
        </Typography>
        <Paper variant="outlined" sx={{ p: 2, mb: 2, whiteSpace: 'pre-wrap' }}>
          <Typography variant="body2">
            {brd.content}
          </Typography>
        </Paper>

        <Box sx={{ display: 'flex', gap: 2, mt: 2 }}>
          <Button
            variant="contained"
            startIcon={<PdfIcon />}
            onClick={handleViewPDF}
          >
            View PDF
          </Button>
          <Button
            variant="outlined"
            onClick={() => setFeedbackOpen(true)}
          >
            Provide Feedback
          </Button>
        </Box>
      </Paper>

      <Dialog open={feedbackOpen} onClose={() => setFeedbackOpen(false)}>
        <DialogTitle>Provide Feedback</DialogTitle>
        <DialogContent>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, mt: 1 }}>
            <Typography component="legend">Rating</Typography>
            <Rating
              value={rating}
              onChange={(_, value) => setRating(value)}
              precision={0.5}
            />
            <TextField
              label="Comments"
              multiline
              rows={4}
              value={comments}
              onChange={(e) => setComments(e.target.value)}
              fullWidth
            />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setFeedbackOpen(false)}>Cancel</Button>
          <Button
            onClick={handleSubmitFeedback}
            disabled={!rating || submittingFeedback}
            variant="contained"
          >
            Submit
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default BRDViewer; 