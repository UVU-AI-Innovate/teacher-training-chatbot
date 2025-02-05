import json
from typing import Dict, List, Optional
from .llm_handler import LLMHandler

class StudentSimulator:
    def __init__(self):
        # Load our training data
        with open('data/second_grade/student_profiles.json', 'r') as f:
            self.student_profiles = json.load(f)
        
        with open('data/second_grade/conversations.json', 'r') as f:
            self.conversations = json.load(f)
            
        with open('data/scenarios/classroom_management.json', 'r') as f:
            self.scenarios = json.load(f)
            
        self.current_student = None
        self.current_scenario = None
        self.conversation_history = []
        self.llm_handler = LLMHandler()
        
    def select_random_student(self) -> None:
        """Randomly select a student profile to simulate"""
        import random
        self.current_student = random.choice(self.student_profiles["student_profiles"])
        self.conversation_history = []
        
    def set_scenario(self, scenario_id: str) -> None:
        """Set the current teaching scenario"""
        for scenario in self.conversations["teaching_scenarios"]:
            if scenario["id"] == scenario_id:
                self.current_scenario = scenario
                break
                
    def generate_response(self, teacher_input: str) -> str:
        """Generate a contextual student response using LLM"""
        if not self.current_student or not self.current_scenario:
            return "Error: Please select a student and scenario first."
            
        response = self.llm_handler.generate_student_response(
            self.current_student,
            self.current_scenario,
            teacher_input,
            self.conversation_history
        )
        
        # Update conversation history
        self.conversation_history.append({
            "teacher": teacher_input,
            "student": response
        })
        
        return response 