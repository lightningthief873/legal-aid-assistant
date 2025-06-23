# AI-Backed Community Legal Aid Assistant

A containerized web application that provides free, localized legal advice for common legal issues using AI/LLM technology. This production-ready template allows developers to quickly deploy powerful legal assistance applications on NodeOps or any containerized infrastructure.

![Legal Aid Assistant](https://img.shields.io/badge/License-MIT-blue.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)
![NodeOps](https://img.shields.io/badge/NodeOps-Compatible-green.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green.svg)
![React](https://img.shields.io/badge/React-Frontend-blue.svg)

## 🚀 Features

### Core Functionality
- **AI-Powered Legal Analysis**: Automatically categorizes legal issues and provides confidence scores
- **Intelligent Advice Generation**: Generates detailed legal guidance using LLM technology
- **Document Generation**: Creates professional legal documents (demand letters, complaints, notices)
- **Resource Lookup**: Connects users to local legal aid organizations and resources
- **Multi-Category Support**: Handles tenant rights, consumer protection, employment, family law, and more

### Technical Features
- **Containerized Architecture**: Ready for deployment on NodeOps, Docker, or Kubernetes
- **Scalable Backend**: FastAPI with SQLAlchemy ORM and async support
- **Modern Frontend**: React with Tailwind CSS and shadcn/ui components
- **PDF Generation**: Professional document creation with ReportLab
- **Health Monitoring**: Built-in health checks and monitoring endpoints
- **Security**: Rate limiting, input validation, and secure API design

### Customization Options
- **Multi-LLM Support**: OpenAI GPT or local LLM integration
- **Jurisdiction Flexibility**: Easily customizable for different legal systems
- **Template System**: Extensible document templates for various legal needs
- **Resource Database**: Configurable legal resource directory
- **Branding**: Customizable UI themes and organization branding

## 📋 Table of Contents

- [Quick Start](#quick-start)
- [Architecture](#architecture)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Deployment](#deployment)
- [Customization](#customization)
- [Contributing](#contributing)
- [License](#license)

## ⚡ Quick Start

### Prerequisites
- Docker and Docker Compose
- OpenAI API key (or local LLM setup)
- 2GB RAM minimum, 4GB recommended

### 1-Minute Deployment

```bash
# Clone the repository
git clone <repository-url>
cd legal-aid-assistant

# Configure environment
cp .env.production .env
# Edit .env with your OpenAI API key and other settings

# Deploy with Docker Compose
./deploy.sh dev

# Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/api/docs
```

## 🏗️ Architecture

### System Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React Frontend │    │  FastAPI Backend │    │   LLM Service   │
│                 │    │                 │    │                 │
│ • User Interface│◄──►│ • Legal Analysis│◄──►│ • OpenAI GPT    │
│ • Form Handling │    │ • Advice Gen.   │    │ • Local LLM     │
│ • PDF Download  │    │ • Doc Generation│    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │
         │                       ▼
         │              ┌─────────────────┐
         │              │   SQLite/       │
         │              │   PostgreSQL    │
         └──────────────┤                 │
                        │ • Legal Issues  │
                        │ • Advice Records│
                        │ • Templates     │
                        │ • Resources     │
                        └─────────────────┘
```

### Component Details

#### Backend (FastAPI)
- **Legal Analyzer**: Categorizes issues and determines urgency
- **LLM Service**: Interfaces with OpenAI or local LLM for advice generation
- **Document Generator**: Creates PDF documents using ReportLab
- **Resource Manager**: Manages legal aid organization database
- **API Layer**: RESTful endpoints with automatic documentation

#### Frontend (React)
- **Issue Submission**: Multi-step form for legal issue input
- **Analysis Display**: Visual representation of AI analysis results
- **Advice Interface**: Formatted display of legal guidance
- **Document Management**: Template selection and PDF generation
- **Resource Browser**: Searchable directory of legal resources

#### Data Layer
- **Legal Issues**: User-submitted problems with metadata
- **Advice Records**: Generated guidance with confidence scores
- **Document Templates**: Customizable legal document formats
- **Legal Resources**: Directory of aid organizations and contacts

## 🛠️ Installation

### Development Setup

1. **Clone Repository**
   ```bash
   git clone <repository-url>
   cd legal-aid-assistant
   ```

2. **Backend Setup**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Frontend Setup**
   ```bash
   cd frontend/legal-aid-frontend
   npm install
   # or
   pnpm install
   ```

4. **Environment Configuration**
   ```bash
   cp backend/.env.example .env
   # Edit .env with your configuration
   ```

5. **Database Initialization**
   ```bash
   cd backend
   python init_db.py
   ```

### Docker Setup

1. **Build Images**
   ```bash
   docker-compose build
   ```

2. **Start Services**
   ```bash
   docker-compose up -d
   ```

3. **Initialize Database**
   ```bash
   docker-compose exec backend python init_db.py
   ```

## ⚙️ Configuration

### Environment Variables

#### Required Settings
```bash
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
SECRET_KEY=your-secure-secret-key

# Database
DATABASE_URL=sqlite:///./legal_aid.db

# Application
DEBUG=false
DEFAULT_JURISDICTION=US
```

#### Optional Settings
```bash
# Local LLM (alternative to OpenAI)
USE_LOCAL_LLM=false
LOCAL_LLM_URL=http://localhost:11434/api/generate

# Rate Limiting
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=3600

# Customization
ORG_NAME="Community Legal Aid"
ORG_CONTACT_EMAIL="help@legal-aid.org"
```

### LLM Configuration

#### OpenAI Setup (Recommended)
1. Get API key from [OpenAI Platform](https://platform.openai.com/)
2. Set `OPENAI_API_KEY` in environment
3. Configure model: `OPENAI_MODEL=gpt-3.5-turbo`

#### Local LLM Setup (Alternative)
1. Install [Ollama](https://ollama.ai/) or similar
2. Set `USE_LOCAL_LLM=true`
3. Configure endpoint: `LOCAL_LLM_URL=http://localhost:11434/api/generate`

## 📖 Usage

### For End Users

1. **Submit Legal Issue**
   - Navigate to the application
   - Fill out the issue description form
   - Specify location and urgency level
   - Submit for AI analysis

2. **Review Analysis**
   - View categorization and confidence score
   - See suggested next steps
   - Proceed to get detailed advice

3. **Get Legal Advice**
   - Receive AI-generated legal guidance
   - Review recommended actions
   - See relevant laws and regulations

4. **Generate Documents**
   - Select appropriate document template
   - Customize with your information
   - Download professional PDF documents

5. **Find Resources**
   - Browse local legal aid organizations
   - Get contact information and specialties
   - Access relevant websites and resources

### For Administrators

1. **Monitor Usage**
   - Access health endpoints: `/api/health`
   - View application metrics
   - Monitor error logs

2. **Manage Templates**
   - Add new document templates
   - Customize existing templates
   - Update legal language

3. **Update Resources**
   - Add local legal organizations
   - Update contact information
   - Manage resource categories

## 📚 API Documentation

### Core Endpoints

#### Legal Analysis
```http
POST /api/analyze
Content-Type: application/json

{
  "description": "My landlord won't fix the heating",
  "location": "California",
  "urgency": "high"
}
```

#### Advice Generation
```http
POST /api/advice
Content-Type: application/json

{
  "issue_id": 1,
  "additional_context": "Lease expires next month"
}
```

#### Document Generation
```http
POST /api/generate
Content-Type: application/json

{
  "issue_id": 1,
  "template_id": 1,
  "document_type": "demand_letter"
}
```

#### Resource Lookup
```http
GET /api/resources?jurisdiction=US&organization_type=legal_aid
```

### Response Formats

#### Analysis Response
```json
{
  "category": "tenant_rights",
  "confidence": 0.95,
  "urgency": "high",
  "suggested_actions": [
    "Document all communications with landlord",
    "Take photos of heating issues",
    "Review lease agreement"
  ],
  "relevant_templates": [...]
}
```

#### Advice Response
```json
{
  "advice": "Based on California tenant law...",
  "next_steps": [
    "Send written notice to landlord",
    "Contact local housing authority"
  ],
  "relevant_laws": [
    "California Civil Code Section 1941.1",
    "Warranty of Habitability"
  ],
  "confidence": 0.88
}
```

### Interactive API Documentation

Access the full interactive API documentation at:
- **Swagger UI**: `http://localhost:8000/api/docs`
- **ReDoc**: `http://localhost:8000/api/redoc`

## 🚀 Deployment

### NodeOps Deployment

1. **Prepare Configuration**
   ```bash
   # Edit nodeops-deployment.yaml
   # Update secrets and domain names
   ```

2. **Deploy to NodeOps**
   ```bash
   kubectl apply -f nodeops-deployment.yaml
   ```

3. **Verify Deployment**
   ```bash
   kubectl get pods -l app=legal-aid-backend
   kubectl get services
   ```

### Docker Swarm Deployment

1. **Initialize Swarm**
   ```bash
   docker swarm init
   ```

2. **Deploy Stack**
   ```bash
   docker stack deploy -c docker-compose.prod.yml legal-aid
   ```

### Traditional Server Deployment

1. **Install Dependencies**
   ```bash
   # Install Python 3.11, Node.js 18+, nginx
   ```

2. **Build Frontend**
   ```bash
   cd frontend/legal-aid-frontend
   npm run build
   ```

3. **Configure nginx**
   ```bash
   # Copy nginx configuration
   # Set up SSL certificates
   ```

4. **Start Services**
   ```bash
   # Start backend with gunicorn
   # Serve frontend with nginx
   ```

### Environment-Specific Configurations

#### Development
```bash
./deploy.sh dev
```

#### Staging
```bash
./deploy.sh prod
# With staging environment variables
```

#### Production
```bash
./deploy.sh prod
# With production SSL and monitoring
```

## 🎨 Customization

### Legal Categories

Add new legal categories by updating:
1. `backend/app/models/schemas.py` - Add to `LegalCategory` enum
2. `backend/app/services/legal_analyzer.py` - Add category templates
3. Frontend category displays

### Document Templates

Create new templates:
1. Add template to `backend/init_db.py`
2. Create template content with Jinja2 syntax
3. Update frontend template selection

### UI Customization

Modify the frontend:
1. Update `src/App.css` for styling
2. Modify components in `src/components/`
3. Change branding in header and footer

### LLM Prompts

Customize AI behavior:
1. Edit prompts in `backend/app/services/llm_service.py`
2. Adjust temperature and token limits
3. Add domain-specific instructions

## 🧪 Testing

### Backend Testing
```bash
cd backend
pytest tests/
```

### Frontend Testing
```bash
cd frontend/legal-aid-frontend
npm test
```

### Integration Testing
```bash
# Start services
docker-compose up -d

# Run integration tests
python tests/integration/test_api.py
```

### Load Testing
```bash
# Install artillery
npm install -g artillery

# Run load tests
artillery run tests/load/api-load-test.yml
```

## 📊 Monitoring

### Health Checks
- Backend: `GET /api/health`
- Frontend: `GET /health`
- Database connectivity
- LLM service availability

### Metrics
- Request count and latency
- Error rates by endpoint
- Document generation statistics
- User engagement metrics

### Logging
- Structured JSON logging
- Error tracking with stack traces
- User action audit logs
- Performance monitoring

## 🔒 Security

### Data Protection
- Input validation and sanitization
- SQL injection prevention
- XSS protection
- Rate limiting

### API Security
- CORS configuration
- Request size limits
- Authentication (optional)
- HTTPS enforcement

### Privacy
- No persistent user data storage
- Optional email collection
- Data retention policies
- GDPR compliance ready

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Workflow
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

### Code Standards
- Python: Black formatting, type hints
- JavaScript: ESLint, Prettier
- Documentation: Clear comments and docstrings
- Testing: Comprehensive test coverage

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

### Documentation
- [API Reference](docs/api.md)
- [Deployment Guide](docs/deployment.md)
- [Customization Guide](docs/customization.md)

### Community
- [GitHub Issues](https://github.com/your-org/legal-aid-assistant/issues)
- [Discussions](https://github.com/your-org/legal-aid-assistant/discussions)
- [Discord Community](https://discord.gg/legal-aid-assistant)

### Professional Support
For enterprise deployments and custom development:
- Email: support@legal-aid-assistant.com
- Website: https://legal-aid-assistant.com

## 🙏 Acknowledgments

- OpenAI for GPT API
- FastAPI and React communities
- Legal aid organizations worldwide
- NodeOps platform team

---

**Disclaimer**: This tool provides general legal information only and is not a substitute for professional legal advice. Always consult with a qualified attorney for legal matters specific to your situation.

