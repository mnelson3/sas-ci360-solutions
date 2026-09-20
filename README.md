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

The identity-bridge cycle (`sasci360solutions.identity_data`) calls CI360's Marketing Data API — file transfer location, import request jobs, and tables — through the `sasci360soldata` client, which itself generates JWT auth tokens via `sasci360apicore.encryption`. Two `sasci360apicore` primitives are used directly:

1. **Communication**: sends the status/support emails over SMTP
2. **Reporter**: persists every API response payload as a JSON report for auditability

`sasci360apicore.scheduler.Scheduler` is available for whatever process calls `CI360Main.check_and_run()` on a recurring cadence (see `src/UnixService.py`/`src/SASCI360Service.py`).

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
   - `UnixService.py`: Linux systemd service support
   - `SASCI360Service.py`: Windows service integration

2. **Module Layer**: Business logic and automation components
   - **CI360Main** (`sasci360solutions/main.py`): orchestrates the identity-bridge cycle
   - **sasci360soldata**: CI360 Marketing Data API client (file transfer, import request jobs, tables)
   - **Communication** / **Reporter**: provided by the `sasci360apicore` dependency
   - **Logger**: Structured logging built on Python's `logging` module

3. **Configuration Layer**: Centralized settings management
   - `Standard`: Singleton configuration class (`src/standard.py`)

### Project Structure

```
sas-ci360-solutions/
├── src/
│   ├── standard.py                 # Configuration singleton
│   ├── UnixService.py              # Linux systemd entry point
│   ├── SASCI360Service.py          # Windows service entry point
│   └── sasci360solutions/          # Main package
│       ├── __init__.py
│       ├── main.py                 # CI360Main orchestrator (identity-bridge cycle)
│       ├── content/                # Reserved for future content-delivery integration
│       ├── identity_data/          # Identity-bridge cycle
│       │   ├── CreateIdentityBridgeReports.py
│       │   ├── SendIdentityBridgeStatusMessage.py
│       │   ├── SendIdentityBridgeSupportMessage.py
│       │   └── UploadIdentityBridgeData.py
│       ├── marketing_data/         # Marketing data / table metadata
│       │   └── TablesAction.py
│       ├── planning/                # Reserved for future Plan API integration
│       └── setup/                   # Reserved for future setup utilities
└── tests/                           # Test suite (mocked, no live tenant required)
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

Configuration is managed through `config/config.ini` (copy `config/config.ini.example` to start). See that file for the full set of keys; the sections are:

```ini
[EMAIL]
email_server = smtp.example.com
email_server_login = automation@example.com
email_server_password = changeme
email_msg_status_to = admin@example.com
; ... plus email_msg_support_* and their _dev/_test/_prod variants

[FILES]
export_file = export.csv
; ... plus export_change_file and their _dev/_test/_prod variants

[IDENTITIES]
identity_bridge_table_id = changeme
secret_key = changeme
tenant_id = changeme
; ... plus their _dev/_test/_prod variants

[PATHS]
external_gateway_path = extapigwservice-training.ci360.sas.com
file_transfer_location_path = /marketingData/fileTransferLocation
import_request_jobs_path = /marketingData/importRequestJobs
; ... plus export_path/export_post_path and their _dev/_test/_prod variants

[SETTINGS]
algorithm = HS256
encoding = UTF-8
tenant_name = Example Tenant
; ... plus tenant_environment/tenant_number/tenant_product/tenant_url
```

Keys suffixed `_dev`/`_test`/`_prod` hold that environment's value; construct `Standard(mode="development"|"test"|"production")` to select one at construction time, or omit `mode` to get the bare (default) key's value.

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

JWT-based authentication is handled by `sasci360soldata.base.CI360DataBase`, which generates a token from `sasci360apicore.encryption` at construction time:

```python
from sasci360soldata.base import CI360DataBase, CI360DataConfig
from standard import Standard

standard = Standard(mode="test")
client = CI360DataBase(
    CI360DataConfig(
        algorithm=standard.algorithm,
        encoding=standard.encoding,
        host="https://{0}".format(standard.external_gateway_path),
        secret_key=standard.secret_key,
        tenant_id=standard.tenant_id,
    )
)

jobs = client.get_import_request_jobs(data_descriptor_id=standard.identity_bridge_table_id)
```

`sasci360apicore.communication.Communication` is a separate, unrelated client for sending status/support emails over SMTP — it has no CI360 authentication role.

### Testing Strategy

#### Test Structure

Tests are organized to mirror source structure:

```
tests/
├── TestCreateIdentityBridgeReports.py
├── TestMain.py
├── TestSendIdentityBridgeStatusMessage.py
├── TestSendIdentityBridgeSupportMessage.py
├── TestTablesAction.py
└── TestUploadIdentityBridgeData.py
```

#### Running Tests

```bash
# Run all tests
python -m pytest

# Run specific test
python -m pytest tests/TestCreateIdentityBridgeReports.py

# Run with coverage
python -m pytest --cov=src --cov-report=html

# Run with verbose output
python -m pytest -v
```

The full suite is mocked and runs without a live CI360 tenant or SMTP server: every module accepts its collaborators (`standard`, `client`, `reporter`, `communication`) as constructor keyword arguments, so tests pass in fakes instead of patching module internals.

#### Writing Tests

Follow this pattern for new tests — inject fakes via constructor kwargs rather than patching:

```python
from types import SimpleNamespace
from unittest.mock import MagicMock

from sasci360solutions.identity_data.SendIdentityBridgeStatusMessage import (
    SendIdentityBridgeStatusMessage,
)


def test_send_status_message_success():
    standard = SimpleNamespace(
        email_server="smtp.example.com",
        email_server_login="automation@example.com",
        email_server_password="changeme",
        email_server_port="465",
        email_msg_status_from="noreply@example.com",
        email_msg_status_to="admin@example.com",
        email_msg_support_cc="support@example.com",
        reports_path="/reports/",
    )
    communication = MagicMock()

    instance = SendIdentityBridgeStatusMessage(standard=standard, communication=communication)
    result = instance.run(time_stamp="20260101000000", success=True)

    assert result is True
    communication.send_email.assert_called_once()
```

See `tests/TestCreateIdentityBridgeReports.py` and `tests/TestMain.py` for examples mocking the `sasci360soldata` client and chaining multiple mocked collaborators together.

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
# Test connectivity to your CI360 gateway
curl -I https://extapigwservice-<env>.ci360.sas.com/marketingData/tables

# Validate credentials generate a token
python -c "
from standard import Standard
from sasci360apicore.encryption import Encryption
s = Standard(mode='test')
e = Encryption(algorithm=s.algorithm, encoding=s.encoding)
print(e.generate_jwt(secret_key=s.secret_key, tenant_id=s.tenant_id))
"
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
