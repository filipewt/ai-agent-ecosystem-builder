"""
Product Coordinator Agent - Handles human interaction and project definition
"""

from typing import Dict, Any, List, Optional
from .base_agent import BaseAgent

class CoordinatorAgent(BaseAgent):
    """Agent responsible for human interaction and project definition"""
    
    def __init__(self):
        super().__init__(
            agent_id="coord_001",
            name="Product Coordinator",
            description="Converses with human, defines scope, and clarifies goals"
        )
        self.project_requirements = {}
        self.conversation_history = []
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute coordinator functionality"""
        try:
            user_input = context.get("user_input", "")
            
            if not user_input:
                return self._start_conversation()
            
            # Add user input to conversation history
            self.conversation_history.append({"role": "user", "content": user_input})
            
            # Analyze user input and respond
            response = self._analyze_and_respond(user_input, context)
            
            # Add response to conversation history
            self.conversation_history.append({"role": "assistant", "content": response})
            
            return self.create_response(
                True,
                response,
                {"conversation_updated": True}
            )
            
        except Exception as e:
            self.logger.error(f"Coordinator execution failed: {str(e)}")
            return self.create_response(False, f"Coordinator failed: {str(e)}")
    
    def _start_conversation(self) -> Dict[str, Any]:
        """Start the initial conversation"""
        welcome_message = """🧭 Product Coordinator: Hello! I'm here to help you define your Python project.

Let's start by understanding what you want to build:

1. What type of Python application do you need?
2. What are the main features and functionality?
3. Any specific requirements or constraints?
4. What's the target audience or use case?

Please describe your project in detail, and I'll help clarify the scope and suggest improvements."""
        
        return self.create_response(
            True,
            welcome_message,
            {"conversation_started": True}
        )
    
    def _analyze_and_respond(self, user_input: str, context: Dict[str, Any]) -> str:
        """Analyze user input and generate appropriate response"""
        try:
            # Use LLM to analyze and respond
            messages = [
                {
                    "role": "system",
                    "content": """You are a Product Coordinator for a Python development project. Your role is to:
1. Understand the user's requirements
2. Ask clarifying questions
3. Suggest improvements
4. Define clear project scope
5. Wait for explicit "Start development" command before proceeding

Be conversational, helpful, and thorough in understanding requirements."""
                },
                {
                    "role": "user",
                    "content": user_input
                }
            ]
            
            # Add conversation history for context
            for msg in self.conversation_history[-6:]:  # Last 6 messages for context
                messages.insert(-1, msg)
            
            response = self.call_llm(messages)
            
            # Check if user wants to start development
            if "start development" in user_input.lower() or "begin development" in user_input.lower():
                return self._finalize_project_definition(response)
            
            return response
            
        except Exception as e:
            self.logger.error(f"LLM analysis failed: {str(e)}")
            return f"I apologize, but I encountered an issue processing your request. Please try again."
    
    def _finalize_project_definition(self, response: str) -> str:
        """Finalize project definition and prepare for development"""
        self.log_action("Project definition finalized")
        
        final_message = f"""🧭 Product Coordinator: {response}

✅ Project scope confirmed and ready for development!

The development team will now:
1. Design the system architecture
2. Write the Python code
3. Implement testing and validation
4. Create documentation
5. Set up version control

Starting development phase now..."""
        
        return final_message
    
    def get_project_requirements(self) -> Dict[str, Any]:
        """Get current project requirements"""
        return {
            "requirements": self.project_requirements,
            "conversation_length": len(self.conversation_history),
            "project_defined": len(self.project_requirements) > 0
        }
    
    def update_requirements(self, key: str, value: Any):
        """Update project requirements"""
        self.project_requirements[key] = value
        self.log_action(f"Updated requirement: {key}")
    
    def clear_conversation(self):
        """Clear conversation history"""
        self.conversation_history = []
        self.log_action("Conversation history cleared")
