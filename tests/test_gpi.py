#!/usr/bin/env python3
"""
Unit tests for the GPI SDK.
"""

import sys
import os
import unittest
from unittest.mock import patch, MagicMock

# Add the parent directory to the path so we can import the gpi package
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import gpi
from gpi.core.agent import Agent
from gpi.core.registry import Registry
from gpi.core.broker import Broker
from gpi.core.context import ContextManager

class TestAgent(unittest.TestCase):
    """Tests for the Agent class."""
    
    def test_agent_creation(self):
        """Test creating an agent with specific attributes."""
        agent = Agent("TestAgent", "test001", ["talk", "think"])
        
        self.assertEqual(agent.name, "TestAgent")
        self.assertEqual(agent.agent_id, "test001")
        self.assertEqual(agent.abilities, ["talk", "think"])
        self.assertTrue(agent.active)
    
    def test_has_ability(self):
        """Test checking if an agent has a specific ability."""
        agent = Agent("TestAgent", "test001", ["talk", "think"])
        
        self.assertTrue(agent.has_ability("talk"))
        self.assertTrue(agent.has_ability("think"))
        self.assertFalse(agent.has_ability("learn"))
    
    def test_add_ability(self):
        """Test adding an ability to an agent."""
        agent = Agent("TestAgent", "test001", ["talk"])
        
        self.assertTrue(agent.add_ability("think"))
        self.assertEqual(agent.abilities, ["talk", "think"])
        
        # Adding an existing ability should return False
        self.assertFalse(agent.add_ability("talk"))
        self.assertEqual(agent.abilities, ["talk", "think"])
    
    def test_remove_ability(self):
        """Test removing an ability from an agent."""
        agent = Agent("TestAgent", "test001", ["talk", "think"])
        
        self.assertTrue(agent.remove_ability("talk"))
        self.assertEqual(agent.abilities, ["think"])
        
        # Removing a non-existent ability should return False
        self.assertFalse(agent.remove_ability("learn"))
        self.assertEqual(agent.abilities, ["think"])
    
    def test_activate_deactivate(self):
        """Test activating and deactivating an agent."""
        agent = Agent("TestAgent", "test001", ["talk", "think"])
        
        self.assertTrue(agent.is_active())
        
        agent.deactivate()
        self.assertFalse(agent.is_active())
        
        agent.activate()
        self.assertTrue(agent.is_active())
    
    def test_process_message(self):
        """Test agent's ability to process a message."""
        agent = Agent("TestAgent", "test001", ["talk", "think"])
        
        response = agent.process_message("test_context", "Hello")
        self.assertIn("TestAgent", response)
        self.assertIn("Hello", response)
        self.assertIn("test_context", response)

class TestRegistry(unittest.TestCase):
    """Tests for the Registry class."""
    
    def test_register_agent(self):
        """Test registering an agent in the registry."""
        registry = Registry()
        agent = Agent("TestAgent", "test001", ["talk"])
        
        self.assertTrue(registry.register_agent(agent))
        self.assertEqual(registry.get_agent("test001"), agent)
        
        # Registering the same agent ID again should return False
        self.assertFalse(registry.register_agent(agent))
    
    def test_register_llm(self):
        """Test registering an LLM in the registry."""
        registry = Registry()
        llm_info = registry.register_llm("TestLLM", "test_api_key", "/path/to/model")
        
        self.assertEqual(llm_info["name"], "TestLLM")
        self.assertEqual(llm_info["api_key"], "test_api_key")
        self.assertEqual(llm_info["model_path"], "/path/to/model")
        self.assertTrue(llm_info["active"])
        
        stored_llm = registry.get_llm("TestLLM")
        self.assertEqual(stored_llm, llm_info)
    
    def test_get_agents_by_ability(self):
        """Test getting agents by ability."""
        registry = Registry()
        
        agent1 = Agent("Agent1", "a001", ["talk", "think"])
        agent2 = Agent("Agent2", "a002", ["talk", "learn"])
        agent3 = Agent("Agent3", "a003", ["think", "learn"])
        
        registry.register_agent(agent1)
        registry.register_agent(agent2)
        registry.register_agent(agent3)
        
        talk_agents = registry.get_agents_by_ability("talk")
        self.assertEqual(len(talk_agents), 2)
        self.assertIn(agent1, talk_agents)
        self.assertIn(agent2, talk_agents)
        
        learn_agents = registry.get_agents_by_ability("learn")
        self.assertEqual(len(learn_agents), 2)
        self.assertIn(agent2, learn_agents)
        self.assertIn(agent3, learn_agents)
        
        # Test with inactive agent
        agent2.deactivate()
        talk_agents = registry.get_agents_by_ability("talk")
        self.assertEqual(len(talk_agents), 1)
        self.assertIn(agent1, talk_agents)

class TestContextManager(unittest.TestCase):
    """Tests for the ContextManager class."""
    
    def test_set_get_context(self):
        """Test setting and getting context."""
        ctx_manager = ContextManager()
        
        self.assertIsNone(ctx_manager.get_context())
        
        ctx_manager.set_context("test_context")
        self.assertEqual(ctx_manager.get_context(), "test_context")
    
    def test_context_history(self):
        """Test context history management."""
        ctx_manager = ContextManager()
        
        # Initially, history should be empty
        self.assertEqual(len(ctx_manager.get_context_history()), 0)
        
        # Setting multiple contexts should add them to history
        ctx_manager.set_context("context1")
        ctx_manager.set_context("context2")
        
        history = ctx_manager.get_context_history()
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0], "context1")
        
        # Clear and restore should work
        ctx_manager.clear_context()
        self.assertIsNone(ctx_manager.get_context())
        
        restored = ctx_manager.restore_previous_context()
        self.assertTrue(restored)
        self.assertEqual(ctx_manager.get_context(), "context1")
        
        # History should now be empty
        self.assertEqual(len(ctx_manager.get_context_history()), 0)

class TestBroker(unittest.TestCase):
    """Tests for the Broker class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.registry = Registry()
        self.broker = Broker(self.registry)
        
        # Register an agent
        self.agent = Agent("TestAgent", "test001", ["talk", "think"])
        self.registry.register_agent(self.agent)
        
        # Register an LLM
        self.llm = self.registry.register_llm("TestLLM", "test_key")
    
    def test_process_message_no_context(self):
        """Test processing a message without setting context."""
        response = self.broker.process_message("Hello")
        self.assertIn("Error", response)
        self.assertIn("No context", response)
    
    def test_process_message_with_context(self):
        """Test processing a message with context."""
        # Set a context that matches the agent's abilities
        self.broker.set_context("talk about something")
        
        response = self.broker.process_message("Hello")
        self.assertIn("TestAgent", response)
        self.assertIn("Hello", response)
    
    def test_generate_response(self):
        """Test generating a context-aware response."""
        # Set a context
        self.broker.set_context("test context")
        
        response = self.broker.generate_response("Hello")
        self.assertIn("Context-Aware Response", response)

class TestGPIInterface(unittest.TestCase):
    """Tests for the GPI interface functions."""
    
    def test_create_agent(self):
        """Test creating an agent through the interface."""
        agent = gpi.create.agent("InterfaceAgent", "i001", ["talk"])
        
        self.assertEqual(agent.name, "InterfaceAgent")
        self.assertEqual(agent.agent_id, "i001")
        self.assertEqual(agent.abilities, ["talk"])
    
    def test_register_agent(self):
        """Test registering an agent through the interface."""
        agent = gpi.register.agent("RegisteredAgent", "r001", ["think"])
        
        self.assertEqual(agent.name, "RegisteredAgent")
        self.assertEqual(agent.agent_id, "r001")
        self.assertEqual(agent.abilities, ["think"])
    
    def test_register_llm(self):
        """Test registering an LLM through the interface."""
        llm = gpi.register.llm("InterfaceLLM", "interface_key")
        
        self.assertEqual(llm["name"], "InterfaceLLM")
        self.assertEqual(llm["api_key"], "interface_key")
    
    @patch('requests.post')
    def test_register_agent_http(self, mock_post):
        """Test registering an agent via HTTP."""
        # Set up the mock
        mock_response = MagicMock()
        mock_response.json.return_value = {"status": "success"}
        mock_post.return_value = mock_response
        
        response = gpi.register.agent_http("http://example.com", {"name": "HttpAgent"})
        
        # Verify the mock was called correctly
        mock_post.assert_called_once()
        self.assertEqual(response, {"status": "success"})
    
    def test_car_and_bapi(self):
        """Test the car and bapi functions."""
        # Create an agent first so there's something to respond
        agent = gpi.create.agent("CarAgent", "car001", ["talk"])
        
        # Test car
        car_response = gpi.car("test_context", "Hello from CAR")
        self.assertIn("Context-Aware Response", car_response)
        
        # Test bapi
        bapi_response = gpi.bapi("bapi_context", "Hello from BAPI")
        self.assertIn("CarAgent", bapi_response)

if __name__ == "__main__":
    unittest.main() 