# CloudPioneer - Enterprise Cloud Optimization Platform

CloudPioneer is a SaaS platform that provides intelligent cloud resource optimization at scale. Our platform helps organizations reduce cloud costs, improve efficiency, and maintain optimal performance across their entire cloud infrastructure.

[![License](https://img.shields.io/badge/license-Enterprise-blue.svg)](https://cloudpioneer.com/license)
[![Security Rating](https://img.shields.io/badge/security-A+-brightgreen.svg)](https://cloudpioneer.com/security)

## Why CloudPioneer?

- **One-Click Deployment**: Install our agent with a single command
- **Cost Optimization**: Reduce cloud costs by up to 40%
- **AI-Powered**: Intelligent resource prediction and optimization
- **Enterprise-Grade Security**: SOC 2 Type II certified
- **Global Scale**: Built for millions of concurrent nodes
- **Real-Time Analytics**: Comprehensive dashboards and insights

## Features

### Core Capabilities
- AI-powered resource usage prediction
- Automated resource optimization
- Real-time monitoring and visualization
- Multi-cloud support (AWS, GCP, Azure)
- Cost and sustainability tracking
- Anomaly detection and alerting

### Enterprise Features
- Multi-tenant architecture
- Role-based access control (RBAC)
- Custom branding options
- API access with SDKs
- Webhook integrations
- Advanced analytics and reporting

### Security & Compliance
- SOC 2 Type II certified
- GDPR compliant
- End-to-end encryption
- Audit logging
- SSO integration (Okta, Azure AD, Google)

## Quick Start

### Install Agent
```bash
curl -fsSL https://install.cloudpioneer.com | bash -s -- --api-key YOUR_API_KEY
```

### Access Dashboard
Visit [https://dashboard.cloudpioneer.com](https://dashboard.cloudpioneer.com) to access your account.

## Documentation

- [Getting Started Guide](https://docs.cloudpioneer.com/getting-started)
- [API Reference](https://docs.cloudpioneer.com/api)
- [Security Overview](https://docs.cloudpioneer.com/security)
- [Enterprise Features](https://docs.cloudpioneer.com/enterprise)
- [SDK Documentation](https://docs.cloudpioneer.com/sdk)

## Architecture

```
cloudpioneer/
├── frontend/              # React-based dashboard
├── src/
│   ├── agent/            # Lightweight monitoring agent
│   ├── api/              # RESTful & GraphQL APIs
│   ├── auth/             # Authentication & authorization
│   ├── ml/               # ML optimization engine
│   ├── scheduler/        # Resource scheduling
│   └── streaming/        # Real-time data processing
├── terraform/            # Infrastructure as code
└── kubernetes/          # Container orchestration
```

## Project Setup Guide

### Prerequisites
- Git
- Homebrew (for macOS users)
- Python 3.10 (recommended) or higher

### Step-by-Step Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone [repository-url]
   cd Pioneer
   ```

2. **Install Python 3.10** (if not already installed)
   ```bash
   # For macOS users (using Homebrew)
   brew install python@3.10
   ```

3. **Create and Activate Virtual Environment**
   ```bash
   # Create virtual environment using Python 3.10
   /opt/homebrew/opt/python@3.10/bin/python3.10 -m venv venv

   # Activate virtual environment
   source venv/bin/activate  # For macOS/Linux
   ```

4. **Update Package Management Tools**
   ```bash
   # Upgrade pip and install wheel
   pip install --upgrade pip
   pip install wheel
   ```

5. **Install Project Dependencies**
   ```bash
   # Install required packages
   pip install -r requirements.txt
   pip install -e .
   ```

6. **Configure IDE**
   - When prompted, select the new virtual environment (`venv`) for your workspace
   - This ensures proper code completion and development tools integration

7. **Environment Variables**
   ```bash
   # Copy the example environment file
   cp .env.example .env
   # Edit .env with your specific configurations
   ```

### Development Setup

For frontend development:
```bash
cd frontend
npm install
npm start
```

### Starting the Development Servers

#### Backend (FastAPI)

1. **Start the Backend Server**
   ```bash
   # Make sure you're in the project root and virtual environment is activated
   cd /path/to/Pioneer
   source venv/bin/activate

   # Start the FastAPI server using uvicorn
   uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
   ```

   The backend server will be available at:
   - API Documentation: http://localhost:8000/docs
   - Alternative Documentation: http://localhost:8000/redoc
   - Health Check: http://localhost:8000/health
   - API Endpoints: http://localhost:8000/api/v1/

#### Frontend (React)

1. **Start the Frontend Development Server**
   ```bash
   # Navigate to the frontend directory
   cd frontend

   # Install dependencies (if not already installed)
   npm install

   # Start the development server
   npm start
   ```

   The frontend will automatically open in your default browser at http://localhost:3000

#### Development Notes

- Both servers support hot reloading - changes to the code will automatically trigger a refresh
- The frontend is configured to proxy API requests to the backend at http://localhost:8000
- Keep both servers running while developing
- The frontend includes:
  - Material-UI components
  - React Router for navigation
  - React Query for data fetching
  - Nivo and Recharts for data visualization

### Common Issues and Solutions

1. **Python Version Conflicts**
   - If you encounter compilation errors, ensure you're using Python 3.10
   - Some packages may not be compatible with newer Python versions

2. **Package Installation Errors**
   - If you encounter installation errors, try installing packages individually
   - Make sure you have the latest pip and wheel installed

3. **Virtual Environment Issues**
   - If the virtual environment isn't working, delete it and recreate:
     ```bash
     deactivate  # if already in a virtual environment
     rm -rf venv
     /opt/homebrew/opt/python@3.10/bin/python3.10 -m venv venv
     source venv/bin/activate
     ```

### Additional Resources
- [Python Virtual Environments Guide](https://docs.python.org/3/tutorial/venv.html)
- [Pip Package Manager Documentation](https://pip.pypa.io/en/stable/)

## Support

- Enterprise Support: [support@cloudpioneer.com](mailto:support@cloudpioneer.com)
- Documentation: [docs.cloudpioneer.com](https://docs.cloudpioneer.com)
- Status Page: [status.cloudpioneer.com](https://status.cloudpioneer.com)

## Pricing

Visit [cloudpioneer.com/pricing](https://cloudpioneer.com/pricing) for our pricing tiers:

- **Starter**: Free for up to 5 nodes
- **Pro**: For growing businesses
- **Enterprise**: Custom solutions for large organizations

## Security

Report security vulnerabilities to [security@cloudpioneer.com](mailto:security@cloudpioneer.com)

# CloudPioneer

Test change for branch protection rules.

## Overview
A cloud resource optimization platform that helps organizations manage and optimize their cloud infrastructure costs.

## Features
- Resource monitoring and optimization
- Cost analysis and recommendations
- Automated scaling and management
- Real-time alerts and notifications

## Getting Started
1. Clone the repository
2. Install dependencies
3. Configure environment variables
4. Run the application

## Documentation
- [API Documentation](docs/api_documentation.md)
- [Technical Documentation](docs/technical_documentation.md)
- [Troubleshooting Guide](docs/troubleshooting_guide.md)

## Contributing
Please read our [Contributing Guidelines](CONTRIBUTING.md) before submitting any changes.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
