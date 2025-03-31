"""
GPI - SDK Framework for AI Agentic Development
"""

# Import and define the package components
from gpi.core.agent import Agent
from gpi.core.registry import Registry
from gpi.core.broker import Broker
from gpi.context.manager import ContextManager, get_context_manager
from gpi.utils.http import HttpClient
import gpi.context as context_module

# Initialize singletons
_registry = Registry()
_broker = Broker(_registry)
_context_manager = get_context_manager()
_http_client = HttpClient()

# Set the context module manager to use our singleton
context_module._manager = _context_manager

# Define API classes
class create:
    @staticmethod
    def agent(name, agent_id, abilities, external_endpoint=None, api_key=None, agent_type="internal"):
        """
        Create a new agent with specified name, ID, and abilities.
        
        Args:
            name (str): Name of the agent
            agent_id (str): Unique identifier for the agent
            abilities (list): List of strings representing agent abilities
            external_endpoint (str, optional): API endpoint for external agents
            api_key (str, optional): API key for authentication with external agents
            agent_type (str, optional): Type of agent ("internal" or "external")
            
        Returns:
            Agent: The created agent object
        """
        agent = Agent(name, agent_id, abilities, external_endpoint, api_key, agent_type)
        _registry.register_agent(agent)
        return agent
    
    @staticmethod
    def external_agent(name, agent_id, abilities, endpoint, api_key=None):
        """
        Create an external agent with a specified endpoint.
        
        Args:
            name (str): Name of the agent
            agent_id (str): Unique identifier for the agent
            abilities (list): List of strings representing agent abilities
            endpoint (str): API endpoint for the external agent
            api_key (str, optional): API key for authentication with the external agent
            
        Returns:
            Agent: The created external agent object
        """
        return create.agent(name, agent_id, abilities, endpoint, api_key, "external")

class register:
    @staticmethod
    def agent(name, agent_id, abilities, external_endpoint=None, api_key=None, agent_type="internal"):
        """
        Register an agent with the GPI system.
        
        Args:
            name (str): Name of the agent
            agent_id (str): Unique identifier for the agent
            abilities (list): List of strings representing agent abilities
            external_endpoint (str, optional): API endpoint for external agents
            api_key (str, optional): API key for authentication with external agents
            agent_type (str, optional): Type of agent ("internal" or "external")
            
        Returns:
            Agent: The registered agent object
        """
        agent = Agent(name, agent_id, abilities, external_endpoint, api_key, agent_type)
        _registry.register_agent(agent)
        return agent
    
    @staticmethod
    def external_agent(name, agent_id, abilities, endpoint, api_key=None):
        """
        Register an external agent with the GPI system.
        
        Args:
            name (str): Name of the agent
            agent_id (str): Unique identifier for the agent
            abilities (list): List of strings representing agent abilities
            endpoint (str): API endpoint for the external agent
            api_key (str, optional): API key for authentication with the external agent
            
        Returns:
            Agent: The registered external agent object
        """
        return register.agent(name, agent_id, abilities, endpoint, api_key, "external")
    
    @staticmethod
    def llm(name, api_key, model_path=None, config=None):
        """
        Register an LLM/AI with the GPI system.
        
        Args:
            name (str): Name of the LLM/AI
            api_key (str): API key for accessing the LLM/AI
            model_path (str, optional): File path to the model
            config (dict, optional): Model-specific configuration
            
        Returns:
            dict: The registered LLM/AI information
        """
        return _registry.register_llm(name, api_key, model_path, config)
    
    @staticmethod
    def agent_http(endpoint, payload):
        """
        Register an agent via HTTP endpoint.
        
        Args:
            endpoint (str): URL of the registration endpoint
            payload (dict): Agent information to send
            
        Returns:
            dict: Response from the HTTP request
        """
        return _http_client.register_agent(endpoint, payload)
    
    @staticmethod
    def llm_http(endpoint, payload):
        """
        Register an LLM/AI via HTTP endpoint.
        
        Args:
            endpoint (str): URL of the registration endpoint
            payload (dict): LLM/AI information to send
            
        Returns:
            dict: Response from the HTTP request
        """
        return _http_client.register_llm(endpoint, payload)
    
    @staticmethod
    def context_function(func):
        """
        Register a context function with the system.
        
        Args:
            func: The function to register
            
        Returns:
            function: The registered function
        """
        # In the future, implement a registry for context functions
        return func

def car(context=None, message=None, user_id="default", use_llm=False):
    """
    Generate a context-aware response.
    
    Args:
        context (str, optional): The context string (if None, auto-extracted from message)
        message (str): The message to respond to
        user_id (str, optional): User identifier for context tracking
        use_llm (bool, optional): Whether to use LLM for context extraction
        
    Returns:
        str: The context-aware response
    """
    if message is None:
        raise ValueError("Message cannot be None")
    
    # Auto-extract context if not provided
    if context is None:
        # Get the LLM if available and requested
        llm = _registry.get_llm("default") if use_llm else None
        
        # Extract and update context
        context = _context_manager.extract_and_update_context(message, user_id, use_llm, llm)
    else:
        # Manually set context
        _context_manager.set_context(user_id, context)
    
    return _broker.generate_response(message, user_id)

def bapi(context=None, message=None, user_id="default", use_llm=False):
    """
    Use the Broker API to handle communication between agents and LLMs.
    
    Args:
        context (str, optional): The context for the communication (if None, auto-extracted)
        message (str): The message to process
        user_id (str, optional): User identifier for context tracking
        use_llm (bool, optional): Whether to use LLM for context extraction
        
    Returns:
        str: The response generated by the appropriate agent/LLM
    """
    if message is None:
        raise ValueError("Message cannot be None")
    
    # Auto-extract context if not provided
    if context is None:
        # Get the LLM if available and requested
        llm = _registry.get_llm("default") if use_llm else None
        
        # Extract and update context
        context = _context_manager.extract_and_update_context(message, user_id, use_llm, llm)
    else:
        # Manually set context
        _context_manager.set_context(user_id, context)
    
    return _broker.process_message(message, user_id)

# Context management functions
def get_context(user_id="default"):
    """
    Get the current context for a user
    
    Args:
        user_id (str, optional): User identifier
        
    Returns:
        str: The current context or None if no context exists
    """
    return _context_manager.get_context(user_id)

def clear_context(user_id="default"):
    """
    Clear the context for a user
    
    Args:
        user_id (str, optional): User identifier
    """
    _context_manager.clear_context(user_id)

def get_context_history(user_id="default", limit=None):
    """
    Get the context history for a user
    
    Args:
        user_id (str, optional): User identifier
        limit (int, optional): Maximum number of history entries to return
        
    Returns:
        list: List of context strings, most recent first
    """
    return _context_manager.get_context_history(user_id, limit)

# Export the public API
__all__ = [
    'create',
    'register',
    'car',
    'bapi',
    'Agent',
    'get_context',
    'clear_context',
    'get_context_history',
    'context_module'
]
