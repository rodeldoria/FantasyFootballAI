import re
import unittest
from agent_transformer import transform_gpt_response
from gpt import generate_gpt_response

class TestAgentTransformer(unittest.TestCase):

    def setUp(self):
        self.prompt_template = """
You are a skilled IT service management AI, capable of configuring agents to manage various roles within an IT department. I need you to generate detailed information for an agent that will be added to our IT service management system. Please provide the following details for the agent:

1. Name: The official title of the agent.
2. Role: A brief description of the agent's responsibilities.
3. Goal: The primary objective of the agent.
4. Description: Detailed description of the agent's duties.
5. Expected Output: The expected results or outcomes of the agent's work.
6. Max Iterations: The maximum number of iterations the agent should perform (1-10).
7. Allow Delegation: Whether the agent can delegate tasks to others (True or False).
8. Verbose: Whether the agent should provide detailed output (True or False).
9. Is Master: Indicates if this is the master agent responsible for overseeing other agents (True or False).

Based on your instructions, here is the configuration for the new agent:
"""

    def test_transform_gpt_response(self):
        # Step 1: Prompt user for instructions
        instructions = input("Please enter your instructions for the new agent: ")
        
        # Step 2: Combine template and instructions
        prompt = self.prompt_template + instructions
        print("\nStep 2: Generated prompt for GPT:\n")
        print(prompt)
        
        # Step 3: Generate GPT response
        print("\nStep 3: Generating GPT response...\n")
        gpt_response = generate_gpt_response([{"role": "user", "content": prompt}])
        print("GPT Response:", gpt_response)
        
        # Step 4: Transform GPT response
        print("\nStep 4: Transforming GPT response into agent attributes.")
        agent = transform_gpt_response(gpt_response)

        # Step 5: Print transformed agent attributes
        print("\nStep 5: Transformed agent attributes:")
        print(agent)

        # Step 6: Assert transformed agent attributes
        print("\nStep 6: Asserting transformed agent attributes.")
        self.assertNotEqual(agent.name, "N/A")
        self.assertNotEqual(agent.role, "N/A")
        self.assertNotEqual(agent.goal, "N/A")
        self.assertNotEqual(agent.description, "N/A")
        self.assertNotEqual(agent.expected_output, "N/A")
        self.assertTrue(1 <= agent.max_iter <= 10)
        self.assertIsInstance(agent.allow_delegation, bool)
        self.assertIsInstance(agent.verbose, bool)
        self.assertIsInstance(agent.is_master, bool)

if __name__ == '__main__':
    unittest.main()
