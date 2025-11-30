import random

def generate_persona_response(context="distraction"):
    """
    Generates a strict, high-agency response based on the context.
    """
    # In a real implementation, this would call an LLM with a system prompt.
    # For now, we use a list of pre-defined "Daniel Dalen" style quotes.
    
    responses = [
        "Focus on the mission. Close the tab.",
        "Comfort is the enemy of progress. Get back to work.",
        "You said you wanted it. Prove it.",
        "Don't be average. Ship the code.",
        "Distraction is a choice. Choose better.",
        "The market doesn't care about your feelings. Work.",
        "Is this moving the needle? No. Close it.",
        "Discipline equals freedom. Focus."
    ]
    
    return random.choice(responses)

if __name__ == "__main__":
    print(generate_persona_response())
