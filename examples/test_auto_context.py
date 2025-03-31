#!/usr/bin/env python3
"""
Test script for the automatic context extraction functionality.
"""

import sys
import os
import time

# Ensure the parent directory is in the path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import gpi

def test_auto_context():
    """Test the automatic context extraction functionality"""
    print("Testing automatic context extraction functionality...")
    
    # Test basic extraction without LLM enhancement
    print("\n1. Basic extraction (no LLM):")
    test_messages = [
        "What's the weather like in New York today?",
        "Tell me about the latest technology news",
        "How much does a cup of coffee cost in London?",
        "When is the next train to Boston?",
        "I need to book a flight to Paris next week"
    ]
    
    for message in test_messages:
        print(f"\nMessage: \"{message}\"")
        response = gpi.bapi(message=message, use_llm=False)
        context = gpi.get_context()
        print(f"Extracted context: {context}")
        print(f"Response: {response}")
        time.sleep(0.5)  # Add a small delay for readability
    
    # Clear context before next test
    gpi.clear_context()
    
    # Test context history
    print("\n\n2. Context history:")
    user_id = "test_user_123"
    
    for i, message in enumerate(test_messages[:3], 1):
        print(f"\nMessage {i}: \"{message}\"")
        gpi.bapi(message=message, user_id=user_id, use_llm=False)
        
    print("\nContext history:")
    history = gpi.get_context_history(user_id)
    for i, ctx in enumerate(history, 1):
        print(f"  {i}. {ctx}")
    
    # Test manual override
    print("\n\n3. Manual context override:")
    manual_context = "Custom context for a specific purpose"
    print(f"Setting manual context: \"{manual_context}\"")
    
    gpi._context_manager.set_context(user_id, manual_context)
    context = gpi.get_context(user_id)
    
    print(f"Current context: {context}")
    
    # Test with the manual context
    message = "Does this use my manual context?"
    print(f"\nMessage: \"{message}\"")
    response = gpi.bapi(message=message, user_id=user_id, use_llm=False)
    print(f"Response: {response}")
    
    # Test automatic extraction after manual context
    print("\n\n4. Back to automatic extraction:")
    gpi.clear_context(user_id)
    
    message = "What's the population of Tokyo?"
    print(f"\nMessage: \"{message}\"")
    response = gpi.bapi(message=message, user_id=user_id, use_llm=False)
    context = gpi.get_context(user_id)
    print(f"New extracted context: {context}")
    print(f"Response: {response}")

if __name__ == "__main__":
    test_auto_context() 