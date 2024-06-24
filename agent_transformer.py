import re

# Define the Agent model
class Agent:
    def __init__(self, name, role, goal, description, expected_output, max_iter, allow_delegation, verbose, is_master):
        self.name = name
        self.role = role
        self.goal = goal
        self.description = description
        self.expected_output = expected_output
        self.max_iter = max_iter
        self.allow_delegation = allow_delegation
        self.verbose = verbose
        self.is_master = is_master

    def __repr__(self):
        return (f"Name: {self.name}\n"
                f"Role: {self.role}\n"
                f"Goal: {self.goal}\n"
                f"Description: {self.description}\n"
                f"Expected Output: {self.expected_output}\n"
                f"Max Iterations: {self.max_iter}\n"
                f"Allow Delegation: {self.allow_delegation}\n"
                f"Verbose: {self.verbose}\n"
                f"Is Master: {self.is_master}")

# Extract information from GPT response
def extract_gpt_response(response):
    info = {}
    fields = ["Name", "Role", "Goal", "Description", "Expected Output", "Max Iterations", "Allow Delegation", "Verbose", "Is Master"]

    for field in fields:
        pattern = re.compile(rf'{field}:\s*(.*?)\n', re.DOTALL)
        match = pattern.search(response)
        if match:
            info[field] = match.group(1).strip()
        else:
            info[field] = "N/A"

    return info

# Map extracted information to agent attributes with validation
def map_to_agent(info):
    name = info.get('Name', 'N/A')
    role = info.get('Role', 'N/A')
    goal = info.get('Goal', 'N/A')
    description = info.get('Description', 'N/A')
    expected_output = info.get('Expected Output', 'N/A')
    
    # Validate and map max_iter
    try:
        max_iter = int(info.get('Max Iterations', 10))
        if not (1 <= max_iter <= 10):
            raise ValueError
    except ValueError:
        max_iter = 10  # Default to 10 if invalid

    # Map boolean fields
    allow_delegation = info.get('Allow Delegation', 'False').lower() == 'true'
    verbose = info.get('Verbose', 'False').lower() == 'true'
    is_master = info.get('Is Master', 'False').lower() == 'true'

    return Agent(name, role, goal, description, expected_output, max_iter, allow_delegation, verbose, is_master)

# Transform and display the GPT response
def transform_gpt_response(response):
    # Extract information
    info = extract_gpt_response(response)

    # Map to agent attributes
    agent = map_to_agent(info)

    # Return the agent object
    return agent

# Example GPT response
if __name__ == "__main__":
    gpt_response = """Based on your instructions, here is the configuration for the new agent:

Name: Travel Agent from Japan
Role: Provide comprehensive travel assistance and information for travelers to Japan.
Goal: Ensure travelers have a smooth and enjoyable experience in Japan.
Description: The agent should be configured to comprehend and communicate effectively in Japanese. It should also have translation capabilities to cater to non-Japanese speakers. The agent should have a comprehensive database of Japan's geography, cities, attractions, and culture to provide detailed and accurate travel information. It should be programmed with the current travel policies, visa requirements, and procedures for international and domestic travel in Japan. Additionally, the agent should have access to real-time information about transportation options within Japan, including train schedules, bus routes, flight details, and taxi services. The agent should be configured with information about various accommodation options, ranging from luxury hotels to budget-friendly options and traditional Japanese inns (Ryokans). The agent should be able to handle bookings for flights, hotels, and local tours and manage changes, cancellations, and refunds. It should provide information on emergency services in Japan, including embassy details, local hospitals, and police stations. The agent should be able to provide real-time currency conversion rates from other currencies to Japanese Yen and vice versa, access real-time weather updates for different regions within Japan, provide basic Japanese language tips to travelers for better communication during their trip, inform travelers about Japanese culture and etiquette to ensure respectful interactions during their stay, and have knowledge about local Japanese cuisines and recommend popular dishes and restaurants.
Expected Output: Provide accurate and up-to-date travel information and booking capabilities.
Max Iterations: 10
Allow Delegation: True
Verbose: True
Is Master: False
"""

    # Transform and display the GPT response
    agent = transform_gpt_response(gpt_response)
    print(agent)
