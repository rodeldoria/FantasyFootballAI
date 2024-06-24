#!/bin/bash

# Set up the environment
PROJECT_DIR="/Users/rodeliodoria/Desktop/rdoria_AI"
VENV_DIR="$PROJECT_DIR/venv"
PYTHON_BIN="$VENV_DIR/bin/python"
PIP_BIN="$VENV_DIR/bin/pip"

# Activate the virtual environment
source "$VENV_DIR/bin/activate"

# Upgrade pip
echo "Upgrading pip..."
$PIP_BIN install --upgrade pip

# Install required packages
echo "Installing required packages..."
$PIP_BIN install alembic==1.13.1 bcrypt==4.1.3 blinker==1.8.2 click==8.1.7 Flask==3.0.3 Flask-Bcrypt==1.0.1 Flask-Cors==4.0.1 Flask-Login==0.6.3 Flask-Mail==0.10.0 Flask-Migrate==4.0.7 Flask-SQLAlchemy==3.1.1 Flask-WTF==1.2.1 greenlet==3.0.3 itsdangerous==2.2.0 Jinja2==3.1.4 Mako==1.3.5 MarkupSafe==2.1.5 SQLAlchemy==2.0.31 typing_extensions==4.12.2 Werkzeug==3.0.3 WTForms==3.1.2 python-dotenv pandas langchain-openai

# Verify installations
echo "Verifying installations..."
$PIP_BIN list

# Create verification script
VERIFICATION_SCRIPT="$PROJECT_DIR/verify_packages.py"
echo "Creating verification script at $VERIFICATION_SCRIPT..."

cat <<EOL > $VERIFICATION_SCRIPT
import sys
import importlib

packages = [
    "alembic",
    "bcrypt",
    "blinker",
    "click",
    "flask",
    "flask_bcrypt",
    "flask_cors",
    "flask_login",
    "flask_mail",
    "flask_migrate",
    "flask_sqlalchemy",
    "flask_wtf",
    "greenlet",
    "itsdangerous",
    "jinja2",
    "mako",
    "markupsafe",
    "sqlalchemy",
    "typing_extensions",
    "werkzeug",
    "wtforms",
    "dotenv",
    "pandas"
]

print("Python executable: ", sys.executable)

for package in packages:
    try:
        module = importlib.import_module(package)
        print(f"{package} imported successfully")
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
    from langchain_openai import ChatOpenAI
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

# Note: Adjust the import path based on the actual package structure for CrewAI
try:
    from crewai.crew import CrewAI  # Adjust the import path based on the actual package structure
    crew_ai = CrewAI()  # Adjust initialization as per CrewAI's documentation
    result = crew_ai.perform_task("test task")  # Replace with an actual method from CrewAI
    print("CrewAI works correctly from crewai.crew:", result)
except ImportError as e:
    print("Failed to import CrewAI:", e)
except Exception as e:
    print("Error testing CrewAI:", e)

EOL

# Run the verification script
echo "Running verification script..."
$PYTHON_BIN $VERIFICATION_SCRIPT

echo "Setup and verification completed."
