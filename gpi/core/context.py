"""
Module for ContextManager class implementation.

The ContextManager is responsible for managing and tracking the
current context for context-aware operations.
"""

class ContextManager:
    """
    Manages context for context-aware operations in the GPI system.
    """
    
    def __init__(self):
        """
        Initialize the context manager with an empty context.
        """
        self.current_context = None
        self.context_history = []
        self.max_history_size = 10
    
    def set_context(self, context):
        """
        Set the current context.
        
        Args:
            context (str): The context to set
        """
        # Add the current context to history before updating
        if self.current_context:
            self._add_to_history(self.current_context)
        
        self.current_context = context
    
    def get_context(self):
        """
        Get the current context.
        
        Returns:
            str: The current context, or None if no context is set
        """
        return self.current_context
    
    def get_context_history(self):
        """
        Get the context history.
        
        Returns:
            list: The context history
        """
        return self.context_history
    
    def _add_to_history(self, context):
        """
        Add a context to the history.
        
        Args:
            context (str): The context to add to history
        """
        self.context_history.append(context)
        
        # Trim history if it exceeds the maximum size
        if len(self.context_history) > self.max_history_size:
            self.context_history = self.context_history[-self.max_history_size:]
    
    def clear_context(self):
        """
        Clear the current context.
        """
        if self.current_context:
            self._add_to_history(self.current_context)
        
        self.current_context = None
    
    def restore_previous_context(self):
        """
        Restore the previous context from history.
        
        Returns:
            bool: True if a previous context was restored, False otherwise
        """
        if not self.context_history:
            return False
        
        self.current_context = self.context_history.pop()
        return True
    
    def get_context_summary(self):
        """
        Get a summary of the current context and recent history.
        
        Returns:
            str: A summary of the context state
        """
        summary = f"Current Context: {self.current_context or 'None'}\n"
        
        if self.context_history:
            summary += "Recent Context History:\n"
            for i, ctx in enumerate(reversed(self.context_history[-3:])):
                summary += f"  {i+1}. {ctx[:50]}{'...' if len(ctx) > 50 else ''}\n"
        
        return summary
