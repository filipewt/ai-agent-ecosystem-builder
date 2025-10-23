"""
Repository & Delivery Agent - Manages Git repository creation and deployment
"""

import os
import subprocess
from typing import Dict, Any, List, Optional
from .base_agent import BaseAgent

class RepositoryAgent(BaseAgent):
    """Agent responsible for repository creation and deployment"""
    
    def __init__(self):
        super().__init__(
            agent_id="repo_001",
            name="Repository & Delivery Agent",
            description="Manages Git repository creation, commits, and deployment"
        )
        self.git_credentials = {}
        self.repository_info = {}
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute repository operations"""
        try:
            self.log_action("Starting repository operations")
            
            # Check if we have Git credentials
            if not self._has_git_credentials():
                return self._request_git_credentials()
            
            # Initialize Git repository
            self._initialize_git_repository()
            
            # Create .gitignore
            self._create_gitignore()
            
            # Add and commit files
            self._commit_files()
            
            # Create remote repository
            remote_url = self._create_remote_repository()
            
            # Push to remote
            self._push_to_remote(remote_url)
            
            self.log_action("Repository operations completed")
            return self.create_response(
                True,
                "🚀 Repository created and deployed successfully",
                {"repository_url": remote_url}
            )
            
        except Exception as e:
            self.logger.error(f"Repository operations failed: {str(e)}")
            return self.create_response(False, f"Repository operations failed: {str(e)}")
    
    def _has_git_credentials(self) -> bool:
        """Check if Git credentials are available"""
        return bool(self.git_credentials.get("username") and self.git_credentials.get("repository_name"))
    
    def _request_git_credentials(self) -> Dict[str, Any]:
        """Request Git credentials from user"""
        return self.create_response(
            False,
            "Please provide your Git username.",
            {"requires_user_input": True, "input_type": "git_username"}
        )
    
    def set_git_credentials(self, username: str, repository_name: str, is_public: bool = True):
        """Set Git credentials"""
        self.git_credentials = {
            "username": username,
            "repository_name": repository_name,
            "is_public": is_public
        }
        self.log_action(f"Git credentials set: {username}/{repository_name}")
    
    def _initialize_git_repository(self):
        """Initialize Git repository"""
        try:
            subprocess.run(["git", "init"], check=True)
            self.logger.info("Git repository initialized")
        except subprocess.CalledProcessError as e:
            raise Exception(f"Failed to initialize Git repository: {e}")
    
    def _create_gitignore(self):
        """Create .gitignore file"""
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

# Project specific
.env
*.log
backups/
project_docs/
"""
        
        with open(".gitignore", "w") as f:
            f.write(gitignore_content)
        
        self.logger.info("Created .gitignore file")
    
    def _commit_files(self):
        """Add and commit files"""
        try:
            # Add all files
            subprocess.run(["git", "add", "."], check=True)
            
            # Commit
            subprocess.run(["git", "commit", "-m", "Initial commit: AI-generated Python project"], check=True)
            
            self.logger.info("Files committed successfully")
        except subprocess.CalledProcessError as e:
            raise Exception(f"Failed to commit files: {e}")
    
    def _create_remote_repository(self) -> str:
        """Create remote repository (placeholder - would integrate with GitHub API)"""
        username = self.git_credentials["username"]
        repo_name = self.git_credentials["repository_name"]
        
        # This is a placeholder - in a real implementation, you would:
        # 1. Use GitHub API to create repository
        # 2. Handle authentication
        # 3. Set repository visibility
        
        remote_url = f"https://github.com/{username}/{repo_name}.git"
        
        # Add remote origin
        subprocess.run(["git", "remote", "add", "origin", remote_url], check=True)
        
        self.logger.info(f"Remote repository configured: {remote_url}")
        return remote_url
    
    def _push_to_remote(self, remote_url: str):
        """Push to remote repository"""
        try:
            subprocess.run(["git", "push", "-u", "origin", "main"], check=True)
            self.logger.info("Pushed to remote repository")
        except subprocess.CalledProcessError as e:
            raise Exception(f"Failed to push to remote: {e}")
    
    def get_repository_info(self) -> Dict[str, Any]:
        """Get repository information"""
        return {
            "credentials": self.git_credentials,
            "repository_info": self.repository_info
        }
