# test_crewai.py

import sys
# Adjust the import based on the actual package structure
try:
    from crewai import CrewAI
except ImportError:
    print("Failed to import CrewAI. Ensure the package is installed correctly.")

print("Python executable: ", sys.executable)
print("CrewAI imported successfully")

# Initialize CrewAI and perform a basic test
def test_crewai_functionality():
    try:
        crew_ai = CrewAI()  # Adjust initialization as per CrewAI's documentation
        result = crew_ai.perform_task("test task")  # Replace with an actual method from CrewAI
        print("CrewAI task result: ", result)
    except Exception as e:
        print("An error occurred while testing CrewAI:", e)

if __name__ == "__main__":
    test_crewai_functionality()
