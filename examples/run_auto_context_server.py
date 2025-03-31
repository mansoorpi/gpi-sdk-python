#!/usr/bin/env python3
"""
Run the BAPI server with automatic context extraction.
This allows users to interact with agents without manually specifying context.
"""

import sys
import os
import signal

# Ensure the parent directory is in the path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gpi.web.server import bapi
import gpi

def create_sample_agents():
    """Create some sample agents for demonstration purposes"""
    # Create a weather agent
    gpi.create.agent(
        name="Weather Agent",
        agent_id="weather",
        abilities=["talk", "weather"]
    )
    
    # Create a tech news agent
    gpi.create.agent(
        name="Tech News Agent",
        agent_id="tech_news",
        abilities=["talk", "news"]
    )
    
    # Create a travel agent
    gpi.create.agent(
        name="Travel Agent",
        agent_id="travel",
        abilities=["talk", "travel"]
    )
    
    # Create a general purpose agent
    gpi.create.agent(
        name="General Assistant",
        agent_id="assistant",
        abilities=["talk", "think", "reason"]
    )
    
    print("Sample agents created:")
    print("  - Weather Agent (weather)")
    print("  - Tech News Agent (tech_news)")
    print("  - Travel Agent (travel)")
    print("  - General Assistant (assistant)")

def main():
    """
    Initialize and run the BAPI server with automatic context extraction.
    """
    try:
        print("Starting BAPI Server with automatic context extraction...")
        
        # Create sample agents
        create_sample_agents()
        
        print("\nKey features available:")
        print("- Automatic context extraction from user messages")
        print("- Context history tracking per user")
        print("- Manual context override when needed")
        print("- Context management APIs")
        print("\nNavigate to http://127.0.0.1:5000 to access the interface")
        print("Try sending messages without specifying context!")
        
        # Create and start the server on default host/port
        server = bapi()
        server.start(debug=True, use_reloader=True)
    except KeyboardInterrupt:
        print("\nShutting down BAPI server...")
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 