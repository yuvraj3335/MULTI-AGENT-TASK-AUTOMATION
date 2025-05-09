import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

export interface FileResponse {
  file_id: string;
  file_path: string;
  status: string;
  upload_time: string;
  error: string | null;
  transcription?: {
    id: string;
    file_id: string;
    text: string;
    key_points: Array<{
      text: string;
      embedding: number[];
    }>;
    timestamp: string;
  };
}

export interface BRD {
  id: string;
  transcription_id: string;
  selected_key_points: string[];
  content: string;
  pdf_path: string;
  embedding: number[];
  created_at: string;
}

export interface Ticket {
  id: string;
  brd_id: string;
  title: string;
  description: string;
  type: string;
  status: string;
  created_at: string;
}

const api = {
  // File operations
  uploadFile: async (file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    const response = await axios.post(`${API_BASE_URL}/agents/upload`, formData);
    return response.data;
  },

  getFile: async (fileId: string): Promise<FileResponse> => {
    const response = await axios.get(`${API_BASE_URL}/agents/files/${fileId}`);
    return response.data;
  },

  // BRD operations
  createBRD: async (fileId: string, selectedKeyPoints: string[]) => {
    const response = await axios.post(`${API_BASE_URL}/agents/brds`, {
      file_id: fileId,
      selected_key_points: selectedKeyPoints,
    });
    return response.data;
  },

  getBRD: async (brdId: string): Promise<BRD> => {
    const response = await axios.get(`${API_BASE_URL}/agents/brds/${brdId}`);
    return response.data;
  },

  getBRDPDF: async (brdId: string) => {
    window.open(`${API_BASE_URL}/agents/brds/${brdId}/pdf`, '_blank');
  },

  getSimilarBRDs: async (selectedKeyPoints: string[]) => {
    const response = await axios.post(`${API_BASE_URL}/agents/similar_brds`, {
      selected_key_points: selectedKeyPoints,
    });
    return response.data;
  },

  // Ticket operations
  createTicket: async (brdId: string, title: string, description: string, type: string) => {
    const response = await axios.post(`${API_BASE_URL}/agents/tickets`, {
      brd_id: brdId,
      title,
      description,
      type,
    });
    return response.data;
  },

  getTickets: async (): Promise<Ticket[]> => {
    const response = await axios.get(`${API_BASE_URL}/agents/tickets`);
    return response.data;
  },

  // Feedback operations
  submitFeedback: async (brdId: string, rating: number, comments: string) => {
    const response = await axios.post(`${API_BASE_URL}/agents/feedback`, {
      brd_id: brdId,
      rating,
      comments,
    });
    return response.data;
  },
};

export default api; 