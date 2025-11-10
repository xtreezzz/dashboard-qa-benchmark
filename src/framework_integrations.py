"""
Framework integrations for PandasAI, Sketch, and LangChain Pandas Agent.
"""
import pandas as pd
from typing import Dict, Any, Optional
import os
import warnings

warnings.filterwarnings('ignore')


class FrameworkResult:
    """Container for framework results."""
    
    def __init__(self, answer: str, reasoning: str, error: Optional[str] = None, 
                 logs: Optional[str] = None, reproduction_code: Optional[str] = None):
        self.answer = answer
        self.reasoning = reasoning
        self.error = error
        self.logs = logs or ""
        self.reproduction_code = reproduction_code or ""
        self.comparison = None  # Will be set during evaluation
        
    def to_dict(self) -> Dict[str, Any]:
        result_dict = {
            "answer": self.answer,
            "reasoning": self.reasoning,
            "error": self.error or "",
            "logs": self.logs,
            "reproduction_code": self.reproduction_code
        }
        
        # Include comparison result if available
        if self.comparison is not None:
            result_dict["comparison"] = self.comparison
        
        return result_dict


class PandasAIWrapper:
    """Wrapper for PandasAI framework using LiteLLM."""
    
    def __init__(self, api_key: Optional[str] = None):
        try:
            from pandasai import Agent
            from pandasai_litellm.litellm import LiteLLM
            
            self.api_key = api_key or os.getenv('OPENAI_API_KEY')
            if not self.api_key:
                raise ValueError("OpenAI API key required for PandasAI")
            
            # Initialize LiteLLM with OpenAI
            # Default model, can be overridden via environment variable
            model = os.getenv('BENCHMARK_MODEL', 'gpt-5-mini')
            self.llm = LiteLLM(model=model, api_key=self.api_key)
            self.model_name = model
            self.Agent = Agent
            self.available = True
        except ImportError as e:
            self.available = False
            self.error = f"PandasAI or LiteLLM not available: {str(e)}"
        except Exception as e:
            self.available = False
            self.error = f"PandasAI initialization error: {str(e)}"
    
    def query(self, df: pd.DataFrame, question: str) -> FrameworkResult:
        """Query the dataframe using PandasAI."""
        if not self.available:
            return FrameworkResult("", "", error=self.error)
        
        import io
        import sys
        from datetime import datetime
        
        # Capture logs
        log_buffer = io.StringIO()
        original_stdout = sys.stdout
        original_stderr = sys.stderr
        
        try:
            # Redirect stdout/stderr to capture logs
            sys.stdout = log_buffer
            sys.stderr = log_buffer
            
            log_buffer.write(f"[{datetime.now().isoformat()}] Starting PandasAI query\n")
            log_buffer.write(f"Question: {question}\n")
            log_buffer.write(f"DataFrame shape: {df.shape}\n")
            log_buffer.write("="*80 + "\n")
            
            # Create agent with custom OpenAI LLM (with verbose=True for logs)
            agent = self.Agent(df, config={"llm": self.llm, "verbose": True, "enable_cache": False})
            response = agent.chat(question)
            
            # Restore stdout/stderr
            sys.stdout = original_stdout
            sys.stderr = original_stderr
            
            # PandasAI returns the answer directly
            answer = str(response) if response is not None else ""
            reasoning = "PandasAI processed the query and returned the result"
            
            # Get logs
            logs = log_buffer.getvalue()
            log_buffer.write(f"\nAnswer: {answer}\n")
            log_buffer.write(f"[{datetime.now().isoformat()}] Completed successfully\n")
            logs = log_buffer.getvalue()
            
            # Generate reproduction code
            reproduction_code = self._generate_reproduction_code(df, question)
            
            return FrameworkResult(answer, reasoning, logs=logs, reproduction_code=reproduction_code)
        except Exception as e:
            # Restore stdout/stderr
            sys.stdout = original_stdout
            sys.stderr = original_stderr
            
            logs = log_buffer.getvalue()
            logs += f"\n[ERROR] {str(e)}\n"
            return FrameworkResult("", "", error=f"PandasAI error: {str(e)}", logs=logs)
    
    def _generate_reproduction_code(self, df: pd.DataFrame, question: str) -> str:
        """Generate Python code to reproduce this query."""
        df_csv = df.head(10).to_csv(index=False)
        code = f'''"""Reproduce PandasAI Query"""
import pandas as pd
import os
from pandasai import Agent
from pandasai_litellm.litellm import LiteLLM

# Sample data (first 10 rows)
data_csv = """\n{df_csv}"""

df = pd.read_csv(pd.io.common.StringIO(data_csv))

# Initialize PandasAI with LiteLLM
api_key = os.getenv("OPENAI_API_KEY")
llm = LiteLLM(model="gpt-5-mini", api_key=api_key)

# Create agent and query
agent = Agent(df, config={{"llm": llm, "verbose": True, "enable_cache": False}})
question = """{question}"""
response = agent.chat(question)

print(f"Answer: {{response}}")
'''
        return code


class RealSketchWrapper:
    """Wrapper for real Sketch library using Chat API via backend wrapper."""
    
    def __init__(self, api_key: Optional[str] = None):
        try:
            import certifi
            import ssl
            import json
            from urllib import request
            from lambdaprompt import backends
            
            # Fix SSL certificate verification
            os.environ['SSL_CERT_FILE'] = certifi.where()
            
            self.api_key = api_key or os.getenv('OPENAI_API_KEY')
            if not self.api_key:
                raise ValueError("OpenAI API key required for Sketch")
            
            # Create wrapper class that converts Completion API → Chat API
            class CompletionToChatWrapper(backends.OpenAICompletion):
                def __init__(self, openai_api_key=None, **param_override):
                    self.openai_api_key = openai_api_key or os.getenv('OPENAI_API_KEY')
                    self.param_override = param_override
                    self.param_override['model'] = 'gpt-5-mini'
                    # Remove temperature for gpt-5 models
                    self.param_override.pop('temperature', None)
                
                async def __call__(self, prompt, **kwargs):
                    # Prepare request for Chat Completions API
                    messages = [{"role": "user", "content": prompt}]
                    payload = {
                        "model": "gpt-5-mini",
                        "messages": messages
                    }
                    
                    # Make request to OpenAI Chat API
                    url = "https://api.openai.com/v1/chat/completions"
                    headers = {
                        "Authorization": f"Bearer {self.openai_api_key}",
                        "Content-Type": "application/json"
                    }
                    
                    req = request.Request(
                        url,
                        data=json.dumps(payload).encode('utf-8'),
                        headers=headers,
                        method='POST'
                    )
                    
                    # Use certifi SSL context
                    ssl_context = ssl.create_default_context(cafile=certifi.where())
                    
                    with request.urlopen(req, context=ssl_context) as response:
                        result = json.loads(response.read().decode('utf-8'))
                    
                    # Convert Chat API response to Completion API format
                    completion_response = {
                        'choices': [{
                            'text': result['choices'][0]['message']['content']
                        }],
                        'model': 'gpt-5-mini',
                        'object': 'text_completion'
                    }
                    
                    return completion_response
            
            # Replace backend before importing sketch
            backends.OpenAICompletion = CompletionToChatWrapper
            
            # Now import sketch with our custom backend
            import sketch
            
            self.sketch = sketch
            self.available = True
            self.model_name = 'gpt-5-mini'
            
        except ImportError as e:
            self.available = False
            self.error = f"Sketch or dependencies not available: {str(e)}"
        except Exception as e:
            self.available = False
            self.error = f"Sketch initialization error: {str(e)}"
    
    def query(self, df: pd.DataFrame, question: str) -> FrameworkResult:
        """Query the dataframe using real Sketch library."""
        if not self.available:
            return FrameworkResult("", "", error=self.error)
        
        from datetime import datetime
        logs = []
        
        try:
            logs.append(f"[{datetime.now().isoformat()}] Starting Real Sketch query")
            logs.append(f"Question: {question}")
            logs.append(f"DataFrame shape: {df.shape}")
            logs.append("="*80)
            
            # Use sketch's pandas extension
            logs.append("\nCalling df.sketch.ask()...")
            result = df.sketch.ask(question, call_display=False)
            
            # Extract answer from result
            if isinstance(result, dict):
                # Result from wrapper - extract text from choices
                answer_text = result.get('choices', [{}])[0].get('text', '')
            else:
                answer_text = str(result)
            
            # Clean up markdown code blocks if present
            answer = answer_text.strip()
            if answer.startswith('```') and answer.endswith('```'):
                lines = answer.split('\n')
                # Remove first and last lines (``` markers)
                answer = '\n'.join(lines[1:-1]).strip()
            
            reasoning = "Real Sketch library with gpt-5-mini via Chat API wrapper"
            
            logs.append(f"\nRaw result: {result}")
            logs.append(f"\nParsed answer: {answer}")
            logs.append(f"[{datetime.now().isoformat()}] Completed successfully")
            
            # Generate reproduction code
            reproduction_code = self._generate_reproduction_code(df, question)
            
            return FrameworkResult(answer, reasoning, logs="\n".join(logs), reproduction_code=reproduction_code)
        except Exception as e:
            logs.append(f"\n[ERROR] {str(e)}")
            import traceback
            logs.append(traceback.format_exc())
            return FrameworkResult("", "", error=f"Sketch error: {str(e)}", logs="\n".join(logs))
    
    def _generate_reproduction_code(self, df: pd.DataFrame, question: str) -> str:
        """Generate Python code to reproduce this query."""
        df_csv = df.head(10).to_csv(index=False)
        code = f'''"""Reproduce Real Sketch Query"""
import pandas as pd
import os
import certifi
import ssl
import json
from urllib import request
from lambdaprompt import backends

# Fix SSL certificate verification
os.environ['SSLL_CERT_FILE'] = certifi.where()

# Sample data (first 10 rows)
data_csv = """\n{df_csv}"""

df = pd.read_csv(pd.io.common.StringIO(data_csv))

# Create Chat API wrapper
class CompletionToChatWrapper(backends.OpenAICompletion):
    def __init__(self, openai_api_key=None, **param_override):
        self.openai_api_key = openai_api_key or os.getenv('OPENAI_API_KEY')
        self.param_override = param_override
        self.param_override['model'] = 'gpt-5-mini'
        self.param_override.pop('temperature', None)
    
    async def __call__(self, prompt, **kwargs):
        messages = [{{"role": "user", "content": prompt}}]
        payload = {{"model": "gpt-5-mini", "messages": messages}}
        
        url = "https://api.openai.com/v1/chat/completions"
        headers = {{
            "Authorization": f"Bearer {{self.openai_api_key}}",
            "Content-Type": "application/json"
        }}
        
        req = request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers, method='POST')
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        
        with request.urlopen(req, context=ssl_context) as response:
            result = json.loads(response.read().decode('utf-8'))
        
        return {{
            'choices': [{{'text': result['choices'][0]['message']['content']}}],
            'model': 'gpt-5-mini',
            'object': 'text_completion'
        }}

# Replace backend and import sketch
backends.OpenAICompletion = CompletionToChatWrapper
import sketch

# Query using sketch
question = """{question}"""
result = df.sketch.ask(question, call_display=False)

print(f"Answer: {{result}}")
'''
        return code


# Alias for backward compatibility
SketchWrapper = RealSketchWrapper


class LangChainPandasWrapper:
    """Wrapper for LangChain Pandas Agent using modern API."""
    
    def __init__(self, api_key: Optional[str] = None):
        try:
            from langchain_openai import ChatOpenAI
            from langgraph.prebuilt import create_react_agent
            from langchain_core.tools import tool
            
            self.api_key = api_key or os.getenv('OPENAI_API_KEY')
            if not self.api_key:
                raise ValueError("OpenAI API key required for LangChain")
            
            # Set API key in environment
            os.environ['OPENAI_API_KEY'] = self.api_key
            
            # Use model from environment or default
            model = os.getenv('BENCHMARK_MODEL', 'gpt-5-mini')
            
            # gpt-5 models don't support temperature parameter
            llm_params = {"model": model, "api_key": self.api_key}
            if not model.startswith('gpt-5'):
                llm_params["temperature"] = 0
            
            self.llm = ChatOpenAI(**llm_params)
            self.model_name = model
            self.available = True
            
            # Store modules for later use
            self.create_react_agent = create_react_agent
            self.tool_decorator = tool
            
        except ImportError as e:
            self.available = False
            self.error = f"LangChain not available: {str(e)}"
        except Exception as e:
            self.available = False
            self.error = f"LangChain initialization error: {str(e)}"
    
    def query(self, df: pd.DataFrame, question: str) -> FrameworkResult:
        """Query the dataframe using LangChain with Python REPL tool."""
        if not self.available:
            return FrameworkResult("", "", error=self.error)
        
        import io
        import sys
        from datetime import datetime
        
        # Capture logs
        log_buffer = io.StringIO()
        original_stdout = sys.stdout
        original_stderr = sys.stderr
        
        try:
            log_buffer.write(f"[{datetime.now().isoformat()}] Starting LangChain query\n")
            log_buffer.write(f"Question: {question}\n")
            log_buffer.write(f"DataFrame shape: {df.shape}\n")
            log_buffer.write(f"Columns: {list(df.columns)}\n")
            log_buffer.write("="*80 + "\n")
            
            # Create Python tool with access to dataframe using decorator
            @self.tool_decorator
            def python_repl(code: str) -> str:
                """Execute Python code with access to pandas DataFrame 'df'. Use this to analyze data and answer questions. The DataFrame 'df' has shape {df.shape} with columns: {list(df.columns)}. Store your final answer in a variable called 'result'."""
                try:
                    # Create isolated namespace for each execution
                    import numpy as np
                    exec_globals = {
                        "df": df.copy(),  # Use copy to prevent modifications
                        "pd": pd,
                        "np": np,
                        "__builtins__": __builtins__
                    }
                    exec_locals = {}
                    
                    # Execute code
                    exec(code, exec_globals, exec_locals)
                    
                    # Try to get result from locals first, then globals
                    if "result" in exec_locals:
                        return str(exec_locals["result"])
                    elif "result" in exec_globals:
                        return str(exec_globals["result"])
                    else:
                        # If no result variable, return last evaluated expression
                        return "Code executed successfully. Please store your answer in a 'result' variable."
                except Exception as e:
                    return f"Error: {str(e)}"
            
            # Redirect stdout/stderr
            sys.stdout = log_buffer
            sys.stderr = log_buffer
            
            # Create agent using langgraph
            agent = self.create_react_agent(self.llm, [python_repl])
            
            log_buffer.write("\nAgent created, executing query...\n")
            
            # Execute query with higher recursion limit
            response = agent.invoke(
                {"messages": [("human", question)]},
                config={"recursion_limit": 50}
            )
            
            # Restore stdout/stderr
            sys.stdout = original_stdout
            sys.stderr = original_stderr
            
            # Extract answer from langgraph response
            if isinstance(response, dict) and 'messages' in response:
                # Get last message content
                messages = response['messages']
                if messages:
                    last_msg = messages[-1]
                    answer = str(last_msg.content if hasattr(last_msg, 'content') else last_msg)
                else:
                    answer = str(response)
            else:
                answer = str(response)
            
            reasoning = "LangChain agent analyzed the dataframe using Python code execution"
            
            # Get logs
            log_buffer.write(f"\nAnswer: {answer}\n")
            log_buffer.write(f"[{datetime.now().isoformat()}] Completed successfully\n")
            logs = log_buffer.getvalue()
            
            # Generate reproduction code
            reproduction_code = self._generate_reproduction_code(df, question)
            
            return FrameworkResult(answer, reasoning, logs=logs, reproduction_code=reproduction_code)
        except Exception as e:
            # Restore stdout/stderr
            sys.stdout = original_stdout
            sys.stderr = original_stderr
            
            logs = log_buffer.getvalue()
            logs += f"\n[ERROR] {str(e)}\n"
            return FrameworkResult("", "", error=f"LangChain error: {str(e)}", logs=logs)
    
    def _generate_reproduction_code(self, df: pd.DataFrame, question: str) -> str:
        """Generate Python code to reproduce this query."""
        df_csv = df.head(10).to_csv(index=False)
        code = f'''"""Reproduce LangChain Pandas Agent Query"""
import pandas as pd
import os
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_openai import ChatOpenAI

# Sample data (first 10 rows)
data_csv = """\n{df_csv}"""

df = pd.read_csv(pd.io.common.StringIO(data_csv))

# Initialize LangChain
os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(model="gpt-5-mini")

# Create pandas dataframe agent
agent = create_pandas_dataframe_agent(
    llm,
    df,
    verbose=True,
    allow_dangerous_code=True,
    handle_parsing_errors=True
)

# Execute query
question = """{question}"""
response = agent.invoke({{"input": question}})

# Extract answer
if isinstance(response, dict):
    answer = response.get('output', '')
else:
    answer = str(response)

print(f"Answer: {{answer}}")
'''
        return code


class FrameworkManager:
    """Manager for all frameworks."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        
        self.pandasai = PandasAIWrapper(self.api_key)
        self.sketch = SketchWrapper(self.api_key)
        self.langchain = LangChainPandasWrapper(self.api_key)
        
        self.frameworks = {
            'PandasAI': self.pandasai,
            'Sketch': self.sketch,
            'LangChain': self.langchain
        }
    
    def query_all(self, df: pd.DataFrame, question: str) -> Dict[str, FrameworkResult]:
        """Query all frameworks with the same question."""
        results = {}
        
        for name, framework in self.frameworks.items():
            print(f"Querying {name}...")
            result = framework.query(df, question)
            results[name] = result
        
        return results
    
    def get_availability_status(self) -> Dict[str, bool]:
        """Get availability status of all frameworks."""
        return {
            name: fw.available for name, fw in self.frameworks.items()
        }
