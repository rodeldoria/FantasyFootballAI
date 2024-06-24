from flask import jsonify
from TeamAgents import TeamAgents

# Initialize our custom classes for agents
agents = TeamAgents()

agent_map = {
    'Release Manager': {
        'name': 'Release Manager',
        'role': 'Manage Releases',
        'goal': 'Ensure smooth release of new features',
        'description': 'Oversee the release process to ensure new features are deployed smoothly and efficiently.',
        'expected_output': 'Successful release of features',
        'max_iter': 10,
        'allow_delegation': True,
        'verbose': True,
        'is_master': False,
        'agent': agents.release_manager_agent()
    },
    'Problem Manager': {
        'name': 'Problem Manager',
        'role': 'Manage Problems',
        'goal': 'Identify and resolve root causes of incidents',
        'description': 'Investigate and resolve the root causes of incidents to prevent future occurrences.',
        'expected_output': 'Resolved root causes of incidents',
        'max_iter': 10,
        'allow_delegation': True,
        'verbose': True,
        'is_master': False,
        'agent': agents.problem_manager_agent()
    },
    'Incident Manager': {
        'name': 'Incident Manager',
        'role': 'Handle Incidents',
        'goal': 'Resolve IT incidents efficiently',
        'description': 'Investigate and resolve IT incidents to minimize disruption to services.',
        'expected_output': 'Resolved incidents and improved service continuity',
        'max_iter': 10,
        'allow_delegation': True,
        'verbose': True,
        'is_master': False,
        'agent': agents.incident_manager_agent()
    },
    'Change Manager': {
        'name': 'Change Manager',
        'role': 'Manage IT changes efficiently',
        'goal': 'Manage IT changes efficiently',
        'description': 'You are responsible for managing and coordinating changes in the IT infrastructure, ensuring minimal disruption.',
        'expected_output': 'Successful implementation of changes with minimal disruption',
        'max_iter': 15,
        'allow_delegation': True,
        'verbose': True,
        'is_master': False,
        'agent': agents.change_manager_agent()
    },
    'Asset Manager': {
        'name': 'Asset Manager',
        'role': 'Manage IT Assets',
        'goal': 'Ensure accurate tracking and management of IT assets',
        'description': 'Track and manage IT assets to ensure accurate records and efficient use of resources.',
        'expected_output': 'Accurate IT asset records and efficient resource use',
        'max_iter': 10,
        'allow_delegation': True,
        'verbose': True,
        'is_master': False,
        'agent': agents.asset_manager_agent()
    },
    'Configuration Manager': {
        'name': 'Configuration Manager',
        'role': 'Manage Configurations',
        'goal': 'Ensure proper configuration of IT systems',
        'description': 'Manage the configurations of IT systems to ensure they are set up correctly and consistently.',
        'expected_output': 'Properly configured IT systems',
        'max_iter': 10,
        'allow_delegation': True,
        'verbose': True,
        'is_master': False,
        'agent': agents.configuration_manager_agent()
    },
    'Master Agent': {
        'name': 'Master Agent',
        'role': 'Oversee all operations',
        'goal': 'Provide a high-level overview and coordination of all ITSM operations',
        'description': 'Coordinate the activities of all other agents to ensure cohesive and efficient ITSM operations.',
        'expected_output': 'Coordinated and efficient ITSM operations',
        'max_iter': 20,
        'allow_delegation': True,
        'verbose': True,
        'is_master': True,
        'agent': agents.master_agent()
    }
}

def create_agent(agent_data):
    agent = {
        'name': agent_data['name'],
        'role': agent_data['role'],
        'goal': agent_data['goal'],
        'description': agent_data['description'],
        'expected_output': agent_data['expected_output'],
        'max_iter': agent_data['max_iter'],
        'allow_delegation': agent_data['allow_delegation'],
        'verbose': agent_data['verbose'],
        'is_master': agent_data['is_master'],
        'agent': agents.create_agent(agent_data['role'], agent_data['goal'], agent_data['description'], agent_data['expected_output'], agent_data['max_iter'], agent_data['allow_delegation'], agent_data['verbose'])
    }
    agent_map[agent_data['name']] = agent
    return jsonify(success=True)

def add_agent(agent_data):
    return create_agent(agent_data)

def remove_agent(agent_name):
    if agent_name in agent_map:
        del agent_map[agent_name]
        return jsonify(success=True)
    return jsonify(success=False, error="Agent not found")

def list_agents():
    return jsonify(agents=[agent for agent in agent_map.values()])
