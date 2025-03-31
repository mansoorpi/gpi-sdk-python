#!/bin/bash

# Run examples for the GPI SDK
echo "GPI SDK Examples"
echo "================"

# Ensure the script can be executed from any directory
SCRIPT_DIR=$(dirname "$0")
cd "$SCRIPT_DIR" || exit 1

# Check if the package is installed
if ! python -c "import gpi" &> /dev/null; then
    echo "Installing GPI SDK in development mode..."
    pip install -e . || exit 1
fi

# Check for required packages for web interface
if ! python -c "import flask" &> /dev/null; then
    echo "Installing Flask for web interface..."
    pip install flask || exit 1
fi

echo -e "\nChoose an example to run:"
echo "1. Basic usage"
echo "2. HTTP integration"
echo "3. BAPI UI simulation"
echo "4. Run tests"
echo "5. Web interface"
echo "q. Quit"

read -p "Enter your choice: " choice

case "$choice" in
    1)
        echo -e "\nRunning basic usage example..."
        python examples/basic_usage.py
        ;;
    2)
        echo -e "\nRunning HTTP integration example..."
        python examples/http_integration.py
        ;;
    3)
        echo -e "\nRunning BAPI UI simulation..."
        python examples/bapi_ui_simulation.py
        ;;
    4)
        echo -e "\nRunning tests..."
        python -m unittest discover -s tests
        ;;
    5)
        echo -e "\nRunning web interface..."
        python examples/run_web_interface.py
        ;;
    q|Q)
        echo "Exiting."
        exit 0
        ;;
    *)
        echo "Invalid choice. Exiting."
        exit 1
        ;;
esac

echo -e "\nExample completed." 