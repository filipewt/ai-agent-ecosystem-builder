"""
Base Agent class for all agents in the ecosystem
"""

import os
import json
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from datetime import datetime
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv()

class BaseAgent(ABC):
    """Base class for all agents in the ecosystem"""
    
    def __init__(self, agent_id: str, name: str, description: str):
        self.agent_id = agent_id
        self.name = name
        self.description = description
        self.logger = self._setup_logger()
        self.openai_client = None
        self._initialize_openai()
        
    def _setup_logger(self) -> logging.Logger:
        """Setup logger for the agent"""
        logger = logging.getLogger(f"{self.__class__.__name__}")
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                f'%(asctime)s - {self.name} - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            
        return logger
    
    def _initialize_openai(self):
        """Initialize OpenAI client with API key validation"""
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        self.openai_client = openai.OpenAI(api_key=api_key)
        self.logger.info(f"OpenAI client initialized for {self.name}")
    
    def call_llm(self, messages: List[Dict[str, str]], model: str = "gpt-4o-mini") -> str:
        """Call OpenAI LLM with error handling and retry logic"""
        try:
            response = self.openai_client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.7,
                max_tokens=4000
            )
            return response.choices[0].message.content
        except Exception as e:
            self.logger.error(f"LLM call failed: {str(e)}")
            raise Exception(f"Model {model} unavailable. Please try again later.")
    
    def log_action(self, action: str, details: Optional[Dict[str, Any]] = None):
        """Log agent actions with timestamp"""
        timestamp = datetime.now().isoformat()
        log_entry = {
            "timestamp": timestamp,
            "agent_id": self.agent_id,
            "agent_name": self.name,
            "action": action,
            "details": details or {}
        }
        self.logger.info(f"Action: {action} - {details}")
        return log_entry
    
    @abstractmethod
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the agent's main functionality"""
        pass
    
    def validate_input(self, required_fields: List[str], context: Dict[str, Any]) -> bool:
        """Validate that required fields are present in context"""
        missing_fields = [field for field in required_fields if field not in context]
        if missing_fields:
            self.logger.error(f"Missing required fields: {missing_fields}")
            return False
        return True
    
    def create_response(self, success: bool, message: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Create standardized response format"""
        return {
            "success": success,
            "message": message,
            "data": data or {},
            "agent_id": self.agent_id,
            "timestamp": datetime.now().isoformat()
        }
