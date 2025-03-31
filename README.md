# GPI - SDK Framework for AI Agentic Development

A clean SDK framework for AI agentic development, enabling the creation of agents, registration of AI/LLMs, handling context-aware responses, and integration with external systems through HTTP endpoints.

## Features

- Create and register agents
- Register AI/LLM models
- Generate context-aware responses
- Built-in broker API for agent-LLM communication
- HTTP endpoint integration
- Simulation of BAPI UI for agent registration
- Web interface for managing agents, LLMs, and workflows

## Installation

```bash
pip install -e .
```

## Basic Usage Examples

### Creating an Agent

```python
import gpi

# Create an agent
agent = gpi.create.agent("AgentX", "001", ["talk", "think", "learn"])
```

### Registering an LLM

```python
# Register an LLM
gpi.register.llm("GPT-4", "api_key_here", "/path/to/gpt4")
```

### Context-Aware Response

```python
# Get a context-aware response
response = gpi.car("weather_context", "What is the weather today?")
```

### Using Broker API

```python
# Use the broker API
response = gpi.bapi("weather_context", "What is the weather today?")
```

### HTTP Registration

```python
# Register an agent via HTTP
gpi.register.agent_http("http://example.com/register", 
                        {"name": "AgentY", "id": "002", "abilities": ["talk"]})
```

## Web Interface

The GPI SDK includes a web interface for managing agents, LLMs, and creating workflows.

### Running the Web Interface

```bash
python examples/run_web_interface.py
```

This will start the web interface on http://127.0.0.1:5000.

### Web Interface Features

- **Dashboard**: Overview of registered agents and LLMs with quick registration forms
- **Agents Management**: Create, view, and manage agents
- **LLMs Management**: Register and manage LLM configurations
- **Workflow Builder**: Create multi-agent workflows with a visual builder
- **Testing Interface**: Test agents with different contexts and messages

### Multi-Agent Workflows

The web interface allows you to create workflows where multiple agents work together to accomplish a task. For example:

1. A document creation agent generates content based on a prompt
2. A formatting agent structures the content appropriately
3. A PDF conversion agent converts the formatted content to a PDF

## Running Examples

Use the provided script to run various examples:

```bash
./run_examples.sh
```

This will present a menu with options to run:

1. Basic usage example
2. HTTP integration example
3. BAPI UI simulation
4. Run tests
5. Web interface

## Documentation

Each component and function includes comprehensive docstrings explaining its purpose, parameters, and return values.

## Development

To contribute to the development:

1. Clone the repository
2. Install in development mode: `pip install -e .`
3. Run tests: `python -m unittest discover -s tests` 