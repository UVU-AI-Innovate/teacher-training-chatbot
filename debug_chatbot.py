from ai_agent import AIAgent
import json
from colorama import init, Fore, Style
from termcolor import colored
import os
# import keyboard  # Remove this line
from simulator_session import SimulatorSession
from datetime import datetime

# Initialize colorama
init()

class TeacherTrainingSimulator:
    def __init__(self):
        self.chatbot = AIAgent()
        self.session = SimulatorSession()
        self.current_scenario = None
        
    def clear_screen(self):
        """Clear the terminal screen if auto-clear is enabled."""
        if self.session.settings["auto_clear"]:
            os.system('cls' if os.name == 'nt' else 'clear')

    def print_header(self):
        """Print the application header."""
        print(colored("\n🎓 Teacher Training Simulator - Debug Mode 🎓", "cyan", attrs=["bold"]))
        print(colored("=" * 50, "cyan"))
        
        # Show session duration
        duration = datetime.now() - self.session.start_time
        print(colored(f"Session Duration: {duration.seconds//60}m {duration.seconds%60}s", "cyan"))

    def show_quick_tips(self, scenario):
        """Show context-specific teaching tips."""
        if not self.session.settings["show_tips"]:
            return
            
        print(colored("\n💭 Quick Tips:", "cyan", attrs=["bold"]))
        print(colored("-" * 30, "cyan"))
        
        tips = {
            "time_of_day": {
                "morning": "Students are fresh - set clear expectations",
                "after lunch": "Include movement in your lesson",
                "late afternoon": "Keep activities short and varied"
            },
            "learning_style": {
                "visual": "Use diagrams and demonstrations",
                "auditory": "Incorporate verbal explanations",
                "kinesthetic": "Include hands-on activities"
            }
        }
        
        print(f"• Time: {tips['time_of_day'][scenario['time_of_day']]}")
        print(f"• Style: {tips['learning_style'][scenario['student_context']['learning_style']]}")

    def show_example_responses(self, scenario):
        """Show example effective responses for the current scenario."""
        if not self.session.settings["show_examples"]:
            return
            
        print(colored("\n💡 Example Effective Responses:", "green", attrs=["bold"]))
        print(colored("-" * 30, "green"))
        
        context = scenario["behavioral_context"]
        learning_style = scenario["student_context"]["learning_style"]
        
        examples = {
            "frustration": {
                "visual": [
                    "Let's draw this out together. I'll show you step by step.",
                    "Watch how I solve this first, then we'll try one together."
                ],
                "auditory": [
                    "Let's talk through this together. Tell me what you're thinking.",
                    "I'll explain it differently, listen carefully."
                ],
                "kinesthetic": [
                    "Let's use these blocks to work it out together.",
                    "Stand up, we'll act this problem out."
                ]
            }
        }
        
        for example in examples.get(context["type"], {}).get(learning_style, []):
            print(colored(f"→ {example}", "green"))

    def display_progress_metrics(self):
        """Show teacher's progress over time."""
        print(colored("\n📈 Progress Metrics:", "blue", attrs=["bold"]))
        print(colored("-" * 30, "blue"))
        
        avg_score = self.session.get_average_score()
        best_response = self.session.get_best_response()
        areas_for_improvement = self.session.get_areas_for_improvement()
        
        print(f"• Average Score: {avg_score:.2f}")
        if best_response:
            print(f"• Best Response Score: {best_response['score']:.2f}")
            print(f"• Best Response: {best_response['teacher_response']}")
        
        if areas_for_improvement:
            print("\nTop Areas for Improvement:")
            for area in areas_for_improvement:
                print(f"• {area}")

    def configure_simulator(self):
        """Configure simulator settings."""
        print(colored("\n⚙️ Simulator Settings:", "yellow", attrs=["bold"]))
        print(colored("-" * 30, "yellow"))
        
        for key, value in self.session.settings.items():
            choice = input(f"{key} [{value}]: ").strip().lower()
            if choice in ['true', 'false']:
                self.session.settings[key] = choice == 'true'

    def run(self):
        """Run the simulator."""
        self.clear_screen()
        self.print_header()
        
        # Initialize first scenario
        self.current_scenario = self.chatbot.generate_scenario()
        self.display_scenario(self.current_scenario)
        
        # Remove keyboard shortcuts setup
        # keyboard.add_hotkey('ctrl+n', lambda: self.new_scenario())
        # keyboard.add_hotkey('ctrl+h', lambda: self.display_session_history())
        # keyboard.add_hotkey('ctrl+t', lambda: self.show_quick_tips(self.current_scenario))
        # keyboard.add_hotkey('ctrl+d', lambda: self.clear_screen())

        while True:
            choice = self.display_menu()
            
            if choice == "1":
                self.handle_teacher_response()
            elif choice == "2":
                self.new_scenario()
            elif choice == "3":
                self.display_scenario(self.current_scenario)
            elif choice == "4":
                self.display_knowledge_base()
            elif choice == "5":
                self.display_session_history()
            elif choice == "6":
                self.display_progress_metrics()
            elif choice == "7":
                self.show_example_responses(self.current_scenario)
            elif choice == "8":
                self.show_quick_tips(self.current_scenario)
            elif choice == "9":
                self.configure_simulator()
            elif choice == "10":
                print(colored("\nThank you for using the Teacher Training Simulator! 👋", "cyan"))
                break
            else:
                print(colored("\n❌ Invalid choice. Please choose 1-10.", "red"))

    def print_knowledge_summary(self, chatbot):
        """Display summary of loaded knowledge base."""
        print(colored("\n📚 Knowledge Base Summary:", "yellow", attrs=["bold"]))
        print(colored("-" * 30, "yellow"))
        
        # Teaching Strategies
        strategies = chatbot.knowledge_base["teaching_strategies"]
        print(colored("Teaching Strategies:", "yellow"))
        print(f"• Time-based strategies: {len(strategies['time_strategies'])} periods")
        print(f"• Learning styles: {len(strategies['learning_styles'])} types")
        
        # Student Behaviors
        behaviors = chatbot.knowledge_base["student_behaviors"]
        print(colored("\nStudent Behaviors:", "yellow"))
        print(f"• Behavior types: {len(behaviors)} patterns")
        
        # Subject Content
        subjects = chatbot.knowledge_base["subject_content"]
        print(colored("\nSubject Content:", "yellow"))
        print(f"• Subjects covered: {', '.join(subjects.keys())}")
        print(f"• Total strategies: {sum(len(s['strategies']) for s in subjects.values())}")

    def display_menu(self):
        """Display the interactive menu."""
        print(colored("\n📋 Options:", "green", attrs=["bold"]))
        print(colored("1.", "green") + " Respond to student")
        print(colored("2.", "green") + " New scenario")
        print(colored("3.", "green") + " View current scenario")
        print(colored("4.", "green") + " View knowledge base")
        print(colored("5.", "green") + " View session history")
        print(colored("6.", "green") + " Show progress metrics")
        print(colored("7.", "green") + " Show example responses")
        print(colored("8.", "green") + " Show quick tips")
        print(colored("9.", "green") + " Configure simulator")
        print(colored("10.", "green") + " Exit")
        return input(colored("\nChoose an option (1-10): ", "green")).strip()

    def display_scenario(self, scenario):
        """Display the current scenario in a formatted way."""
        print(colored("\n📝 Current Scenario:", "blue", attrs=["bold"]))
        print(colored("-" * 30, "blue"))
        
        # Basic info
        print(colored("Subject:", "blue"), scenario["subject"].title())
        print(colored("Time:", "blue"), scenario["time_of_day"])
        
        # Student profile
        print(colored("\nStudent Profile:", "blue"))
        student = scenario["student_context"]
        print(f"• Learning style: {student['learning_style']}")
        print(f"• Attention span: {student['attention_span']:.2f}")
        print(f"• Social confidence: {student['social_confidence']:.2f}")
        print(f"• Challenges: {', '.join(student['current_challenges'])}")
        
        # Behavioral context
        behavior = scenario["behavioral_context"]
        print(colored("\nBehavioral Context:", "blue"))
        print(f"• Type: {behavior['type']}")
        print(f"• Trigger: {behavior['trigger']}")
        print(f"• Manifestation: {behavior['manifestation']}")
        
        # Learning objectives
        print(colored("\nLearning Objectives:", "blue"))
        for obj in scenario["learning_objectives"]:
            print(f"• {obj}")

    def display_evaluation(self, evaluation):
        """Display the evaluation results in a more readable format."""
        print("\n" + "="*70)
        print(colored("📊 EVALUATION RESULTS", "magenta", attrs=["bold"]))
        print("="*70)
        
        # Overall Score with color coding
        score = evaluation['score']
        score_color = "red" if score < 0.4 else "yellow" if score < 0.8 else "green"
        print(colored(f"\n💯 Overall Score: {score*100:.0f}%", score_color, attrs=["bold"]))
        
        # Context Alignment
        print(colored("\n📍 Context Alignment:", "cyan", attrs=["bold"]))
        print("-" * 40)
        alignments = evaluation['context_alignment']
        for key, value in alignments.items():
            bar = "█" * int(value * 20)
            print(f"{key.replace('_', ' ').title():20}: {bar} {value*100:.0f}%")
        
        # Identified Strategies
        print(colored("\n🎯 Identified Strategies:", "cyan", attrs=["bold"]))
        print("-" * 40)
        for strategy in evaluation['identified_strategies']:
            print(f"• {strategy['type'].replace('_', ' ').title()}:")
            print(f"  Effectiveness: {strategy['effectiveness']*100:.0f}%")
            if strategy['explanation']:
                print(f"  {strategy['explanation']}")
        
        # Feedback and Suggestions
        if evaluation['feedback']:
            print(colored("\n✅ Strengths:", "green", attrs=["bold"]))
            print("-" * 40)
            for item in evaluation['feedback']:
                print(colored(f"✓ {item}", "green"))
        
        print(colored("\n💡 Suggestions:", "yellow", attrs=["bold"]))
        print("-" * 40)
        for suggestion in evaluation['suggestions']:
            print(colored(f"→ {suggestion}", "yellow"))
        
        # Student Reaction
        print(colored("\n🎭 Student Reaction:", "cyan", attrs=["bold"]))
        print("-" * 40)
        print(colored(evaluation['student_reaction'], "cyan"))
        
        # State Changes
        print(colored("\n📈 Student State Changes:", "magenta", attrs=["bold"]))
        print("-" * 40)
        for state, value in evaluation['state_changes'].items():
            bar = "█" * int(value * 20)
            print(f"{state.title():15}: {bar} {value*100:.0f}%")
        
        print("\n" + "="*70 + "\n")

    def handle_teacher_response(self):
        """Handle teacher's response with better debug output."""
        # Get teacher input
        print(colored("\n💭 Enter your response:", "cyan"))
        teacher_response = input("> ").strip()
        
        try:
            # Process response and get evaluation
            print(colored("\nProcessing response...", "yellow"))
            evaluation = self.chatbot.evaluate_response(teacher_response, self.current_scenario)
            self.display_evaluation(evaluation)
            
            # Add to session history
            self.session.add_interaction(teacher_response, evaluation)

        except Exception as e:
            print(colored(f"\n❌ Error during evaluation: {str(e)}", "red"))
            print(colored("Debug info:", "red"))
            import traceback
            traceback.print_exc()

    def new_scenario(self):
        # Generate new scenario
        self.current_scenario = self.chatbot.generate_scenario()
        self.clear_screen()
        self.print_header()
        self.display_scenario(self.current_scenario)

    def display_knowledge_base(self):
        # Display knowledge base
        self.clear_screen()
        self.print_header()
        self.print_knowledge_summary(self.chatbot)

    def display_session_history(self):
        # Display session history
        print(colored("\n📋 Session History:", "yellow", attrs=["bold"]))
        print(colored("-" * 30, "yellow"))
        for interaction in self.session.history:
            print(f"• {interaction['timestamp']} - {interaction['teacher_response']}")
            print(f"  Score: {interaction['score']}")
            print(f"  Student Reaction: {interaction['student_reaction']}")
            print(f"  Feedback: {', '.join(interaction['feedback'])}")
            print(f"  Suggestions: {', '.join(interaction['suggestions'])}")

def main():
    simulator = TeacherTrainingSimulator()
    simulator.run()

if __name__ == "__main__":
    main() 