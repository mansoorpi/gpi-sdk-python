"""
Module for HttpClient class implementation.

The HttpClient is responsible for HTTP-based registration for
agents and LLMs.
"""

import json
import requests

class HttpClient:
    """
    HTTP client for agent and LLM registration over HTTP.
    """
    
    def __init__(self):
        """
        Initialize the HTTP client.
        """
        self.timeout = 30  # Default timeout in seconds
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    
    def register_agent(self, endpoint, payload):
        """
        Register an agent via HTTP endpoint.
        
        Args:
            endpoint (str): URL of the registration endpoint
            payload (dict): Agent information to send
            
        Returns:
            dict: Response from the HTTP request
        """
        try:
            response = requests.post(
                endpoint,
                data=json.dumps(payload),
                headers=self.headers,
                timeout=self.timeout
            )
            
            response.raise_for_status()
            return response.json()
        
        except requests.exceptions.RequestException as e:
            error_message = f"Error registering agent via HTTP: {str(e)}"
            return {'error': error_message, 'success': False}
    
    def register_llm(self, endpoint, payload):
        """
        Register an LLM/AI via HTTP endpoint.
        
        Args:
            endpoint (str): URL of the registration endpoint
            payload (dict): LLM/AI information to send
            
        Returns:
            dict: Response from the HTTP request
        """
        try:
            response = requests.post(
                endpoint,
                data=json.dumps(payload),
                headers=self.headers,
                timeout=self.timeout
            )
            
            response.raise_for_status()
            return response.json()
        
        except requests.exceptions.RequestException as e:
            error_message = f"Error registering LLM via HTTP: {str(e)}"
            return {'error': error_message, 'success': False}
    
    def set_timeout(self, timeout):
        """
        Set the timeout for HTTP requests.
        
        Args:
            timeout (int): Timeout in seconds
            
        Returns:
            int: The new timeout value
        """
        self.timeout = timeout
        return self.timeout
    
    def set_header(self, key, value):
        """
        Set a header for HTTP requests.
        
        Args:
            key (str): Header key
            value (str): Header value
            
        Returns:
            dict: Updated headers
        """
        self.headers[key] = value
        return self.headers
    
    def clear_headers(self):
        """
        Reset headers to default.
        
        Returns:
            dict: Default headers
        """
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        return self.headers
