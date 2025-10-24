"""
Deployment Agent - Handles different deployment options
"""

import os
import sys
import shutil
import subprocess
import json
from datetime import datetime
from typing import Dict, Any, List, Optional
from .base_agent import BaseAgent

class DeploymentAgent(BaseAgent):
    """Agent responsible for deploying applications in different formats"""
    
    def __init__(self, agent_id: str = "deploy_001"):
        super().__init__(
            agent_id=agent_id,
            name="Deployment Agent",
            description="Handles different deployment options including GitHub, executable, and source code"
        )
        self.deployment_options = ["github", "executable", "source_only"]
        self.deployment_path = None
        
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute deployment based on user choice"""
        try:
            self.log_action("Starting deployment process")
            
            # Get deployment choice from context or ask user
            deployment_choice = context.get("deployment_choice", "source_only")
            
            if deployment_choice == "github":
                result = self._deploy_to_github(context)
            elif deployment_choice == "executable":
                result = self._deploy_as_executable(context)
            elif deployment_choice == "source_only":
                result = self._deploy_source_only(context)
            else:
                return self.create_response(False, "Invalid deployment option")
            
            if result["success"]:
                self.log_action("Deployment completed successfully")
                return self.create_response(True, "SUCCESS: Deployment completed", result)
            else:
                return self.create_response(False, f"Deployment failed: {result['message']}")
                
        except Exception as e:
            self.logger.error(f"Deployment failed: {str(e)}")
            return self.create_response(False, f"Deployment failed: {str(e)}")
    
    def _deploy_to_github(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Deploy application to GitHub repository"""
        try:
            self.logger.info("Deploying to GitHub...")
            
            # Create deployment directory
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            deployment_dir = f"github_deploy_{timestamp}"
            os.makedirs(deployment_dir, exist_ok=True)
            
            # Copy application files
            self._copy_application_files(context, deployment_dir)
            
            # Create GitHub-specific files
            self._create_github_files(deployment_dir, context)
            
            # Initialize git repository
            self._initialize_git_repo(deployment_dir)
            
            return {
                "success": True,
                "deployment_path": os.path.abspath(deployment_dir),
                "deployment_type": "github",
                "instructions": f"cd {deployment_dir} && git remote add origin <your-repo-url> && git push -u origin main"
            }
            
        except Exception as e:
            return {"success": False, "message": f"GitHub deployment failed: {str(e)}"}
    
    def _deploy_as_executable(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Deploy application as executable file"""
        try:
            self.logger.info("Creating executable deployment...")
            
            # Create deployment directory
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            deployment_dir = f"executable_deploy_{timestamp}"
            os.makedirs(deployment_dir, exist_ok=True)
            
            # Copy application files
            self._copy_application_files(context, deployment_dir)
            
            # Create executable files
            self._create_executable_files(deployment_dir, context)
            
            # Create installer script
            self._create_installer_script(deployment_dir)
            
            # Actually build the executable
            build_result = self._build_executable(deployment_dir)
            
            if build_result["success"]:
                return {
                    "success": True,
                    "deployment_path": os.path.abspath(deployment_dir),
                    "deployment_type": "executable",
                    "executable_path": build_result.get("executable_path"),
                    "instructions": f"cd {deployment_dir} && python install.py"
                }
            else:
                return {
                    "success": False,
                    "message": f"Executable build failed: {build_result['message']}"
                }
            
        except Exception as e:
            return {"success": False, "message": f"Executable deployment failed: {str(e)}"}
    
    def _deploy_source_only(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Deploy application as source code only"""
        try:
            self.logger.info("Creating source code deployment...")
            
            # Create deployment directory
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            deployment_dir = f"source_deploy_{timestamp}"
            os.makedirs(deployment_dir, exist_ok=True)
            
            # Copy application files
            self._copy_application_files(context, deployment_dir)
            
            # Create source-specific files
            self._create_source_files(deployment_dir, context)
            
            return {
                "success": True,
                "deployment_path": os.path.abspath(deployment_dir),
                "deployment_type": "source_only",
                "instructions": f"cd {deployment_dir} && pip install -r requirements.txt && python src/main.py"
            }
            
        except Exception as e:
            return {"success": False, "message": f"Source deployment failed: {str(e)}"}
    
    def _copy_application_files(self, context: Dict[str, Any], deployment_dir: str):
        """Copy application files to deployment directory"""
        generated_files = context.get("generated_files", [])
        
        for file_path in generated_files:
            if os.path.exists(file_path):
                # Get relative path from current directory
                try:
                    rel_path = os.path.relpath(file_path)
                    dest_path = os.path.join(deployment_dir, rel_path)
                    dest_dir = os.path.dirname(dest_path)
                    
                    if dest_dir:
                        os.makedirs(dest_dir, exist_ok=True)
                    
                    shutil.copy2(file_path, dest_path)
                    self.logger.info(f"Copied {file_path} to {dest_path}")
                except Exception as e:
                    self.logger.warning(f"Failed to copy {file_path}: {e}")
            else:
                self.logger.warning(f"File not found: {file_path}")
        
        # Create logs directory in deployment
        logs_dir = os.path.join(deployment_dir, "logs")
        os.makedirs(logs_dir, exist_ok=True)
        
        # Create a sample log file with instructions
        sample_log_content = """# Application Logs

This directory contains log files generated by your application.

## Log Files
- application_YYYYMMDD_HHMMSS.log - Main application logs
- error_YYYYMMDD_HHMMSS.log - Error logs (if any)
- debug_YYYYMMDD_HHMMSS.log - Debug logs (if enabled)

## Log Levels
- INFO: General information about application flow
- WARNING: Potential issues that don't stop execution
- ERROR: Errors that prevent normal operation
- DEBUG: Detailed debugging information

## Viewing Logs
- Open any .log file in a text editor
- Use `tail -f logs/application_*.log` to follow logs in real-time
- Check the most recent log file for current status

## Troubleshooting
1. Check the most recent log file for errors
2. Look for ERROR or WARNING messages
3. Check the timestamp to see when issues occurred
4. Use DEBUG level for more detailed information

Generated by AI Agent Ecosystem Builder
"""
        
        with open(os.path.join(logs_dir, "README.md"), "w") as f:
            f.write(sample_log_content)
        
        # Copy documentation files
        doc_files = ["README.md", "CHANGELOG.md"]
        for doc_file in doc_files:
            if os.path.exists(doc_file):
                try:
                    shutil.copy2(doc_file, os.path.join(deployment_dir, doc_file))
                    self.logger.info(f"Copied documentation file: {doc_file}")
                except Exception as e:
                    self.logger.warning(f"Failed to copy documentation file {doc_file}: {e}")
    
    def _create_github_files(self, deployment_dir: str, context: Dict[str, Any]):
        """Create GitHub-specific files"""
        # Create .gitignore
        gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
logs/*.log
*.log

# Environment variables
.env
.env.local
.env.production
"""
        
        with open(os.path.join(deployment_dir, ".gitignore"), "w") as f:
            f.write(gitignore_content)
        
        # Create GitHub Actions workflow
        workflow_content = """name: Python Application CI/CD

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.8'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        python -m pytest tests/ -v
    
    - name: Run code quality checks
      run: |
        python -m black --check src/
        python -m flake8 src/
        python -m mypy src/
"""
        
        os.makedirs(os.path.join(deployment_dir, ".github", "workflows"), exist_ok=True)
        with open(os.path.join(deployment_dir, ".github", "workflows", "ci.yml"), "w") as f:
            f.write(workflow_content)
        
        # Create GitHub README
        github_readme = f"""# {context.get('project_name', 'AI Generated Application')}

This application was generated by the AI Agent Ecosystem Builder.

## ROCKET: Quick Start

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd <repo-name>
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python src/main.py
   ```

## FOLDER: Project Structure

```
{os.path.basename(deployment_dir)}/
-- src/                    # Application source code
-- tests/                  # Test files
-- requirements.txt        # Python dependencies
-- README.md              # This file
-- CHANGELOG.md           # Version history
-- .github/               # GitHub Actions workflows
```

## TOOLS: Development

- **Testing:** `python -m pytest tests/ -v`
- **Code Quality:** `python -m black src/ && python -m flake8 src/`
- **Type Checking:** `python -m mypy src/`

## SUCCESS: Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and quality checks
5. Submit a pull request

---
*Generated by AI Agent Ecosystem Builder on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*
"""
        
        with open(os.path.join(deployment_dir, "README.md"), "w") as f:
            f.write(github_readme)
    
    def _create_executable_files(self, deployment_dir: str, context: Dict[str, Any]):
        """Create executable-specific files"""
        # Create setup.py for PyInstaller
        setup_content = f'''"""
Setup script for creating executable
"""

from setuptools import setup, find_packages
import os

# Read requirements
with open('requirements.txt', 'r') as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name="{context.get('project_name', 'ai_generated_app')}",
    version="1.0.0",
    description="AI Generated Python Application",
    author="AI Agent Ecosystem Builder",
    packages=find_packages(),
    install_requires=requirements,
    entry_points={{
        'console_scripts': [
            'ai-app=src.main:main',
        ],
    }},
    python_requires='>=3.8',
)
'''
        
        with open(os.path.join(deployment_dir, "setup.py"), "w") as f:
            f.write(setup_content)
        
        # Create requirements.txt for the executable first
        requirements_content = """# Application Dependencies
# Install with: pip install -r requirements.txt

# Core dependencies
openai>=1.0.0
python-dotenv>=1.0.0
rich>=13.0.0

# Add your specific dependencies here
"""
        
        with open(os.path.join(deployment_dir, "requirements.txt"), "w") as f:
            f.write(requirements_content)
        
        # Create a main application file specifically for executable with logging
        main_app_content = '''"""
Main Application Entry Point for Executable
Auto-generated by AI Agent Ecosystem Builder
"""

import sys
import os
import logging
from datetime import datetime
from pathlib import Path

def setup_logging():
    """Setup logging configuration for executable"""
    # Create logs directory next to executable
    if getattr(sys, 'frozen', False):
        # Running as executable
        base_path = Path(sys.executable).parent
    else:
        # Running as script
        base_path = Path(__file__).parent
    
    logs_dir = base_path / "logs"
    logs_dir.mkdir(exist_ok=True)
    
    # Create timestamped log file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = logs_dir / f"application_{timestamp}.log"
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    logger = logging.getLogger(__name__)
    logger.info(f"Logging initialized. Log file: {log_file}")
    logger.info(f"Executable path: {sys.executable}")
    logger.info(f"Working directory: {os.getcwd()}")
    return logger

def main():
    """Main application function"""
    # Setup logging
    logger = setup_logging()
    
    logger.info("ROCKET: Starting AI-generated Python application (executable)")
    logger.info("=" * 50)
    
    try:
        # Import and run your application modules here
        # This is where you would import your generated modules
        
        logger.info("FOLDER: Application modules loaded successfully")
        logger.info("TOOLS: Customize this main.py file to integrate your generated modules")
        
        # Example of how to use generated modules:
        # from your_module import YourClass
        # app = YourClass()
        # app.run()
        
        logger.info("SUCCESS: Application ready to use!")
        
    except Exception as e:
        logger.error(f"ERROR: Error running application: {e}")
        logger.exception("Full traceback:")
        return 1
    
    logger.info("SUCCESS: Application completed successfully")
    return 0

if __name__ == "__main__":
    sys.exit(main())
'''
        
        # Check if main.py already exists and is functional
        main_path = os.path.join(deployment_dir, "src", "main.py")
        os.makedirs(os.path.dirname(main_path), exist_ok=True)
        
        # Check if main.py already exists and contains functional code
        if os.path.exists(main_path):
            with open(main_path, "r") as f:
                existing_content = f.read()
            
            # Check if it's a functional application (not just a template)
            if any(keyword in existing_content for keyword in 
                   ["CalculatorApp", "GUI application", "app.run()", "tkinter", "mainloop"]):
                self.logger.info("Functional main.py already exists, keeping it")
            else:
                self.logger.info("Overriding template main.py with executable-specific version")
                with open(main_path, "w") as f:
                    f.write(main_app_content)
        else:
            self.logger.info("Creating new main.py for executable")
            with open(main_path, "w") as f:
                f.write(main_app_content)
        
        # Create PyInstaller spec file
        # Find the main Python file - prioritize src/main.py for executables
        main_file = None
        
        # First, check if src/main.py exists (this is what we create for executables)
        if os.path.exists(os.path.join(deployment_dir, "src", "main.py")):
            main_file = "src/main.py"
            self.logger.info(f"Using src/main.py for PyInstaller spec")
        else:
            # Fallback to looking in generated_files
            self.logger.info("src/main.py not found, searching in generated_files")
            for file_path in context.get("generated_files", []):
                if file_path.endswith(".py") and "main" in file_path.lower():
                    main_file = file_path
                    self.logger.info(f"Found main file in generated_files: {file_path}")
                    break
            
            if not main_file:
                # Default to src/main.py if no main file found
                main_file = "src/main.py"
                self.logger.warning("No main file found, defaulting to src/main.py")
        
        self.logger.info(f"PyInstaller will use main file: {main_file}")
        
        spec_content = f'''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['{main_file}'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='{context.get('project_name', 'ai_app')}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
'''
        
        with open(os.path.join(deployment_dir, "app.spec"), "w") as f:
            f.write(spec_content)
        
        # Create build script
        build_script = """#!/usr/bin/env python3
\"\"\"
Build script for creating executable
\"\"\"

import os
import subprocess
import sys

def main():
    \"\"\"Build the executable\"\"\"
    print("ROCKET: Building executable...")
    
    try:
        # Install PyInstaller if not already installed
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        
        # Build the executable
        subprocess.check_call([sys.executable, "-m", "PyInstaller", "app.spec"])
        
        print("SUCCESS: Executable built successfully!")
        print("FOLDER: Check the 'dist' directory for your executable")
        
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Build failed: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
"""
        
        with open(os.path.join(deployment_dir, "build.py"), "w") as f:
            f.write(build_script)
    
    def _create_source_files(self, deployment_dir: str, context: Dict[str, Any]):
        """Create source-specific files"""
        # Create run script
        run_script = """#!/usr/bin/env python3
\"\"\"
Application runner script
\"\"\"

import sys
import os
from pathlib import Path

# Add src directory to path
src_path = Path(__file__).parent / "src"
if src_path.exists():
    sys.path.insert(0, str(src_path))

def main():
    \"\"\"Main application entry point\"\"\"
    try:
        print("ROCKET: Starting your application...")
        
        # Import and run your main application
        if os.path.exists("src/main.py"):
            import main
            if hasattr(main, 'main'):
                main.main()
        else:
            print("FOLDER: Application files ready!")
            print("TOOLS: Customize the run script based on your application structure")
            
    except Exception as e:
        print(f"ERROR: Error running application: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
"""
        
        with open(os.path.join(deployment_dir, "run.py"), "w") as f:
            f.write(run_script)
        
        # Create development script
        dev_script = """#!/usr/bin/env python3
\"\"\"
Development script for running tests and quality checks
\"\"\"

import subprocess
import sys

def main():
    \"\"\"Run development tasks\"\"\"
    print("TOOLS: Running development tasks...")
    
    try:
        # Run tests
        print("TEST: Running tests...")
        subprocess.check_call([sys.executable, "-m", "pytest", "tests/", "-v"])
        
        # Run code quality checks
        print("GEAR: Running code quality checks...")
        subprocess.check_call([sys.executable, "-m", "black", "src/"])
        subprocess.check_call([sys.executable, "-m", "flake8", "src/"])
        subprocess.check_call([sys.executable, "-m", "mypy", "src/"])
        
        print("SUCCESS: All development tasks completed!")
        
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Development task failed: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
"""
        
        with open(os.path.join(deployment_dir, "dev.py"), "w") as f:
            f.write(dev_script)
    
    def _create_installer_script(self, deployment_dir: str):
        """Create installer script for executable"""
        installer_script = """#!/usr/bin/env python3
\"\"\"
Installer script for executable deployment
\"\"\"

import os
import sys
import subprocess
import shutil
from pathlib import Path

def main():
    \"\"\"Install the application\"\"\"
    print("ROCKET: Installing application...")
    
    try:
        # Install dependencies if requirements.txt exists
        if os.path.exists("requirements.txt"):
            print("GEAR: Installing dependencies...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        else:
            print("GEAR: No requirements.txt found, skipping dependency installation")
        
        # Build executable
        print("BUILD: Building executable...")
        subprocess.check_call([sys.executable, "build.py"])
        
        # Create installation directory
        install_dir = Path.home() / "Applications" / "AI_Generated_App"
        install_dir.mkdir(parents=True, exist_ok=True)
        
        # Create logs directory
        logs_dir = install_dir / "logs"
        logs_dir.mkdir(exist_ok=True)
        
        # Copy executable
        if os.path.exists("dist"):
            for file in os.listdir("dist"):
                src = os.path.join("dist", file)
                dst = os.path.join(install_dir, file)
                if os.path.isfile(src):
                    shutil.copy2(src, dst)
                elif os.path.isdir(src):
                    shutil.copytree(src, dst, dirs_exist_ok=True)
        
        print("SUCCESS: Application installed successfully!")
        print(f"FOLDER: Installed to: {install_dir}")
        print(f"FOLDER: Logs directory: {logs_dir}")
        print("TOOLS: Logs will be created when you run the executable")
        print("TOOLS: For PowerShell: cd executable_deploy_YYYYMMDD_HHMMSS; python install.py")
        print("TOOLS: For Command Prompt: cd executable_deploy_YYYYMMDD_HHMMSS && python install.py")
        
    except Exception as e:
        print(f"ERROR: Installation failed: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
"""
        
        with open(os.path.join(deployment_dir, "install.py"), "w") as f:
            f.write(installer_script)
    
    def _build_executable(self, deployment_dir: str) -> Dict[str, Any]:
        """Build the executable using PyInstaller"""
        try:
            self.logger.info("Building executable...")
            
            # Change to deployment directory
            original_dir = os.getcwd()
            os.chdir(deployment_dir)
            
            try:
                # Check if main file exists
                main_files = []
                for file in os.listdir("."):
                    if file.endswith(".py"):
                        main_files.append(file)
                
                # Also check src directory
                if os.path.exists("src"):
                    for file in os.listdir("src"):
                        if file.endswith(".py"):
                            main_files.append(os.path.join("src", file))
                
                if not main_files:
                    return {
                        "success": False,
                        "message": "No Python files found to build executable"
                    }
                
                self.logger.info(f"Found Python files: {main_files}")
                
                # Install PyInstaller if not already installed
                self.logger.info("Installing PyInstaller...")
                subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], 
                             check=True, capture_output=True, text=True)
                
                # Try to build using the spec file first
                if os.path.exists("app.spec"):
                    self.logger.info("Building executable with PyInstaller using spec file...")
                    result = subprocess.run([sys.executable, "-m", "PyInstaller", "app.spec"], 
                                          capture_output=True, text=True)
                else:
                    # Fallback: build directly with main file
                    main_file = main_files[0]  # Use first Python file found
                    self.logger.info(f"Building executable with PyInstaller using {main_file}...")
                    result = subprocess.run([sys.executable, "-m", "PyInstaller", "--onefile", main_file], 
                                          capture_output=True, text=True)
                
                if result.returncode == 0:
                    # Find the executable
                    dist_dir = os.path.join(deployment_dir, "dist")
                    if os.path.exists(dist_dir):
                        # Look for executable files
                        for file in os.listdir(dist_dir):
                            file_path = os.path.join(dist_dir, file)
                            if os.path.isfile(file_path) and (file.endswith('.exe') or not file.endswith('.py')):
                                self.logger.info(f"Executable created: {file_path}")
                                return {
                                    "success": True,
                                    "executable_path": file_path,
                                    "message": "Executable built successfully"
                                }
                    
                    # If no specific executable found, return the dist directory
                    return {
                        "success": True,
                        "executable_path": dist_dir,
                        "message": "Executable built successfully (check dist directory)"
                    }
                else:
                    return {
                        "success": False,
                        "message": f"PyInstaller build failed: {result.stderr}"
                    }
                    
            finally:
                # Change back to original directory
                os.chdir(original_dir)
                
        except subprocess.CalledProcessError as e:
            return {
                "success": False,
                "message": f"Build process failed: {str(e)}"
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Build failed: {str(e)}"
            }
        finally:
            # Ensure we're back in the original directory
            try:
                os.chdir(original_dir)
            except:
                pass

    def _initialize_git_repo(self, deployment_dir: str):
        """Initialize git repository"""
        try:
            # Change to deployment directory
            original_dir = os.getcwd()
            os.chdir(deployment_dir)
            
            # Initialize git repository
            subprocess.run(["git", "init"], check=True)
            subprocess.run(["git", "add", "."], check=True)
            subprocess.run(["git", "commit", "-m", "Initial commit - AI Generated Application"], check=True)
            
            # Change back to original directory
            os.chdir(original_dir)
            
            self.logger.info("Git repository initialized successfully")
            
        except subprocess.CalledProcessError as e:
            self.logger.warning(f"Git initialization failed: {e}")
        except Exception as e:
            self.logger.warning(f"Git initialization failed: {e}")
        finally:
            # Ensure we're back in the original directory
            try:
                os.chdir(original_dir)
            except:
                pass
