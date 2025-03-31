#!/usr/bin/env python3
"""
Run the GPI SDK BAPI Server.

This script launches the plain BAPI server without any sample data.
It uses the default settings from the bapi class.
"""

import sys
import os

# Add the parent directory to the path so we can import the gpi package
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import gpi
from gpi.web.server import bapi

def main():
    """
    Main function to run the BAPI server.
    """
    try:
        # Create a server instance with a non-default port to avoid conflicts
        server = bapi(host='127.0.0.1', port=8080)
        
        print("Starting GPI BAPI Server")
        print("=======================\n")
        print(f"BAPI Server running at http://127.0.0.1:8080")
        print("Press Ctrl+C to stop the server")
        
        # Start the server with debug mode and reloader
        server.start(debug=True, use_reloader=True)
        
    except KeyboardInterrupt:
        print("\nServer stopped by user.")
    except Exception as e:
        print(f"Error starting server: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 