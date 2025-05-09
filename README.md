# Multi-Agent Task Automation System

A  task automation system that leverages multiple AI agents to streamline and automate complex workflows. The system combines modern web technologies with advanced AI capabilities to provide an intuitive and powerful task automation platform.

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
### Core Components

1. **Reasoning & Planning Agent**
   - The heart of the system, coordinating all the agents and managing their interactions.
   - Keeps the workflow running smoothly, prioritizes tasks, and ensures everything stays on track.
   - Handles any errors that pop up and ensures that the system’s state remains consistent.

2. **Specialized Agents**
   - **Audio-to-Text Agent**: Transcribes audio and video content into text using OpenAI Whisper.
   - **Key Point Extraction Agent**: Pulls out important information from text using sentence transformers.
   - **Knowledge Base Agent**: Takes care of storing and retrieving all data.
   - **BRD Author Agent**: Automatically generates Business Requirement Documents from the gathered data.
   - **Task Management Agent**: Responsible for creating, assigning, and tracking tasks throughout the process.
   - **Quality Check Agent**: Ensures that everything produced meets the highest quality standards and compliance.
   - **Communication Agent**: Handles all notifications and communication between agents.
   - **Feedback Agent**: Collects user feedback and uses it to continuously improve the system.

### Workflow Process

1. **Input Processing**
   - The system can handle different types of input, like audio, video, and PDF files.
   - Files are checked, validated, and stored securely.
   - Each file gets a unique ID for easy tracking.

2. **Content Extraction**
   - Audio and video files are converted into text.
   - PDFs are processed to pull out all the text content.
   - Everything is standardized for consistent processing.

3. **Information Analysis**
   - Important details are extracted from the content using advanced Natural Language Processing (NLP).
   - A deeper semantic analysis is performed to understand the meaning behind the words.
   - The content is converted into vectors for easy comparison and matching.

4. **Document Generation**
   - Business Requirement Documents (BRDs) are created from the extracted information.
   - A quality check is done on the generated documents to ensure they meet the required standards.
   - The documents are then converted into a standardized format like PDF.

5. **Task Management**
   - Tasks are generated from the BRDs and automatically assigned and prioritized.
   - The system keeps track of the task’s progress and updates the status in real-time.

### Technical Implementation

#### Backend Architecture
```python
# How the agents interact in the system
ReasoningPlanningAgent
├── AudioToTextAgent      # Converts audio/video to text
├── KeyPointExtractionAgent   # Pulls out key information from content
├── KnowledgeBaseAgent    # Stores and retrieves all data
├── BRDAuthorAgent        # Generates Business Requirement Documents
├── TaskManagementAgent   # Manages task creation and tracking
├── QualityCheckAgent     # Ensures content quality
├── CommunicationAgent    # Handles notifications
└── FeedbackAgent         # Gathers and processes user feedback

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


