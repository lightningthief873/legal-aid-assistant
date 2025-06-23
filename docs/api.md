# API Documentation

## Overview

The AI-Backed Community Legal Aid Assistant provides a RESTful API for legal issue analysis, advice generation, document creation, and resource lookup. All endpoints return JSON responses and follow standard HTTP status codes.

## Base URL

- Development: `http://localhost:8000/api`
- Production: `https://your-domain.com/api`

## Authentication

Currently, the API does not require authentication for basic usage. Future versions may include optional user authentication for enhanced features.

## Rate Limiting

- **Limit**: 100 requests per hour per IP address
- **Headers**: Rate limit information is included in response headers
  - `X-RateLimit-Limit`: Maximum requests allowed
  - `X-RateLimit-Remaining`: Requests remaining in current window
  - `X-RateLimit-Reset`: Time when the rate limit resets

## Error Handling

### Error Response Format

```json
{
  "error": "Error type",
  "detail": "Detailed error message",
  "timestamp": "2024-01-01T12:00:00Z"
}
```

### HTTP Status Codes

- `200 OK`: Request successful
- `400 Bad Request`: Invalid request data
- `404 Not Found`: Resource not found
- `422 Unprocessable Entity`: Validation error
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Server error

## Endpoints

### Health Check

#### GET /health

Check the health status of the API and its dependencies.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00Z",
  "version": "1.0.0",
  "database_connected": true,
  "llm_available": true
}
```

### Legal Issue Analysis

#### POST /analyze

Analyze a legal issue and provide categorization with initial guidance.

**Request Body:**
```json
{
  "description": "My landlord won't fix the broken heating system in my apartment",
  "location": "California",
  "urgency": "high",
  "user_email": "user@example.com"
}
```

**Parameters:**
- `description` (string, required): Detailed description of the legal issue
- `location` (string, optional): State, city, or jurisdiction
- `urgency` (string, optional): "low", "medium", or "high" (default: "medium")
- `user_email` (string, optional): User's email for follow-up

**Response:**
```json
{
  "category": "tenant_rights",
  "confidence": 0.95,
  "urgency": "high",
  "suggested_actions": [
    "Document all communications with your landlord",
    "Take photos of the heating system issues",
    "Review your lease agreement carefully"
  ],
  "relevant_templates": [
    {
      "id": 1,
      "name": "Tenant Demand for Repairs",
      "category": "tenant_rights",
      "description": "Letter demanding landlord make necessary repairs"
    }
  ],
  "estimated_complexity": "moderate"
}
```

### Legal Advice Generation

#### POST /advice

Generate detailed legal advice for a specific issue.

**Request Body:**
```json
{
  "issue_id": 1,
  "additional_context": "The lease expires next month and I'm worried about my security deposit"
}
```

**Parameters:**
- `issue_id` (integer, required): ID of the analyzed legal issue
- `additional_context` (string, optional): Additional information to consider

**Response:**
```json
{
  "id": 1,
  "issue_id": 1,
  "advice": "Based on California tenant law, your landlord has a legal obligation to maintain heating systems in rental properties. Under California Civil Code Section 1941.1, landlords must keep rental properties in habitable condition...",
  "next_steps": [
    "Send a written notice to your landlord requesting repairs",
    "Keep copies of all communications",
    "Contact your local housing authority if repairs aren't made",
    "Consider withholding rent if legally permitted in your jurisdiction"
  ],
  "relevant_laws": [
    "California Civil Code Section 1941.1",
    "Warranty of Habitability",
    "Local Housing Codes"
  ],
  "confidence": 0.88,
  "model_used": "gpt-3.5-turbo",
  "generated_at": "2024-01-01T12:00:00Z"
}
```

### Document Generation

#### POST /generate

Generate a legal document based on a template and issue data.

**Request Body:**
```json
{
  "issue_id": 1,
  "template_id": 1,
  "document_type": "demand_letter",
  "custom_data": {
    "sender_name": "John Doe",
    "sender_address": "123 Main St, Anytown, CA 90210",
    "recipient_name": "Property Management Company",
    "recipient_address": "456 Business Ave, Anytown, CA 90210",
    "deadline": "10 days"
  }
}
```

**Parameters:**
- `issue_id` (integer, required): ID of the legal issue
- `template_id` (integer, required): ID of the document template
- `document_type` (string, required): Type of document to generate
- `custom_data` (object, optional): Additional data for document customization

**Response:**
```json
{
  "id": 1,
  "issue_id": 1,
  "template_id": 1,
  "document_type": "demand_letter",
  "file_name": "demand_letter_1_20240101_120000.pdf",
  "generated_at": "2024-01-01T12:00:00Z",
  "download_url": "/api/documents/1/download"
}
```

#### GET /documents/{document_id}/download

Download a generated document.

**Response:** PDF file download

### Document Templates

#### GET /templates

Get available document templates, optionally filtered by category.

**Query Parameters:**
- `category` (string, optional): Filter by legal category

**Response:**
```json
[
  {
    "id": 1,
    "name": "Tenant Demand for Repairs",
    "category": "tenant_rights",
    "description": "Letter demanding landlord make necessary repairs",
    "required_fields": ["landlord_name", "property_address", "issue_details", "deadline"]
  },
  {
    "id": 2,
    "name": "Consumer Complaint Letter",
    "category": "consumer_protection",
    "description": "Formal complaint to business about defective product or service",
    "required_fields": ["recipient_name", "recipient_address", "complaint_details"]
  }
]
```

#### GET /templates/{template_id}

Get a specific document template by ID.

**Response:**
```json
{
  "id": 1,
  "name": "Tenant Demand for Repairs",
  "category": "tenant_rights",
  "description": "Letter demanding landlord make necessary repairs",
  "required_fields": ["landlord_name", "property_address", "issue_details", "deadline"]
}
```

### Legal Resources

#### POST /resources/search

Search for legal resources based on criteria.

**Request Body:**
```json
{
  "jurisdiction": "US",
  "categories": ["tenant_rights", "consumer_protection"],
  "organization_type": "legal_aid"
}
```

**Parameters:**
- `jurisdiction` (string, optional): Jurisdiction code (default: "US")
- `categories` (array, optional): Legal categories to filter by
- `organization_type` (string, optional): Type of organization

**Response:**
```json
[
  {
    "id": 1,
    "name": "Legal Aid Society",
    "organization_type": "legal_aid",
    "description": "Provides free legal services to low-income individuals",
    "website": "https://www.legalaid.org",
    "phone": "1-800-LEGAL-AID",
    "email": "help@legalaid.org",
    "address": "123 Legal St, Anytown, CA 90210",
    "jurisdiction": "US",
    "categories": ["tenant_rights", "family_law", "immigration"]
  }
]
```

#### GET /resources

Get legal resources with optional filtering.

**Query Parameters:**
- `jurisdiction` (string, optional): Jurisdiction code (default: "US")
- `organization_type` (string, optional): Type of organization
- `skip` (integer, optional): Number of records to skip (default: 0)
- `limit` (integer, optional): Maximum records to return (default: 100)

#### GET /resources/{resource_id}

Get a specific legal resource by ID.

#### GET /organization-types

Get list of available organization types.

**Response:**
```json
{
  "organization_types": [
    "legal_aid",
    "court",
    "pro_bono",
    "government",
    "nonprofit",
    "bar_association",
    "self_help"
  ],
  "descriptions": {
    "legal_aid": "Legal aid organizations providing free or low-cost legal services",
    "court": "Court systems and judicial resources",
    "pro_bono": "Pro bono attorney networks and volunteer legal services"
  }
}
```

#### GET /categories

Get list of supported legal categories.

**Response:**
```json
{
  "categories": [
    "tenant_rights",
    "consumer_protection",
    "employment",
    "family_law",
    "immigration",
    "criminal",
    "civil_rights",
    "debt_collection",
    "housing",
    "healthcare"
  ],
  "descriptions": {
    "tenant_rights": "Landlord-tenant disputes, evictions, housing conditions",
    "consumer_protection": "Fraud, scams, unfair business practices",
    "employment": "Workplace issues, discrimination, wage disputes"
  }
}
```

### Legal Issues

#### GET /issues

Get list of legal issues with optional filtering.

**Query Parameters:**
- `skip` (integer, optional): Number of records to skip (default: 0)
- `limit` (integer, optional): Maximum records to return (default: 100)
- `category` (string, optional): Filter by category

#### GET /issues/{issue_id}

Get a specific legal issue by ID.

#### GET /issues/{issue_id}/advice

Get all advice records for a specific legal issue.

#### GET /issues/{issue_id}/documents

Get all generated documents for a specific legal issue.

## Data Models

### Legal Categories

- `tenant_rights`: Landlord-tenant disputes, evictions, housing conditions
- `consumer_protection`: Fraud, scams, unfair business practices
- `employment`: Workplace issues, discrimination, wage disputes
- `family_law`: Divorce, custody, domestic relations
- `immigration`: Immigration status, deportation, asylum
- `criminal`: Criminal defense, expungement, rights
- `civil_rights`: Discrimination, civil liberties violations
- `debt_collection`: Debt disputes, bankruptcy, creditor harassment
- `housing`: Housing discrimination, accessibility, public housing
- `healthcare`: Medical bills, insurance disputes, patient rights
- `other`: Issues that don't fit the above categories

### Document Types

- `demand_letter`: Formal demand for action or payment
- `complaint_letter`: Complaint to business or organization
- `notice`: Legal notice or notification
- `response`: Response to legal action
- `petition`: Formal request to court or authority

### Urgency Levels

- `low`: General inquiry, no immediate action required
- `medium`: Important matter requiring attention
- `high`: Urgent situation requiring immediate action

## SDK and Client Libraries

### Python Client

```python
import requests

class LegalAidClient:
    def __init__(self, base_url="http://localhost:8000/api"):
        self.base_url = base_url
    
    def analyze_issue(self, description, location=None, urgency="medium"):
        response = requests.post(f"{self.base_url}/analyze", json={
            "description": description,
            "location": location,
            "urgency": urgency
        })
        return response.json()
    
    def get_advice(self, issue_id, additional_context=None):
        response = requests.post(f"{self.base_url}/advice", json={
            "issue_id": issue_id,
            "additional_context": additional_context
        })
        return response.json()

# Usage
client = LegalAidClient()
analysis = client.analyze_issue("My landlord won't fix the heating")
advice = client.get_advice(analysis["issue_id"])
```

### JavaScript Client

```javascript
class LegalAidClient {
    constructor(baseUrl = 'http://localhost:8000/api') {
        this.baseUrl = baseUrl;
    }
    
    async analyzeIssue(description, location = null, urgency = 'medium') {
        const response = await fetch(`${this.baseUrl}/analyze`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ description, location, urgency })
        });
        return response.json();
    }
    
    async getAdvice(issueId, additionalContext = null) {
        const response = await fetch(`${this.baseUrl}/advice`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                issue_id: issueId, 
                additional_context: additionalContext 
            })
        });
        return response.json();
    }
}

// Usage
const client = new LegalAidClient();
const analysis = await client.analyzeIssue("My landlord won't fix the heating");
const advice = await client.getAdvice(analysis.issue_id);
```

## Webhooks (Future Feature)

Future versions will support webhooks for real-time notifications:

- Issue analysis completion
- Document generation completion
- New resource additions
- System health alerts

## Versioning

The API uses semantic versioning. Current version: `v1`

- Breaking changes will increment the major version
- New features will increment the minor version
- Bug fixes will increment the patch version

## Support

For API support and questions:
- GitHub Issues: [Repository Issues](https://github.com/your-org/legal-aid-assistant/issues)
- Email: api-support@legal-aid-assistant.com
- Documentation: [Full Documentation](https://docs.legal-aid-assistant.com)

