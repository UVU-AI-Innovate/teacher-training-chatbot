import sys
import os

# Add the project's root directory to the system path so that 'src' can be imported.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import json

from src.ai.chatbot import TeacherTrainingChatbot


def initialize_chatbot() -> TeacherTrainingChatbot:
    """Initialize the chatbot instance, stored in session state."""
    if 'chatbot' not in st.session_state:
        st.session_state.chatbot = TeacherTrainingChatbot()
    return st.session_state.chatbot

def generate_scenario(chatbot: TeacherTrainingChatbot, category: str, persona: str) -> dict:
    """Generate a scenario using the chatbot and store it in session state."""
    scenario = chatbot.generate_scenario(category, persona)
    st.session_state.scenario = scenario
    return scenario

def evaluate_teacher_response(chatbot: TeacherTrainingChatbot, teacher_response: str):
    """
    Evaluate the teacher response based on the current scenario.
    Returns a tuple of (evaluation, suggestions), or None if no scenario.
    """
    scenario = st.session_state.get('scenario')
    if scenario is None:
        st.error("Please generate a scenario first!")
        return None, None
    evaluation = chatbot.evaluate_response(scenario, teacher_response)
    suggestions = chatbot.get_improvement_suggestions(evaluation)
    return evaluation, suggestions

def render_generate_scenario_section(chatbot: TeacherTrainingChatbot):
    st.header("Generate Scenario")
    category = st.selectbox("Select Category", ["classroom_management"])
    persona = st.selectbox("Select Persona", ["active"])
    if st.button("Generate Scenario"):
        scenario = generate_scenario(chatbot, category, persona)
        st.subheader("Generated Scenario")
        st.json(scenario)

def render_evaluate_teacher_response_section(chatbot: TeacherTrainingChatbot):
    st.header("Evaluate Teacher Response")
    teacher_response = st.text_area("Enter Teacher Response", height=200)
    if st.button("Evaluate Response"):
        evaluation, suggestions = evaluate_teacher_response(chatbot, teacher_response)
        if evaluation is not None:
            st.subheader("Response Evaluation")
            st.json(evaluation)
            st.subheader("Improvement Suggestions")
            st.text(suggestions)

def main():
    st.title("Teacher Training Chatbot Web App")
    chatbot = initialize_chatbot()
    render_generate_scenario_section(chatbot)
    render_evaluate_teacher_response_section(chatbot)


if __name__ == "__main__":
    main() 