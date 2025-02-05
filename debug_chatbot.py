from chatbot import TeacherTrainingChatbot
import json
from colorama import init, Fore, Style
from termcolor import colored
import os

# Initialize colorama
init()

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Print the application header."""
    print(colored("\n🎓 Teacher Training Simulator - Debug Mode 🎓", "cyan", attrs=["bold"]))
    print(colored("=" * 50, "cyan"))

def print_knowledge_summary(chatbot):
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

def display_menu():
    """Display the interactive menu."""
    print(colored("\n📋 Options:", "green", attrs=["bold"]))
    print(colored("1.", "green") + " Respond to student")
    print(colored("2.", "green") + " New scenario")
    print(colored("3.", "green") + " View current scenario")
    print(colored("4.", "green") + " View knowledge base")
    print(colored("5.", "green") + " Exit")
    return input(colored("\nChoose an option (1-5): ", "green")).strip()

def display_scenario(scenario):
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

def display_evaluation(evaluation):
    """Display the evaluation results in a formatted way."""
    print(colored("\n📊 Evaluation Results:", "magenta", attrs=["bold"]))
    print(colored("-" * 50, "magenta"))
    
    # Overall explanation
    print(evaluation['overall_explanation'])
    
    # Context alignment
    print(colored("\nContext Alignment:", "magenta"))
    for key, value in evaluation['context_alignment'].items():
        print(f"• {key.replace('_', ' ').title()}: {value:.2f}")
    
    # Strategies
    print(colored("\nIdentified Strategies:", "magenta"))
    for strategy in evaluation['identified_strategies']:
        print(f"• {strategy['type'].replace('_', ' ').title()}: {strategy['effectiveness']:.2f}")
        if strategy['explanation']:
            print(f"  {strategy['explanation']}")
    
    # Feedback
    if evaluation['feedback']:
        print(colored("\nStrengths:", "green"))
        for strength in evaluation['feedback']:
            print(colored(f"✓ {strength}", "green"))
    
    print(colored("\nSuggestions:", "yellow"))
    for suggestion in evaluation['suggestions']:
        print(colored(f"→ {suggestion}", "yellow"))
    
    # Student reaction
    print(colored("\nStudent Reaction:", "cyan"))
    print(colored(evaluation['student_reaction'], "cyan"))

def main():
    clear_screen()
    print_header()
    
    # Initialize the chatbot
    print(colored("\nInitializing system...", "yellow"))
    chatbot = TeacherTrainingChatbot()
    
    # Display knowledge base summary
    print_knowledge_summary(chatbot)
    
    # Generate initial scenario
    scenario = chatbot.generate_scenario()
    display_scenario(scenario)

    while True:
        choice = display_menu()
        
        if choice == "1":
            # Get teacher input
            print(colored("\n💭 Enter your response:", "cyan"))
            teacher_response = input("> ").strip()
            
            try:
                # Process response and get evaluation
                evaluation = chatbot.evaluate_response(teacher_response, scenario)
                display_evaluation(evaluation)

            except Exception as e:
                print(colored(f"\n❌ Error during evaluation: {str(e)}", "red"))
                print(colored("Debug info:", "red"))
                import traceback
                traceback.print_exc()
                
        elif choice == "2":
            # Generate new scenario
            scenario = chatbot.generate_scenario()
            clear_screen()
            print_header()
            display_scenario(scenario)
            
        elif choice == "3":
            # Display current scenario
            clear_screen()
            print_header()
            display_scenario(scenario)
            
        elif choice == "4":
            # Display knowledge base
            clear_screen()
            print_header()
            print_knowledge_summary(chatbot)
            
        elif choice == "5":
            print(colored("\nThank you for using the Teacher Training Simulator! 👋", "cyan"))
            break
            
        else:
            print(colored("\n❌ Invalid choice. Please choose 1-5.", "red"))

if __name__ == "__main__":
    main() 