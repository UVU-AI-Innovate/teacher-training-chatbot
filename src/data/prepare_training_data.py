import json
from typing import List, Dict

def format_conversation(student: Dict, scenario: Dict) -> List[Dict]:
    """Format a single conversation for training"""
    conversations = []
    
    # Format student simulation examples
    system_prompt = f"""You are simulating a second-grade student named {student['name']}.
Student Profile: {json.dumps(student)}
Scenario: {scenario['context']}"""
    
    for interaction in scenario['sample_interactions']:
        conversations.append({
            "instruction": f"{system_prompt}\nTeacher says: {interaction['student']}",
            "response": interaction['student']
        })
    
    return conversations

def prepare_training_data():
    """Prepare all training data"""
    # Load your existing data
    with open('data/second_grade/student_profiles.json', 'r') as f:
        students = json.load(f)['student_profiles']
        
    with open('data/second_grade/conversations.json', 'r') as f:
        scenarios = json.load(f)['teaching_scenarios']
        
    # Format all conversations
    training_data = []
    for student in students:
        for scenario in scenarios:
            training_data.extend(format_conversation(student, scenario))
            
    # Save formatted data
    with open('data/training/second_grade_conversations.json', 'w') as f:
        json.dump(training_data, f, indent=2)

if __name__ == "__main__":
    prepare_training_data() 