"""
Module for Agent class implementation.
"""

class Agent:
    """
    Represents an agent with a name, ID, and abilities.
    
    An agent can perform tasks based on its abilities and interact
    with other agents and LLMs.
    """
    
    def __init__(self, name, agent_id, abilities, external_endpoint=None, api_key=None, agent_type="internal"):
        """
        Initialize an agent with name, ID, and abilities.
        
        Args:
            name (str): Name of the agent
            agent_id (str): Unique identifier for the agent
            abilities (list): List of strings representing agent abilities
            external_endpoint (str, optional): API endpoint for external agents
            api_key (str, optional): API key for authentication with external agents
            agent_type (str, optional): Type of agent ("internal" or "external")
        """
        self.name = name
        self.agent_id = agent_id
        self.abilities = abilities
        self.active = True
        self.external_endpoint = external_endpoint
        self.api_key = api_key
        self.agent_type = agent_type
    
    def __str__(self):
        """
        String representation of the agent.
        
        Returns:
            str: String representation
        """
        return f"Agent(name={self.name}, id={self.agent_id}, type={self.agent_type}, abilities={self.abilities})"
    
    def has_ability(self, ability):
        """
        Check if the agent has a specific ability.
        
        Args:
            ability (str): The ability to check for
            
        Returns:
            bool: True if the agent has the ability, False otherwise
        """
        return ability in self.abilities
    
    def add_ability(self, ability):
        """
        Add an ability to the agent.
        
        Args:
            ability (str): The ability to add
            
        Returns:
            bool: True if ability was added, False if already present
        """
        if ability in self.abilities:
            return False
        
        self.abilities.append(ability)
        return True
    
    def remove_ability(self, ability):
        """
        Remove an ability from the agent.
        
        Args:
            ability (str): The ability to remove
            
        Returns:
            bool: True if ability was removed, False if not present
        """
        if ability not in self.abilities:
            return False
        
        self.abilities.remove(ability)
        return True
    
    def deactivate(self):
        """
        Deactivate the agent.
        """
        self.active = False
    
    def activate(self):
        """
        Activate the agent.
        """
        self.active = True
    
    def is_active(self):
        """
        Check if the agent is active.
        
        Returns:
            bool: True if active, False otherwise
        """
        return self.active
    
    def is_external(self):
        """
        Check if the agent is external.
        
        Returns:
            bool: True if external, False if internal
        """
        return self.agent_type == "external"
    
    def process_message(self, context, message):
        """
        Process a message with the given context.
        
        Args:
            context (str): The context for processing the message
            message (str): The message to process
            
        Returns:
            str: The response from the agent
        """
        # If this is an external agent with an endpoint, we would call the external API
        if self.is_external() and self.external_endpoint:
            return self._call_external_endpoint(context, message)
        
        # This is a simple simulation of message processing for internal agents
        # In a real implementation, this would use the agent's abilities
        # to generate a more sophisticated response
        
        response = f"Agent {self.name} received: {message} (Context: {context})"
        
        # Simulate different responses based on abilities
        if "talk" in self.abilities:
            response += f"\nI can talk and respond to your message."
        
        if "think" in self.abilities:
            response += f"\nI've analyzed your request and am processing it."
        
        if "learn" in self.abilities:
            response += f"\nI'm learning from this interaction to improve future responses."
            
        return response
    
    def _call_external_endpoint(self, context, message):
        """
        Call the external endpoint for an external agent.
        
        Args:
            context (str): The context for processing the message
            message (str): The message to process
            
        Returns:
            str: The response from the external agent
        """
        import requests
        import json
        
        # Skip the actual API call if no endpoint is provided
        if not self.external_endpoint:
            return f"External agent {self.name} has no endpoint configured"
        
        try:
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
            
            # Add API key if provided
            if self.api_key:
                headers['Authorization'] = f'Bearer {self.api_key}'
            
            payload = {
                'agent_id': self.agent_id,
                'context': context,
                'message': message
            }
            
            response = requests.post(
                self.external_endpoint,
                data=json.dumps(payload),
                headers=headers,
                timeout=30  # 30 seconds timeout
            )
            
            response.raise_for_status()
            
            # Parse the response JSON
            response_data = response.json()
            
            # Return the response message or a default message
            return response_data.get('response', f"External agent {self.name} responded but provided no message")
            
        except requests.exceptions.RequestException as e:
            # In a real implementation, you'd want to log this error
            return f"Error communicating with external agent {self.name}: {str(e)}"
