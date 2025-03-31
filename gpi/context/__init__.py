"""
Context management module for GPI.
This module handles automatic context extraction, tracking, and management.
"""

from .extractor import extract_context, ContextInfo
from .manager import ContextManager, get_context_manager

# Global context manager instance
_manager = ContextManager()

def get_manager():
    """Get the global context manager instance"""
    return _manager

# Export functions
__all__ = [
    'extract_context',
    'ContextInfo',
    'ContextManager',
    'get_context_manager',
    'get_manager'
] 