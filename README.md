# SAS Customer Intelligence 360 Solutions

## SAS 360 SOLUTIONS - Automation Engine

> **Status: canonical.** This is the actively maintained identity-bridge and reporting orchestration layer, built on the `sol-*` client libraries.

This repository contains the core automation engine for SAS Customer Intelligence 360, providing a service-based framework for running CI360 operations programmatically.

### Overview

The SAS CI360 Solutions project implements a Windows/Linux service that automates various CI360 processes, including data processing, campaign execution, and workflow management. It serves as the central orchestration layer for CI360 operations.

### Features

- Windows Service integration for automated execution
- Linux systemd service support
- Integration with SAS CI360 APIs
- Logging and error handling
- Scheduled task execution

### Prerequisites

- Python 3.8+
- Access to SAS Customer Intelligence 360 environment
- Required dependencies (see requirements.txt)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/mnelson3/sas-ci360-solutions.git
   cd sas-ci360-solutions
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure the service:
   - Update `config/config.ini` with your CI360 environment settings
   - For Windows: Install as a service using `python SASCI360Service.py install`
   - For Linux: Copy `src/sas_ci360_solutions.service` to `/etc/systemd/system/` and enable

### Getting Started

1. Configure your CI360 connection in `config/config.ini`
2. Start the service:
   - Windows: `python SASCI360Service.py start`
   - Linux: `sudo systemctl start sas_ci360_solutions`

### Solutions Code

This engine builds on `sasci360apicore` (an internal SAS CI360 API client library, not published on PyPI) for:

1. **Communication**: Handles API communications with CI360
2. **Connection**: Manages secure connections to CI360 endpoints
3. **Reporter**: Generates reports on automation activities

and provides its own logging and JWT-based authentication on top of it.

### Troubleshooting

- Check service logs in `logs/service.log`
- Verify CI360 API connectivity
- Ensure all dependencies are installed
- Review configuration settings

## 🛠️ Developer/Implementation Guide

This section provides comprehensive guidance for developers working with the SAS CI360 Solutions automation engine.

### Architecture Overview

The SAS CI360 Solutions project follows a modular, service-oriented architecture designed for enterprise-grade automation:

```
┌─────────────────────────────────────────────────────────────┐
│                    SAS CI360 Solutions                      │
│                    Automation Engine                        │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐           │
│  │  Services   │ │  Modules    │ │  Config     │           │
│  │  Layer      │ │  Layer      │ │  Layer      │           │
│  └─────────────┘ └─────────────┘ └─────────────┘           │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐           │
│  │ Windows     │ │ Linux       │ │ SAS CI360   │           │
│  │ Service     │ │ systemd     │ │ APIs        │           │
│  └─────────────┘ └─────────────┘ └─────────────┘           │
└─────────────────────────────────────────────────────────────┘
```

#### Core Components

1. **Service Layer**: Platform-specific service implementations
   - `WindowsService.py`: Windows service integration
   - `UnixService.py`: Linux systemd service support
   - `SASCI360Service.py`: Cross-platform service manager

2. **Module Layer**: Business logic and automation components
   - **Communication** / **Connection** / **Reporter**: provided by the `sasci360apicore` dependency
   - **Logger**: Structured logging built on Python's `logging` module

3. **Configuration Layer**: Centralized settings management
   - `Standard`: Singleton configuration class (`src/standard.py`)

### Project Structure

```
sas-ci360-solutions/
├── src/
│   ├── standard.py                 # Configuration singleton
│   ├── WindowsService.py           # Windows service entry point
│   ├── UnixService.py              # Linux systemd entry point
│   ├── SASCI360Service.py          # Cross-platform service manager
│   └── sasci360solutions/          # Main package
│       ├── __init__.py
│       ├── main.py                 # Application entry point
│       ├── content/                # Content management
│       ├── content_delivery/       # Email/content delivery
│       │   └── BuildEmailData.py
│       ├── identity_data/          # Identity management
│       │   ├── CreateIdentityBridgeReports.py
│       │   ├── SendIdentityBridgeStatusMessage.py
│       │   ├── SendIdentityBridgeSupportMessage.py
│       │   └── UploadIdentityBridgeData.py
│       ├── marketing_data/         # Marketing data processing
│       │   ├── CleanData.py
│       │   ├── CreateData.py
│       │   └── TablesAction.py
│       ├── planning/                # Planning integrations
│       └── setup/                   # Setup utilities
└── tests/                           # Test suite
```

`config/`, `data/`, and `logs/` are created locally at runtime and are not tracked in the repo (see `.gitignore`).

### Development Environment Setup

#### Prerequisites

- **Python 3.8+** with pip and virtualenv
- **Git** for version control
- **Access to SAS CI360 environment** for testing
- **Code editor** (VS Code recommended with Python extensions)

#### Local Development Setup

1. **Clone and Setup Virtual Environment**:
   ```bash
   git clone https://github.com/mnelson3/sas-ci360-solutions.git
   cd sas-ci360-solutions
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   pip install -e .  # Install in development mode
   ```

3. **Install Development Tools**:
   ```bash
   pip install pre-commit black isort flake8 mypy bandit
   pre-commit install  # Install git hooks
   ```

4. **Configure Environment**:
   ```bash
   cp config/config.ini.example config/config.ini
   # Edit config/config.ini with your CI360 credentials
   ```

#### Code Quality Tools

The project uses automated code quality enforcement:

- **Black**: Code formatting (127 char line length)
- **isort**: Import sorting (black profile)
- **flake8**: Linting (max complexity: 10)
- **mypy**: Type checking (with missing import tolerance)
- **bandit**: Security vulnerability scanning
- **pre-commit**: Automated quality gates

Run quality checks:
```bash
pre-commit run --all-files  # Run all checks
black .                     # Format code
isort .                     # Sort imports
flake8 .                    # Lint code
mypy .                      # Type check
bandit -r .                 # Security scan
```

### Configuration Management

#### Standard Configuration Class

The `Standard` class provides centralized configuration:

```python
from standard import Standard

# Get singleton instance
config = Standard.get_instance()

# Access configuration
log_path = config.gDirLog
data_path = config.gDsDscCsv
delimiter = config.delimiter()
```

#### Environment Configuration

Configuration is managed through `config/config.ini`:

```ini
[CI360]
base_url = https://your-ci360-instance.com
client_id = your-client-id
client_secret = your-client-secret
tenant_id = your-tenant-id

[EMAIL]
smtp_server = smtp.company.com
smtp_port = 587
from_address = automation@company.com

[LOGGING]
level = INFO
file = logs/service.log
```

### Module Development

#### Creating New Modules

1. **Choose appropriate package** (identity_data, marketing_data, etc.)
2. **Follow naming conventions**:
   - Classes: PascalCase
   - Methods: snake_case
   - Constants: UPPER_CASE

3. **Implement standard interface**:
   ```python
   class NewModule:
       def __init__(self):
           self.logger = logging.getLogger(__name__)
           self._standard = Standard.get_instance()

       def run(self):
           """Main execution method."""
           try:
               # Implementation here
               pass
           except Exception as e:
               self.logger.exception(f"Module execution failed: {e}")
               raise
   ```

#### Error Handling

All modules should implement comprehensive error handling:

```python
import logging
from typing import Optional

class ExampleModule:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def process_data(self, data: dict) -> Optional[dict]:
        """Process data with proper error handling."""
        try:
            # Validate input
            if not data:
                raise ValueError("Input data cannot be empty")

            # Process data
            result = self._transform_data(data)

            self.logger.info(f"Successfully processed {len(result)} records")
            return result

        except ValueError as e:
            self.logger.error(f"Validation error: {e}")
            raise
        except Exception as e:
            self.logger.exception(f"Unexpected error in process_data: {e}")
            raise
```

### API Integration

#### CI360 API Client

The project integrates with multiple SAS CI360 APIs:

- **Marketing Data API**: Table operations, data imports
- **Identity API**: Identity bridge management
- **Content API**: Email and content delivery
- **Planning API**: Budget and planning data

#### Authentication

JWT-based authentication is handled through the `communication` module:

```python
from sasci360apicore import communication

# Initialize client
client = communication.Communication(
    base_url=config.ci360_base_url,
    client_id=config.client_id,
    client_secret=config.client_secret
)

# Authenticate
token = client.authenticate()
```

### Testing Strategy

#### Test Structure

Tests are organized to mirror source structure:

```
tests/
├── TestBuildEmailData.py
├── TestCreateIdentityBridgeReports.py
├── TestDownloadDiscover.py
├── TestSendIdentityBridgeStatusMessage.py
├── TestSendIdentityBridgeSupportMessage.py
└── TestUploadIdentityBridgeData.py
```

#### Running Tests

```bash
# Run all tests
python -m pytest

# Run specific test
python -m pytest tests/TestBuildEmailData.py

# Run with coverage
python -m pytest --cov=src --cov-report=html

# Run with verbose output
python -m pytest -v
```

#### Writing Tests

Follow these patterns for new tests:

```python
import unittest
from unittest.mock import Mock, patch
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from sasci360solutions.content_delivery.BuildEmailData import BuildEmailData


class TestBuildEmailData(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        self.instance = BuildEmailData.get_instance()

    def test_build_email_list_success(self):
        """Test successful email list building."""
        # Arrange
        expected_result = {"status": "success"}

        # Act
        with patch('pandas.read_csv') as mock_csv:
            mock_csv.return_value = Mock()
            result = self.instance.build_email_list()

        # Assert
        self.assertIsNotNone(result)

    def tearDown(self):
        """Clean up test fixtures."""
        pass


if __name__ == '__main__':
    unittest.main()
```

### Deployment and Operations

#### Service Installation

**Windows Service**:
```batch
python SASCI360Service.py install
python SASCI360Service.py start
```

**Linux Service**:
```bash
sudo cp src/sas_ci360_solutions.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable sas_ci360_solutions
sudo systemctl start sas_ci360_solutions
```

#### Monitoring and Logging

Logs are written to `logs/service.log` with the following levels:
- **DEBUG**: Detailed diagnostic information
- **INFO**: General operational messages
- **WARNING**: Warning conditions
- **ERROR**: Error conditions
- **CRITICAL**: Critical errors requiring immediate attention

#### Health Checks

Monitor service health through:
- Log file analysis
- Service status checks
- API endpoint monitoring
- Database connection validation

### Contributing Workflow

#### Development Process

1. **Create Feature Branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Implement Changes**:
   - Follow code quality standards
   - Add comprehensive tests
   - Update documentation

3. **Quality Assurance**:
   ```bash
   pre-commit run --all-files  # Quality checks
   python -m pytest           # Run tests
   ```

4. **Submit Pull Request**:
   - Provide detailed description
   - Reference related issues
   - Request review from maintainers

#### Code Review Guidelines

- **Functionality**: Does the code work as intended?
- **Quality**: Passes all automated checks?
- **Documentation**: Is code well-documented?
- **Testing**: Adequate test coverage?
- **Performance**: Efficient implementation?
- **Security**: No security vulnerabilities?

### Troubleshooting for Developers

#### Common Issues

**Import Errors**:
```bash
# Ensure virtual environment is activated
source .venv/bin/activate

# Install missing dependencies
pip install -r requirements.txt

# Check Python path
python -c "import sys; print(sys.path)"
```

**Configuration Issues**:
```bash
# Validate config file
python -c "import configparser; c = configparser.ConfigParser(); c.read('config/config.ini'); print('Config loaded successfully')"

# Check file permissions
ls -la config/config.ini
```

**Service Startup Issues**:
```bash
# Check service logs
tail -f logs/service.log

# Validate service configuration
python SASCI360Service.py --help

# Test manual execution
python src/sasci360solutions/main.py
```

**API Connection Issues**:
```bash
# Test connectivity
curl -I https://your-ci360-instance.com/api/v1/status

# Validate credentials
python -c "from sasci360apicore import communication; c = communication.Communication(...); print(c.authenticate())"
```

#### Performance Optimization

- **Database Queries**: Use appropriate indexing
- **Memory Usage**: Implement streaming for large datasets
- **API Calls**: Implement retry logic and rate limiting
- **Logging**: Use appropriate log levels to avoid overhead

### Security Considerations

#### Code Security

- **Input Validation**: Validate all user inputs
- **Secure Credentials**: Never hardcode secrets
- **HTTPS Only**: All API communications use HTTPS
- **Token Management**: Implement proper token refresh

#### Operational Security

- **Access Control**: Implement role-based access
- **Audit Logging**: Log all sensitive operations
- **Data Encryption**: Encrypt sensitive data at rest
- **Regular Updates**: Keep dependencies updated

## Contributing

We welcome code contributions! Please read [CONTRIBUTING](CONTRIBUTING.md) for details on how to submit contributions to this project.

## License

### Nelson Grey LLC Community License 1.0

This project is licensed under the [Nelson Grey LLC Community License 1.0](LICENSE).

#### What does this mean?

- **✅ Free for individuals, education, and research**: You can use, modify, and distribute this software for non-commercial purposes
- **✅ Commercial evaluation**: You can evaluate the software for commercial use for free
- **❌ Commercial production use**: If you use this software in production for commercial purposes, you need a commercial license
- **🔄 Automatic conversion**: On December 13, 2029 (4 years from release), this automatically converts to Apache License 2.0

#### Why this license?

This license choice balances:
- **Open source accessibility** for individual developers and researchers
- **Protection for commercial investment** in the project
- **Sustainable development** through commercial licensing for production use
- **Future openness** with automatic conversion to permissive licensing

For commercial licensing inquiries, please contact support@nelsongrey.com.

### Additional Resources

For more information, see [REST APIs](https://go.documentation.sas.com/doc/en/cintcdc/production.a/cintapis/ch-rest-apis.htm).
