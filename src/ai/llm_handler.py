from typing import Dict, List, Optional
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import json

class LLMHandler:
    def __init__(self, 
                 base_model: str = "mistralai/Mistral-7B-Instruct-v0.1",
                 lora_weights: str = None):
        """Initialize with a fine-tuned LLM model"""
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Loading model on {self.device}...")
        
        # Load base model
        self.model = AutoModelForCausalLM.from_pretrained(
            base_model,
            device_map="auto",
            torch_dtype=torch.float16
        )
            
        self.tokenizer = AutoTokenizer.from_pretrained(base_model)
        
    def generate_text(self, 
                     prompt: str, 
                     max_length: int = 150, 
                     temperature: float = 0.7,
                     top_p: float = 0.9) -> str:
        """Generate text using the fine-tuned LLM"""
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        
        outputs = self.model.generate(
            **inputs,
            max_length=max_length,
            temperature=temperature,
            top_p=top_p,
            do_sample=True,
            pad_token_id=self.tokenizer.eos_token_id
        )
        
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        response = response[len(prompt):].strip()
        return response
        
    def generate_student_response(self, 
                                student_profile: Dict,
                                scenario: Dict,
                                teacher_input: str,
                                conversation_history: List[Dict]) -> str:
        """Generate a student response using local LLM"""
        
        # Create the prompt
        prompt = self._create_student_prompt(
            student_profile,
            scenario,
            teacher_input,
            conversation_history
        )
        
        try:
            full_prompt = f"{prompt['system']}\n\n{prompt['user']}"
            response = self.generate_text(full_prompt, max_length=150, temperature=0.7)
            return response
        except Exception as e:
            print(f"LLM Error: {e}")
            return "I'm not sure how to respond to that."
            
    def evaluate_teacher_response(self,
                                scenario: Dict,
                                teacher_response: str) -> Dict:
        """Evaluate teacher's response using local LLM"""
        
        prompt = self._create_evaluation_prompt(scenario, teacher_response)
        
        try:
            full_prompt = f"{prompt['system']}\n\n{prompt['user']}"
            response = self.generate_text(full_prompt, max_length=300, temperature=0.3)
            
            # Parse the JSON response
            # Add error handling in case the LLM doesn't generate valid JSON
            try:
                return json.loads(response)
            except json.JSONDecodeError:
                print("Warning: LLM generated invalid JSON. Using fallback response.")
                return self._create_fallback_evaluation()
                
        except Exception as e:
            print(f"LLM Error: {e}")
            return self._create_fallback_evaluation()
            
    def _create_student_prompt(self,
                             student_profile: Dict,
                             scenario: Dict,
                             teacher_input: str,
                             conversation_history: List[Dict]) -> Dict:
        """Create prompt for student response generation"""
        
        system_prompt = f"""<|system|>
You are simulating a second-grade student named {student_profile['name']}.

Student Profile:
- Learning style: {student_profile['learning_style']}
- Challenges: {', '.join(student_profile['challenges'])}
- Strengths: {', '.join(student_profile['strengths'])}
- Background: {student_profile['background']}

Current Scenario: {scenario['scenario']}

Respond as this student would, keeping in mind their:
1. Age (second grade, around 7-8 years old)
2. Learning style and challenges
3. Background and strengths
4. Emotional state in the current scenario

Keep responses brief and age-appropriate.</s>"""

        user_prompt = f"<|user|>Teacher says: {teacher_input}\n\nHow would {student_profile['name']} respond?</s>"
        
        return {
            "system": system_prompt,
            "user": user_prompt
        }
        
    def _create_evaluation_prompt(self,
                                scenario: Dict,
                                teacher_response: str) -> Dict:
        """Create prompt for teacher response evaluation"""
        
        system_prompt = """<|system|>
You are an expert in elementary education pedagogy, evaluating a teacher-in-training's response to a classroom scenario.

Analyze the response based on:
1. Teaching principles demonstrated
2. Areas for improvement
3. Effectiveness of the approach

Provide feedback in the following JSON format:
{
    "principles_demonstrated": ["principle1", "principle2"],
    "areas_for_improvement": ["area1", "area2"],
    "specific_feedback": "Detailed feedback here",
    "suggestions": ["suggestion1", "suggestion2"]
}</s>"""

        user_prompt = f"""<|user|>Scenario: {scenario['scenario']}

Teacher's Response: {teacher_response}

Expected Teaching Principles: {', '.join(scenario['teaching_objectives'])}

Evaluate this response and provide feedback in the specified JSON format.</s>"""
        
        return {
            "system": system_prompt,
            "user": user_prompt
        }
        
    def _create_fallback_evaluation(self) -> Dict:
        """Create a fallback evaluation when LLM fails"""
        return {
            "principles_demonstrated": [],
            "areas_for_improvement": ["Unable to evaluate response"],
            "specific_feedback": "The system was unable to evaluate this response. Please try again.",
            "suggestions": ["Please rephrase your response and try again."]
        } 