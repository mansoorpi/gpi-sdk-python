#!/usr/bin/env python3
"""
BAPI UI Simulation for the GPI SDK.

This script simulates a chat-like bot interface for registering agents.
"""

import sys
import os
import time

# Add the parent directory to the path so we can import the gpi package
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import gpi

def print_bot_message(message):
    """Print a message as if it came from a bot."""
    print("\n🤖 BAPI: ", end="")
    for char in message:
        print(char, end="", flush=True)
        time.sleep(0.01)
    print()

def get_user_input(prompt):
    """Get input from the user with a prompt."""
    print(f"\n👤 {prompt}", end=" ")
    return input()

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def bapi_ui_simulation():
    """
    Simulate a BAPI UI for agent registration.
    """
    clear_screen()
    print("=" * 50)
    print("         GPI - BAPI UI SIMULATION")
    print("=" * 50)
    
    print_bot_message("Hello! I'm BAPI, your Broker API assistant.")
    time.sleep(0.5)
    print_bot_message("I can help you register agents and work with the GPI system.")
    time.sleep(0.5)
    print_bot_message("Let's register a new agent. I'll guide you through the process.")
    
    # Get agent information
    name = get_user_input("What should we name this agent?")
    agent_id = get_user_input("Please provide a unique ID for the agent:")
    
    # Get abilities
    print_bot_message("Great! Now, let's define the agent's abilities.")
    print_bot_message("Common abilities include: talk, think, learn, calculate, connect.")
    ability_input = get_user_input("Enter abilities separated by commas:")
    abilities = [ability.strip() for ability in ability_input.split(",")]
    
    # Confirm registration
    print_bot_message(f"I'll register an agent with these details:")
    print(f"\nName: {name}")
    print(f"ID: {agent_id}")
    print(f"Abilities: {abilities}")
    
    confirm = get_user_input("Does this look correct? (yes/no)")
    
    if confirm.lower() in ["yes", "y"]:
        # Register the agent
        print_bot_message("Registering your agent...")
        agent = gpi.register.agent(name, agent_id, abilities)
        time.sleep(1)
        print_bot_message(f"✅ Success! Agent '{name}' has been registered with ID '{agent_id}'.")
        
        # Test the agent
        print_bot_message("Let's test your agent with a simple message:")
        context = "test conversation"
        message = "Hello, agent!"
        
        print_bot_message(f"Sending message to {name} with context '{context}'...")
        time.sleep(1)
        
        response = agent.process_message(context, message)
        print("\n📝 Response from agent:")
        print("-" * 50)
        print(response)
        print("-" * 50)
        
        print_bot_message("Would you like to register another agent?")
        another = get_user_input("Enter yes/no:")
        
        if another.lower() in ["yes", "y"]:
            # Recursive call to register another agent
            bapi_ui_simulation()
        else:
            print_bot_message("Thank you for using the BAPI UI simulation. Goodbye!")
    else:
        print_bot_message("Registration cancelled. Would you like to start over?")
        restart = get_user_input("Enter yes/no:")
        
        if restart.lower() in ["yes", "y"]:
            bapi_ui_simulation()
        else:
            print_bot_message("Thank you for using the BAPI UI simulation. Goodbye!")

def main():
    """Main function to start the BAPI UI simulation."""
    try:
        bapi_ui_simulation()
    except KeyboardInterrupt:
        print("\n\nBAPI UI simulation interrupted. Goodbye!")
    except Exception as e:
        print(f"\nAn error occurred: {e}")

if __name__ == "__main__":
    main() 