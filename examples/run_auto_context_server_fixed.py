#!/usr/bin/env python3
"""
Run the BAPI server with automatic context extraction.
This allows users to interact with agents without manually specifying context.
This version includes a fix for NLTK SSL certificate issues.
"""

import sys
import os
import signal
import ssl

# Fix for NLTK SSL certificate issues - must be done before importing nltk
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass  # Legacy Python that doesn't verify HTTPS certificates by default
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context

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
        print("\n🚀 Starting BAPI Server with automatic context extraction...")
        
        # Create sample agents
        create_sample_agents()
        
        print("\n✨ Key features available:")
        print("- 🧠 Automatic context extraction from user messages")
        print("- 📜 Context history tracking per user")
        print("- 🔄 Manual context override when needed")
        print("- 🔌 Context management APIs")
        print("\n🌐 Navigate to http://127.0.0.1:5000 to access the interface")
        print("💡 Try sending messages without specifying context!")
        print("\n📝 Sample questions to try:")
        print("- What's the weather like in San Francisco?")
        print("- Tell me about the latest technology news")
        print("- I want to travel to Paris next week")
        print("- How many cups are in a gallon?")
        
        # Create and start the server on default host/port
        server = bapi()
        server.start(debug=True, use_reloader=True)
    except KeyboardInterrupt:
        print("\n👋 Shutting down BAPI server...")
        return 0
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 