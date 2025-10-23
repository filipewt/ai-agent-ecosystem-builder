"""
Testing & Quality Agent - Runs tests and validates code quality
"""

import subprocess
import os
import sys
from typing import Dict, Any, List, Optional
from .base_agent import BaseAgent

class TestingAgent(BaseAgent):
    """Agent responsible for testing and quality validation"""
    
    def __init__(self):
        super().__init__(
            agent_id="test_001",
            name="Testing & Quality Agent",
            description="Runs tests and validates code quality"
        )
        self.test_results = {}
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute testing operations"""
        try:
            self.log_action("Starting testing operations")
            
            # Get files to test
            files_to_test = context.get("generated_files", [])
            if not files_to_test:
                return self.create_response(
                    False,
                    "No files provided for testing"
                )
            
            # Run syntax validation
            syntax_results = self._validate_syntax(files_to_test)
            
            # Run unit tests if they exist
            test_results = self._run_tests()
            
            # Run integration tests if applicable
            integration_results = self._run_integration_tests()
            
            # Compile results
            all_results = {
                "syntax_validation": syntax_results,
                "unit_tests": test_results,
                "integration_tests": integration_results
            }
            
            # Determine overall success
            overall_success = self._evaluate_results(all_results)
            
            self.log_action("Testing operations completed")
            return self.create_response(
                overall_success,
                "🧪 Testing completed successfully" if overall_success else "🧪 Testing found issues",
                {"test_results": all_results}
            )
            
        except Exception as e:
            self.logger.error(f"Testing operations failed: {str(e)}")
            return self.create_response(False, f"Testing operations failed: {str(e)}")
    
    def _validate_syntax(self, files: List[str]) -> Dict[str, Any]:
        """Validate Python syntax"""
        results = {}
        
        for file_path in files:
            try:
                with open(file_path, 'r') as f:
                    code = f.read()
                
                # Try to compile the code
                compile(code, file_path, 'exec')
                results[file_path] = {"syntax_valid": True, "error": None}
                
            except SyntaxError as e:
                results[file_path] = {
                    "syntax_valid": False,
                    "error": f"Syntax error: {str(e)}"
                }
            except Exception as e:
                results[file_path] = {
                    "syntax_valid": False,
                    "error": f"Unexpected error: {str(e)}"
                }
        
        return results
    
    def _run_tests(self) -> Dict[str, Any]:
        """Run unit tests"""
        try:
            # Look for test files
            test_files = self._find_test_files()
            
            if not test_files:
                return {"status": "no_tests", "message": "No test files found"}
            
            # Run pytest
            result = subprocess.run(
                ["python", "-m", "pytest", "-v"] + test_files,
                capture_output=True,
                text=True
            )
            
            return {
                "status": "completed",
                "return_code": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr
            }
            
        except FileNotFoundError:
            return {"status": "pytest_not_found", "message": "pytest not available"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def _find_test_files(self) -> List[str]:
        """Find test files in the project"""
        test_files = []
        
        # Look for common test file patterns
        for root, dirs, files in os.walk("."):
            for file in files:
                if (file.startswith("test_") and file.endswith(".py")) or \
                   (file.endswith("_test.py")):
                    test_files.append(os.path.join(root, file))
        
        return test_files
    
    def _run_integration_tests(self) -> Dict[str, Any]:
        """Run integration tests"""
        try:
            # Look for integration test files
            integration_test_files = []
            for root, dirs, files in os.walk("."):
                for file in files:
                    if file.startswith("integration_test_") and file.endswith(".py"):
                        integration_test_files.append(os.path.join(root, file))
            
            if not integration_test_files:
                return {"status": "no_integration_tests", "message": "No integration tests found"}
            
            # Run integration tests
            result = subprocess.run(
                ["python", "-m", "pytest", "-v"] + integration_test_files,
                capture_output=True,
                text=True
            )
            
            return {
                "status": "completed",
                "return_code": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr
            }
            
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def _evaluate_results(self, results: Dict[str, Any]) -> bool:
        """Evaluate test results and determine overall success"""
        # Check syntax validation
        syntax_results = results.get("syntax_validation", {})
        for file_path, result in syntax_results.items():
            if not result.get("syntax_valid", False):
                return False
        
        # Check unit tests
        unit_tests = results.get("unit_tests", {})
        if unit_tests.get("status") == "completed" and unit_tests.get("return_code") != 0:
            return False
        
        # Check integration tests
        integration_tests = results.get("integration_tests", {})
        if integration_tests.get("status") == "completed" and integration_tests.get("return_code") != 0:
            return False
        
        return True
    
    def generate_test_report(self, results: Dict[str, Any]) -> str:
        """Generate a human-readable test report"""
        report = ["🧪 Testing Report", "=" * 50]
        
        # Syntax validation
        syntax_results = results.get("syntax_validation", {})
        report.append("\n📝 Syntax Validation:")
        for file_path, result in syntax_results.items():
            if result.get("syntax_valid"):
                report.append(f"  ✅ {file_path}")
            else:
                report.append(f"  ❌ {file_path}: {result.get('error', 'Unknown error')}")
        
        # Unit tests
        unit_tests = results.get("unit_tests", {})
        report.append("\n🧪 Unit Tests:")
        if unit_tests.get("status") == "completed":
            if unit_tests.get("return_code") == 0:
                report.append("  ✅ All unit tests passed")
            else:
                report.append("  ❌ Some unit tests failed")
                report.append(f"  Output: {unit_tests.get('stdout', '')}")
        else:
            report.append(f"  ℹ️ {unit_tests.get('message', 'No unit tests')}")
        
        # Integration tests
        integration_tests = results.get("integration_tests", {})
        report.append("\n🔗 Integration Tests:")
        if integration_tests.get("status") == "completed":
            if integration_tests.get("return_code") == 0:
                report.append("  ✅ All integration tests passed")
            else:
                report.append("  ❌ Some integration tests failed")
                report.append(f"  Output: {integration_tests.get('stdout', '')}")
        else:
            report.append(f"  ℹ️ {integration_tests.get('message', 'No integration tests')}")
        
        return "\n".join(report)
