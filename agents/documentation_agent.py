"""
Documentation Agent - Updates documentation and docstrings
"""

import os
import json
from datetime import datetime
from typing import Dict, Any, List, Optional
from .base_agent import BaseAgent

class DocumentationAgent(BaseAgent):
    """Agent responsible for documentation"""
    
    def __init__(self):
        super().__init__(
            agent_id="doc_001",
            name="Documentation Agent",
            description="Updates documentation, README, and docstrings"
        )
        self.documentation_files = []
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute documentation operations"""
        try:
            self.log_action("Starting documentation operations")
            
            # Get project information
            project_info = context.get("project_requirements", {})
            generated_files = context.get("generated_files", [])
            
            # Create README
            readme_path = self._create_readme(project_info, generated_files)
            
            # Update docstrings
            docstring_results = self._update_docstrings(generated_files)
            
            # Create changelog
            changelog_path = self._create_changelog()
            
            # Create API documentation
            api_docs_path = self._create_api_documentation(generated_files)
            
            self.documentation_files = [readme_path, changelog_path, api_docs_path]
            
            self.log_action("Documentation operations completed")
            return self.create_response(
                True,
                "📘 Documentation updated successfully",
                {
                    "documentation_files": self.documentation_files,
                    "docstring_results": docstring_results
                }
            )
            
        except Exception as e:
            self.logger.error(f"Documentation operations failed: {str(e)}")
            return self.create_response(False, f"Documentation operations failed: {str(e)}")
    
    def _create_readme(self, project_info: Dict[str, Any], generated_files: List[str]) -> str:
        """Create README.md file"""
        try:
            readme_content = self._generate_readme_content(project_info, generated_files)
            
            with open("README.md", "w") as f:
                f.write(readme_content)
            
            self.logger.info("Created README.md")
            return "README.md"
            
        except Exception as e:
            self.logger.error(f"Failed to create README: {str(e)}")
            raise
    
    def _generate_readme_content(self, project_info: Dict[str, Any], generated_files: List[str]) -> str:
        """Generate README content using LLM"""
        try:
            messages = [
                {
                    "role": "system",
                    "content": """You are a technical writer creating a comprehensive README.md file for a Python project. Include:

1. Project title and description
2. Installation instructions
3. Usage examples
4. API documentation
5. Contributing guidelines
6. License information

Make it professional and comprehensive."""
                },
                {
                    "role": "user",
                    "content": f"Create README for project: {json.dumps(project_info, indent=2)}\nGenerated files: {generated_files}"
                }
            ]
            
            response = self.call_llm(messages)
            return response
            
        except Exception as e:
            self.logger.error(f"Failed to generate README content: {str(e)}")
            # Fallback README
            return f"""# Python Project

## Description
{project_info.get('description', 'A Python application')}

## Installation
```bash
pip install -r requirements.txt
```

## Usage
```bash
python src/main.py
```

## Generated Files
{chr(10).join(f"- {file}" for file in generated_files)}

## Contributing
Please feel free to submit issues and enhancement requests.

## License
This project is licensed under the MIT License.
"""
    
    def _update_docstrings(self, files: List[str]) -> Dict[str, Any]:
        """Update docstrings in generated files"""
        results = {}
        
        for file_path in files:
            try:
                if not os.path.exists(file_path):
                    continue
                
                # Read file content
                with open(file_path, 'r') as f:
                    content = f.read()
                
                # Check if file has docstrings
                has_docstrings = '"""' in content or "'''" in content
                
                if not has_docstrings:
                    # Add basic docstrings
                    updated_content = self._add_docstrings(content)
                    
                    # Write back to file
                    with open(file_path, 'w') as f:
                        f.write(updated_content)
                    
                    results[file_path] = {"updated": True, "docstrings_added": True}
                else:
                    results[file_path] = {"updated": False, "docstrings_added": False}
                
            except Exception as e:
                results[file_path] = {"updated": False, "error": str(e)}
        
        return results
    
    def _add_docstrings(self, content: str) -> str:
        """Add basic docstrings to Python code"""
        lines = content.split('\n')
        updated_lines = []
        
        for i, line in enumerate(lines):
            updated_lines.append(line)
            
            # Add docstring after function/class definitions
            if line.strip().startswith('def ') or line.strip().startswith('class '):
                # Check if next line already has docstring
                if i + 1 < len(lines) and not lines[i + 1].strip().startswith('"""'):
                    # Add basic docstring
                    indent = len(line) - len(line.lstrip())
                    docstring = ' ' * (indent + 4) + '"""Docstring for this function/class."""'
                    updated_lines.append(docstring)
        
        return '\n'.join(updated_lines)
    
    def _create_changelog(self) -> str:
        """Create CHANGELOG.md file"""
        try:
            changelog_content = """# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - {date}

### Added
- Initial project setup
- Core functionality implementation
- Documentation and testing

### Changed
- N/A

### Removed
- N/A

### Fixed
- N/A
""".format(date=datetime.now().strftime("%Y-%m-%d"))
            
            with open("CHANGELOG.md", "w") as f:
                f.write(changelog_content)
            
            self.logger.info("Created CHANGELOG.md")
            return "CHANGELOG.md"
            
        except Exception as e:
            self.logger.error(f"Failed to create changelog: {str(e)}")
            raise
    
    def _create_api_documentation(self, generated_files: List[str]) -> str:
        """Create API documentation"""
        try:
            api_docs_content = self._generate_api_documentation(generated_files)
            
            os.makedirs("docs", exist_ok=True)
            api_docs_path = "docs/API.md"
            
            with open(api_docs_path, "w") as f:
                f.write(api_docs_content)
            
            self.logger.info("Created API documentation")
            return api_docs_path
            
        except Exception as e:
            self.logger.error(f"Failed to create API documentation: {str(e)}")
            raise
    
    def _generate_api_documentation(self, generated_files: List[str]) -> str:
        """Generate API documentation using LLM"""
        try:
            messages = [
                {
                    "role": "system",
                    "content": """You are a technical writer creating API documentation. Analyze the Python files and create comprehensive API documentation including:

1. Module descriptions
2. Class and function signatures
3. Parameter descriptions
4. Return value descriptions
5. Usage examples

Format as Markdown."""
                },
                {
                    "role": "user",
                    "content": f"Create API documentation for files: {generated_files}"
                }
            ]
            
            response = self.call_llm(messages)
            return response
            
        except Exception as e:
            self.logger.error(f"Failed to generate API documentation: {str(e)}")
            # Fallback API documentation
            return f"""# API Documentation

## Generated Files

{chr(10).join(f"- {file}" for file in generated_files)}

## Usage

Please refer to the individual files for detailed API documentation.

## Examples

```python
# Example usage
from src import main

# Your code here
```
"""
    
    def get_documentation_files(self) -> List[str]:
        """Get list of documentation files"""
        return self.documentation_files
