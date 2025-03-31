"""
Module for Broker class implementation.

The Broker is responsible for handling communication between agents and LLMs,
and for generating responses based on the current context.
"""

import gpi.context

class Broker:
    """
    Broker API (BAPI) for handling communication between agents and LLMs.
    """
    
    def __init__(self, registry):
        """
        Initialize the broker with a reference to the registry.
        
        Args:
            registry: The registry containing agents and LLMs
        """
        self.registry = registry
        self.context_manager = gpi.context.get_manager()
    
    def process_message(self, message, user_id="default"):
        """
        Process a message using the current context and available agents/LLMs.
        
        This function determines which agent or LLM should handle the message
        based on the current context and the message content.
        
        Args:
            message (str): The message to process
            user_id (str, optional): User identifier for context tracking
            
        Returns:
            str: The generated response
        """
        # Get the current context for this user
        context = self.context_manager.get_context(user_id)
        
        if context:
            # If we have context, try to find an agent with an appropriate ability for the context
            context_abilities = self._extract_abilities_from_context(context)
            
            for ability in context_abilities:
                agents = self.registry.get_agents_by_ability(ability)
                if agents:
                    # Use the first agent with the required ability
                    response = agents[0].process_message(context, message)
                    return response
        
        # If no context or no agent matches context, check for any active agents
        active_agents = self.registry.get_active_agents()
        if active_agents:
            # Use the first active agent
            agent_context = context or "No specific context available"
            response = active_agents[0].process_message(agent_context, message)
            return response
        
        # If no agent can handle the message, try to use an LLM
        active_llms = self.registry.get_active_llms()
        if active_llms:
            # Use the first active LLM
            return self._simulate_llm_response(active_llms[0], message, context or "No specific context")
        
        # If no agent or LLM can handle the message, return a default response
        return f"No agent or LLM available to process message: {message}"
    
    def generate_response(self, message, user_id="default"):
        """
        Generate a context-aware response for the given message.
        
        This function is similar to process_message, but specifically focused on
        generating a response that takes into account the current context.
        
        Args:
            message (str): The message to respond to
            user_id (str, optional): User identifier for context tracking
            
        Returns:
            str: The context-aware response
        """
        # Get the current context for this user
        context = self.context_manager.get_context(user_id)
        
        # Get all active agents that might be able to help
        active_agents = self.registry.get_active_agents()
        
        if active_agents:
            # For simplicity, use the first active agent
            # In a real system, we would select the most appropriate agent
            agent_context = context or "No specific context available"
            response = active_agents[0].process_message(agent_context, message)
            return f"Context-Aware Response: {response}"
        
        # If no agent is available, try to use an LLM
        active_llms = self.registry.get_active_llms()
        if active_llms:
            return f"Context-Aware Response: {self._simulate_llm_response(active_llms[0], message, context or 'No specific context')}"
        
        # If no agent or LLM is available, return a default response
        return f"No agent or LLM available to generate a context-aware response for: {message}"
    
    def _extract_abilities_from_context(self, context):
        """
        Extract relevant abilities from the given context.
        
        Args:
            context (str): The context to analyze
            
        Returns:
            list: List of abilities that might be relevant for the context
        """
        # This is a simple implementation that looks for keywords in the context
        # In a real system, this would involve more sophisticated NLP techniques
        
        abilities = []
        
        if "talk" in context.lower() or "conversation" in context.lower() or "chat" in context.lower():
            abilities.append("talk")
        
        if "think" in context.lower() or "analyze" in context.lower() or "reason" in context.lower():
            abilities.append("think")
        
        if "learn" in context.lower() or "study" in context.lower() or "adapt" in context.lower():
            abilities.append("learn")
        
        # Add more mappings as needed
        
        return abilities
    
    def _simulate_llm_response(self, llm_info, message, context):
        """
        Simulate a response from an LLM.
        
        Args:
            llm_info (dict): Information about the LLM
            message (str): The message to process
            context (str): The current context
            
        Returns:
            str: The simulated LLM response
        """
        # This is a simple simulation of an LLM response
        # In a real system, this would call the actual LLM API
        
        llm_name = llm_info["name"]
        context_summary = context[:30] + "..." if len(context) > 30 else context
        
        return f"LLM {llm_name} response (Context: {context_summary}): I have processed your message: '{message}' and generated this response based on the current context."
