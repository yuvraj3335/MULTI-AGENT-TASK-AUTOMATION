import React, { useState, useEffect } from 'react';
import {
  Box,
  Paper,
  Typography,
  CircularProgress,
  Button,
  Alert,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  List,
  ListItem,
  ListItemText,
  Divider,
} from '@mui/material';
import api, { Ticket } from '../services/api';

interface TicketManagerProps {
  brdId?: string;
}

const TicketManager: React.FC<TicketManagerProps> = ({ brdId }) => {
  const [tickets, setTickets] = useState<Ticket[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [createDialogOpen, setCreateDialogOpen] = useState(false);
  const [newTicket, setNewTicket] = useState({
    title: '',
    description: '',
    type: 'feature',
  });

  useEffect(() => {
    fetchTickets();
  }, []);

  const fetchTickets = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await api.getTickets();
      setTickets(brdId ? response.filter(t => t.brd_id === brdId) : response);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load tickets');
    } finally {
      setLoading(false);
    }
  };

  const handleCreateTicket = async () => {
    if (!brdId) return;

    try {
      await api.createTicket(
        brdId,
        newTicket.title,
        newTicket.description,
        newTicket.type
      );
      setCreateDialogOpen(false);
      setNewTicket({ title: '', description: '', type: 'feature' });
      fetchTickets();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create ticket');
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

  return (
    <Box sx={{ p: 2 }}>
      <Paper sx={{ p: 2 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
          <Typography variant="h6">
            Tickets
          </Typography>
          {brdId && (
            <Button
              variant="contained"
              onClick={() => setCreateDialogOpen(true)}
            >
              Create Ticket
            </Button>
          )}
        </Box>

        {tickets.length === 0 ? (
          <Typography color="textSecondary">
            No tickets found
          </Typography>
        ) : (
          <List>
            {tickets.map((ticket, index) => (
              <React.Fragment key={ticket.id}>
                {index > 0 && <Divider />}
                <ListItem>
                  <ListItemText
                    primary={ticket.title}
                    secondary={
                      <>
                        <Typography component="span" variant="body2" color="textSecondary">
                          Type: {ticket.type}
                        </Typography>
                        <br />
                        <Typography component="span" variant="body2">
                          {ticket.description}
                        </Typography>
                      </>
                    }
                  />
                </ListItem>
              </React.Fragment>
            ))}
          </List>
        )}
      </Paper>

      <Dialog
        open={createDialogOpen}
        onClose={() => setCreateDialogOpen(false)}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>Create New Ticket</DialogTitle>
        <DialogContent>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, mt: 1 }}>
            <TextField
              label="Title"
              value={newTicket.title}
              onChange={(e) => setNewTicket(prev => ({ ...prev, title: e.target.value }))}
              fullWidth
            />
            <TextField
              label="Description"
              multiline
              rows={4}
              value={newTicket.description}
              onChange={(e) => setNewTicket(prev => ({ ...prev, description: e.target.value }))}
              fullWidth
            />
            <FormControl fullWidth>
              <InputLabel>Type</InputLabel>
              <Select
                value={newTicket.type}
                label="Type"
                onChange={(e) => setNewTicket(prev => ({ ...prev, type: e.target.value }))}
              >
                <MenuItem value="feature">Feature</MenuItem>
                <MenuItem value="bug">Bug</MenuItem>
                <MenuItem value="improvement">Improvement</MenuItem>
              </Select>
            </FormControl>
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setCreateDialogOpen(false)}>Cancel</Button>
          <Button
            onClick={handleCreateTicket}
            variant="contained"
            disabled={!newTicket.title || !newTicket.description}
          >
            Create
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default TicketManager; 