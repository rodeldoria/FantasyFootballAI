from crewai import Crew, Process, Task
from langchain.chat_models import ChatOpenAI
from ITSMTeamAgen import ITSMTeamAgents
from Agent_Tasks import Agent_Tasks
# from file_io import save_markdown
from dotenv import load_dotenv
import os
import json

from Teamagents import Teamagents

# Load environment variables from .env file
load_dotenv()

# Get the OpenAI API key from the environment variable
openai_api_key = os.getenv('OPENAI_API_KEY')

# Print the API key to verify it's loaded correctly
print(f"OpenAI API Key: {openai_api_key}")

# Check if the API key is available; if not, show an error
if not openai_api_key:
    raise ValueError("OpenAI API key is missing. Please set the environment variable 'OPENAI_API_KEY'.")

# Set up the OpenAI GPT-4 model with our API key
OpenAIGPT4 = ChatOpenAI(
    api_key=openai_api_key,
    model="gpt-4"
)

# Initialize our custom classes for agents and tasks
agents = Teamagents()
tasks = Agent_Tasks()

# Create instances of different agents
incident_manager = agents.incident_manager_agent()
change_manager = agents.change_manager_agent()
service_desk_agent = agents.service_desk_agent()
problem_manager = agents.problem_manager_agent()
release_manager = agents.release_manager_agent()
asset_manager = agents.asset_manager_agent()
configuration_manager = agents.configuration_manager_agent()
case_manager = agents.case_manager_agent()
service_catalog_manager = agents.service_catalog_manager_agent()

# Create instances of different tasks and assign them to agents
handle_incident_task = tasks.handle_incident_task(incident_manager)
manage_change_task = tasks.manage_change_task(change_manager)
support_service_desk_task = tasks.support_service_desk_task(service_desk_agent)
manage_problem_task = tasks.manage_problem_task(problem_manager, [handle_incident_task])
manage_release_task = tasks.manage_release_task(release_manager)
manage_asset_task = tasks.manage_asset_task(asset_manager)
manage_configuration_task = tasks.manage_configuration_task(configuration_manager)
handle_case_task = tasks.handle_case_task(case_manager)
manage_service_catalog_task = tasks.manage_service_catalog_task(service_catalog_manager)

# Combine agents and tasks into a crew, which is managed by the OpenAI GPT-4 model
crew = Crew(
    agents=[
        incident_manager, change_manager, service_desk_agent, problem_manager,
        release_manager, asset_manager, configuration_manager, case_manager,
        service_catalog_manager
    ],
    tasks=[
        handle_incident_task, manage_change_task, support_service_desk_task,
        manage_problem_task, manage_release_task, manage_asset_task,
        manage_configuration_task, handle_case_task, manage_service_catalog_task
    ],
    process=Process.hierarchical,  # Use a hierarchical process for the crew
    manager_llm=OpenAIGPT4,  # Use GPT-4 as the language model manager
    verbose=2  # Set the verbosity level for detailed output
)

def generate_gpt_response(prompt):
    """
    Generate a response from GPT-4 based on the provided prompt.
    """
    response = OpenAIGPT4.invoke(prompt)
    return response.content.strip()

def execute_task(agents, problem, instructions, collaborative=False):
    """
    Create a new task for all agents or a single agent with a specific instruction.
    Generate a detailed project plan using GPT-4.
    """
    # Debug print to confirm task details
    print(f"[DEBUG] Executing task for agents, Problem: {problem}")

    if collaborative:
        all_prompts = []
        for agent in agents:
            prompt = [
                {"role": "system", "content": f"You are the {agent.role}."},
                {"role": "user", "content": f"Here's the problem: {problem}. Instructions: {instructions}. Provide a detailed plan including risks, concerns, and blockers."}
            ]
            all_prompts.append(prompt)
        responses = [generate_gpt_response(prompt) for prompt in all_prompts]
        combined_response = "\n\n".join([f"### {agent.role} Response:\n{response}" for agent, response in zip(agents, responses)])
        agent_roles = [agent.role for agent in agents]
        return f"### Agents Involved:\n{', '.join(agent_roles)}\n\n{combined_response}"
    else:
        # If not collaborative, use the first agent only
        prompt = [
            {"role": "system", "content": f"You are the {agents[0].role}."},
            {"role": "user", "content": f"Here's the problem: {problem}. Instructions: {instructions}. Provide a detailed plan including risks, concerns, and blockers."}
        ]
        response = generate_gpt_response(prompt)
        return f"### Agents Involved:\n{agents[0].role}\n\n### {agents[0].role} Response:\n{response}"

def interactive_cli():
    """
    Provide a simple command-line interface for the user to interact with the ITSM team.
    """
    print("Welcome to the ITSM Team Interactive CLI")
    
    while True:
        # Ask the user whether they want a single agent, all agents, or a custom selection of agents
        mode = input("Do you want a single agent, all agents, or a custom selection of agents to respond? (single/all/custom or 'exit' to quit): ").strip().lower()
        
        if mode == 'exit':
            print("Exiting the CLI.")
            return  # Exit the command-line interface

        collaborative = (mode == 'all')
        
        if mode == 'single':
            # Ask the user to select an agent
            print("Available agents: Incident Manager, Change Manager, Service Desk Agent, Problem Manager, Release Manager, Asset Manager, Configuration Manager, Case Manager, Service Catalog Manager")
            agent_role = input("Select an agent (or 'exit' to quit): ").strip().title()
            
            if agent_role == 'Exit':
                print("Exiting the CLI.")
                return  # Exit the command-line interface

            agent_map = {
                'Incident Manager': incident_manager,
                'Change Manager': change_manager,
                'Service Desk Agent': service_desk_agent,
                'Problem Manager': problem_manager,
                'Release Manager': release_manager,
                'Asset Manager': asset_manager,
                'Configuration Manager': configuration_manager,
                'Case Manager': case_manager,
                'Service Catalog Manager': service_catalog_manager
            }
            
            if agent_role not in agent_map:
                print("Invalid agent selected. Please try again.")
                continue  # Loop back to agent selection

            selected_agents = [agent_map[agent_role]]

        elif mode == 'custom':
            # Ask the user to select multiple agents
            print("Available agents: Incident Manager, Change Manager, Service Desk Agent, Problem Manager, Release Manager, Asset Manager, Configuration Manager, Case Manager, Service Catalog Manager")
            selected_roles = input("Select agents (comma-separated list or 'exit' to quit): ").strip().title().split(',')
            
            if 'Exit' in selected_roles:
                print("Exiting the CLI.")
                return  # Exit the command-line interface

            agent_map = {
                'Incident Manager': incident_manager,
                'Change Manager': change_manager,
                'Service Desk Agent': service_desk_agent,
                'Problem Manager': problem_manager,
                'Release Manager': release_manager,
                'Asset Manager': asset_manager,
                'Configuration Manager': configuration_manager,
                'Case Manager': case_manager,
                'Service Catalog Manager': service_catalog_manager
            }
            
            selected_agents = []
            for role in selected_roles:
                role = role.strip()
                if role in agent_map:
                    selected_agents.append(agent_map[role])
                else:
                    print(f"Invalid agent role '{role}' selected. Please try again.")
                    selected_agents = []  # Clear the list to start over
                    break

            if not selected_agents:
                continue  # Loop back to agent selection

        else:
            selected_agents = [
                incident_manager, change_manager, service_desk_agent, problem_manager,
                release_manager, asset_manager, configuration_manager, case_manager,
                service_catalog_manager
            ]
        
        # Ask the user for a problem statement
        problem = input("What is the problem? (type 'exit' to quit): ").strip()
        
        if problem == 'exit':
            print("Exiting the CLI.")
            return  # Exit the command-line interface
        
        # Ask the user for instructions to solve the problem
        instructions = input("What instructions do you have to solve it? ").strip()
        
        if instructions == 'exit':
            print("Exiting the CLI.")
            return  # Exit the command-line interface
        
        # Execute the task with the provided problem and instructions
        print(f"[DEBUG] Problem: {problem}")
        print(f"[DEBUG] Instructions: {instructions}")
        result = execute_task(selected_agents, problem, instructions, collaborative=collaborative)
        print("Collaborative ITSM Result:")
        print(result)

# Start the command-line interface if this script is run directly
if __name__ == "__main__":
    interactive_cli()
