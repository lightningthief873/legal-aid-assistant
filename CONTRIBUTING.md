# Contributing to AI-Backed Community Legal Aid Assistant

Thank you for your interest in contributing to the AI-Backed Community Legal Aid Assistant! This project aims to provide accessible legal guidance to underserved communities, and we welcome contributions from developers, legal professionals, and community advocates.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Contributing Guidelines](#contributing-guidelines)
- [Pull Request Process](#pull-request-process)
- [Issue Guidelines](#issue-guidelines)
- [Development Standards](#development-standards)
- [Testing](#testing)
- [Documentation](#documentation)
- [Community](#community)

## Code of Conduct

This project adheres to a Code of Conduct that we expect all contributors to follow. Please read [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) before contributing.

### Our Pledge

We are committed to making participation in this project a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, gender identity and expression, level of experience, nationality, personal appearance, race, religion, or sexual identity and orientation.

## Getting Started

### Ways to Contribute

- **Code Contributions**: Bug fixes, new features, performance improvements
- **Documentation**: Improve guides, add examples, fix typos
- **Legal Content**: Review legal templates, add jurisdiction-specific content
- **Testing**: Write tests, report bugs, test new features
- **Design**: UI/UX improvements, accessibility enhancements
- **Translation**: Localize the application for different languages
- **Community**: Help other users, answer questions, provide feedback

### Before You Start

1. **Check existing issues**: Look for existing issues or discussions about your idea
2. **Create an issue**: For new features or significant changes, create an issue first
3. **Get feedback**: Discuss your approach with maintainers before starting work
4. **Start small**: Begin with small contributions to familiarize yourself with the codebase

## Development Setup

### Prerequisites

- Python 3.11+
- Node.js 18+
- Docker and Docker Compose
- Git

### Local Development

1. **Fork and Clone**
   ```bash
   git clone https://github.com/your-username/legal-aid-assistant.git
   cd legal-aid-assistant
   ```

2. **Set Up Backend**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Development dependencies
   ```

3. **Set Up Frontend**
   ```bash
   cd frontend/legal-aid-frontend
   npm install
   ```

4. **Environment Configuration**
   ```bash
   cp backend/.env.example .env
   # Edit .env with your configuration
   ```

5. **Initialize Database**
   ```bash
   cd backend
   python init_db.py
   ```

6. **Start Development Servers**
   ```bash
   # Backend (in one terminal)
   cd backend
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   
   # Frontend (in another terminal)
   cd frontend/legal-aid-frontend
   npm run dev
   ```

### Docker Development

```bash
# Start all services
./deploy.sh dev

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## Contributing Guidelines

### Types of Contributions

#### Bug Fixes
- Fix existing functionality that isn't working as expected
- Include tests that verify the fix
- Update documentation if necessary

#### New Features
- Add new functionality that enhances the application
- Discuss the feature in an issue before implementation
- Include comprehensive tests and documentation

#### Documentation
- Improve existing documentation
- Add new guides or examples
- Fix typos or unclear explanations

#### Legal Content
- Review and improve legal templates
- Add jurisdiction-specific content
- Ensure legal accuracy and clarity

### Contribution Process

1. **Create an Issue** (for significant changes)
2. **Fork the Repository**
3. **Create a Feature Branch**
4. **Make Your Changes**
5. **Write Tests**
6. **Update Documentation**
7. **Submit a Pull Request**

## Pull Request Process

### Before Submitting

1. **Test Your Changes**
   ```bash
   # Run backend tests
   cd backend
   pytest
   
   # Run frontend tests
   cd frontend/legal-aid-frontend
   npm test
   
   # Run integration tests
   ./scripts/test-integration.sh
   ```

2. **Check Code Quality**
   ```bash
   # Python code formatting
   cd backend
   black .
   isort .
   flake8 .
   
   # JavaScript code formatting
   cd frontend/legal-aid-frontend
   npm run lint
   npm run format
   ```

3. **Update Documentation**
   - Update README if necessary
   - Add or update API documentation
   - Include inline code comments

### Pull Request Template

When submitting a pull request, please include:

```markdown
## Description
Brief description of the changes made.

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Testing
- [ ] Tests pass locally
- [ ] New tests added for new functionality
- [ ] Manual testing completed

## Checklist
- [ ] Code follows the project's style guidelines
- [ ] Self-review of code completed
- [ ] Code is commented, particularly in hard-to-understand areas
- [ ] Documentation updated
- [ ] No new warnings introduced

## Screenshots (if applicable)
Include screenshots for UI changes.

## Related Issues
Closes #(issue number)
```

### Review Process

1. **Automated Checks**: CI/CD pipeline runs tests and quality checks
2. **Code Review**: Maintainers review code for quality and correctness
3. **Legal Review**: Legal content changes reviewed by legal professionals
4. **Testing**: Changes tested in staging environment
5. **Approval**: At least one maintainer approval required
6. **Merge**: Changes merged into main branch

## Issue Guidelines

### Reporting Bugs

Use the bug report template and include:

- **Description**: Clear description of the bug
- **Steps to Reproduce**: Detailed steps to reproduce the issue
- **Expected Behavior**: What you expected to happen
- **Actual Behavior**: What actually happened
- **Environment**: OS, browser, version information
- **Screenshots**: If applicable
- **Additional Context**: Any other relevant information

### Feature Requests

Use the feature request template and include:

- **Problem Statement**: What problem does this solve?
- **Proposed Solution**: Detailed description of the feature
- **Alternatives**: Alternative solutions considered
- **Use Cases**: How would this feature be used?
- **Implementation Notes**: Technical considerations

### Legal Content Issues

For legal content issues, include:

- **Jurisdiction**: Which legal system/jurisdiction
- **Content Type**: Template, advice, resource information
- **Issue Description**: What needs to be corrected or improved
- **Legal Authority**: Relevant laws, regulations, or cases
- **Suggested Changes**: Specific improvements

## Development Standards

### Code Style

#### Python (Backend)
- Follow PEP 8 style guide
- Use Black for code formatting
- Use isort for import sorting
- Use type hints for function parameters and return values
- Maximum line length: 88 characters

```python
# Good example
def analyze_legal_issue(
    description: str, 
    location: Optional[str] = None
) -> Dict[str, Any]:
    """Analyze a legal issue and return categorization."""
    # Implementation here
    pass
```

#### JavaScript/React (Frontend)
- Use ESLint and Prettier for code formatting
- Use TypeScript for type safety (when applicable)
- Follow React best practices
- Use functional components with hooks

```javascript
// Good example
const LegalIssueForm = ({ onSubmit }) => {
  const [description, setDescription] = useState('');
  
  const handleSubmit = useCallback((e) => {
    e.preventDefault();
    onSubmit({ description });
  }, [description, onSubmit]);
  
  return (
    <form onSubmit={handleSubmit}>
      {/* Form content */}
    </form>
  );
};
```

### Commit Messages

Use conventional commit format:

```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

Examples:
```
feat(backend): add document generation endpoint
fix(frontend): resolve form validation issue
docs(api): update endpoint documentation
```

### Branch Naming

Use descriptive branch names:

- `feature/add-document-templates`
- `fix/form-validation-bug`
- `docs/update-deployment-guide`
- `refactor/improve-llm-service`

## Testing

### Test Requirements

All contributions must include appropriate tests:

#### Backend Tests
- Unit tests for business logic
- Integration tests for API endpoints
- Database tests for data models

```python
# Example test
def test_analyze_legal_issue():
    """Test legal issue analysis."""
    analyzer = LegalAnalyzer()
    result = analyzer.analyze_issue("Landlord won't fix heating")
    
    assert result["category"] == "tenant_rights"
    assert result["confidence"] > 0.8
    assert len(result["suggested_actions"]) > 0
```

#### Frontend Tests
- Component tests with React Testing Library
- Integration tests for user workflows
- Accessibility tests

```javascript
// Example test
test('submits legal issue form', async () => {
  const mockSubmit = jest.fn();
  render(<LegalIssueForm onSubmit={mockSubmit} />);
  
  await user.type(screen.getByLabelText(/description/i), 'Test issue');
  await user.click(screen.getByRole('button', { name: /submit/i }));
  
  expect(mockSubmit).toHaveBeenCalledWith({
    description: 'Test issue'
  });
});
```

### Running Tests

```bash
# Backend tests
cd backend
pytest -v

# Frontend tests
cd frontend/legal-aid-frontend
npm test

# Integration tests
./scripts/test-integration.sh

# Coverage reports
pytest --cov=app
npm test -- --coverage
```

## Documentation

### Documentation Standards

- Use clear, concise language
- Include code examples
- Keep documentation up-to-date with code changes
- Use proper markdown formatting

### Types of Documentation

1. **Code Documentation**
   - Docstrings for Python functions/classes
   - JSDoc comments for JavaScript functions
   - Inline comments for complex logic

2. **API Documentation**
   - OpenAPI/Swagger specifications
   - Request/response examples
   - Error handling documentation

3. **User Documentation**
   - Installation guides
   - Usage tutorials
   - Troubleshooting guides

4. **Developer Documentation**
   - Architecture overview
   - Contributing guidelines
   - Deployment instructions

## Community

### Communication Channels

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: General questions and community discussions
- **Discord**: Real-time chat and support
- **Email**: legal-aid-assistant@example.com for sensitive issues

### Getting Help

- Check existing documentation first
- Search GitHub issues for similar problems
- Ask questions in GitHub Discussions
- Join our Discord community for real-time help

### Mentorship

New contributors can request mentorship:

- Comment on issues tagged `good-first-issue`
- Reach out to maintainers for guidance
- Participate in community calls and discussions

### Recognition

We recognize contributors through:

- Contributor list in README
- Special recognition for significant contributions
- Invitation to join the maintainer team for consistent contributors

## Legal Considerations

### Legal Content Accuracy

When contributing legal content:

- Ensure accuracy of legal information
- Cite relevant laws and regulations
- Include appropriate disclaimers
- Consider jurisdiction-specific variations

### Intellectual Property

- Ensure you have rights to contribute code/content
- All contributions are licensed under the project's MIT license
- Do not include copyrighted material without permission

### Privacy and Security

- Do not include personal information in code or documentation
- Follow security best practices
- Report security vulnerabilities privately

## Release Process

### Versioning

We use semantic versioning (SemVer):
- MAJOR: Breaking changes
- MINOR: New features (backward compatible)
- PATCH: Bug fixes (backward compatible)

### Release Schedule

- Patch releases: As needed for critical bugs
- Minor releases: Monthly for new features
- Major releases: Quarterly or as needed for breaking changes

### Changelog

All changes are documented in CHANGELOG.md following Keep a Changelog format.

## Questions?

If you have questions about contributing, please:

1. Check this guide and other documentation
2. Search existing GitHub issues and discussions
3. Create a new GitHub discussion
4. Contact maintainers directly for sensitive matters

Thank you for contributing to making legal assistance more accessible to everyone!

