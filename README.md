# Multi-Agent Task Automation System

A sophisticated task automation system that leverages multiple AI agents to streamline and automate complex workflows. The system combines modern web technologies with advanced AI capabilities to provide an intuitive and powerful task automation platform.

## 🚀 Features

- **Multi-Agent Collaboration**: Orchestrates multiple AI agents to work together on complex tasks
- **Interactive Web Interface**: Modern React-based UI for easy task management and monitoring
- **Real-time Task Processing**: FastAPI backend for efficient task handling and agent coordination
- **Advanced AI Integration**: Incorporates various AI models and capabilities through Hugging Face Hub
- **Document Processing**: Supports PDF processing and text analysis
- **Scalable Architecture**: Built with modern tools and practices for production deployment

## 🧠 System Architecture & Working Principles

### Multi-Agent System Overview

The system implements a sophisticated multi-agent architecture where specialized AI agents collaborate to process and transform various types of inputs into structured business outputs. Here's a detailed breakdown of the system's components and their interactions:

#### Core Components

1. **Reasoning & Planning Agent**
   - Acts as the central coordinator for all agent activities
   - Manages the workflow and orchestrates agent interactions
   - Handles error recovery and task prioritization
   - Maintains the system's state and ensures data consistency

2. **Specialized Agents**
   - **Audio-to-Text Agent**: Converts audio/video content to text using OpenAI Whisper
   - **Key Point Extraction Agent**: Uses sentence transformers to identify and extract crucial information
   - **Knowledge Base Agent**: Manages data persistence and retrieval operations
   - **BRD Author Agent**: Generates Business Requirement Documents from processed information
   - **Task Management Agent**: Handles task creation, assignment, and tracking
   - **Quality Check Agent**: Ensures output quality and compliance
   - **Communication Agent**: Manages notifications and inter-agent communication
   - **Feedback Agent**: Processes and incorporates user feedback for system improvement

### Workflow Process

1. **Input Processing**
   - System accepts multiple input formats (audio, video, PDF)
   - Files are validated and stored securely
   - Unique identifiers are assigned for tracking

2. **Content Extraction**
   - Audio/video files are transcribed to text
   - PDFs are processed for text extraction
   - Content is normalized for consistent processing

3. **Information Analysis**
   - Key points are extracted using advanced NLP
   - Semantic analysis is performed using sentence transformers
   - Content is vectorized for similarity matching

4. **Document Generation**
   - BRDs are generated based on extracted information
   - Quality checks are performed on generated content
   - Documents are converted to standardized formats (PDF)

5. **Task Management**
   - Tasks are created based on document content
   - Automatic assignment and prioritization
   - Progress tracking and status updates

### Technical Implementation

#### Backend Architecture
```python
# Core components interaction
ReasoningPlanningAgent
├── AudioToTextAgent      # Handles media transcription
├── KeyPointExtractionAgent   # Extracts key information
├── KnowledgeBaseAgent    # Manages data persistence
├── BRDAuthorAgent       # Generates documents
├── TaskManagementAgent  # Handles task workflow
├── QualityCheckAgent    # Ensures output quality
├── CommunicationAgent   # Manages notifications
└── FeedbackAgent       # Processes user feedback
```

#### Key Features Implementation

1. **Intelligent Document Processing**
   - Utilizes PyPDF2 for PDF processing
   - Implements OpenAI Whisper for audio transcription
   - Uses sentence transformers for semantic analysis

2. **Smart Content Matching**
   - Employs cosine similarity for content comparison
   - Maintains vector embeddings for quick matching
   - Implements intelligent suggestion system

3. **Asynchronous Processing**
   - Uses FastAPI for async request handling
   - Implements background tasks for long-running processes
   - Maintains task queues for efficient processing

4. **Data Management**
   - MongoDB for structured data storage
   - File-based storage for documents and media
   - Efficient serialization and deserialization

### System Intelligence

1. **Adaptive Learning**
   - System learns from user feedback
   - Continuously improves document generation
   - Adapts to different content types and formats

2. **Quality Assurance**
   - Automated validation of generated content
   - Consistency checks across documents
   - Error detection and correction

3. **Smart Recommendations**
   - Suggests similar existing documents
   - Provides intelligent task assignments
   - Offers content improvement suggestions

## 🛠️ Tech Stack

### Frontend
- React 19.1.0
- Material-UI (MUI) for component design
- Vite for build tooling
- React Router for navigation
- Axios for API communication

### Backend
- FastAPI framework
- MongoDB for data persistence
- Sentence Transformers for text processing
- OpenAI Whisper for audio processing
- Python 3.x

## 📋 Prerequisites

- Node.js (v16 or higher)
- Python 3.8 or higher
- MongoDB instance
- Virtual environment tool (venv)

## 🔧 Installation

### Backend Setup
1. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment variables:
   Create a `.env` file in the backend directory with necessary credentials.

### Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

## 🚀 Running the Application

### Development Mode

1. Start the backend server:
   ```bash
   cd backend
   uvicorn server:app --reload
   ```

2. Start the frontend development server:
   ```bash
   cd frontend
   npm run dev
   ```

### Production Mode

1. Build the frontend:
   ```bash
   cd frontend
   npm run build
   ```

2. Start the backend server:
   ```bash
   cd backend
   uvicorn server:app
   ```

## 📁 Project Structure

```
.
├── frontend/               # React frontend application
│   ├── src/               # Source code
│   ├── public/            # Static assets
│   └── package.json       # Frontend dependencies
├── backend/               # FastAPI backend
│   ├── server.py         # Main server file
│   ├── schema.py         # Data models
│   ├── agents/           # AI agent implementations
│   └── templates/        # Backend templates
├── docs/                 # Documentation
├── data/                 # Data storage
└── requirements.txt      # Python dependencies
```

## 🔐 Security

- Environment variables are used for sensitive data


