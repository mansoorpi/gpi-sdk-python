#!/usr/bin/env python3
"""
Run the BAPI server with external agent support and documentation.
This provides a simple way to test our updated features.
"""

import sys
import os
import signal

# Ensure the parent directory is in the path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gpi.web.server import bapi

def main():
    """
    Initialize and run the BAPI server with documentation and external agent support.
    """
    try:
        print("Starting BAPI Server with documentation and external agent support...")
        print("Features available:")
        print("- Register internal agents")
        print("- Register external agents with API endpoints")
        print("- Documentation tab with code examples")
        print("- View agent details and test responses")
        print("\nNavigate to http://127.0.0.1:5000 to access the interface")
        
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