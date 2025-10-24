"""
Core Logic Agent - Writes Python code according to architecture
"""

import os
import json
from typing import Dict, Any, List, Optional
from .base_agent import BaseAgent

class CoreLogicAgent(BaseAgent):
    """Agent responsible for writing Python code"""
    
    def __init__(self):
        super().__init__(
            agent_id="core_001",
            name="Core Logic Agent",
            description="Writes Python code according to architecture specifications"
        )
        self.generated_files = []
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute code generation"""
        try:
            self.log_action("Starting code generation")
            
            # Store context for use in other methods
            self.context = context
            
            # Load architecture
            architecture = self._load_architecture()
            if not architecture:
                return self.create_response(
                    False,
                    "No architecture found. Cannot generate code."
                )
            
            # Generate code for each module
            generated_files = []
            for module in architecture.get("modules", []):
                file_path = self._generate_module_code(module)
                if file_path:
                    generated_files.append(file_path)
            
            # Create main application file
            main_file = self._create_main_application()
            if main_file:
                generated_files.append(main_file)
            
            # Create a default calculator GUI if this is a GUI application
            project_description = context.get("project_description", "").lower()
            if any(keyword in project_description for keyword in 
                   ['gui', 'interface', 'window', 'calculator', 'desktop', 'tkinter', 'pyqt', 'kivy']):
                calculator_gui = self._create_default_calculator_gui()
                if calculator_gui:
                    generated_files.append(calculator_gui)
            
            self.generated_files = generated_files
            self.log_action("Code generation completed")
            
            return self.create_response(
                True,
                "🧠 Core logic written successfully",
                {"generated_files": generated_files}
            )
            
        except Exception as e:
            self.logger.error(f"Code generation failed: {str(e)}")
            return self.create_response(False, f"Code generation failed: {str(e)}")
    
    def _load_architecture(self) -> Optional[Dict[str, Any]]:
        """Load architecture from file"""
        try:
            with open("project_docs/architecture.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            self.logger.error("Architecture file not found")
            return None
        except json.JSONDecodeError as e:
            self.logger.error(f"Invalid architecture file: {e}")
            return None
    
    def _generate_module_code(self, module: Dict[str, Any]) -> Optional[str]:
        """Generate code for a specific module"""
        try:
            module_name = module.get("name", "unknown_module")
            file_path = f"src/{module_name.lower().replace(' ', '_')}.py"
            
            # Create src directory if it doesn't exist
            os.makedirs("src", exist_ok=True)
            
            # Generate code using LLM
            code = self._generate_code_with_llm(module)
            
            # Write code to file
            with open(file_path, "w") as f:
                f.write(code)
            
            self.logger.info(f"Generated code for {module_name}: {file_path}")
            return file_path
            
        except Exception as e:
            self.logger.error(f"Failed to generate code for module {module.get('name', 'unknown')}: {str(e)}")
            return None
    
    def _create_main_application(self) -> str:
        """Create a main application file that ties everything together"""
        try:
            # Get project context to determine what type of application to create
            project_name = getattr(self, 'context', {}).get('project_name', 'ai_generated_app')
            project_description = getattr(self, 'context', {}).get('project_description', 'A Python application')
            
            # Determine if this should be a GUI application
            is_gui_app = any(keyword in project_description.lower() for keyword in 
                           ['gui', 'interface', 'window', 'calculator', 'desktop', 'tkinter', 'pyqt', 'kivy'])
            
            if is_gui_app:
                main_code = self._create_gui_application(project_name, project_description)
            else:
                main_code = self._create_console_application(project_name, project_description)
            
            main_path = "src/main.py"
            with open(main_path, "w") as f:
                f.write(main_code)
            
            self.logger.info(f"Created main application file: {main_path}")
            return main_path
            
        except Exception as e:
            self.logger.error(f"Failed to create main application: {str(e)}")
            return None
    
    def _create_gui_application(self, project_name: str, project_description: str) -> str:
        """Create a GUI application main file"""
        return f'''"""
{project_name} - GUI Application
Auto-generated by AI Agent Ecosystem Builder
Description: {project_description}
"""

import sys
import os
import logging
from datetime import datetime
from pathlib import Path

# Add current directory to path for imports
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

def setup_logging():
    """Setup logging configuration"""
    # Create logs directory if it doesn't exist
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    
    # Create timestamped log file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = logs_dir / f"application_{{timestamp}}.log"
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    logger = logging.getLogger(__name__)
    logger.info(f"Logging initialized. Log file: {{log_file}}")
    return logger

def main():
    """Main application function"""
    # Setup logging
    logger = setup_logging()
    
    logger.info("ROCKET: Starting {project_name} GUI application")
    logger.info("=" * 50)
    
    try:
        # Import and run the GUI application
        from {project_name.lower().replace(' ', '_')}_gui import {project_name.replace(' ', '')}App
        
        logger.info("FOLDER: GUI application modules loaded successfully")
        logger.info("TOOLS: Starting GUI application...")
        
        # Create and run the GUI application
        app = {project_name.replace(' ', '')}App()
        app.run()
        
        logger.info("SUCCESS: GUI application completed successfully")
        
    except ImportError as e:
        logger.error(f"ERROR: Failed to import GUI application: {{e}}")
        logger.info("TOOLS: Creating a basic calculator GUI as fallback...")
        
        # Fallback to a basic calculator GUI
        from calculator_gui import CalculatorApp
        app = CalculatorApp()
        app.run()
        
    except Exception as e:
        logger.error(f"ERROR: Error running GUI application: {{e}}")
        logger.exception("Full traceback:")
        return 1
    
    logger.info("SUCCESS: GUI application completed successfully")
    return 0

if __name__ == "__main__":
    sys.exit(main())
'''
    
    def _create_console_application(self, project_name: str, project_description: str) -> str:
        """Create a console application main file"""
        return f'''"""
{project_name} - Console Application
Auto-generated by AI Agent Ecosystem Builder
Description: {project_description}
"""

import sys
import os
import logging
from datetime import datetime
from pathlib import Path

# Add current directory to path for imports
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

def setup_logging():
    """Setup logging configuration"""
    # Create logs directory if it doesn't exist
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    
    # Create timestamped log file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = logs_dir / f"application_{{timestamp}}.log"
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    logger = logging.getLogger(__name__)
    logger.info(f"Logging initialized. Log file: {{log_file}}")
    return logger

def main():
    """Main application function"""
    # Setup logging
    logger = setup_logging()
    
    logger.info("ROCKET: Starting {project_name} console application")
    logger.info("=" * 50)
    
    try:
        # Import and run your application modules here
        logger.info("FOLDER: Application modules loaded successfully")
        logger.info("TOOLS: Running console application...")
        
        # Example console application logic
        print(f"Welcome to {{project_name}}!")
        print(f"Description: {{project_description}}")
        
        # Add your application logic here
        logger.info("SUCCESS: Console application ready to use!")
        
    except Exception as e:
        logger.error(f"ERROR: Error running console application: {{e}}")
        logger.exception("Full traceback:")
        return 1
    
    logger.info("SUCCESS: Console application completed successfully")
    return 0

if __name__ == "__main__":
    sys.exit(main())
'''
    
    def _create_default_calculator_gui(self) -> str:
        """Create a default calculator GUI as fallback"""
        try:
            calculator_code = '''"""
Calculator GUI Application
Auto-generated by AI Agent Ecosystem Builder
"""

import tkinter as tk
from tkinter import ttk
import logging

class CalculatorApp:
    """Simple Calculator GUI Application"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.info("Initializing Calculator GUI...")
        
        # Create main window
        self.root = tk.Tk()
        self.root.title("Calculator")
        self.root.geometry("300x400")
        self.root.resizable(False, False)
        
        # Calculator state
        self.current = "0"
        self.total = 0
        self.input_value = 0
        self.operator = ""
        self.result = False
        
        # Create GUI
        self.create_widgets()
        
        self.logger.info("Calculator GUI initialized successfully")
    
    def create_widgets(self):
        """Create the calculator GUI widgets"""
        self.logger.info("Creating calculator widgets...")
        
        # Display frame
        display_frame = ttk.Frame(self.root)
        display_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Display entry
        self.display_var = tk.StringVar()
        self.display_var.set("0")
        self.display = ttk.Entry(
            display_frame, 
            textvariable=self.display_var, 
            font=("Arial", 16), 
            justify="right",
            state="readonly"
        )
        self.display.pack(fill=tk.X)
        
        # Button frame
        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Button layout
        buttons = [
            ("C", 0, 0), ("±", 0, 1), ("%", 0, 2), ("÷", 0, 3),
            ("7", 1, 0), ("8", 1, 1), ("9", 1, 2), ("×", 1, 3),
            ("4", 2, 0), ("5", 2, 1), ("6", 2, 2), ("-", 2, 3),
            ("1", 3, 0), ("2", 3, 1), ("3", 3, 2), ("+", 3, 3),
            ("0", 4, 0), (".", 4, 1), ("=", 4, 2)
        ]
        
        # Configure grid weights
        for i in range(5):
            button_frame.grid_rowconfigure(i, weight=1)
        for i in range(4):
            button_frame.grid_columnconfigure(i, weight=1)
        
        # Create buttons
        for (text, row, col) in buttons:
            if text == "0":
                btn = ttk.Button(button_frame, text=text, command=lambda t=text: self.button_click(t))
                btn.grid(row=row, column=col, columnspan=2, sticky="nsew", padx=2, pady=2)
            else:
                btn = ttk.Button(button_frame, text=text, command=lambda t=text: self.button_click(t))
                btn.grid(row=row, column=col, sticky="nsew", padx=2, pady=2)
        
        self.logger.info("Calculator widgets created successfully")
    
    def button_click(self, value):
        """Handle button clicks"""
        self.logger.info(f"Button clicked: {value}")
        
        if value.isdigit():
            self.number_click(value)
        elif value == ".":
            self.decimal_click()
        elif value in ["+", "-", "×", "÷"]:
            self.operator_click(value)
        elif value == "=":
            self.equals_click()
        elif value == "C":
            self.clear_click()
        elif value == "±":
            self.plus_minus_click()
        elif value == "%":
            self.percent_click()
    
    def number_click(self, number):
        """Handle number button clicks"""
        if self.result:
            self.current = "0"
            self.result = False
        
        if self.current == "0":
            self.current = number
        else:
            self.current += number
        
        self.display_var.set(self.current)
    
    def decimal_click(self):
        """Handle decimal point clicks"""
        if self.result:
            self.current = "0"
            self.result = False
        
        if "." not in self.current:
            self.current += "."
            self.display_var.set(self.current)
    
    def operator_click(self, op):
        """Handle operator button clicks"""
        if self.operator and not self.result:
            self.equals_click()
        
        self.input_value = float(self.current)
        self.operator = op
        self.result = True
    
    def equals_click(self):
        """Handle equals button clicks"""
        if self.operator:
            try:
                current_value = float(self.current)
                
                if self.operator == "+":
                    result = self.input_value + current_value
                elif self.operator == "-":
                    result = self.input_value - current_value
                elif self.operator == "×":
                    result = self.input_value * current_value
                elif self.operator == "÷":
                    if current_value == 0:
                        self.display_var.set("Error")
                        self.logger.error("Division by zero attempted")
                        return
                    result = self.input_value / current_value
                
                self.current = str(result)
                self.display_var.set(self.current)
                self.operator = ""
                self.result = True
                
                self.logger.info(f"Calculation result: {result}")
                
            except Exception as e:
                self.display_var.set("Error")
                self.logger.error(f"Calculation error: {e}")
    
    def clear_click(self):
        """Handle clear button clicks"""
        self.current = "0"
        self.total = 0
        self.input_value = 0
        self.operator = ""
        self.result = False
        self.display_var.set("0")
        self.logger.info("Calculator cleared")
    
    def plus_minus_click(self):
        """Handle plus/minus button clicks"""
        if self.current != "0":
            if self.current.startswith("-"):
                self.current = self.current[1:]
            else:
                self.current = "-" + self.current
            self.display_var.set(self.current)
    
    def percent_click(self):
        """Handle percent button clicks"""
        try:
            value = float(self.current)
            result = value / 100
            self.current = str(result)
            self.display_var.set(self.current)
            self.logger.info(f"Percent calculation: {value}% = {result}")
        except Exception as e:
            self.logger.error(f"Percent calculation error: {e}")
    
    def run(self):
        """Run the calculator application"""
        self.logger.info("Starting calculator application...")
        try:
            self.root.mainloop()
            self.logger.info("Calculator application closed")
        except Exception as e:
            self.logger.error(f"Error running calculator: {e}")
            raise
'''
            
            calculator_path = "src/calculator_gui.py"
            with open(calculator_path, "w") as f:
                f.write(calculator_code)
            
            self.logger.info(f"Created default calculator GUI: {calculator_path}")
            return calculator_path
            
        except Exception as e:
            self.logger.error(f"Failed to create default calculator GUI: {str(e)}")
            return None
    
    def _generate_code_with_llm(self, module: Dict[str, Any]) -> str:
        """Generate code using LLM"""
        try:
            messages = [
                {
                    "role": "system",
                    "content": """You are a Python developer. Generate clean, well-structured Python code based on the module specification. Follow these guidelines:

1. Use proper Python conventions (PEP 8)
2. Include comprehensive docstrings
3. Add type hints
4. Include error handling
5. Write clean, readable code
6. Include example usage if applicable

Return only the Python code, no explanations."""
                },
                {
                    "role": "user",
                    "content": f"Generate Python code for module: {json.dumps(module, indent=2)}"
                }
            ]
            
            response = self.call_llm(messages)
            
            # Clean up response to ensure it's valid Python
            code = self._clean_code_response(response)
            return code
            
        except Exception as e:
            self.logger.error(f"LLM code generation failed: {str(e)}")
            raise
    
    def _clean_code_response(self, response: str) -> str:
        """Clean up LLM response to ensure valid Python"""
        lines = response.split('\n')
        cleaned_lines = []
        
        # Remove markdown code blocks if present
        in_code_block = False
        for line in lines:
            if line.strip().startswith('```'):
                in_code_block = not in_code_block
                continue
            if not in_code_block and line.strip():
                cleaned_lines.append(line)
        
        return '\n'.join(cleaned_lines)
    
    def get_generated_files(self) -> List[str]:
        """Get list of generated files"""
        return self.generated_files
    
    def validate_generated_code(self) -> Dict[str, Any]:
        """Validate generated code"""
        validation_results = {}
        
        for file_path in self.generated_files:
            try:
                # Basic syntax validation
                with open(file_path, 'r') as f:
                    code = f.read()
                
                # Try to compile the code
                compile(code, file_path, 'exec')
                validation_results[file_path] = {"syntax_valid": True}
                
            except SyntaxError as e:
                validation_results[file_path] = {
                    "syntax_valid": False,
                    "error": str(e)
                }
            except Exception as e:
                validation_results[file_path] = {
                    "syntax_valid": False,
                    "error": f"Unexpected error: {str(e)}"
                }
        
        return validation_results
