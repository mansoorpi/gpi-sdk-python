#!/usr/bin/env python3
"""
HTTP Integration example for the GPI SDK.

This script demonstrates how to use the SDK to register agents and LLMs
via HTTP endpoints.
"""

import sys
import os
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import threading

# Add the parent directory to the path so we can import the gpi package
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import gpi

# Simple HTTP server for testing
class TestHandler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))
        
        # Process the data based on the endpoint
        if self.path == '/register/agent':
            print(f"Server received agent registration: {data}")
            response = {"status": "success", "message": f"Agent {data.get('name', 'Unknown')} registered"}
        elif self.path == '/register/llm':
            print(f"Server received LLM registration: {data}")
            response = {"status": "success", "message": f"LLM {data.get('name', 'Unknown')} registered"}
        else:
            response = {"status": "error", "message": "Unknown endpoint"}
        
        self._set_headers()
        self.wfile.write(json.dumps(response).encode('utf-8'))
    
    def log_message(self, format, *args):
        # Suppress console output for cleaner example output
        return

def start_server(port=8000):
    """Start a test HTTP server on the specified port."""
    server = HTTPServer(('localhost', port), TestHandler)
    print(f"Starting test server on port {port}...")
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    return server

def main():
    """
    Main function demonstrating HTTP integration with the GPI SDK.
    """
    print("GPI SDK HTTP Integration Example")
    print("===============================")
    
    # Start the test server
    server = start_server()
    time.sleep(1)  # Give the server a moment to start
    
    try:
        # Register an agent via HTTP
        print("\n1. Registering an agent via HTTP...")
        agent_payload = {
            "name": "RemoteAgent",
            "id": "remote001",
            "abilities": ["talk", "think", "connect"]
        }
        
        response = gpi.register.agent_http(
            "http://localhost:8000/register/agent",
            agent_payload
        )
        print(f"Response from server: {response}")
        
        # Register an LLM via HTTP
        print("\n2. Registering an LLM via HTTP...")
        llm_payload = {
            "name": "RemoteGPT",
            "api_key": "remote_api_key_456",
            "model_path": "/remote/path/to/model",
            "config": {
                "temperature": 0.5,
                "max_tokens": 2048
            }
        }
        
        response = gpi.register.llm_http(
            "http://localhost:8000/register/llm",
            llm_payload
        )
        print(f"Response from server: {response}")
        
        print("\nExample completed successfully!")
        
    except Exception as e:
        print(f"Error occurred: {e}")
    
    finally:
        # Shutdown the server
        print("\nShutting down test server...")
        server.shutdown()

if __name__ == "__main__":
    main() 