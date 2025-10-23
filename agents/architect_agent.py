"""
Architect Agent - Designs system architecture and modules
"""

import os
import json
from typing import Dict, Any, List, Optional
from .base_agent import BaseAgent

class ArchitectAgent(BaseAgent):
    """Agent responsible for system architecture design"""
    
    def __init__(self):
        super().__init__(
            agent_id="arch_001",
            name="Architect Agent",
            description="Designs system architecture, modules, and dependencies"
        )
        self.architecture = {}
        self.modules = []
        self.dependencies = []
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute architecture design"""
        try:
            self.log_action("Starting architecture design")
            
            # Get project requirements from context
            requirements = context.get("project_requirements", {})
            if not requirements:
                # Create default requirements if none provided
                requirements = {
                    "description": "A Python application",
                    "user_description": "A general-purpose Python application",
                    "conversation_history": []
                }
                self.logger.info("No specific requirements found, using default architecture")
            
            # Design architecture
            architecture = self._design_architecture(requirements)
            
            # Create module structure
            modules = self._design_modules(architecture)
            
            # Identify dependencies
            dependencies = self._identify_dependencies(modules)
            
            # Save architecture to file
            self._save_architecture(architecture, modules, dependencies)
            
            self.log_action("Architecture design completed")
            return self.create_response(
                True,
                "🏗️ Architecture designed successfully",
                {
                    "architecture": architecture,
                    "modules": modules,
                    "dependencies": dependencies
                }
            )
            
        except Exception as e:
            self.logger.error(f"Architecture design failed: {str(e)}")
            return self.create_response(False, f"Architecture design failed: {str(e)}")
    
    def _design_architecture(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Design the system architecture"""
        try:
            # Create a basic architecture if requirements are minimal
            if not requirements.get("user_description") or len(requirements.get("user_description", "").strip()) < 10:
                return self._create_default_architecture()
            
            messages = [
                {
                    "role": "system",
                    "content": """You are a Software Architect designing a Python application. Based on the requirements, create a comprehensive architecture design including:

1. System overview and purpose
2. Main components and their responsibilities
3. Data flow and interactions
4. Technology stack recommendations
5. Scalability considerations
6. Security considerations

Return the architecture as a structured JSON object."""
                },
                {
                    "role": "user",
                    "content": f"Design architecture for: {json.dumps(requirements, indent=2)}"
                }
            ]
            
            response = self.call_llm(messages)
            
            # Try to parse JSON response
            try:
                architecture = json.loads(response)
            except json.JSONDecodeError:
                # If not JSON, create structured architecture
                architecture = {
                    "overview": response,
                    "components": [],
                    "data_flow": "",
                    "technology_stack": [],
                    "scalability": "",
                    "security": ""
                }
            
            return architecture
            
        except Exception as e:
            self.logger.error(f"Architecture design failed: {str(e)}")
            # Fall back to default architecture
            return self._create_default_architecture()
    
    def _create_default_architecture(self) -> Dict[str, Any]:
        """Create a default architecture for basic Python applications"""
        return {
            "overview": "A Python application with modular structure",
            "components": [
                {
                    "name": "Main Application",
                    "description": "Core application logic and entry point",
                    "responsibilities": ["Application initialization", "Main workflow", "Error handling"]
                },
                {
                    "name": "Utilities",
                    "description": "Helper functions and utilities",
                    "responsibilities": ["Common functions", "Data processing", "File operations"]
                }
            ],
            "data_flow": "Simple linear flow from input to processing to output",
            "technology_stack": ["Python 3.8+", "Standard Library"],
            "scalability": "Designed for single-user applications",
            "security": "Basic input validation and error handling"
        }
    
    def _design_modules(self, architecture: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Design module structure"""
        try:
            # Create default modules if architecture is basic
            if not architecture.get("components") or len(architecture.get("components", [])) < 2:
                return self._create_default_modules()
            
            messages = [
                {
                    "role": "system",
                    "content": """Based on the architecture, design the Python module structure. For each module, specify:

1. Module name and purpose
2. Main classes and functions
3. Dependencies on other modules
4. File structure
5. Key responsibilities

Return as a list of module specifications."""
                },
                {
                    "role": "user",
                    "content": f"Design modules for architecture: {json.dumps(architecture, indent=2)}"
                }
            ]
            
            response = self.call_llm(messages)
            
            # Parse modules from response
            modules = self._parse_modules_from_response(response)
            return modules
            
        except Exception as e:
            self.logger.error(f"Module design failed: {str(e)}")
            return self._create_default_modules()
    
    def _create_default_modules(self) -> List[Dict[str, Any]]:
        """Create default modules for basic applications"""
        return [
            {
                "name": "Main Application",
                "description": "Core application logic and entry point",
                "responsibilities": ["Application initialization", "Main workflow", "Error handling"],
                "classes": ["Application"],
                "functions": ["main", "run", "initialize"]
            },
            {
                "name": "Utilities",
                "description": "Helper functions and utilities",
                "responsibilities": ["Common functions", "Data processing", "File operations"],
                "classes": ["FileHandler", "DataProcessor"],
                "functions": ["process_data", "save_file", "load_file"]
            }
        ]
    
    def _parse_modules_from_response(self, response: str) -> List[Dict[str, Any]]:
        """Parse modules from LLM response"""
        # This is a simplified parser - in practice, you'd want more robust parsing
        modules = []
        lines = response.split('\n')
        current_module = {}
        
        for line in lines:
            line = line.strip()
            if line.startswith('Module:') or line.startswith('##'):
                if current_module:
                    modules.append(current_module)
                current_module = {"name": line.replace('Module:', '').replace('##', '').strip()}
            elif line.startswith('-') or line.startswith('*'):
                if 'description' not in current_module:
                    current_module['description'] = []
                current_module['description'].append(line[1:].strip())
        
        if current_module:
            modules.append(current_module)
        
        return modules
    
    def _identify_dependencies(self, modules: List[Dict[str, Any]]) -> List[str]:
        """Identify external dependencies"""
        try:
            messages = [
                {
                    "role": "system",
                    "content": """Based on the modules and architecture, identify all external Python packages that will be needed. Return only a list of package names, one per line."""
                },
                {
                    "role": "user",
                    "content": f"Identify dependencies for modules: {json.dumps(modules, indent=2)}"
                }
            ]
            
            response = self.call_llm(messages)
            
            # Parse dependencies from response
            dependencies = [line.strip() for line in response.split('\n') if line.strip()]
            return dependencies
            
        except Exception as e:
            self.logger.error(f"Dependency identification failed: {str(e)}")
            return []
    
    def _save_architecture(self, architecture: Dict[str, Any], modules: List[Dict[str, Any]], dependencies: List[str]):
        """Save architecture to file"""
        try:
            arch_data = {
                "architecture": architecture,
                "modules": modules,
                "dependencies": dependencies,
                "created_at": self.log_action("Architecture saved")["timestamp"]
            }
            
            os.makedirs("project_docs", exist_ok=True)
            with open("project_docs/architecture.json", "w") as f:
                json.dump(arch_data, f, indent=2)
            
            self.logger.info("Architecture saved to project_docs/architecture.json")
            
        except Exception as e:
            self.logger.error(f"Failed to save architecture: {str(e)}")
            raise
