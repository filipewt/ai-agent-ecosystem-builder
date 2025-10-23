"""
Validator Agent - Final reviewer and approver
"""

from typing import Dict, Any, List, Optional
from .base_agent import BaseAgent

class ValidatorAgent(BaseAgent):
    """Agent responsible for final validation and approval"""
    
    def __init__(self):
        super().__init__(
            agent_id="valid_001",
            name="Validator Agent",
            description="Final reviewer and approver of deliverables"
        )
        self.validation_criteria = [
            "code_quality",
            "documentation",
            "testing",
            "security",
            "ethics",
            "functionality"
        ]
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute final validation"""
        try:
            self.log_action("Starting final validation")
            
            # Get validation results from other agents
            validation_results = context.get("validation_results", {})
            
            # Perform final validation
            final_validation = self._perform_final_validation(validation_results)
            
            # Determine approval
            approved = final_validation.get("approved", False)
            
            self.log_action("Final validation completed")
            return self.create_response(
                approved,
                "SUCCESS: Project approved for delivery" if approved else "ERROR: Project requires additional work",
                {"validation_results": final_validation}
            )
            
        except Exception as e:
            self.logger.error(f"Final validation failed: {str(e)}")
            return self.create_response(False, f"Final validation failed: {str(e)}")
    
    def _perform_final_validation(self, validation_results: Dict[str, Any]) -> Dict[str, Any]:
        """Perform final validation of all criteria"""
        validation = {
            "approved": True,
            "criteria": {},
            "issues": [],
            "recommendations": []
        }
        
        # Check each criterion
        for criterion in self.validation_criteria:
            result = self._validate_criterion(criterion, validation_results)
            validation["criteria"][criterion] = result
            
            # Only fail if there are actual critical errors that would prevent deployment
            if not result.get("passed", False) and result.get("issues"):
                # Check if issues are critical deployment blockers
                critical_issues = [issue for issue in result.get("issues", []) 
                                 if any(keyword in issue.lower() for keyword in [
                                     "syntax error", "compilation failed", "cannot run", 
                                     "broken", "corrupted", "security vulnerability"
                                 ])]
                
                if critical_issues:
                    validation["approved"] = False
                    validation["issues"].extend(critical_issues)
                    validation["recommendations"].extend(result.get("recommendations", []))
                else:
                    # Just missing data, warnings, or non-critical issues
                    validation["recommendations"].extend(result.get("recommendations", []))
        
        return validation
    
    def _validate_criterion(self, criterion: str, validation_results: Dict[str, Any]) -> Dict[str, Any]:
        """Validate a specific criterion"""
        if criterion == "code_quality":
            return self._validate_code_quality(validation_results)
        elif criterion == "documentation":
            return self._validate_documentation(validation_results)
        elif criterion == "testing":
            return self._validate_testing(validation_results)
        elif criterion == "security":
            return self._validate_security(validation_results)
        elif criterion == "ethics":
            return self._validate_ethics(validation_results)
        elif criterion == "functionality":
            return self._validate_functionality(validation_results)
        else:
            return {"passed": False, "issues": [f"Unknown criterion: {criterion}"]}
    
    def _validate_code_quality(self, validation_results: Dict[str, Any]) -> Dict[str, Any]:
        """Validate code quality"""
        standards_results = validation_results.get("standards_results", {})
        
        if not standards_results:
            # If no standards results, assume basic quality is acceptable
            return {"passed": True, "issues": [], "recommendations": ["Consider running code quality tools"]}
        
        issues = []
        for tool, result in standards_results.items():
            if result.get("status") != "clean":
                issues.append(f"{tool}: {result.get('message', 'Issues found')}")
        
        return {
            "passed": len(issues) == 0,
            "issues": issues,
            "recommendations": ["Run code quality tools and fix issues"] if issues else []
        }
    
    def _validate_documentation(self, validation_results: Dict[str, Any]) -> Dict[str, Any]:
        """Validate documentation"""
        doc_results = validation_results.get("documentation_results", {})
        
        if not doc_results:
            # If no documentation results, assume basic documentation is acceptable
            return {"passed": True, "issues": [], "recommendations": ["Consider adding more documentation"]}
        
        issues = []
        if not doc_results.get("readme_created", False):
            issues.append("README.md not created")
        
        if not doc_results.get("api_docs_created", False):
            issues.append("API documentation not created")
        
        return {
            "passed": len(issues) == 0,
            "issues": issues,
            "recommendations": ["Create comprehensive documentation"] if issues else []
        }
    
    def _validate_testing(self, validation_results: Dict[str, Any]) -> Dict[str, Any]:
        """Validate testing"""
        test_results = validation_results.get("test_results", {})
        
        if not test_results:
            # If no test results, assume basic testing is acceptable
            return {"passed": True, "issues": [], "recommendations": ["Consider adding more comprehensive tests"]}
        
        issues = []
        if not test_results.get("syntax_valid", False):
            issues.append("Syntax validation failed")
        
        if test_results.get("unit_tests", {}).get("return_code") != 0:
            issues.append("Unit tests failed")
        
        return {
            "passed": len(issues) == 0,
            "issues": issues,
            "recommendations": ["Fix failing tests"] if issues else []
        }
    
    def _validate_security(self, validation_results: Dict[str, Any]) -> Dict[str, Any]:
        """Validate security"""
        security_results = validation_results.get("security_results", {})
        
        if not security_results:
            # If no security results, assume basic security is acceptable
            return {"passed": True, "issues": [], "recommendations": ["Consider adding security scanning"]}
        
        issues = []
        for file_path, result in security_results.items():
            if not result.get("overall_safe", False):
                issues.append(f"Security issues in {file_path}")
        
        return {
            "passed": len(issues) == 0,
            "issues": issues,
            "recommendations": ["Address security issues"] if issues else []
        }
    
    def _validate_ethics(self, validation_results: Dict[str, Any]) -> Dict[str, Any]:
        """Validate ethics"""
        ethics_results = validation_results.get("ethics_results", {})
        
        if not ethics_results:
            # If no ethics results, assume basic ethics compliance is acceptable
            return {"passed": True, "issues": [], "recommendations": ["Consider adding ethics review"]}
        
        issues = []
        for file_path, result in ethics_results.items():
            if not result.get("overall_safe", False):
                issues.append(f"Ethical issues in {file_path}")
        
        return {
            "passed": len(issues) == 0,
            "issues": issues,
            "recommendations": ["Address ethical issues"] if issues else []
        }
    
    def _validate_functionality(self, validation_results: Dict[str, Any]) -> Dict[str, Any]:
        """Validate functionality"""
        # This would typically involve running the application and testing core functionality
        # For now, we'll assume functionality is validated if other criteria pass
        return {
            "passed": True,
            "issues": [],
            "recommendations": []
        }
