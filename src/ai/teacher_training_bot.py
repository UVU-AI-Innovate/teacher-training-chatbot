from typing import Dict, Optional, List
from .student_simulator import StudentSimulator
from .llm_handler import LLMHandler

class TeacherTrainingBot:
    def __init__(self):
        self.student_simulator = StudentSimulator()
        self.llm_handler = LLMHandler()
        self.current_scenario = None
        self.feedback_history = []
        
    def start_scenario(self, scenario_id: str) -> Dict:
        """Start a new teaching scenario"""
        self.student_simulator.select_random_student()
        self.student_simulator.set_scenario(scenario_id)
        self.current_scenario = scenario_id
        
        return {
            "student": self.student_simulator.current_student,
            "scenario": self.student_simulator.current_scenario,
            "initial_prompt": "How would you handle this situation?"
        }
        
    def evaluate_response(self, teacher_response: str) -> Dict:
        """Evaluate the teacher's response and provide feedback using LLM"""
        if not self.current_scenario:
            return {"error": "No active scenario"}
            
        # Get student's reaction
        student_reaction = self.student_simulator.generate_response(teacher_response)
        
        # Get LLM evaluation
        feedback = self.llm_handler.evaluate_teacher_response(
            self.student_simulator.current_scenario,
            teacher_response
        )
        
        # Store feedback history
        self.feedback_history.append({
            "teacher_response": teacher_response,
            "student_reaction": student_reaction,
            "feedback": feedback
        })
        
        return {
            "student_reaction": student_reaction,
            "feedback": feedback
        } 