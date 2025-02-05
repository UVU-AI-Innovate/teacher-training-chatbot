"""Simple chat interface for the teacher training simulator."""
from chatbot import TeacherTrainingChatbot

def main():
    print("=== Second Grade Teacher Training Simulator ===")
    print("\nWelcome to your personalized teaching practice session!")
    
    bot = TeacherTrainingChatbot()
    bot.setup_teacher_profile()
    
    print("\nNow let's start practicing with some teaching scenarios.")
    print("Type 'quit' to end the session, 'new' for a new scenario, or 'help' for commands.")
    
    bot.start_interactive_session()

if __name__ == "__main__":
    main() 