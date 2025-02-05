from src.ai.llm_handler import LLMHandler
import json

def main():
    # Initialize the LLM handler without LoRA weights for now
    print("Initializing LLM handler (this may take a few moments while the model loads)...")
    llm = LLMHandler(base_model="mistralai/Mistral-7B-Instruct-v0.1", lora_weights=None)
    
    # Load scenario data
    with open("data/scenarios/classroom_management.json", "r") as f:
        scenarios = json.load(f)
    
    # Use the first scenario
    scenario = scenarios["classroom_management_scenarios"][0]
    
    # Create a sample student profile
    student_profile = {
        "name": "Alex",
        "learning_style": "Visual learner",
        "challenges": ["Gets distracted easily", "Takes time to process instructions"],
        "strengths": ["Creative", "Eager to help others"],
        "background": "Comes from a supportive family, enjoys art and reading"
    }
    
    print("\nScenario Context:")
    print(f"Student: {student_profile['name']}")
    print(f"Background: {student_profile['background']}")
    print(f"Context: {scenario['scenario']}")
    
    conversation_history = []
    
    # Example interaction loop
    while True:
        # Get teacher's response
        teacher_response = input("\nTeacher's response (type 'quit' to end): ")
        if teacher_response.lower() == 'quit':
            break
            
        # Generate student's reaction
        student_reaction = llm.generate_student_response(
            student_profile,
            scenario,
            teacher_response,
            conversation_history
        )
        
        # Get evaluation of teacher's response
        evaluation = llm.evaluate_teacher_response(scenario, teacher_response)
        
        # Update conversation history
        conversation_history.append({
            "teacher": teacher_response,
            "student": student_reaction
        })
        
        print("\nStudent's reaction:", student_reaction)
        print("\nFeedback:")
        print("Principles demonstrated:", ", ".join(evaluation['principles_demonstrated']))
        print("Areas for improvement:", ", ".join(evaluation['areas_for_improvement']))
        print("\nSpecific Feedback:", evaluation['specific_feedback'])
        print("\nSuggestions:")
        for suggestion in evaluation['suggestions']:
            print(f"- {suggestion}")

if __name__ == "__main__":
    main() 