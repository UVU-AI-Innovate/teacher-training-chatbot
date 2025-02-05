# UTTA Development (Phase One - Chatbot)

An AI-powered educational simulation chatbot designed to help teachers develop and refine their teaching strategies through interactive text-based practice with a simulated second-grade student.

## System Overview

```mermaid
sequenceDiagram
    participant T as Teacher
    participant UI as User Interface
    participant Engine as AI Engine
    participant KB as Knowledge Base
    
    %% Styling
    rect rgb(240, 248, 255)
        Note over T,KB: Initial Setup
        Note over T,UI: Teacher runs web app (streamlit run web_app.py)
        T->>+UI: Start Session
        Note over T,UI: Select teaching subject & grade level
        UI->>+Engine: Initialize System
        Note over Engine: Configure LLM & load models
        Engine->>+KB: Load Teaching Data
        KB-->>-Engine: Scenarios & Strategies
        Engine-->>-UI: Ready for Interaction
        Note over UI: Display scenario options
    end
    
    Note over T,KB: Teaching Interaction
    rect rgb(230, 255, 240)
        Note over T,UI: Teacher types response to student situation
        T->>+UI: Enter Teaching Response
        Note over UI: Process text input & validate
        UI->>+Engine: Process Input
        Note over Engine: Analyze teaching approach
        Engine->>+KB: Query Knowledge Base
        KB-->>-Engine: Relevant Teaching Patterns
        Note over Engine: Generate student behavior
        Engine->>Engine: Generate Response
        Engine-->>-UI: Student Response & Feedback
        Note over UI: Show student reaction & teaching tips
        UI-->>-T: Display Interaction
        Note over UI: Save interaction history
        UI->>KB: Store Interaction Data
    end
    
    rect rgb(255, 240, 245)
        Note over T,KB: Progress Tracking
        Note over T,UI: Teacher clicks "View Progress"
        T->>+UI: Review Performance
        Note over UI: Generate analytics request
        UI->>+KB: Fetch Analytics
        Note over KB: Process teaching patterns
        KB-->>-UI: Progress Data
        Note over UI: Create visual reports
        UI-->>-T: Show Progress Report
        Note over T: View scores, trends & suggestions
    end
```

The application works through three main components that interact seamlessly to provide a realistic teaching simulation:

1. **User Interface**: Handles teacher interactions through both terminal and web interfaces
2. **AI Engine**: Processes inputs and generates contextual responses using LLM technology
3. **Knowledge Base**: Manages teaching scenarios, strategies, and interaction history

## Application Components

### 1. Core AI Engine

The AI Engine is the core of our application, handling:
- Natural language processing of teacher inputs
- Context management for conversations
- LLM-based response generation
- Response evaluation and feedback


### 2. Knowledge Management System

The Knowledge Management System handles:
- Storage and retrieval of teaching scenarios
- Vector-based similarity search
- Response pattern matching
- Performance analytics


### 3. User Interface System

The User Interface System provides:
- Interactive chat interface
- Real-time feedback display
- Progress tracking and visualization
- Session management


## Component Details

### AI Engine Configuration
```python
# Example AI engine configuration
config = {
    "model": "llama-2-7b-chat",
    "context_length": 2048,
    "temperature": 0.7,
    "response_cache": True
}
```

### Knowledge Base Structure
```python
# Example knowledge base entry
scenario = {
    "context": "Math Class",
    "difficulty": "intermediate",
    "student_state": {
        "learning_style": "visual",
        "attention": 0.8,
        "frustration": 0.3
    }
}
```

### Interface Features
```python
# Example interface configuration
ui_config = {
    "chat_history": 10,
    "feedback_delay": 0.5,
    "auto_suggestions": True,
    "progress_tracking": True
}
```

## Getting Started

### For Teachers
```bash
# Terminal interface
python terminal_app.py

# Web interface
streamlit run web_app.py
```

### For Developers
```bash
# Installation
git clone https://github.com/yourusername/teacher-training-simulator.git
pip install -r requirements.txt

# Development
python -m pytest tests/
python run_dev_server.py
```

## Contributing

### AI Development
- Model integration and tuning
- Prompt engineering
- Response generation
- Evaluation metrics

### Data Management
- Scenario development
- Knowledge base expansion
- Analytics implementation
- Pattern recognition

### Web Development
- Interface improvements
- Feature implementation
- Performance optimization
- User experience enhancement

## License

This project is licensed under the MIT License - see the LICENSE file for details.