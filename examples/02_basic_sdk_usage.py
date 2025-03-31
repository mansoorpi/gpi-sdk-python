#!/usr/bin/env python3
"""
Basic usage example for the GPI SDK.

This script demonstrates how to use the SDK to create agents,
register LLMs, and generate context-aware responses.
"""

import sys
import os

# Add the parent directory to the path so we can import the gpi package
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import gpi

def main():
    """
    Main function demonstrating basic usage of the GPI SDK.
    """
    print("GPI SDK Basic Usage Example")
    print("==========================")
    
    # Create an agent
    print("\n1. Creating an agent...")
    agent = gpi.create.agent("AssistantAgent", "001", ["talk", "think", "learn"])
    print(f"Agent created: {agent}")
    
    # Register an LLM
    print("\n2. Registering an LLM...")
    llm = gpi.register.llm("GPT-4", "sim_api_key_123", "/path/to/simulated/gpt4", {"temperature": 0.7})
    print(f"LLM registered: {llm}")
    
    # Generate a context-aware response
    print("\n3. Generating context-aware responses...")
    
    # Context 1: Weather
    weather_context = "weather conversation about temperature and conditions"
    response = gpi.car(weather_context, "What's the weather like today?")
    print(f"\nContext: {weather_context}")
    print(f"Query: What's the weather like today?")
    print(f"Response: {response}")
    
    # Context 2: Technical
    tech_context = "technical discussion about programming and thinking about algorithms"
    response = gpi.car(tech_context, "What's a good sorting algorithm?")
    print(f"\nContext: {tech_context}")
    print(f"Query: What's a good sorting algorithm?")
    print(f"Response: {response}")
    
    # Use the Broker API
    print("\n4. Using the Broker API...")
    learning_context = "learning about machine learning concepts"
    response = gpi.bapi(learning_context, "Explain neural networks")
    print(f"\nContext: {learning_context}")
    print(f"Query: Explain neural networks")
    print(f"Response: {response}")
    
    # Create another agent with different abilities
    print("\n5. Creating and using a specialized agent...")
    math_agent = gpi.create.agent("MathAgent", "002", ["think", "calculate"])
    print(f"Agent created: {math_agent}")
    
    # Try to use it (note: our simplified implementation will just use the first agent)
    math_context = "mathematical calculation and thinking"
    response = gpi.bapi(math_context, "What is 355 divided by 113?")
    print(f"\nContext: {math_context}")
    print(f"Query: What is 355 divided by 113?")
    print(f"Response: {response}")
    
    print("\nExample completed successfully!")

if __name__ == "__main__":
    main() 