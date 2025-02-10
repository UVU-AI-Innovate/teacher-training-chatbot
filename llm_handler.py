"""
Natural Language Processing for Teacher Training

This module provides intelligent language processing capabilities for the
teacher training simulation system. It handles the generation of realistic
student responses and evaluation of teaching strategies.

Key Features:
1. Teaching Response Analysis - Evaluates pedagogical approaches
2. Student Response Generation - Creates age-appropriate reactions
3. Contextual Understanding - Considers teaching scenario context
4. Fallback Mechanisms - Ensures system reliability

The system uses local LLM deployment for privacy and consistent performance
while maintaining high-quality educational interactions.
"""

import requests
import json
import time
import os
import signal
import subprocess

class PedagogicalLanguageProcessor:
    """
    Manages natural language processing for teacher training simulations.
    
    This class provides:
    - Analysis of teaching strategies and responses
    - Generation of realistic student reactions
    - Evaluation of pedagogical effectiveness
    - Context-aware interaction handling
    
    The processor maintains educational context while generating
    responses that reflect real classroom dynamics.
    
    Attributes:
        model (str): Name of the language model being used
        base_url (str): Endpoint for LLM API communication
        system_prompt (str): Core instruction set for teaching evaluation
    """
    
    def __init__(self, model_name="mistral"):
        self.model = model_name
        self.base_url = "http://localhost:11434/api"
        self.system_prompt = """You are an expert teacher evaluator, analyzing teaching responses 
        in a training simulation. Provide detailed, constructive feedback."""

    def ensure_server_running(self):
        """Ensure Ollama server is running."""
        if not self.check_server():
            print("\nStarting Ollama server...")
            try:
                subprocess.Popen(
                    ["ollama", "serve"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                for _ in range(5):
                    time.sleep(2)
                    if self.check_server():
                        print("Ollama server started successfully!")
                        return True
                print("Failed to start Ollama server.")
                return False
            except Exception as e:
                print(f"Error starting Ollama server: {e}")
                return False
        return True

    def check_server(self):
        """Check if Ollama server is running."""
        try:
            response = requests.get(f"{self.base_url}/version", timeout=2)
            return response.status_code == 200
        except Exception:
            return False

    def analyze_teaching_response(self, prompt: str) -> dict:
        """Analyze teacher's response using local LLM."""
        if not self.ensure_server_running():
            return self._get_fallback_evaluation()

        try:
            # Create a safe version of the prompt with escaped quotes
            safe_prompt = prompt.replace('"', '\\"')
            
            evaluation_prompt = (
                'Please analyze this teacher\'s response to a second-grade student.\n\n'
                f'The teacher\'s response was: "{safe_prompt}"\n\n'
                'Evaluate the response and provide feedback using this exact JSON structure:\n'
                '{\n'
                '    "score": 0.75,\n'
                '    "strengths": ["Example strength 1", "Example strength 2"],\n'
                '    "suggestions": ["Example suggestion 1", "Example suggestion 2"],\n'
                '    "explanation": "Example explanation"\n'
                '}\n\n'
                'Your evaluation should focus on:\n'
                '1. Clarity and age-appropriateness\n'
                '2. Teaching effectiveness\n'
                '3. Student engagement\n'
                '4. Emotional support\n\n'
                'Return only the JSON object with no additional text or formatting.'
            )

            response = requests.post(
                f"{self.base_url}/generate",
                json={
                    "model": self.model,
                    "prompt": evaluation_prompt,
                    "system": "You are a teaching expert. Return only a valid JSON object with no additional text.",
                    "stream": False
                },
                timeout=10
            )
            response.raise_for_status()
            result = response.json()["response"].strip()
            
            try:
                # Clean the response
                result = result.replace('```json', '').replace('```', '').strip()
                if result.startswith('"') and result.endswith('"'):
                    result = result[1:-1]
                result = result.replace('\\"', '"')
                
                # Try to extract JSON object if there's extra text
                import re
                json_matches = re.findall(r'(\{[\s\S]*\})', result)
                if json_matches:
                    result = json_matches[0]
                
                # Parse the JSON
                parsed_result = json.loads(result)
                
                # Create a valid result structure
                valid_result = {
                    "score": 0.5,
                    "strengths": ["Basic teaching approach"],
                    "suggestions": ["Consider adding more specific strategies"],
                    "explanation": "Basic evaluation provided"
                }
                
                # Update with parsed values if they exist and are valid
                if isinstance(parsed_result.get("score"), (int, float)):
                    valid_result["score"] = float(parsed_result["score"])
                
                if isinstance(parsed_result.get("strengths"), list):
                    valid_result["strengths"] = [str(s) for s in parsed_result["strengths"]]
                elif isinstance(parsed_result.get("strengths"), str):
                    valid_result["strengths"] = [parsed_result["strengths"]]
                
                if isinstance(parsed_result.get("suggestions"), list):
                    valid_result["suggestions"] = [str(s) for s in parsed_result["suggestions"]]
                elif isinstance(parsed_result.get("suggestions"), str):
                    valid_result["suggestions"] = [parsed_result["suggestions"]]
                
                if isinstance(parsed_result.get("explanation"), str):
                    valid_result["explanation"] = parsed_result["explanation"]
                
                return valid_result
                
            except json.JSONDecodeError as e:
                print(f"JSON parsing error: {e}")
                print(f"Raw response: {result}")
                return self._structure_free_text_response(result)
                
        except Exception as e:
            print(f"Error in LLM analysis: {e}")
            return self._get_fallback_evaluation()

    def _structure_free_text_response(self, text: str) -> dict:
        """Convert free text response to structured format."""
        try:
            # Remove any markdown formatting
            text = text.replace("```", "").strip()
            
            # Simple heuristic to estimate score based on positive/negative words
            positive_words = ['good', 'great', 'excellent', 'effective', 'well', 'clear', 'appropriate']
            negative_words = ['improve', 'consider', 'should', 'could', 'better', 'unclear', 'missing']
            
            text_lower = text.lower()
            score = 0.5  # Default score
            
            # Adjust score based on positive/negative words
            score += sum(0.1 for word in positive_words if word in text_lower)
            score -= sum(0.1 for word in negative_words if word in text_lower)
            score = max(0.1, min(1.0, score))  # Keep score between 0.1 and 1.0
            
            # Split text into strengths and suggestions
            lines = [line.strip() for line in text.split('\n') if line.strip()]
            strengths = []
            suggestions = []
            
            for line in lines:
                line_lower = line.lower()
                if any(word in line_lower for word in positive_words):
                    strengths.append(line)
                elif any(word in line_lower for word in negative_words):
                    suggestions.append(line)
                elif 'strength' in line_lower or 'positive' in line_lower:
                    strengths.append(line)
                elif 'suggest' in line_lower or 'improve' in line_lower:
                    suggestions.append(line)
            
            return {
                "score": score,
                "strengths": strengths or ["Basic teaching elements present"],
                "suggestions": suggestions or ["Consider adding more specific strategies"],
                "explanation": text
            }
        except Exception as e:
            print(f"Error structuring response: {e}")
            return self._get_fallback_evaluation()

    def _get_fallback_evaluation(self) -> dict:
        """Provide fallback evaluation when LLM is unavailable."""
        return {
            "score": 0.5,
            "strengths": ["Response provided basic teaching interaction"],
            "suggestions": ["Consider adding more specific teaching strategies"],
            "explanation": "Basic evaluation provided due to processing limitations"
        }

    def generate_student_reaction(self, context: dict, teacher_response: str, effectiveness: float) -> str:
        """Generate contextual student reaction using local LLM."""
        if not self.ensure_server_running():
            return "*looks uncertain* Okay..."

        prompt = f"""
        As a second-grade student, generate a realistic reaction to the teacher's response.
        
        Context:
        - Subject: {context['subject']}
        - Current Challenge: {context['difficulty']}
        - Student's State: {context['behavioral_context']['type']}
        - Response Effectiveness: {effectiveness}
        
        Teacher's Response: "{teacher_response}"
        
        Generate a natural, age-appropriate reaction that:
        1. Reflects the effectiveness of the teacher's approach
        2. Shows realistic second-grade behavior
        3. Maintains consistency with the student's current state
        4. Includes both verbal response and behavioral cues (in *asterisks*)
        
        Response should be a single line of dialogue/action.
        """

        try:
            response = requests.post(
                f"{self.base_url}/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "system": "You are a second-grade student in a classroom situation.",
                    "stream": False
                },
                timeout=10
            )
            response.raise_for_status()
            return response.json()["response"].strip()
            
        except Exception as e:
            print(f"Error generating reaction: {e}")
            return "*looks uncertain* Okay..." 