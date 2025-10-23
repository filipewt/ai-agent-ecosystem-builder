# AI Agent Ecosystem Builder

A self-initializing multi-agent ecosystem that autonomously manages the full development lifecycle of Python applications. This system provides real-time feedback through a minimal chat UI, ensures cost control by using only `gpt-4o-mini`, and handles everything from environment setup to deployment.

## 🚀 Features

### Core Capabilities
- **Autonomous Development**: Fully automated Python application development lifecycle
- **Multi-Agent Architecture**: Specialized agents for each development phase
- **Real-time Feedback**: Minimal chat UI with auto-scroll for live updates
- **Cost Control**: Uses only `gpt-4o-mini` model with pause/resume workflow
- **Comprehensive Logging**: Built-in logging system for all generated applications

### Development Lifecycle Management
- **Environment Setup**: Virtual environment creation, dependency management, API key handling
- **Code Development**: Architecture design, core logic implementation, standards enforcement
- **Quality Assurance**: Testing, documentation, ethics checks, security validation
- **Deployment Options**: GitHub repository, executable files, or source code only

### Deployment Options
1. **GitHub Repository**: Complete Git setup with CI/CD workflows
2. **Executable File**: Standalone executable with PyInstaller
3. **Source Code Only**: Development-ready source code package

## 🏗️ Architecture

### Agent System
- **Environment Agent**: Virtual environment and dependency management
- **Coordinator Agent**: Human interaction and scope definition
- **Architect Agent**: Application architecture and module design
- **Core Logic Agent**: Python code implementation
- **Standards Agent**: Code quality enforcement (Black, Flake8, Mypy)
- **Testing Agent**: Test execution and validation
- **Documentation Agent**: README, changelogs, and docstring generation
- **Ethics Agent**: Safety and ethical compliance checks
- **Validator Agent**: Final review and approval
- **Repository Agent**: Git repository creation and management
- **Deployment Agent**: Multi-option deployment handling

### Workflow
1. **Environment Setup**: Create venv, install dependencies, configure API keys
2. **Architecture Design**: Define application structure and modules
3. **Code Generation**: Implement core logic and functionality
4. **Quality Assurance**: Run tests, enforce standards, validate security
5. **Documentation**: Generate comprehensive documentation
6. **Deployment**: Package and deploy using chosen method

## 📦 Installation

### Prerequisites
- Python 3.8+
- OpenAI API key

### Setup
1. Clone the repository:
```bash
git clone https://github.com/yourusername/ai-agent-ecosystem-builder.git
cd ai-agent-ecosystem-builder
```

2. Create and activate virtual environment:
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment:
```bash
cp env_example.txt .env
# Edit .env and add your OPENAI_API_KEY
```

## 🚀 Usage

### Basic Usage
```bash
python main.py
```

### Environment Variables
Create a `.env` file with:
```
OPENAI_API_KEY=your_openai_api_key_here
```

### Deployment Options
When prompted, choose your deployment method:
- **GitHub**: Creates a complete Git repository with CI/CD
- **Executable**: Builds a standalone executable file
- **Source Code**: Generates development-ready source code

## 🔧 Configuration

### Model Configuration
The system is configured to use only `gpt-4o-mini` for cost control. No fallback models are used.

### Logging
All generated applications include comprehensive logging:
- File logging with timestamped log files
- Console output for real-time monitoring
- Log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
- Log files stored in `logs/` directory

### PowerShell Compatibility
The system provides instructions for both PowerShell and Command Prompt:
- **PowerShell**: `cd deployment_dir; python install.py`
- **Command Prompt**: `cd deployment_dir && python install.py`

## 📁 Project Structure

```
ai-agent-ecosystem-builder/
├── agents/                 # Agent implementations
│   ├── base_agent.py      # Base agent class
│   ├── environment_agent.py
│   ├── coordinator_agent.py
│   ├── architect_agent.py
│   ├── core_logic_agent.py
│   ├── standards_agent.py
│   ├── testing_agent.py
│   ├── documentation_agent.py
│   ├── ethics_agent.py
│   ├── validator_agent.py
│   ├── repository_agent.py
│   └── deployment_agent.py
├── main.py                # Main entry point
├── requirements.txt       # Python dependencies
├── env_example.txt        # Environment variables template
├── DEPLOYMENT_OPTIONS.md  # Deployment documentation
└── README.md             # This file
```

## 🛠️ Development

### Adding New Agents
1. Create a new agent class inheriting from `BaseAgent`
2. Implement the `execute` method
3. Add the agent to the orchestrator in `main.py`

### Customizing Workflows
Modify the workflow in `main.py` to add new steps or change the order of operations.

## 📋 Requirements

### Python Dependencies
- `openai>=1.0.0` - OpenAI API client
- `python-dotenv>=1.0.0` - Environment variable management
- `rich>=13.0.0` - Rich text and beautiful formatting
- `pyinstaller>=5.0.0` - Executable creation
- `pytest>=7.0.0` - Testing framework
- `black>=22.0.0` - Code formatting
- `flake8>=5.0.0` - Linting
- `mypy>=1.0.0` - Type checking

### System Requirements
- Python 3.8 or higher
- Windows, Linux, or macOS
- Internet connection for OpenAI API

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:
1. Check the documentation in `DEPLOYMENT_OPTIONS.md`
2. Review the agent implementations in the `agents/` directory
3. Open an issue on GitHub

## 🎯 Roadmap

- [ ] Additional deployment targets (Docker, AWS, etc.)
- [ ] Custom agent plugins
- [ ] Advanced logging and monitoring
- [ ] Integration with other AI models
- [ ] Web-based UI for remote development

---

**Built with ❤️ by the AI Agent Ecosystem Builder**