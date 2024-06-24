import json
import os

# Define the path to the prompts file
PROMPTS_FILE = 'prompts.json'

def list_prompts():
    if os.path.exists(PROMPTS_FILE):
        with open(PROMPTS_FILE, 'r') as f:
            return json.load(f)
    return []

def save_prompt(prompt_data):
    prompts = list_prompts()
    prompts.append(prompt_data)
    with open(PROMPTS_FILE, 'w') as f:
        json.dump(prompts, f)

def search_prompts(query):
    prompts = list_prompts()
    return [prompt for prompt in prompts if query.lower() in prompt['name'].lower()]

def get_prompt_by_id(prompt_id):
    prompts = list_prompts()
    for prompt in prompts:
        if prompt['id'] == prompt_id:
            return prompt
    return None

def update_prompt(prompt_id, updated_data):
    prompts = list_prompts()
    for i, prompt in enumerate(prompts):
        if prompt['id'] == prompt_id:
            prompts[i] = updated_data
            with open(PROMPTS_FILE, 'w') as f:
                json.dump(prompts, f)
            return True
    return False
