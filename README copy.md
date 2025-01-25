# CloudPioneer

An AI-powered cloud resource optimization platform that intelligently manages cloud resources to reduce costs and improve efficiency.

> **Note**: This is a private repository. Access is restricted to authorized contributors only.

## Features

- AI-powered resource usage prediction
- Automated scheduling of cloud resource shutdown/startup
- Real-time monitoring and visualization
- Multi-cloud support
- Cost and sustainability tracking
- Authentication System
  - Email/Password Authentication
  - Google OAuth Integration
  - JWT-based Session Management

## Project Structure
```
cloud-pioneer/
├── src/                    # Source code
│   ├── agents/            # Resource monitoring agents
│   ├── api/               # API endpoints
│   ├── ml/                # Machine learning models
│   └── scheduler/         # Scheduling engine
├── tests/                 # Test files
├── config/                # Configuration files
└── docs/                  # Documentation
```

## Requirements

- Python 3.9+
- TensorFlow 2.x
- FastAPI
- PostgreSQL
- Docker & Kubernetes

## Getting Started

CloudPioneer can be set up either using Docker or running services locally. Choose the method that best suits your development needs.

### Prerequisites

- Python 3.9+
- Node.js and npm (for frontend)
- Git
- Docker and Docker Compose (optional)
- PostgreSQL (if not using Docker)

### Quick Start with Docker

1. Clone the repository:
   ```bash
   git clone https://github.com/ashedrack/code-pilot.git
   ```

2. Copy environment configuration:
   ```bash
   cp .env.example .env
   ```

3. Build and start services:
   ```bash
   docker compose up --build
   ```

### Local Development Setup

1. Clone and setup backend:
   ```bash
   git clone https://github.com/ashedrack/code-pilot.git
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. Setup frontend:
   ```bash
   cd frontend
   npm install
   ```

3. Start services:
   ```bash
   # Terminal 1 - Backend
   python -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload

   # Terminal 2 - Frontend
   cd frontend
   npm start
   ```

### Access the Application

- Frontend Dashboard: http://localhost:3000
- API Documentation: http://localhost:8000/docs
- Backend API: http://localhost:8000

For detailed setup instructions and troubleshooting, refer to our [Technical Documentation](docs/technical_documentation.md).

## Contributing

This is a private repository. Please contact the repository owner for contribution guidelines and access permissions.

## License

MIT License
