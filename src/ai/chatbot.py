"""
Advanced teacher training chatbot with scenario generation and evaluation capabilities.

This module implements a sophisticated chatbot for teacher training,
using the Ollama LLM for natural language interactions and feedback.
"""

from typing import Dict, List, Optional, Union
import json
import logging
from datetime import datetime
from pathlib import Path
import yaml

from .ollama_handler import OllamaHandler
from .embedding import EmbeddingHandler
from .rag_pipeline import RAGPipeline

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TeacherTrainingChatbot:
    def __init__(self, 
                model_name: str = "mistral",
                resources_dir: Optional[str] = None):
        """Initialize the teacher training chatbot with advanced components.
        
        Args:
            model_name: Name of the Ollama model to use
            resources_dir: Directory containing educational resources
        """
        try:
            # Initialize LLM components
            self.llm = OllamaHandler(model_name=model_name)
            self.embedding_handler = EmbeddingHandler()
            self.rag = RAGPipeline(
                embedding_handler=self.embedding_handler,
                resources_dir=resources_dir or Path(__file__).parent.parent.parent / "data/education_resources"
            )
            logger.info(f"Successfully initialized {model_name} model and components")
            
            # Load educational resources
            self._load_resources()
            
        except Exception as e:
            logger.error(f"Failed to initialize components: {str(e)}")
            raise

    def _load_resources(self):
        """Load educational resources and configurations."""
        try:
            # Load teaching scenarios
            scenarios_path = Path(__file__).parent.parent.parent / "data/scenarios"
            self.scenarios = {}
            for scenario_file in scenarios_path.glob("*.json"):
                with open(scenario_file, "r") as f:
                    self.scenarios[scenario_file.stem] = json.load(f)
            
            # Load student profiles
            profiles_path = Path(__file__).parent.parent.parent / "data/student_profiles"
            self.student_profiles = {}
            for profile_file in profiles_path.glob("*.json"):
                with open(profile_file, "r") as f:
                    self.student_profiles[profile_file.stem] = json.load(f)
            
            # Load curriculum structure
            curriculum_path = Path(__file__).parent.parent.parent / "data/education_resources/curriculum/structure.yaml"
            with open(curriculum_path, "r") as f:
                self.curriculum = yaml.safe_load(f)
                
        except Exception as e:
            logger.error(f"Failed to load resources: {str(e)}")
            raise

    def generate_scenario(self, 
                       category: str,
                       grade_level: str,
                       difficulty: str = "moderate",
                       specific_focus: Optional[str] = None) -> Dict:
        """Generate a detailed educational scenario with RAG enhancement.
        
        Args:
            category: Type of teaching scenario
            grade_level: Target grade level
            difficulty: Scenario difficulty level
            specific_focus: Optional specific teaching focus
            
        Returns:
            Dictionary containing the generated scenario
        """
        # Get relevant teaching resources
        context = self.rag.get_relevant_context(
            query=f"{category} {grade_level} {specific_focus or ''}",
            n_results=3
        )
        
        prompt = self._create_scenario_prompt(
            category=category,
            grade_level=grade_level,
            difficulty=difficulty,
            specific_focus=specific_focus,
            context=context
        )
        
        try:
            response = self.llm.generate(
                prompt=prompt["content"],
                system_prompt=prompt["system"],
                temperature=0.7
            )
            
            scenario = {
                "category": category,
                "grade_level": grade_level,
                "difficulty": difficulty,
                "specific_focus": specific_focus,
                "description": response,
                "context": context,
                "timestamp": datetime.now().isoformat()
            }
            
            return scenario
            
        except Exception as e:
            logger.error(f"Error generating scenario: {str(e)}")
            raise

    def evaluate_response(self, 
                        scenario: Dict,
                        teacher_response: str,
                        evaluation_criteria: Optional[List[str]] = None) -> Dict:
        """Evaluate teacher's response with detailed feedback.
        
        Args:
            scenario: The teaching scenario
            teacher_response: Teacher's response to evaluate
            evaluation_criteria: Optional specific criteria to evaluate
            
        Returns:
            Dictionary containing the evaluation results
        """
        # Get relevant teaching standards and best practices
        context = self.rag.get_relevant_context(
            query=f"teaching standards best practices {scenario['category']} {scenario['grade_level']}",
            n_results=3
        )
        
        prompt = self._create_evaluation_prompt(
            scenario=scenario,
            teacher_response=teacher_response,
            evaluation_criteria=evaluation_criteria,
            context=context
        )
        
        try:
            response = self.llm.generate(
                prompt=prompt["content"],
                system_prompt=prompt["system"],
                temperature=0.3,
                max_tokens=1000
            )
            
            # Parse the evaluation response
            try:
                evaluation = json.loads(response)
            except json.JSONDecodeError:
                logger.warning("Failed to parse evaluation as JSON, using raw response")
                evaluation = {
                    "raw_feedback": response,
                    "error": "Failed to structure evaluation"
                }
            
            return {
                "scenario": scenario,
                "teacher_response": teacher_response,
                "evaluation": evaluation,
                "context": context,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error evaluating response: {str(e)}")
            raise

    def get_improvement_suggestions(self, 
                                evaluation_result: Dict,
                                focus_areas: Optional[List[str]] = None) -> Dict:
        """Generate specific improvement suggestions with resources.
        
        Args:
            evaluation_result: Previous evaluation results
            focus_areas: Optional specific areas to focus suggestions on
            
        Returns:
            Dictionary containing suggestions and resources
        """
        # Get relevant teaching resources for improvements
        context = self.rag.get_relevant_context(
            query=f"teaching improvement strategies {' '.join(focus_areas or [])}",
            n_results=3
        )
        
        prompt = self._create_improvement_prompt(
            evaluation_result=evaluation_result,
            focus_areas=focus_areas,
            context=context
        )
        
        try:
            response = self.llm.generate(
                prompt=prompt["content"],
                system_prompt=prompt["system"],
                temperature=0.5
            )
            
            return {
                "suggestions": response,
                "resources": context,
                "focus_areas": focus_areas,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error generating suggestions: {str(e)}")
            raise

    def _create_scenario_prompt(self, **kwargs) -> Dict:
        """Create a detailed prompt for scenario generation."""
        system = """You are an expert in education and teacher training.
Create detailed, realistic classroom scenarios that help teachers develop their skills.
Focus on practical situations that require critical thinking and pedagogical knowledge."""
        
        content = f"""Generate a detailed classroom scenario with the following parameters:

Category: {kwargs['category']}
Grade Level: {kwargs['grade_level']}
Difficulty: {kwargs['difficulty']}
{f"Specific Focus: {kwargs['specific_focus']}" if kwargs.get('specific_focus') else ''}

Relevant Teaching Context:
{yaml.dump(kwargs['context'], default_flow_style=False)}

Provide:
1. Detailed situation description
2. Student behavior and background
3. Classroom context and environment
4. Immediate challenges
5. Learning objectives
6. Key considerations
7. Success criteria

Format the response as a clear narrative that requires teacher intervention."""
        
        return {"system": system, "content": content}

    def _create_evaluation_prompt(self, **kwargs) -> Dict:
        """Create a detailed prompt for response evaluation."""
        system = """You are an expert in education evaluation and teacher development.
Provide detailed, constructive feedback on teaching responses using evidence-based criteria.
Focus on specific strengths and actionable improvements."""
        
        content = f"""Evaluate this teacher's response to the following scenario:

Scenario:
{kwargs['scenario']['description']}

Teacher's Response:
{kwargs['teacher_response']}

Evaluation Criteria:
{yaml.dump(kwargs.get('evaluation_criteria', ['Pedagogical Approach', 'Student Engagement', 'Classroom Management']), default_flow_style=False)}

Teaching Standards Context:
{yaml.dump(kwargs['context'], default_flow_style=False)}

Provide a detailed evaluation in JSON format with:
1. Strengths (with specific examples)
2. Areas for improvement (with actionable suggestions)
3. Overall effectiveness score (1-10)
4. Specific feedback for each evaluation criterion
5. Alignment with teaching standards
6. Impact on student learning"""
        
        return {"system": system, "content": content}

    def _create_improvement_prompt(self, **kwargs) -> Dict:
        """Create a detailed prompt for improvement suggestions."""
        system = """You are an expert in teacher professional development.
Provide specific, actionable suggestions for improvement based on evidence-based practices.
Focus on practical strategies that can be implemented immediately."""
        
        content = f"""Based on the following evaluation:
{yaml.dump(kwargs['evaluation_result'], default_flow_style=False)}

Focus Areas:
{yaml.dump(kwargs.get('focus_areas', []), default_flow_style=False)}

Relevant Resources:
{yaml.dump(kwargs['context'], default_flow_style=False)}

Provide specific improvement suggestions including:
1. Immediate action steps
2. Long-term development strategies
3. Recommended resources and readings
4. Practice exercises
5. Success metrics
6. Follow-up activities

Format suggestions as clear, implementable steps with rationale and expected outcomes."""
        
        return {"system": system, "content": content}

def main():
    """Test the chatbot functionality"""
    try:
        # Initialize chatbot
        chatbot = TeacherTrainingChatbot()
        
        # Generate test scenario
        scenario = chatbot.generate_scenario("classroom_management", "active")
        print("\nGenerated Scenario:")
        print(json.dumps(scenario, indent=2))
        
        # Test teacher response
        test_response = """
        I would first observe the student's behavior to understand the triggers. 
        Then, I would quietly approach them and provide clear, specific feedback about the behavior.
        I would redirect their energy to productive tasks and use positive reinforcement when they display appropriate behavior.
        If needed, I would implement a simple behavior management plan with clear expectations and consequences.
        """
        
        # Evaluate response
        evaluation = chatbot.evaluate_response(scenario, test_response)
        print("\nResponse Evaluation:")
        print(json.dumps(evaluation, indent=2))
        
        # Get improvement suggestions
        suggestions = chatbot.get_improvement_suggestions(evaluation)
        print("\nImprovement Suggestions:")
        print(suggestions)
        
    except Exception as e:
        logger.error(f"Error in main: {str(e)}")
        raise

if __name__ == "__main__":
    main() 