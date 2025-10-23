"""
Team Orchestrator Agent - Controls workflows and manages agent coordination
"""

import asyncio
import json
from typing import Dict, Any, List, Optional
from datetime import datetime
from .base_agent import BaseAgent

class OrchestratorAgent(BaseAgent):
    """Orchestrates all agents and manages workflow execution"""
    
    def __init__(self):
        super().__init__(
            agent_id="orch_001",
            name="Team Orchestrator",
            description="Controls workflows, enforces policies, and manages agent coordination"
        )
        self.agents = {}
        self.workflow_state = "initializing"
        self.current_step = 0
        self.workflow_steps = []
        self.paused = False
        self.pause_reason = None
    
    def register_agent(self, agent: BaseAgent):
        """Register an agent with the orchestrator"""
        self.agents[agent.agent_id] = agent
        self.logger.info(f"Registered agent: {agent.name}")
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the orchestrated workflow"""
        try:
            if self.paused:
                return self._handle_pause_resume(context)
            
            self.log_action("Starting workflow execution")
            
            # Phase 0: Environment Setup
            if self.workflow_state == "initializing":
                return self._execute_environment_setup(context)
            
            # Phase 1: Project Definition
            elif self.workflow_state == "definition":
                return self._execute_definition_phase(context)
            
            # Phase 2: Development
            elif self.workflow_state == "development":
                return self._execute_development_phase(context)
            
            # Phase 3: Delivery
            elif self.workflow_state == "delivery":
                return self._execute_delivery_phase(context)
            
            else:
                return self.create_response(False, f"Unknown workflow state: {self.workflow_state}")
                
        except Exception as e:
            self.logger.error(f"Workflow execution failed: {str(e)}")
            return self.create_response(False, f"Workflow execution failed: {str(e)}")
    
    def _execute_environment_setup(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute environment setup phase"""
        self.log_action("Executing environment setup phase")
        
        if "env_agent" not in self.agents:
            return self.create_response(False, "Environment agent not registered")
        
        env_agent = self.agents["env_001"]
        result = env_agent.execute(context)
        
        if result["success"]:
            self.workflow_state = "definition"
            return self.create_response(
                True,
                "⚙️ Environment setup completed. Moving to definition phase.",
                {"next_phase": "definition"}
            )
        else:
            return result
    
    def _execute_definition_phase(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute project definition phase"""
        self.log_action("Executing definition phase")
        
        if "coord_001" not in self.agents:
            return self.create_response(False, "Coordinator agent not registered")
        
        coordinator = self.agents["coord_001"]
        result = coordinator.execute(context)
        
        if result["success"] and result.get("data", {}).get("project_defined", False):
            self.workflow_state = "development"
            return self.create_response(
                True,
                "🧭 Project definition completed. Starting development phase.",
                {"next_phase": "development"}
            )
        else:
            return result
    
    def _execute_development_phase(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute development phase with all agents"""
        self.log_action("Executing development phase")
        
        # Define development workflow steps
        dev_steps = [
            ("arch_001", "Architect Agent", "Designing system architecture"),
            ("core_001", "Core Logic Agent", "Writing Python code"),
            ("backup_001", "Backup Agent", "Creating backups"),
            ("standards_001", "Standards Agent", "Enforcing coding standards"),
            ("test_001", "Testing Agent", "Running tests and validation"),
            ("doc_001", "Documentation Agent", "Updating documentation"),
            ("ethics_001", "Ethics Agent", "Security and ethics review"),
            ("valid_001", "Validator Agent", "Final validation")
        ]
        
        for agent_id, agent_name, description in dev_steps:
            if agent_id not in self.agents:
                continue
                
            self.log_action(f"Executing {agent_name}: {description}")
            agent = self.agents[agent_id]
            result = agent.execute(context)
            
            if not result["success"]:
                return self.create_response(
                    False,
                    f"Development step failed: {agent_name} - {result['message']}"
                )
        
        self.workflow_state = "delivery"
        return self.create_response(
            True,
            "🧠 Development phase completed. Moving to delivery phase.",
            {"next_phase": "delivery"}
        )
    
    def _execute_delivery_phase(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute delivery phase"""
        self.log_action("Executing delivery phase")
        
        if "repo_001" not in self.agents:
            return self.create_response(False, "Repository agent not registered")
        
        repo_agent = self.agents["repo_001"]
        result = repo_agent.execute(context)
        
        if result["success"]:
            self.workflow_state = "completed"
            return self.create_response(
                True,
                "🚀 Project delivery completed successfully!",
                {"project_completed": True}
            )
        else:
            return result
    
    def pause_workflow(self, reason: str):
        """Pause the workflow"""
        self.paused = True
        self.pause_reason = reason
        self.log_action(f"Workflow paused: {reason}")
    
    def resume_workflow(self):
        """Resume the workflow"""
        self.paused = False
        self.pause_reason = None
        self.log_action("Workflow resumed")
    
    def _handle_pause_resume(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle pause/resume logic"""
        if context.get("user_input") == "Try again":
            self.resume_workflow()
            return self.create_response(
                True,
                "Workflow resumed. Continuing from last step.",
                {"resumed": True}
            )
        else:
            return self.create_response(
                False,
                f"⏸️ Workflow paused: {self.pause_reason}. Type 'Try again' to resume.",
                {"paused": True, "reason": self.pause_reason}
            )
    
    def get_workflow_status(self) -> Dict[str, Any]:
        """Get current workflow status"""
        return {
            "workflow_state": self.workflow_state,
            "paused": self.paused,
            "pause_reason": self.pause_reason,
            "current_step": self.current_step,
            "total_steps": len(self.workflow_steps),
            "registered_agents": list(self.agents.keys())
        }
    
    def handle_model_unavailable(self, model: str) -> Dict[str, Any]:
        """Handle model unavailability"""
        self.pause_workflow(f"Model {model} unavailable")
        return self.create_response(
            False,
            f"⏸️ Model {model} is unavailable.\nNo fallback will be used to maintain cost control.\nType 'Try again' once you want to resume.",
            {"model_unavailable": True, "model": model}
        )
