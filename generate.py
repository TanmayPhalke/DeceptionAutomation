import generateconversation
import tqdm
import time

def get_scenario():
    scenario = input("Enter a scenario to generate conversation: ")
    return scenario

def generate_chat():
    scenario = get_scenario()
    print(f"Generating chat for scenario: {scenario}")

    output = generateconversation.main(scenario)  # Call the main function from generateconversation.py with scenario as argument
    print("\n-------------------------------------------------")
    print("*************CHAT GENERATION SUCCESSFUL*************")

    print("Output from generateconversation.py: {output}")