"""
Ethics & Security Agent - Checks for unsafe or unethical operations
"""

import re
from typing import Dict, Any, List, Optional
from .base_agent import BaseAgent

class EthicsAgent(BaseAgent):
    """Agent responsible for ethics and security review"""
    
    def __init__(self):
        super().__init__(
            agent_id="ethics_001",
            name="Ethics & Security Agent",
            description="Checks for unsafe or unethical operations"
        )
        self.security_patterns = [
            r"eval\(",
            r"exec\(",
            r"__import__\(",
            r"subprocess\.",
            r"os\.system\(",
            r"shell=True",
            r"pickle\.loads\(",
            r"marshal\.loads\(",
            r"compile\(",
            r"input\(",
            r"raw_input\("
        ]
        self.ethical_concerns = [
            "discrimination",
            "bias",
            "harmful",
            "dangerous",
            "illegal",
            "unethical"
        ]
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute ethics and security review"""
        try:
            self.log_action("Starting ethics and security review")
            
            # Get files to review
            files_to_review = context.get("generated_files", [])
            if not files_to_review:
                return self.create_response(
                    False,
                    "No files provided for ethics review"
                )
            
            # Review each file
            review_results = {}
            for file_path in files_to_review:
                result = self._review_file(file_path)
                review_results[file_path] = result
            
            # Determine overall safety
            overall_safe = all(
                result.get("security_issues", []) == [] and 
                result.get("ethical_issues", []) == []
                for result in review_results.values()
            )
            
            self.log_action("Ethics and security review completed")
            return self.create_response(
                overall_safe,
                "🔒 Security and ethics review passed" if overall_safe else "🔒 Security and ethics issues found",
                {"review_results": review_results}
            )
            
        except Exception as e:
            self.logger.error(f"Ethics review failed: {str(e)}")
            return self.create_response(False, f"Ethics review failed: {str(e)}")
    
    def _review_file(self, file_path: str) -> Dict[str, Any]:
        """Review a single file for security and ethical issues"""
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            
            # Check for security issues
            security_issues = self._check_security_issues(content)
            
            # Check for ethical issues
            ethical_issues = self._check_ethical_issues(content)
            
            return {
                "security_issues": security_issues,
                "ethical_issues": ethical_issues,
                "overall_safe": len(security_issues) == 0 and len(ethical_issues) == 0
            }
            
        except Exception as e:
            return {
                "security_issues": [],
                "ethical_issues": [],
                "error": str(e),
                "overall_safe": False
            }
    
    def _check_security_issues(self, content: str) -> List[str]:
        """Check for security issues in code"""
        issues = []
        
        for pattern in self.security_patterns:
            matches = re.findall(pattern, content)
            if matches:
                issues.append(f"Potential security risk: {pattern} found {len(matches)} times")
        
        return issues
    
    def _check_ethical_issues(self, content: str) -> List[str]:
        """Check for ethical issues in code"""
        issues = []
        
        content_lower = content.lower()
        for concern in self.ethical_concerns:
            if concern in content_lower:
                issues.append(f"Potential ethical concern: {concern}")
        
        return issues
