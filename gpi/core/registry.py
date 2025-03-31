"""
Module for Registry class implementation.
"""

class Registry:
    """
    Registry for agents and LLMs/AIs.
    
    Manages the registration and retrieval of agents and LLMs/AIs in the GPI system.
    """
    
    def __init__(self):
        """
        Initialize the registry with empty dictionaries for agents and LLMs.
        """
        self.agents = {}  # agent_id -> Agent
        self.llms = {}    # llm_name -> LLM info
    
    def register_agent(self, agent):
        """
        Register an agent with the registry.
        
        Args:
            agent: The agent object to register
            
        Returns:
            bool: True if registration was successful, False otherwise
        """
        if agent.agent_id in self.agents:
            return False
        
        self.agents[agent.agent_id] = agent
        return True
    
    def register_llm(self, name, api_key, model_path=None, config=None):
        """
        Register an LLM with the registry.
        
        Args:
            name (str): Name of the LLM
            api_key (str): API key for the LLM
            model_path (str, optional): Path to the model file
            config (dict, optional): Additional configuration for the LLM
            
        Returns:
            dict: The registered LLM information
        """
        llm_info = {
            "name": name,
            "api_key": api_key,
            "model_path": model_path,
            "config": config or {},
            "active": True
        }
        
        self.llms[name] = llm_info
        return llm_info
    
    def get_agent(self, agent_id):
        """
        Get an agent by ID.
        
        Args:
            agent_id (str): The ID of the agent to retrieve
            
        Returns:
            Agent or None: The agent if found, None otherwise
        """
        return self.agents.get(agent_id)
    
    def get_llm(self, name):
        """
        Get an LLM by name.
        
        Args:
            name (str): The name of the LLM to retrieve
            
        Returns:
            dict or None: The LLM information if found, None otherwise
        """
        return self.llms.get(name)
    
    def deactivate_agent(self, agent_id):
        """
        Deactivate an agent by ID.
        
        Args:
            agent_id (str): The ID of the agent to deactivate
            
        Returns:
            bool: True if successful, False otherwise
        """
        agent = self.get_agent(agent_id)
        if agent:
            agent.deactivate()
            return True
        return False
    
    def activate_agent(self, agent_id):
        """
        Activate an agent by ID.
        
        Args:
            agent_id (str): The ID of the agent to activate
            
        Returns:
            bool: True if successful, False otherwise
        """
        agent = self.get_agent(agent_id)
        if agent:
            agent.activate()
            return True
        return False
    
    def deactivate_llm(self, name):
        """
        Deactivate an LLM by name.
        
        Args:
            name (str): The name of the LLM to deactivate
            
        Returns:
            bool: True if successful, False otherwise
        """
        llm = self.get_llm(name)
        if llm:
            llm["active"] = False
            return True
        return False
    
    def activate_llm(self, name):
        """
        Activate an LLM by name.
        
        Args:
            name (str): The name of the LLM to activate
            
        Returns:
            bool: True if successful, False otherwise
        """
        llm = self.get_llm(name)
        if llm:
            llm["active"] = True
            return True
        return False
    
    def get_agents_by_ability(self, ability):
        """
        Get all agents that have a specific ability.
        
        Args:
            ability (str): The ability to filter by
            
        Returns:
            list: List of agents with the specified ability
        """
        return [agent for agent in self.agents.values() 
                if agent.has_ability(ability) and agent.is_active()]
    
    def get_active_agents(self):
        """
        Get all active agents.
        
        Returns:
            list: List of active agents
        """
        return [agent for agent in self.agents.values() if agent.is_active()]
    
    def get_active_llms(self):
        """
        Get all active LLMs.
        
        Returns:
            list: List of active LLMs
        """
        return [llm for llm in self.llms.values() if llm["active"]]
