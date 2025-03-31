"""
Web server implementation for the GPI SDK.
"""

import os
import json
import threading
from flask import Flask, render_template, request, jsonify, redirect, url_for

import gpi

class bapi:
    """
    Web server for the GPI SDK providing a browser-based interface.
    """
    
    def __init__(self, host='127.0.0.1', port=5000):
        """
        Initialize the web server.
        
        Args:
            host (str): Host address to bind to
            port (int): Port to listen on
        """
        self.host = host
        self.port = port
        self.app = Flask(__name__,
                        template_folder=os.path.join(os.path.dirname(__file__), 'templates'),
                        static_folder=os.path.join(os.path.dirname(__file__), 'static'))
        self.register_routes()
        self.server_thread = None
        self.running = False
        
    def register_routes(self):
        """Register the Flask routes."""
        
        @self.app.route('/')
        def index():
            """Main dashboard page."""
            return render_template('index.html')
        
        @self.app.route('/agents')
        def agents():
            """Agent management page."""
            return render_template('agents.html')
        
        @self.app.route('/llms')
        def llms():
            """LLM management page."""
            return render_template('llms.html')
        
        @self.app.route('/workflows')
        def workflows():
            """Workflow management page."""
            return render_template('workflows.html')
        
        @self.app.route('/documentation')
        def documentation():
            """Documentation page."""
            return render_template('documentation.html')
        
        @self.app.route('/api/agents', methods=['GET'])
        def get_agents():
            """API endpoint to get all agents."""
            agents_dict = {}
            for agent_id, agent in gpi._registry.agents.items():
                agents_dict[agent_id] = {
                    'name': agent.name,
                    'id': agent.agent_id,
                    'abilities': agent.abilities,
                    'active': agent.is_active(),
                    'type': agent.agent_type,
                    'external_endpoint': agent.external_endpoint
                }
            return jsonify(agents_dict)
        
        @self.app.route('/api/agents', methods=['POST'])
        def create_agent():
            """API endpoint to create a new agent."""
            data = request.json
            name = data.get('name')
            agent_id = data.get('id')
            abilities = data.get('abilities', [])
            agent_type = data.get('type', 'internal')
            external_endpoint = data.get('external_endpoint')
            api_key = data.get('api_key')
            
            if not name or not agent_id:
                return jsonify({'error': 'Name and ID are required'}), 400
            
            if agent_type == 'external' and not external_endpoint:
                return jsonify({'error': 'External agents require an external_endpoint'}), 400
            
            if agent_type == 'external':
                agent = gpi.create.external_agent(name, agent_id, abilities, external_endpoint, api_key)
            else:
                agent = gpi.create.agent(name, agent_id, abilities)
                
            return jsonify({
                'name': agent.name,
                'id': agent.agent_id,
                'abilities': agent.abilities,
                'active': agent.is_active(),
                'type': agent.agent_type,
                'external_endpoint': agent.external_endpoint
            })
        
        @self.app.route('/api/agents/<agent_id>', methods=['DELETE'])
        def delete_agent(agent_id):
            """API endpoint to delete an agent."""
            agent = gpi._registry.get_agent(agent_id)
            if not agent:
                return jsonify({'error': 'Agent not found'}), 404
            
            # For now, we just deactivate the agent as there's no direct delete method
            gpi._registry.deactivate_agent(agent_id)
            return jsonify({'success': True})
        
        @self.app.route('/api/llms', methods=['GET'])
        def get_llms():
            """API endpoint to get all LLMs."""
            return jsonify(gpi._registry.llms)
        
        @self.app.route('/api/llms', methods=['POST'])
        def create_llm():
            """API endpoint to create a new LLM."""
            data = request.json
            name = data.get('name')
            api_key = data.get('api_key')
            model_path = data.get('model_path')
            config = data.get('config', {})
            
            if not name or not api_key:
                return jsonify({'error': 'Name and API key are required'}), 400
            
            llm = gpi.register.llm(name, api_key, model_path, config)
            return jsonify(llm)
        
        @self.app.route('/api/llms/<llm_name>', methods=['DELETE'])
        def delete_llm(llm_name):
            """API endpoint to delete an LLM."""
            llm = gpi._registry.get_llm(llm_name)
            if not llm:
                return jsonify({'error': 'LLM not found'}), 404
            
            # For now, we just deactivate the LLM
            gpi._registry.deactivate_llm(llm_name)
            return jsonify({'success': True})
        
        @self.app.route('/api/bapi', methods=['POST'])
        def bapi_endpoint():
            """API endpoint for BAPI operations."""
            data = request.json
            context = data.get('context')
            message = data.get('message')
            user_id = data.get('user_id', 'default')
            use_llm = data.get('use_llm', False)
            
            if not message:
                return jsonify({'error': 'Message is required'}), 400
            
            try:
                # Debug info
                print(f"\n=== BAPI Request ===")
                print(f"Message: {message}")
                print(f"Context: {context}")
                print(f"User ID: {user_id}")
                print(f"Use LLM: {use_llm}")
                
                # Get information about registered agents
                active_agents = gpi._registry.get_active_agents()
                print(f"Active Agents: {[f'{a.name} ({a.agent_id})' for a in active_agents]}")
                
                # Get information about weather agents specifically
                weather_agents = gpi._registry.get_agents_by_ability('weather')
                print(f"Weather Agents: {[f'{a.name} ({a.agent_id})' for a in weather_agents]}")
                
                # Context is optional now - will be auto-extracted if not provided
                response = gpi.bapi(context, message, user_id, use_llm)
                
                # If context was auto-extracted, include it in the response
                current_context = gpi.get_context(user_id)
                print(f"Final Context: {current_context}")
                print(f"Response: {response}")
                print(f"=== End of Request ===\n")
                
                return jsonify({
                    'response': response,
                    'context': current_context,
                    'auto_extracted': context is None and current_context is not None
                })
            except Exception as e:
                import traceback
                error_msg = f"Error in BAPI processing: {str(e)}\n{traceback.format_exc()}"
                print(error_msg)
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/car', methods=['POST'])
        def car_endpoint():
            """API endpoint for context-aware responses."""
            data = request.json
            context = data.get('context')
            message = data.get('message')
            user_id = data.get('user_id', 'default')
            use_llm = data.get('use_llm', False)
            
            if not message:
                return jsonify({'error': 'Message is required'}), 400
            
            try:
                # Context is optional now - will be auto-extracted if not provided
                response = gpi.car(context, message, user_id, use_llm)
                
                # If context was auto-extracted, include it in the response
                current_context = gpi.get_context(user_id)
                
                return jsonify({
                    'response': response,
                    'context': current_context,
                    'auto_extracted': context is None and current_context is not None
                })
            except Exception as e:
                import traceback
                error_msg = f"Error in CAR processing: {str(e)}\n{traceback.format_exc()}"
                print(error_msg)
                return jsonify({'error': str(e)}), 500
            
        @self.app.route('/api/context', methods=['GET'])
        def get_context():
            """API endpoint to get the current context for a user."""
            user_id = request.args.get('user_id', 'default')
            context = gpi.get_context(user_id)
            
            return jsonify({
                'context': context,
                'user_id': user_id
            })
            
        @self.app.route('/api/context', methods=['POST'])
        def set_context():
            """API endpoint to manually set the context for a user."""
            data = request.json
            context = data.get('context')
            user_id = data.get('user_id', 'default')
            
            if not context:
                return jsonify({'error': 'Context is required'}), 400
            
            gpi._context_manager.set_context(user_id, context)
            
            return jsonify({
                'success': True,
                'context': context,
                'user_id': user_id
            })
            
        @self.app.route('/api/context', methods=['DELETE'])
        def clear_context():
            """API endpoint to clear the context for a user."""
            user_id = request.args.get('user_id', 'default')
            
            gpi.clear_context(user_id)
            
            return jsonify({
                'success': True,
                'user_id': user_id
            })
            
        @self.app.route('/api/context/history', methods=['GET'])
        def get_context_history():
            """API endpoint to get the context history for a user."""
            user_id = request.args.get('user_id', 'default')
            limit = request.args.get('limit')
            
            if limit:
                try:
                    limit = int(limit)
                except ValueError:
                    return jsonify({'error': 'Limit must be an integer'}), 400
            
            history = gpi.get_context_history(user_id, limit)
            
            return jsonify({
                'history': history,
                'user_id': user_id
            })
        
        @self.app.route('/api/workflow', methods=['POST'])
        def execute_workflow():
            """API endpoint to execute a workflow between agents."""
            data = request.json
            workflow_steps = data.get('steps', [])
            initial_context = data.get('initial_context')
            initial_message = data.get('initial_message', '')
            user_id = data.get('user_id', 'default')
            use_llm = data.get('use_llm', False)
            
            if not workflow_steps:
                return jsonify({'error': 'Workflow steps are required'}), 400
                
            if not initial_message:
                return jsonify({'error': 'Initial message is required'}), 400
            
            # Handle automatic context extraction if needed
            auto_extracted = False
            if initial_context is None:
                # Get the LLM if available and requested
                llm = gpi._registry.get_llm("default") if use_llm else None
                
                # Extract and update context
                initial_context = gpi._context_manager.extract_and_update_context(
                    initial_message, user_id, use_llm, llm
                )
                auto_extracted = True
            
            results = []
            current_context = initial_context
            current_message = initial_message
            
            for step in workflow_steps:
                agent_id = step.get('agent_id')
                operation = step.get('operation', 'process')
                
                agent = gpi._registry.get_agent(agent_id)
                if not agent:
                    results.append({
                        'error': f'Agent {agent_id} not found',
                        'step': step
                    })
                    continue
                
                try:
                    if operation == 'process':
                        response = agent.process_message(current_context, current_message)
                    else:
                        # Can add other operations like transform, etc.
                        response = f"Unknown operation: {operation}"
                    
                    results.append({
                        'agent_id': agent_id,
                        'operation': operation,
                        'input': current_message,
                        'output': response
                    })
                    
                    # The output of this step becomes the input for the next step
                    current_message = response
                    
                except Exception as e:
                    results.append({
                        'error': str(e),
                        'step': step
                    })
            
            response_data = {
                'workflow_results': results,
                'final_output': current_message
            }
            
            # Include the extracted context information if auto-extracted
            if auto_extracted:
                response_data['auto_extracted_context'] = initial_context
                response_data['auto_extracted'] = True
            
            return jsonify(response_data)
        
        @self.app.route('/api/debug', methods=['GET'])
        def debug_info():
            """API endpoint to get debug information."""
            # Get information about registered agents
            agents_info = []
            for agent_id, agent in gpi._registry.agents.items():
                agents_info.append({
                    'name': agent.name,
                    'id': agent.agent_id,
                    'abilities': agent.abilities,
                    'active': agent.is_active(),
                    'type': agent.agent_type,
                    'external_endpoint': agent.external_endpoint
                })
            
            # Get information about LLMs
            llms_info = list(gpi._registry.llms.values())
            
            # Get active agents
            active_agents = [f"{a.name} ({a.agent_id})" for a in gpi._registry.get_active_agents()]
            
            # Get agents by ability
            weather_agents = [f"{a.name} ({a.agent_id})" for a in gpi._registry.get_agents_by_ability("weather")]
            
            return jsonify({
                'agents': agents_info,
                'llms': llms_info,
                'active_agents': active_agents,
                'weather_agents': weather_agents
            })
    
    def start(self, debug=False, use_reloader=False):
        """
        Start the web server.
        
        Args:
            debug (bool): Whether to run Flask in debug mode
            use_reloader (bool): Whether to use Flask's reloader
            
        Returns:
            bool: True if server started successfully, False otherwise
        """
        if self.running:
            print("Server is already running.")
            return False
        
        if use_reloader:
            # Run in the main thread with reloader
            self.running = True
            self.app.run(host=self.host, port=self.port, debug=debug, use_reloader=use_reloader)
            return True
        
        # Run in a separate thread without reloader
        def run_server():
            self.app.run(host=self.host, port=self.port, debug=debug, use_reloader=False, threaded=True)
        
        self.server_thread = threading.Thread(target=run_server)
        self.server_thread.daemon = True
        self.server_thread.start()
        self.running = True
        
        print(f"GPI Web interface started at http://{self.host}:{self.port}/")
        return True
    
    def stop(self):
        """
        Stop the web server.
        
        Returns:
            bool: True if server stopped successfully, False otherwise
        """
        if not self.running:
            print("Server is not running.")
            return False
        
        self.running = False
        # There's no clean way to stop a Flask server in a separate thread
        # In a production setting, use a proper WSGI server like Gunicorn
        print("Please terminate the process to stop the server.")
        return True 