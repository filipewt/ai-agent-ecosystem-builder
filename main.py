"""
Main entry point for the AI Agent Ecosystem Builder
"""

import os
import sys
import asyncio
import json
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Add agents directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'agents'))

from agents.environment_agent import EnvironmentAgent
from agents.orchestrator_agent import OrchestratorAgent
from agents.coordinator_agent import CoordinatorAgent
from agents.architect_agent import ArchitectAgent
from agents.core_logic_agent import CoreLogicAgent
from agents.standards_agent import StandardsAgent
from agents.backup_agent import BackupAgent
from agents.testing_agent import TestingAgent
from agents.documentation_agent import DocumentationAgent
from agents.ethics_agent import EthicsAgent
from agents.validator_agent import ValidatorAgent
from agents.repository_agent import RepositoryAgent
from agents.deployment_agent import DeploymentAgent

class AIAgentEcosystem:
    """Main class for the AI Agent Ecosystem"""
    
    def __init__(self):
        self.agents = {}
        self.orchestrator = None
        self.context = {}
        self.workflow_state = "initializing"
        
    def initialize_agents(self):
        """Initialize all agents"""
        try:
            # Create agents
            self.agents["env_001"] = EnvironmentAgent()
            self.agents["coord_001"] = CoordinatorAgent()
            self.agents["arch_001"] = ArchitectAgent()
            self.agents["core_001"] = CoreLogicAgent()
            self.agents["standards_001"] = StandardsAgent()
            self.agents["backup_001"] = BackupAgent()
            self.agents["test_001"] = TestingAgent()
            self.agents["doc_001"] = DocumentationAgent()
            self.agents["ethics_001"] = EthicsAgent()
            self.agents["valid_001"] = ValidatorAgent()
            self.agents["repo_001"] = RepositoryAgent()
            self.agents["deploy_001"] = DeploymentAgent()
            
            # Create orchestrator
            self.orchestrator = OrchestratorAgent()
            
            # Register agents with orchestrator
            for agent in self.agents.values():
                self.orchestrator.register_agent(agent)
            
            print("SUCCESS: All agents initialized successfully")
            
        except Exception as e:
            print(f"ERROR: Failed to initialize agents: {str(e)}")
            sys.exit(1)
    
    def setup_environment(self):
        """Setup environment and check API key"""
        try:
            # Load environment variables
            load_dotenv()
            
            # Check if API key exists
            api_key = os.getenv('OPENAI_API_KEY')
            if not api_key:
                print("KEY: Please enter your OPENAI_API_KEY to continue setup.")
                api_key = input("OPENAI_API_KEY: ").strip()
                
                if not api_key:
                    print("ERROR: API key is required. Exiting.")
                    sys.exit(1)
                
                # Save API key to .env file
                with open('.env', 'w') as f:
                    f.write(f"OPENAI_API_KEY={api_key}\n")
                
                # Reload environment
                load_dotenv()
            
            print("SUCCESS: API key saved and environment ready.")
            
        except Exception as e:
            print(f"ERROR: Environment setup failed: {str(e)}")
            sys.exit(1)
    
    def run_workflow(self):
        """Run the main workflow"""
        try:
            print("ROCKET: Starting AI Agent Ecosystem Builder")
            print("=" * 50)
            
            # Phase 0: Environment Setup
            print("GEAR: Environment Agent: Checking virtual environment...")
            env_result = self.agents["env_001"].execute(self.context)
            
            if not env_result["success"]:
                print(f"ERROR: Environment setup failed: {env_result['message']}")
                return
            
            print("SUCCESS: Environment activated successfully.")
            
            # Phase 1: Project Definition
            print("\nCOMPASS: Product Coordinator: Starting project definition...")
            print("Please describe your Python project requirements:")
            
            # Collect project requirements
            project_requirements = {}
            conversation_history = []
            
            while True:
                user_input = input("\nYou: ").strip()
                if not user_input:
                    continue
                
                self.context["user_input"] = user_input
                coord_result = self.agents["coord_001"].execute(self.context)
                
                print(f"\n{coord_result['message']}")
                
                # Store the conversation and requirements
                conversation_history.append({"role": "user", "content": user_input})
                conversation_history.append({"role": "assistant", "content": coord_result['message']})
                
                # Extract requirements from the conversation
                if "requirements" in user_input.lower() or "need" in user_input.lower() or "want" in user_input.lower():
                    project_requirements["description"] = user_input
                
                if "start development" in user_input.lower():
                    # Store all collected requirements
                    project_requirements["conversation_history"] = conversation_history
                    project_requirements["user_description"] = " ".join([msg["content"] for msg in conversation_history if msg["role"] == "user"])
                    break
            
            # Store project requirements in context
            self.context["project_requirements"] = project_requirements
            
            # Phase 2: Development
            print("\nBRAIN: Starting development phase...")
            
            # Architect
            print("BUILD: Architect Agent: Designing system architecture...")
            arch_result = self.agents["arch_001"].execute(self.context)
            if not arch_result["success"]:
                print(f"ERROR: Architecture design failed: {arch_result['message']}")
                return
            
            # Core Logic
            print("BRAIN: Core Logic Agent: Writing Python code...")
            core_result = self.agents["core_001"].execute(self.context)
            if not core_result["success"]:
                print(f"ERROR: Code generation failed: {core_result['message']}")
                return
            
            # Update context with generated files
            self.context["generated_files"] = core_result.get("data", {}).get("generated_files", [])
            
            # Backup
            print("BACKUP: Backup Agent: Creating backups...")
            backup_result = self.agents["backup_001"].execute(self.context)
            if not backup_result["success"]:
                print(f"ERROR: Backup failed: {backup_result['message']}")
                return
            
            # Standards
            print("PUZZLE: Standards Agent: Enforcing coding standards...")
            standards_result = self.agents["standards_001"].execute(self.context)
            if not standards_result["success"]:
                print(f"ERROR: Standards enforcement failed: {standards_result['message']}")
                return
            
            # Testing
            print("TEST: Testing Agent: Running tests and validation...")
            test_result = self.agents["test_001"].execute(self.context)
            if not test_result["success"]:
                print(f"ERROR: Testing failed: {test_result['message']}")
                return
            
            # Documentation
            print("DOCS: Documentation Agent: Updating documentation...")
            doc_result = self.agents["doc_001"].execute(self.context)
            if not doc_result["success"]:
                print(f"ERROR: Documentation failed: {doc_result['message']}")
                return
            
            # Ethics
            print("SECURITY: Ethics Agent: Security and ethics review...")
            ethics_result = self.agents["ethics_001"].execute(self.context)
            if not ethics_result["success"]:
                print(f"ERROR: Ethics review failed: {ethics_result['message']}")
                return
            
            # Collect validation results from all agents
            validation_results = {
                "standards_results": standards_result.get("data", {}).get("standards_results", {}),
                "test_results": test_result.get("data", {}).get("test_results", {}),
                "documentation_results": doc_result.get("data", {}),
                "security_results": ethics_result.get("data", {}).get("review_results", {}),
                "ethics_results": ethics_result.get("data", {}).get("review_results", {})
            }
            
            # Add validation results to context
            self.context["validation_results"] = validation_results
            
            # Validator
            print("SUCCESS: Validator Agent: Final validation...")
            validator_result = self.agents["valid_001"].execute(self.context)
            if not validator_result["success"]:
                print(f"ERROR: Validation failed: {validator_result['message']}")
                return
            
            # Phase 3: Delivery
            print("\nROCKET: Starting delivery phase...")
            
            # Ask user for deployment preference
            print("\nTOOLS: Choose deployment option:")
            print("1. GitHub Repository (with CI/CD)")
            print("2. Executable File (standalone)")
            print("3. Source Code Only (development)")
            
            while True:
                choice = input("\nEnter your choice (1-3): ").strip()
                if choice == "1":
                    deployment_choice = "github"
                    break
                elif choice == "2":
                    deployment_choice = "executable"
                    break
                elif choice == "3":
                    deployment_choice = "source_only"
                    break
                else:
                    print("ERROR: Invalid choice. Please enter 1, 2, or 3.")
            
            # Set deployment choice in context
            self.context["deployment_choice"] = deployment_choice
            
            # Deploy using deployment agent
            print(f"PACKAGE: Deploying as {deployment_choice}...")
            deployment_result = self.agents["deploy_001"].execute(self.context)
            
            if deployment_result["success"]:
                print("SUCCESS: Project delivery completed successfully!")
                print(f"FOLDER: Application created in: {deployment_result['data']['deployment_path']}")
                
                # Show executable path if it's an executable deployment
                if deployment_choice == "executable" and "executable_path" in deployment_result["data"]:
                    print(f"EXECUTABLE: Built executable at: {deployment_result['data']['executable_path']}")
                
                print(f"ROCKET: Instructions: {deployment_result['data']['instructions']}")
                
                # Add PowerShell-specific instructions
                if deployment_choice == "executable":
                    print("TOOLS: For PowerShell users:")
                    print("TOOLS: cd executable_deploy_YYYYMMDD_HHMMSS; python install.py")
                    print("TOOLS: For Command Prompt users:")
                    print("TOOLS: cd executable_deploy_YYYYMMDD_HHMMSS && python install.py")
            else:
                print(f"ERROR: Deployment failed: {deployment_result['message']}")
            
        except KeyboardInterrupt:
            print("\n\nPAUSE: Workflow interrupted by user")
        except Exception as e:
            print(f"\nERROR: Workflow failed: {str(e)}")
            print("Type 'Try again' to resume from the last step")
    
    def _create_deployment_package(self):
        """Create a complete deployment package for the application"""
        try:
            import shutil
            import os
            from datetime import datetime
            
            # Create deployment directory
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            deployment_dir = f"deployed_app_{timestamp}"
            os.makedirs(deployment_dir, exist_ok=True)
            
            # Copy generated files
            generated_files = self.context.get("generated_files", [])
            for file_path in generated_files:
                if os.path.exists(file_path):
                    # Create directory structure in deployment
                    rel_path = os.path.relpath(file_path)
                    dest_path = os.path.join(deployment_dir, rel_path)
                    dest_dir = os.path.dirname(dest_path)
                    
                    if dest_dir:
                        os.makedirs(dest_dir, exist_ok=True)
                    
                    shutil.copy2(file_path, dest_path)
            
            # Copy documentation files
            doc_files = ["README.md", "CHANGELOG.md"]
            for doc_file in doc_files:
                if os.path.exists(doc_file):
                    shutil.copy2(doc_file, os.path.join(deployment_dir, doc_file))
            
            # Create requirements.txt for the deployed app
            with open(os.path.join(deployment_dir, "requirements.txt"), "w") as f:
                f.write("""# Application Dependencies
# Install with: pip install -r requirements.txt

# Core dependencies
openai>=1.0.0
python-dotenv>=1.0.0
rich>=13.0.0

# Add your specific dependencies here
""")
            
            # Create run script
            run_script = """#!/usr/bin/env python3
\"\"\"
Auto-generated application runner
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
        # Import and run your main application
        # This will be customized based on your generated code
        print("ROCKET: Starting your application...")
        
        # Example: If you have a main.py in src/
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
            
            # Create deployment README
            deployment_readme = f"""# Deployed Application

This is your auto-generated Python application created by the AI Agent Ecosystem Builder.

## ROCKET: Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application:**
   ```bash
   python run.py
   ```

## FOLDER: Project Structure

```
{deployment_dir}/
-- src/                    # Your application source code
-- requirements.txt        # Python dependencies
-- run.py                 # Application runner
-- README.md              # Project documentation
-- CHANGELOG.md           # Version history
```

## TOOLS: Customization

- Edit files in the `src/` directory to customize your application
- Update `requirements.txt` to add new dependencies
- Modify `run.py` to change how the application starts

## Generated Files

{chr(10).join(f"- {file}" for file in generated_files if os.path.exists(file))}

## Next Steps

1. Test your application: `python run.py`
2. Customize the code in the `src/` directory
3. Add new features as needed
4. Deploy to your preferred platform

---
*Generated by AI Agent Ecosystem Builder on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*
"""
            
            with open(os.path.join(deployment_dir, "DEPLOYMENT_README.md"), "w") as f:
                f.write(deployment_readme)
            
            # Get run instructions
            run_instructions = f"cd {deployment_dir} && python run.py"
            
            return {
                "success": True,
                "deployment_path": os.path.abspath(deployment_dir),
                "run_instructions": run_instructions,
                "files_created": len(generated_files)
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Deployment package creation failed: {str(e)}"
            }

def main():
    """Main entry point"""
    ecosystem = AIAgentEcosystem()
    
    try:
        # Setup environment
        ecosystem.setup_environment()
        
        # Initialize agents
        ecosystem.initialize_agents()
        
        # Run workflow
        ecosystem.run_workflow()
        
    except Exception as e:
        print(f"ERROR: System error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
