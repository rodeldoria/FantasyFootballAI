from crewai import Crew, Process, Task
from langchain_openai import ChatOpenAI
from ITSMTeamAgen import ITSMTeamAgents
from Agent_Tasks import Agent_Tasks
from Teamagents import Teamagents
from file_io import save_markdown
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get the OpenAI API key from the environment variable
openai_api_key = os.getenv('OPENAI_API_KEY')

# Print the API key to verify it's loaded correctly
print(f"OpenAI API Key: {openai_api_key}")

# Check if the API key is available
if not openai_api_key:
    raise ValueError("OpenAI API key is missing. Please set the environment variable 'OPENAI_API_KEY'.")

# Initialize the OpenAI GPT-4 language model
OpenAIGPT4 = ChatOpenAI(
    api_key=openai_api_key,
    model="gpt-4"
)

# Initialize the agents and tasks
agents = Teamagents()
tasks = Agent_Tasks()

# Instantiate the agents
incident_manager = agents.incident_manager_agent()
change_manager = agents.change_manager_agent()
service_desk_manager = agents.service_desk_manager_agent()
problem_manager = agents.problem_manager_agent()

# Form the crew with all agents
crew = Crew(
    agents=[incident_manager, change_manager, service_desk_manager, problem_manager],
    process=Process.hierarchical,
    manager_llm=OpenAIGPT4,
    verbose=2
)

def interactive_cli():
    print("Welcome to the ITSM Team Interactive CLI")
    selected_agent = None

    while True:
        if not selected_agent:
            print("\nPlease select an agent to interact with (type 'exit' to quit):")
            print("Options: 'Incident Manager', 'Change Manager', 'Service Desk Manager', 'Problem Manager'")

            agent_input = input("Select agent: ").strip().lower()

            if agent_input == 'incident manager':
                selected_agent = incident_manager
                print("Incident Manager selected.")
            elif agent_input == 'change manager':
                selected_agent = change_manager
                print("Change Manager selected.")
            elif agent_input == 'service desk manager':
                selected_agent = service_desk_manager
                print("Service Desk Manager selected.")
            elif agent_input == 'problem manager':
                selected_agent = problem_manager
                print("Problem Manager selected.")
            elif agent_input == 'exit':
                print("Exiting the CLI.")
                break
            else:
                print("Invalid agent. Please try again.")
        else:
            print(f"\nYou are now interacting with the {selected_agent.role}.")
            print("Enter your task or instruction for this agent (type 'back' to select another agent or 'exit' to quit):")

            task_input = input("Enter your instruction: ").strip().lower()

            if task_input == 'back':
                selected_agent = None
                continue
            elif task_input == 'exit':
                print("Exiting the CLI.")
                break
            else:
                result = execute_task(selected_agent, task_input)
                print("Agent's Response:")
                print(result)

def execute_task(agent, task_input):
    # Create a new task with the specified agent and input
    task = Task(
        role=f"Task for {agent.role}",
        goal=task_input,
        agent=agent,
        allow_delegation=True,
        verbose=True,
        max_iter=10
    )
    crew.tasks = [task]  # Assign the new task to the crew
    results = crew.kickoff(inputs={})
    return results

if __name__ == "__main__":
    interactive_cli()

