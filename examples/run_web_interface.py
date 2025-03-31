#!/usr/bin/env python3
"""
Run the GPI SDK Web Interface.

This script launches the web interface for the GPI SDK.
"""

import sys
import os
import time

# Add the parent directory to the path so we can import the gpi package
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import gpi
from gpi.web.server import bapi

def create_sample_data():
    """Create some sample agents and LLMs for demonstration."""
    # Create sample agents
    gpi.create.agent("AssistantAgent", "assist001", ["talk", "think", "learn"])
    gpi.create.agent("DocumentAgent", "doc001", ["read", "write", "summarize"])
    gpi.create.agent("ConverterAgent", "convert001", ["convert", "process", "transform"])
    
    # Register sample LLMs
    gpi.register.llm("GPT-4", "demo_api_key_gpt4", config={"temperature": 0.7})
    gpi.register.llm("Claude", "demo_api_key_claude", config={"max_tokens": 8000})

def main():
    """
    Main function to run the web interface.
    """
    print("GPI SDK Web Interface")
    print("====================")
    
    try:
        # Create sample data for demonstration
        print("Creating sample data for demonstration...")
        create_sample_data()
        
        # Start the web server
        host = '127.0.0.1'
        port = 5000
        
        print(f"\nStarting GPI Web Interface on http://{host}:{port}")
        print("Press Ctrl+C to stop the server")
        
        server = bapi(host=host, port=port)
        server.start(debug=True, use_reloader=True)
        
    except KeyboardInterrupt:
        print("\nWeb interface stopped by user.")
    except Exception as e:
        print(f"\nError: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 