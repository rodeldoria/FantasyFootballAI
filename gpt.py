import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from matplotlib import pyplot as plt
import pandas as pd
import json

load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
openai_api = ChatOpenAI(api_key=OPENAI_API_KEY, model="gpt-4")

def parse_instructions(instructions):
    prompt = [
        {"role": "system", "content": "You are a skilled IT service management AI, capable of understanding detailed instructions to configure an agent."},
        {"role": "user", "content": f"Based on the following instructions, configure an agent: {instructions}"}
    ]

    response = generate_gpt_response(prompt)

    # Simulated parsing of the response to match the expected fields
    parsed_response = {
        "name": response.get("name", "Undefined Name"),
        "role": response.get("role", "Undefined Role"),
        "goal": response.get("goal", "Undefined Goal"),
        "description": response.get("description", "Undefined Description"),
        "expected_output": response.get("expected_output", "Undefined Output"),
        "max_iter": response.get("max_iter", 5),
        "allow_delegation": response.get("allow_delegation", "False"),
        "verbose": response.get("verbose", "False"),
        "is_master": response.get("is_master", "False")
    }

    return parsed_response

def generate_gpt_response(prompt):
    response = openai_api.invoke(prompt)
    print("GPT response:", response.content.strip())  # Log response

    return response.content.strip()

def format_output(response):
    formatted_response = response.replace('\n', '<br>')
    return formatted_response

def execute_task(agent_map, selected_agents, instructions, collaborative=False):
    agents = [agent_map[agent] for agent in selected_agents]
    response_set = set()
    agent_responses = []

    for agent in agents:
        prompt = [
            {"role": "system", "content": f"You are the {agent['role']}."},
            {"role": "user", "content": f"Instructions: {instructions}. Provide a detailed plan including risks, concerns, and blockers."}
        ]
        print("Agent prompt:", prompt)  # Log prompt
        response = generate_gpt_response(prompt)
        formatted_response = format_output(response)
        if formatted_response not in response_set:
            response_set.add(formatted_response)
            agent_responses.append({
                "role": agent['role'],
                "response": formatted_response
            })

    combined_response = "\n\n".join([f"<div class='card mb-3'><div class='card-header'>{agent_response['role']} Response</div><div class='card-body'><p>{agent_response['response']}</p></div></div>" for agent_response in agent_responses])
    agent_roles = [agent['role'] for agent in agents]

    if collaborative:
        manager_prompt = [
            {"role": "system", "content": f"You are the Manager Agent."},
            {"role": "user", "content": f"Here are the responses from different agents:\n\n{combined_response}\n\nProvide a detailed analysis and summary including risks, concerns, and blockers."}
        ]
        print("Manager prompt:", manager_prompt)  # Log prompt
        manager_response = generate_gpt_response(manager_prompt)

        return {
            "agent_responses": agent_responses,
            "manager_response": format_output(manager_response),
            "agent_roles": agent_roles
        }
    else:
        return {
            "agent_responses": agent_responses,
            "manager_response": "",
            "agent_roles": agent_roles
        }

def generate_chart_data(data, analysis_prompt):
    """
    Generate chart data using GPT-4 based on the provided data and analysis prompt.
    The response should be a JSON string that can be parsed into chart data.
    """
    prompt = [
        {"role": "system", "content": "You are a data analyst."},
        {"role": "user", "content": f"Here is the data: {data}. {analysis_prompt}"}
    ]
    response = generate_gpt_response(prompt)
    try:
        chart_data = json.loads(response)
        return chart_data
    except json.JSONDecodeError:
        raise ValueError("Failed to parse chart data from GPT response")

def create_visualization(data, chart_type="bar"):
    """
    Create a visualization from the data using Matplotlib.
    """
    df = pd.DataFrame(data)
    
    plt.figure(figsize=(10, 6))
    
    if chart_type == "bar":
        df.plot(kind="bar")
    elif chart_type == "line":
        df.plot(kind="line")
    elif chart_type == "pie":
        df.plot(kind="pie", subplots=True)
    
    plt.tight_layout()
    plt.savefig('/path/to/save/plot.png')
    plt.close()
    return '/path/to/save/plot.png'
