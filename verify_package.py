# verify_packages.py

import sys
import importlib

packages = {
    "matplotlib.pyplot": "plt",
    "langchain_community.chat_models": "ChatOpenAI",
    "openai": "openai",
    "crewai": "CrewAI"  # Adjust the import path based on the actual package structure
}

print("Python executable: ", sys.executable)

for package, alias in packages.items():
    try:
        module = importlib.import_module(package)
        print(f"{package} imported successfully as {alias}")
    except ImportError as e:
        print(f"Failed to import {package}: {e}")

# Test basic functionality
try:
    import matplotlib.pyplot as plt
    plt.figure()
    print("matplotlib works correctly")
except Exception as e:
    print("Error testing matplotlib:", e)

try:
    from langchain_community.chat_models import ChatOpenAI
    chat_model = ChatOpenAI()
    print("ChatOpenAI works correctly")
except Exception as e:
    print("Error testing ChatOpenAI:", e)

try:
    import openai
    openai.api_key = "sk-test"  # Use a test key
    print("openai works correctly")
except Exception as e:
    print("Error testing openai:", e)

try:
    from crewai import CrewAI  # Adjust the import path based on the actual package structure
    crew_ai = CrewAI()  # Adjust initialization as per CrewAI's documentation
    result = crew_ai.perform_task("test task")  # Replace with an actual method from CrewAI
    print("CrewAI works correctly:", result)
except Exception as e:
    print("Error testing CrewAI:", e)
