from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for
from werkzeug.utils import secure_filename
import os
import pandas as pd
from agents import add_agent, remove_agent, agent_map
from gpt import create_visualization, execute_task, generate_chart_data, generate_gpt_response
from slack_utils import send_slack_message, search_slack
from prompt_utils import list_prompts, save_prompt, search_prompts, get_prompt_by_id, update_prompt
from agent_transformer import transform_gpt_response

# Initialize Flask application
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Route to populate agent fields using AI
@app.route('/ai_populate', methods=['POST'])
def ai_populate():
    try:
        data = request.json
        instructions = data.get('instructions')

        print("Received instructions:", instructions)  # Log received instructions

        if not instructions:
            print("No instructions provided")
            return jsonify({"error": "No instructions provided"}), 400

        prompt_template = """
You are a skilled AI, capable of configuring agents to manage various roles within different departments. I need you to generate detailed information for an agent that will be added to our management system. Please provide the following details for the agent:

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

        prompt = prompt_template + instructions

        try:
            gpt_response = generate_gpt_response(prompt)
            print("GPT Response:", gpt_response)

            agent = transform_gpt_response(gpt_response)
            response = {
                "name": agent.name,
                "role": agent.role,
                "goal": agent.goal,
                "description": agent.description,
                "expected_output": agent.expected_output,
                "max_iter": agent.max_iter,
                "allow_delegation": agent.allow_delegation,
                "verbose": agent.verbose,
                "is_master": agent.is_master,
                "success": True
            }
            print("Returning response:", response)  # Log response
            return jsonify(response), 200
        except Exception as e:
            print("Exception occurred:", str(e))  # Log exception
            return jsonify({"error": str(e)}), 500
    except Exception as e:
        print("Failed to parse request data:", str(e))  # Log exception
        return jsonify({"error": "Failed to parse request data"}), 400

# Home route to list all agents
@app.route('/')
def index():
    return render_template('index.html', agents=agent_map.keys())

# Route to add a new agent
@app.route('/add_agent', methods=['GET', 'POST'])
def add_agent_page():
    if request.method == 'POST':
        agent_data = request.form.to_dict()
        add_agent(agent_data)
        return redirect(url_for('index'))
    return render_template('add_agent.html')

# Route to execute a task
@app.route('/execute', methods=['GET', 'POST'])
def execute():
    if request.method == 'POST':
        selected_agents = request.form.getlist('agents')
        instructions = request.form['instructions']
        collaborative = 'collaborative' in request.form

        data_input = request.form.get('dataInput', '')
        file_input = request.files.get('fileInput')

        data = None
        if file_input:
            filename = secure_filename(file_input.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file_input.save(filepath)

            if filename.endswith('.csv'):
                data = pd.read_csv(filepath).to_json()
            elif filename.endswith('.xlsx'):
                data = pd.read_excel(filepath).to_json()

        if not data and data_input:
            data = data_input

        print("Executing task with data:", data)  # Log data
        gpt_output = execute_task(agent_map, selected_agents, instructions, collaborative)

        print("GPT Output:", gpt_output)  # Log GPT output
        return jsonify(output=gpt_output)
    return render_template('execute_task.html', agents=agent_map.keys(), prompts=list_prompts())

# Route to generate chart
@app.route('/generate_chart', methods=['POST'])
def generate_chart():
    data = request.json['data']
    analysis_prompt = request.json['analysis_prompt']
    try:
        chart_data = generate_chart_data(data, analysis_prompt)
        chart_path = create_visualization(chart_data)
        return jsonify(chart_path=chart_path)
    except ValueError as e:
        return jsonify(error=str(e)), 400

# Route to send Slack message
@app.route('/send_slack', methods=['POST'])
def send_slack():
    data = request.json
    message = data['message']
    target = data['target']
    
    try:
        send_slack_message(message, target)
        return jsonify(success=True)
    except Exception as e:
        return jsonify(success=False, error=str(e))

# Route to search Slack
@app.route('/search_slack', methods=['GET'])
def search_slack_route():
    query = request.args.get('query')
    results = search_slack(query)
    return jsonify(results=results)

# Route to list all prompts
@app.route('/prompts')
def prompts_page():
    prompts = list_prompts()
    return render_template('prompts.html', prompts=prompts)

# Route to get a specific prompt by ID
@app.route('/get_prompt/<int:prompt_id>')
def get_prompt(prompt_id):
    prompt = get_prompt_by_id(prompt_id)
    if prompt:
        return jsonify(prompt)
    else:
        return jsonify({"error": "Prompt not found"}), 404

# Route to save changes to a specific prompt
@app.route('/save_prompt/<int:prompt_id>', methods=['POST'])
def save_prompt_changes(prompt_id):
    prompt_data = request.json
    success = update_prompt(prompt_id, prompt_data)
    if success:
        return jsonify(success=True)
    else:
        return jsonify(success=False, error="Error updating prompt")

# Route to save a new prompt
@app.route('/save_prompt', methods=['POST'])
def save_prompt_route():
    prompt_data = request.json
    save_prompt(prompt_data)
    return jsonify(success=True)

# Route to remove an agent
@app.route('/remove_agent', methods=['POST'])
def remove_agent_route():
    agent_name = request.json['name']
    remove_agent(agent_name)
    return jsonify(success=True)

# Route to serve chart files
@app.route('/chart/<filename>')
def serve_chart(filename):
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename))

# New route to handle GPT response and transform it into agent attributes
@app.route('/transform_agent', methods=['POST'])
def transform_agent():
    data = request.json
    instructions = data.get("instructions")
    
    if not instructions:
        return jsonify({"error": "No instructions provided"}), 400

    prompt_template = """
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
    
    # Append user instructions to the prompt template
    prompt = prompt_template + instructions

    try:
        # Generate GPT response
        gpt_response = generate_gpt_response(prompt)
        print("GPT Response:", gpt_response)  # Log GPT response

        # Transform GPT response into agent attributes
        agent = transform_gpt_response(gpt_response)
        response = {
            "name": agent.name,
            "role": agent.role,
            "goal": agent.goal,
            "description": agent.description,
            "expected_output": agent.expected_output,
            "max_iter": agent.max_iter,
            "allow_delegation": agent.allow_delegation,
            "verbose": agent.verbose,
            "is_master": agent.is_master
        }
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run Flask application
if __name__ == '__main__':
    app.run(debug=True, port=5001)
