"""Streamlit interface for the teacher training simulator."""
import streamlit as st
from knowledge_processor import KnowledgeProcessor
from chatbot import TeacherTrainingChatbot

def initialize_knowledge_base():
    """Initialize and load knowledge base."""
    processor = KnowledgeProcessor()
    
    try:
        # Try to load processed knowledge
        processor.load()
        st.success("✅ Knowledge base loaded successfully")
    except:
        # Process knowledge base files
        with st.spinner("Processing knowledge base..."):
            processor.process_directory("knowledge_base")
            processor.save()
            st.success("✅ Knowledge base processed and saved")
    
    return processor

def initialize_session():
    """Initialize or reset session state."""
    if 'initialized' not in st.session_state:
        st.session_state.knowledge_processor = initialize_knowledge_base()
        st.session_state.chatbot = TeacherTrainingChatbot()
        st.session_state.messages = []
        st.session_state.current_scenario = st.session_state.chatbot.generate_scenario()
        initial_reaction = st.session_state.chatbot.get_initial_reaction(st.session_state.current_scenario)
        st.session_state.messages.append({"role": "student", "content": initial_reaction})
        st.session_state.initialized = True

def display_evaluation(evaluation):
    try:
        score = evaluation.get('score', evaluation.get('overall_score', 0.0))
        st.progress(score)
        
        # Handle feedback flexibly
        if isinstance(evaluation.get('feedback'), list):
            for item in evaluation['feedback']:
                st.success(f"✓ {item}")
        elif isinstance(evaluation.get('feedback'), dict):
            for strength in evaluation['feedback'].get('strengths', []):
                st.success(f"✓ {strength}")
        
        # Handle suggestions
        suggestions = (evaluation.get('suggestions', []) 
                     or evaluation.get('feedback', {}).get('suggestions', []))
        for suggestion in suggestions:
            st.info(f"→ {suggestion}")
        
        # Always show reaction if available
        if reaction := evaluation.get('student_reaction'):
            st.write("#### Student Reaction")
            st.write(reaction)
            
    except Exception as e:
        st.error(f"Error displaying evaluation: {str(e)}")
        st.write("Raw evaluation:", evaluation)

def main():
    st.set_page_config(
        page_title="Teacher Training Simulator",
        page_icon="🎓",
        layout="wide"
    )
    
    st.title("🎓 Second Grade Teacher Training Simulator")
    
    # Initialize session if needed
    initialize_session()
    
    # Display current scenario
    with st.expander("Current Scenario", expanded=True):
        st.write(st.session_state.current_scenario['description'])
        st.write("**Context:**")
        st.write(f"- Subject: {st.session_state.current_scenario['subject'].title()}")
        st.write(f"- Challenge: {st.session_state.current_scenario['difficulty']}")
    
    # Chat interface
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
    
    # Teacher input
    if prompt := st.chat_input("Your response..."):
        # Add teacher's response
        st.session_state.messages.append({
            "role": "teacher",
            "content": prompt
        })
        
        # Evaluate response
        evaluation = st.session_state.knowledge_processor.evaluate_response(
            prompt, 
            st.session_state.current_scenario
        )
        
        display_evaluation(evaluation)
        
        # Get student reaction
        response = st.session_state.chatbot.evaluate_response(
            prompt, 
            st.session_state.current_scenario
        )
        
        # Add student's response
        st.session_state.messages.append({
            "role": "student",
            "content": response["student_reaction"]
        })
        
        st.rerun()
    
    # New scenario button
    if st.button("🔄 New Scenario"):
        st.session_state.current_scenario = st.session_state.chatbot.generate_scenario()
        st.session_state.messages = []
        initial_reaction = st.session_state.chatbot.get_initial_reaction(st.session_state.current_scenario)
        st.session_state.messages.append({"role": "student", "content": initial_reaction})
        st.rerun()

if __name__ == "__main__":
    main() 