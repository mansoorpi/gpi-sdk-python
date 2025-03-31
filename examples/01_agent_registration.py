import os
import sys
import time
import signal
from dotenv import load_dotenv

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gpi import create, register, car, bapi

def timeout_handler(signum, frame):
    """Handle timeout signal."""
    raise TimeoutError("Operation timed out")

def process_with_timeout(func, *args, timeout=5, **kwargs):
    """Execute a function with a timeout using signal."""
    # Set the signal handler
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(timeout)
    
    try:
        result = func(*args, **kwargs)
        signal.alarm(0)  # Disable the alarm
        return result
    except TimeoutError:
        return "Operation timed out. Please try again."
    finally:
        signal.alarm(0)  # Ensure the alarm is disabled

def main():
    # Load environment variables
    load_dotenv()
    
    print("\n=== GPI Agent Registration and Context Extraction Example ===\n")
    
    # 1. Create an Agent
    print("1. Creating an Agent...")
    agent = create.agent(
        name="DocumentProcessor",
        agent_id="doc_proc_001",
        abilities=["read", "analyze", "summarize", "format"]
    )
    print(f"Created agent: {agent.name} (ID: {agent.agent_id})")
    print(f"Abilities: {', '.join(agent.abilities)}\n")
    
    # 2a. Register Agent Internally
    print("2a. Registering Agent Internally...")
    register.agent(
        name=agent.name,
        agent_id=agent.agent_id,
        abilities=agent.abilities
    )
    print("Agent registered successfully!\n")
    
    # 2b. Register External Agent via HTTP
    print("2b. Registering External Agent via HTTP...")
    external_agent_payload = {
        "name": "ExternalAnalyzer",
        "agent_id": "ext_analyzer_001",
        "abilities": ["analyze", "classify", "recommend"],
        "endpoint": "http://example.com/analyzer"
    }
    
    try:
        register.agent_http(
            endpoint="http://example.com/register",
            payload=external_agent_payload
        )
        print("External agent registered successfully!\n")
    except Exception as e:
        print(f"Note: External agent registration failed (expected as example.com is not real): {str(e)}\n")
    
    # 3. Register LLM
    print("3. Registering LLM...")
    try:
        register.llm(
            name="GPT-4",
            api_key=os.getenv("OPENAI_API_KEY", "your-api-key-here"),
            model_path="gpt-4"
        )
        print("LLM registered successfully!\n")
    except Exception as e:
        print(f"Note: LLM registration failed (expected as API key is not set): {str(e)}\n")
    
    # 4. Context Extraction and Usage
    print("4. Demonstrating Context Extraction and Usage...")
    
    # Example document for context
    document = """
    The Global Positioning System (GPS) is a satellite-based navigation system that provides 
    location and time information in all weather conditions, anywhere on or near the Earth 
    where there is an unobstructed line of sight to four or more GPS satellites.
    """
    
    # Extract context from the document using car function
    print("Extracting context from document...")
    try:
        # Use the car function directly with the document as context
        context = document.strip()
        print(f"Using document as context: {context}\n")
        
        # Use the context with BAPI (with timeout)
        print("Using context with BAPI...")
        message = "What are the key features of this system?"
        
        # Process BAPI call with timeout
        print("Processing message (will timeout after 5 seconds)...")
        response = process_with_timeout(
            bapi,
            context=context,
            message=message,
            timeout=5
        )
        
        print(f"Message: {message}")
        print(f"Response: {response}\n")
    except Exception as e:
        print(f"Error during context processing: {str(e)}\n")
    
    print("=== Example Completed Successfully ===")

if __name__ == "__main__":
    main() 