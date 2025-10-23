"""
Coding Standards Agent - Enforces code quality and standards
"""

import subprocess
import os
from typing import Dict, Any, List, Optional
from .base_agent import BaseAgent

class StandardsAgent(BaseAgent):
    """Agent responsible for enforcing coding standards"""
    
    def __init__(self):
        super().__init__(
            agent_id="standards_001",
            name="Coding Standards Agent",
            description="Enforces PEP 8 compliance and code quality standards"
        )
        self.standards_tools = ["black", "flake8", "mypy"]
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute standards enforcement"""
        try:
            self.log_action("Starting standards enforcement")
            
            # Get files to check
            files_to_check = context.get("generated_files", [])
            if not files_to_check:
                return self.create_response(
                    False,
                    "No files provided for standards checking"
                )
            
            # Run standards checks
            results = {}
            for tool in self.standards_tools:
                tool_results = self._run_standards_tool(tool, files_to_check)
                results[tool] = tool_results
            
            # Apply fixes where possible
            self._apply_automatic_fixes(files_to_check)
            
            self.log_action("Standards enforcement completed")
            return self.create_response(
                True,
                "🧩 Coding standards enforced successfully",
                {"standards_results": results}
            )
            
        except Exception as e:
            self.logger.error(f"Standards enforcement failed: {str(e)}")
            return self.create_response(False, f"Standards enforcement failed: {str(e)}")
    
    def _run_standards_tool(self, tool: str, files: List[str]) -> Dict[str, Any]:
        """Run a specific standards tool"""
        try:
            if tool == "black":
                return self._run_black(files)
            elif tool == "flake8":
                return self._run_flake8(files)
            elif tool == "mypy":
                return self._run_mypy(files)
            else:
                return {"error": f"Unknown tool: {tool}"}
                
        except Exception as e:
            self.logger.error(f"Failed to run {tool}: {str(e)}")
            return {"error": str(e)}
    
    def _run_black(self, files: List[str]) -> Dict[str, Any]:
        """Run Black code formatter"""
        try:
            # Run black in check mode first
            result = subprocess.run(
                ["black", "--check", "--diff"] + files,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                return {"status": "clean", "message": "Code is properly formatted"}
            else:
                return {
                    "status": "needs_formatting",
                    "message": "Code needs formatting",
                    "diff": result.stdout
                }
                
        except FileNotFoundError:
            return {"error": "Black not found. Please install with: pip install black"}
        except Exception as e:
            return {"error": str(e)}
    
    def _run_flake8(self, files: List[str]) -> Dict[str, Any]:
        """Run Flake8 linter"""
        try:
            result = subprocess.run(
                ["flake8"] + files,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                return {"status": "clean", "message": "No linting issues found"}
            else:
                return {
                    "status": "has_issues",
                    "message": "Linting issues found",
                    "issues": result.stdout
                }
                
        except FileNotFoundError:
            return {"error": "Flake8 not found. Please install with: pip install flake8"}
        except Exception as e:
            return {"error": str(e)}
    
    def _run_mypy(self, files: List[str]) -> Dict[str, Any]:
        """Run MyPy type checker"""
        try:
            result = subprocess.run(
                ["mypy"] + files,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                return {"status": "clean", "message": "No type checking issues found"}
            else:
                return {
                    "status": "has_issues",
                    "message": "Type checking issues found",
                    "issues": result.stdout
                }
                
        except FileNotFoundError:
            return {"error": "MyPy not found. Please install with: pip install mypy"}
        except Exception as e:
            return {"error": str(e)}
    
    def _apply_automatic_fixes(self, files: List[str]):
        """Apply automatic fixes where possible"""
        try:
            # Run black to format code
            subprocess.run(
                ["black"] + files,
                check=False
            )
            self.logger.info("Applied Black formatting")
            
        except Exception as e:
            self.logger.error(f"Failed to apply automatic fixes: {str(e)}")
    
    def get_standards_report(self, files: List[str]) -> Dict[str, Any]:
        """Get comprehensive standards report"""
        report = {
            "files_checked": files,
            "tools_used": self.standards_tools,
            "results": {}
        }
        
        for tool in self.standards_tools:
            report["results"][tool] = self._run_standards_tool(tool, files)
        
        return report
