"""
Context manager for GPI.
This module maintains context history and provides context management functions.
"""

import time
from typing import Dict, List, Optional, Any
import threading
import json
import os

from .extractor import ContextInfo, extract_context

# Singleton pattern
_manager_instance = None
_manager_lock = threading.Lock()

def get_context_manager():
    """Get the singleton context manager instance"""
    global _manager_instance
    with _manager_lock:
        if _manager_instance is None:
            _manager_instance = ContextManager()
        return _manager_instance


class ContextManager:
    """Manages context for the GPI system"""
    
    def __init__(self, history_size: int = 10, persistence_path: str = None):
        """
        Initialize the context manager
        
        Args:
            history_size: Number of context entries to keep in history
            persistence_path: Path to persist context history (None for no persistence)
        """
        self.history_size = history_size
        self.persistence_path = persistence_path
        self.context_history: Dict[str, List[Dict]] = {}  # user_id -> list of context entries
        self.active_contexts: Dict[str, Dict] = {}  # user_id -> active context
        self.session_data: Dict[str, Dict] = {}  # user_id -> session data
        self._lock = threading.Lock()
        
        # Load persisted context if available
        if persistence_path and os.path.exists(persistence_path):
            try:
                with open(persistence_path, 'r') as f:
                    data = json.load(f)
                    self.context_history = data.get('history', {})
                    self.active_contexts = data.get('active', {})
            except Exception as e:
                print(f"Failed to load persisted context: {e}")
    
    def get_context(self, user_id: str = "default") -> Optional[str]:
        """
        Get the current context for a user
        
        Args:
            user_id: User identifier
            
        Returns:
            String representation of the current context or None if no context exists
        """
        with self._lock:
            context_data = self.active_contexts.get(user_id)
            if context_data:
                return ContextInfo.from_dict(context_data).to_string()
            return None
    
    def extract_and_update_context(self, message: str, user_id: str = "default", 
                                  use_llm: bool = False, llm = None) -> str:
        """
        Extract context from a message and update the context history
        
        Args:
            message: User message to extract context from
            user_id: User identifier
            use_llm: Whether to use LLM for context extraction
            llm: LLM instance to use
            
        Returns:
            String representation of the extracted context
        """
        # Extract context
        context_info = extract_context(message, use_llm, llm)
        
        # Update context history
        self._update_context(user_id, context_info)
        
        # Return string representation
        return context_info.to_string()
    
    def _update_context(self, user_id: str, context_info: ContextInfo) -> None:
        """
        Update the context history for a user
        
        Args:
            user_id: User identifier
            context_info: Context information to add
        """
        with self._lock:
            # Convert to dict for storage
            context_dict = context_info.to_dict()
            
            # Add timestamp
            context_dict['timestamp'] = time.time()
            
            # Initialize history list if it doesn't exist
            if user_id not in self.context_history:
                self.context_history[user_id] = []
            
            # Add to history
            self.context_history[user_id].append(context_dict)
            
            # Limit history size
            if len(self.context_history[user_id]) > self.history_size:
                self.context_history[user_id] = self.context_history[user_id][-self.history_size:]
            
            # Update active context
            self.active_contexts[user_id] = context_dict
            
            # Persist if path is set
            self._persist()
    
    def set_context(self, user_id: str, context: str) -> None:
        """
        Manually set the context for a user
        
        Args:
            user_id: User identifier
            context: Context string
        """
        with self._lock:
            # Create a simple context info
            context_info = ContextInfo(
                topic="",
                entities=[],
                keywords=set(),
                intent="manual",
                confidence=1.0,  # High confidence since manually set
                original_query=context,
                llm_enhanced=False
            )
            
            # Update context
            self._update_context(user_id, context_info)
    
    def clear_context(self, user_id: str = "default") -> None:
        """
        Clear the context for a user
        
        Args:
            user_id: User identifier
        """
        with self._lock:
            if user_id in self.active_contexts:
                del self.active_contexts[user_id]
            
            # Persist change
            self._persist()
    
    def get_context_history(self, user_id: str = "default", limit: int = None) -> List[str]:
        """
        Get the context history for a user
        
        Args:
            user_id: User identifier
            limit: Maximum number of history entries to return (None for all)
            
        Returns:
            List of context strings, most recent first
        """
        with self._lock:
            if user_id not in self.context_history:
                return []
            
            history = self.context_history[user_id]
            
            # Apply limit if specified
            if limit is not None:
                history = history[-limit:]
            
            # Convert to strings
            return [ContextInfo.from_dict(entry).to_string() for entry in reversed(history)]
    
    def store_session_data(self, user_id: str, key: str, value: Any) -> None:
        """
        Store session data for a user
        
        Args:
            user_id: User identifier
            key: Data key
            value: Data value
        """
        with self._lock:
            if user_id not in self.session_data:
                self.session_data[user_id] = {}
            
            self.session_data[user_id][key] = value
    
    def get_session_data(self, user_id: str, key: str, default: Any = None) -> Any:
        """
        Get session data for a user
        
        Args:
            user_id: User identifier
            key: Data key
            default: Default value if not found
            
        Returns:
            The stored value or default if not found
        """
        with self._lock:
            if user_id not in self.session_data:
                return default
            
            return self.session_data[user_id].get(key, default)
    
    def _persist(self) -> None:
        """Persist context history and active contexts if path is set"""
        if not self.persistence_path:
            return
        
        try:
            data = {
                'history': self.context_history,
                'active': self.active_contexts
            }
            
            # Create directory if needed
            os.makedirs(os.path.dirname(self.persistence_path), exist_ok=True)
            
            with open(self.persistence_path, 'w') as f:
                json.dump(data, f)
        except Exception as e:
            print(f"Failed to persist context: {e}") 