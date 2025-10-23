"""
Environment Agent - Handles virtual environment setup and API key management
"""

import os
import sys
import subprocess
import platform
from typing import Dict, Any, Optional
from .base_agent import BaseAgent

class EnvironmentAgent(BaseAgent):
    """Agent responsible for environment setup and validation"""
    
    def __init__(self):
        super().__init__(
            agent_id="env_001",
            name="Environment Agent",
            description="Manages virtual environment, dependencies, and API key setup"
        )
        self.venv_path = "venv"
        self.activation_script = self._get_activation_script()
    
    def _get_activation_script(self) -> str:
        """Get the appropriate activation script based on OS"""
        if platform.system() == "Windows":
            return os.path.join(self.venv_path, "Scripts", "activate")
        else:
            return os.path.join(self.venv_path, "bin", "activate")
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute environment setup process"""
        try:
            self.log_action("Starting environment setup")
            
            # Check if venv exists
            if not self._check_venv_exists():
                self.log_action("Creating virtual environment")
                self._create_venv()
            
            # Check if venv is activated
            if not self._is_venv_active():
                self.log_action("Virtual environment not active")
                return self.create_response(
                    False, 
                    "Virtual environment needs to be activated. Please run: source venv/Scripts/activate (Windows) or source venv/bin/activate (Unix)"
                )
            
            # Install dependencies
            self.log_action("Installing dependencies")
            self._install_dependencies()
            
            # Check API key
            if not self._check_api_key():
                self.log_action("API key not found")
                return self.create_response(
                    False,
                    "OPENAI_API_KEY not found. Please set it in your environment or .env file"
                )
            
            self.log_action("Environment setup completed successfully")
            return self.create_response(
                True,
                "✅ Environment activated successfully",
                {"venv_path": self.venv_path, "dependencies_installed": True}
            )
            
        except Exception as e:
            self.logger.error(f"Environment setup failed: {str(e)}")
            return self.create_response(False, f"Environment setup failed: {str(e)}")
    
    def _check_venv_exists(self) -> bool:
        """Check if virtual environment exists"""
        return os.path.exists(self.venv_path)
    
    def _create_venv(self):
        """Create virtual environment"""
        try:
            subprocess.run([sys.executable, "-m", "venv", self.venv_path], check=True)
            self.logger.info("Virtual environment created successfully")
        except subprocess.CalledProcessError as e:
            raise Exception(f"Failed to create virtual environment: {e}")
    
    def _is_venv_active(self) -> bool:
        """Check if virtual environment is active"""
        return hasattr(sys, 'real_prefix') or (
            hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
        )
    
    def _install_dependencies(self):
        """Install required dependencies"""
        try:
            # Upgrade pip first
            subprocess.run([
                sys.executable, "-m", "pip", "install", "--upgrade", "pip"
            ], check=True)
            
            # Install requirements
            subprocess.run([
                sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
            ], check=True)
            
            self.logger.info("Dependencies installed successfully")
        except subprocess.CalledProcessError as e:
            raise Exception(f"Failed to install dependencies: {e}")
    
    def _check_api_key(self) -> bool:
        """Check if OpenAI API key is available"""
        api_key = os.getenv('OPENAI_API_KEY')
        return api_key is not None and api_key.strip() != ""
    
    def request_api_key(self) -> Dict[str, Any]:
        """Request API key from user"""
        return self.create_response(
            False,
            "🔑 Please enter your OPENAI_API_KEY to continue setup.",
            {"requires_user_input": True, "input_type": "api_key"}
        )
    
    def save_api_key(self, api_key: str) -> Dict[str, Any]:
        """Save API key to .env file"""
        try:
            with open('.env', 'w') as f:
                f.write(f"OPENAI_API_KEY={api_key}\n")
            
            # Reload environment
            from dotenv import load_dotenv
            load_dotenv()
            
            self.log_action("API key saved successfully")
            return self.create_response(
                True,
                "✅ API key saved and environment ready.",
                {"api_key_saved": True}
            )
        except Exception as e:
            return self.create_response(False, f"Failed to save API key: {str(e)}")
    
    def validate_environment(self) -> Dict[str, Any]:
        """Validate that environment is properly set up"""
        checks = {
            "venv_exists": self._check_venv_exists(),
            "venv_active": self._is_venv_active(),
            "api_key_available": self._check_api_key(),
            "dependencies_installed": self._check_dependencies()
        }
        
        all_passed = all(checks.values())
        
        return self.create_response(
            all_passed,
            "Environment validation completed",
            {"checks": checks}
        )
    
    def _check_dependencies(self) -> bool:
        """Check if required dependencies are installed"""
        try:
            import openai
            import langchain
            import chromadb
            import fastapi
            import pydantic
            import rich
            import pytest
            import black
            import flake8
            import mypy
            import git
            return True
        except ImportError:
            return False
