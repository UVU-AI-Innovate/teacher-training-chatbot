# Teacher Training Simulator 🎓

An AI-powered second-grade student simulator for teacher training, designed to help teachers practice their responses to various classroom scenarios.

## Overview

This simulator creates realistic classroom scenarios and provides immediate feedback on teaching strategies. It uses advanced AI including LLMs, speech synthesis, and computer vision to create an immersive training environment.

## Key Features

### 1. Scenario Generation
- Creates contextual teaching scenarios
- Considers multiple factors:
  - Time of day (morning, after lunch, late afternoon)
  - Subject matter (math, reading)
  - Student learning styles (visual, auditory, kinesthetic)
  - Behavioral triggers
  - Student states

### 2. Knowledge Management
The system processes and stores teaching knowledge from various sources:
- Teaching strategies
- Student behaviors
- Classroom management techniques
- Subject-specific content
- Learning style adaptations
- Behavioral interventions

Supported file formats:
- PDF Documents (.pdf)
- Word Documents (.docx)
- Text Files (.txt)
- Markdown Files (.md)
- JSON Files (.json)
- YAML Files (.yml)
- CSV Files (.csv)

### 3. Response Evaluation
Evaluates teacher responses across four dimensions:
1. Time-appropriate strategies (20%)
2. Learning style alignment (20%)
3. Behavioral management (30%)
4. Subject-specific support (30%)

### 4. Student Simulation
- Generates contextual student reactions
- Simulates different learning styles
- Models emotional states and engagement levels
- Provides behavioral feedback

## Technical Architecture

### System Overview

```mermaid
graph TB
    subgraph Frontend["Frontend Layer"]
        UI[Terminal Interface]
        Session[Session Manager]
    end

    subgraph Core["Core Processing Layer"]
        Chat[EduAgent]
        Eval[Response Evaluator]
        Sim[Student Simulator]
        Scen[Scenario Generator]
    end

    subgraph Models["Model Layer"]
        LLM[Primary LLM]
        Emb[Embedding Model]
    end

    subgraph Knowledge["Knowledge Layer"]
        KB[Knowledge Base]
        VS[Vector Store]
        Meta[Metadata Store]
    end

    UI --> Session
    Session --> Chat
    Chat --> Eval
    Chat --> Sim
    Chat --> Scen
    
    Eval --> LLM
    Sim --> LLM
    Scen --> LLM
    
    KB --> VS
    VS --> Emb
    KB --> Meta
    
    Eval --> VS
    Sim --> VS
    Scen --> VS

    style Frontend fill:#f9f,stroke:#333,stroke-width:2px
    style Core fill:#bbf,stroke:#333,stroke-width:2px
    style Models fill:#bfb,stroke:#333,stroke-width:2px
    style Knowledge fill:#fbb,stroke:#333,stroke-width:2px
```

### Data Flow Architecture

```mermaid
sequenceDiagram
    participant T as Teacher
    participant UI as Interface
    participant C as Chatbot Core
    participant LLM as Language Model
    participant K as Knowledge Base

    T->>UI: Input Response
    UI->>C: Process Input
    
    par Knowledge Retrieval
        C->>K: Fetch Relevant Strategies
        K-->>C: Return Matched Strategies
    and LLM Processing
        C->>LLM: Generate Evaluation
        LLM-->>C: Return Analysis
    end
    
    C->>UI: Generate Feedback
    UI->>T: Display Results
```

### Knowledge Processing Pipeline

```mermaid
graph LR
    subgraph Input["Input Processing"]
        R[Raw Files] --> E[Extraction]
        E --> C[Chunking]
    end

    subgraph Embedding["Embedding Generation"]
        C --> V[Vector Creation]
        V --> S[Similarity Indexing]
    end

    subgraph Storage["Storage Layer"]
        S --> VS[Vector Store]
        S --> M[Metadata DB]
    end

    style Input fill:#f9f,stroke:#333,stroke-width:2px
    style Embedding fill:#bbf,stroke:#333,stroke-width:2px
    style Storage fill:#bfb,stroke:#333,stroke-width:2px
```

### LLM Integration Architecture

```mermaid
graph TB
    subgraph Input["Input Layer"]
        TR[Teacher Response]
        SC[Scenario Context]
    end

    subgraph Processing["LLM Processing"]
        direction TB
        PE[Primary Evaluation]
        SM[Strategy Matching]
        CA[Context Analysis]
    end

    subgraph Output["Output Generation"]
        SR[Student Response]
        FB[Feedback]
        MS[Metrics & Scores]
    end

    TR --> PE
    SC --> PE
    PE --> SM
    PE --> CA
    
    SM --> SR
    CA --> FB
    SM & CA --> MS

    style Input fill:#f9f,stroke:#333,stroke-width:2px
    style Processing fill:#bbf,stroke:#333,stroke-width:2px
    style Output fill:#bfb,stroke:#333,stroke-width:2px
```

### Model Deployment Options

```mermaid
graph TB
    subgraph HP["High Performance"]
        M7B[Mistral 7B]
        MiniLM1[MiniLM-L6-v2]
        RAM1[18GB RAM]
    end

    subgraph BA["Balanced"]
        PHI[Phi-2]
        MiniLM2[MiniLM-L6-v2]
        RAM2[8GB RAM]
    end

    subgraph LW["Lightweight"]
        TL[TinyLlama-1.1B]
        MiniLM3[MiniLM-L6-v2]
        RAM3[6GB RAM]
    end

    style HP fill:#bfb,stroke:#333,stroke-width:2px
    style BA fill:#bbf,stroke:#333,stroke-width:2px
    style LW fill:#f9f,stroke:#333,stroke-width:2px
```

### Components

1. `EduAgent` (formerly TeacherTrainingChatbot)
   - Core simulation engine powered by multimodal AI technology
   - **AI Integration**:
     ```mermaid
     graph TB
         subgraph Agent["EduAgent System"]
             direction TB
             Input[["Multimodal Input"]]
             Context[Scenario Context]
             AI[AI Engine]
             KB[Knowledge Base]
             Output[["Multimodal Output"]]
             
             subgraph Inputs["Input Processing"]
                 Text[Text Input]
                 Voice[Voice Input]
                 Visual[Visual Input]
             end
             
             subgraph Outputs["Output Generation"]
                 Speech[Speech Synthesis]
                 Animation[Visual Feedback]
                 Text2[Text Response]
             end
             
             Inputs --> Input
             Input --> AI
             Context --> AI
             KB --> AI
             AI --> Output
             Output --> Outputs
         end

         style Inputs fill:#f9f,stroke:#333,stroke-width:2px
         style Outputs fill:#bfb,stroke:#333,stroke-width:2px
     ```
   - **Key AI Capabilities**:
     - Natural Language Processing (Text & Voice)
     - Speech Synthesis for realistic student voices
     - Visual Avatar Generation
     - Gesture and Expression Synthesis
     - Real-time Interaction Processing
   
   - **Multimodal Processing Pipeline**:
     ```
     1. Input Processing:
        - Text Input: Natural Language Processing
        - Voice Input: Speech-to-Text + Tone Analysis
        - Visual Input: Gesture/Expression Recognition
     
     2. AI Processing:
        - Core LLM Processing (Mistral/Llama/etc.)
        - Emotional State Modeling
        - Behavioral Pattern Analysis
        - Context Integration
     
     3. Output Generation:
        - Text Generation
        - Speech Synthesis
        - Visual Avatar Animation
        - Emotional Expression Rendering
     ```
   - **Interaction Modes**:
     - Text-only (Current)
     - Voice-enabled (Planned)
     - Visual Avatar (Planned)
     - Full Multimodal (Future)

2. `KnowledgeManager`
   - Processes teaching resources
   - Manages vector embeddings
   - Handles similarity search

3. `KnowledgeStore`
   - Persistent storage for processed knowledge
   - Vector database for semantic search
   - Document metadata management

4. `TerminalInterface`
   - User interaction handling
   - Display formatting
   - Session management

### Data Flow

1. Knowledge Processing:
   ```
   Raw Files → Extraction → Chunking → Embedding → Vector Store
   ```

2. Scenario Generation:
   ```
   Context Selection → State Generation → Scenario Assembly
   ```

3. Response Evaluation:
   ```
   Teacher Input → Strategy Matching → Multi-dimensional Scoring → Feedback Generation
   ```

## Recommended LLMs

The teacher training simulator is designed to work with various Language Learning Models (LLMs). Here are recommended open-source, local LLMs that work well with this system:

### Why These Models for Educational Chatbots?

Educational chatbots have specific requirements that make certain LLMs more suitable:
1. **Context Understanding**: Must maintain coherent dialogue about educational concepts
2. **Consistent Persona**: Need to maintain a consistent student personality
3. **Real-time Response**: Quick inference for natural conversation flow
4. **Domain Knowledge**: Understanding of educational terminology and concepts
5. **Resource Efficiency**: Ability to run locally on standard hardware

### Primary Recommendation: Mistral
- **Model**: Mistral 7B
- **Why**: Excellent balance of performance and resource requirements
- **Use Cases**: Main response evaluation, student simulation, scenario generation
- **Requirements**: ~16GB RAM
- **Strengths for Chatbots**:
  - Strong dialogue management capabilities
  - Excellent context retention across conversations
  - Good at role-playing (crucial for student simulation)
  - Efficient token processing for quick responses
  - Built-in educational domain knowledge

### Alternative Options:

1. **Llama 2**
   - Models: 7B or 13B variants
   - Good for: Complex teaching strategy evaluation
   - Requirements: 16-24GB RAM
   - **Chatbot Advantages**:
     - Superior instruction following
     - Strong multi-turn conversation abilities
     - Excellent at maintaining consistent personas
     - High-quality educational content generation
     - Well-tested in production environments

2. **BLOOMZ**
   - Models: BLOOMZ-7B1
   - Good for: Multilingual capabilities
   - Requirements: ~16GB RAM
   - **Chatbot Advantages**:
     - Excellent for diverse student populations
     - Strong cross-cultural understanding
     - Good at handling educational terminology
     - Natural conversational flow in multiple languages
     - Consistent personality across languages

3. **Phi-2**
   - Model: Phi-2 (2.7B parameters)
   - Good for: Lightweight deployments
   - Requirements: ~6GB RAM
   - **Chatbot Advantages**:
     - Very fast response generation
     - Good at concise, focused answers
     - Strong performance on educational tasks
     - Efficient context processing
     - Low latency for real-time interactions

4. **TinyLlama**
   - Model: TinyLlama-1.1B
   - Good for: Resource-constrained environments
   - Requirements: ~4GB RAM
   - **Chatbot Advantages**:
     - Ultra-fast inference
     - Good at short, focused interactions
     - Efficient memory usage
     - Suitable for rapid back-and-forth dialogue
     - Works well on basic hardware

### Embedding Models
For semantic search and knowledge retrieval, the system uses:
- **all-MiniLM-L6-v2**: Lightweight sentence transformer model
- Purpose: Generates embeddings for teaching strategies and responses
- Requirements: ~1GB RAM
- Performance: Excellent for semantic similarity tasks
- **Chatbot Benefits**:
  - Fast retrieval of relevant teaching strategies
  - Accurate semantic matching for response evaluation
  - Efficient memory usage alongside main LLM
  - Good at understanding paraphrased student questions
  - Helps maintain conversation coherence

### Deployment Recommendations:

1. **High-Performance Setup** (Best for complex scenarios):
   - Primary: Mistral 7B
   - Embedding: all-MiniLM-L6-v2
   - Total RAM Required: ~18GB
   - Ideal for: Full-featured teaching simulations with complex student behaviors

2. **Balanced Setup** (Good for most use cases):
   - Primary: Phi-2
   - Embedding: all-MiniLM-L6-v2
   - Total RAM Required: ~8GB
   - Ideal for: Standard teaching scenarios with good response times

3. **Lightweight Setup** (Basic functionality):
   - Primary: TinyLlama-1.1B
   - Embedding: all-MiniLM-L6-v2
   - Total RAM Required: ~6GB
   - Ideal for: Basic teaching interactions and rapid prototyping

### Model Quantization Options
All recommended models support various quantization levels:
- **GGUF Format**: 4-bit, 5-bit, and 8-bit quantization available
- **Memory Reduction**: Up to 75% reduction in RAM requirements
- **Speed Impact**: Minimal impact on response quality
- **Recommendation**: Start with 4-bit quantization for optimal balance

All models can be downloaded and run locally using [Ollama](https://ollama.ai/) or [llama.cpp](https://github.com/ggerganov/llama.cpp).

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/teacher-training-simulator.git

# Install dependencies
pip install -r requirements.txt
```

## Usage

```bash
# Run the simulator
python terminal_app.py
```

## Knowledge Base Structure

```
knowledge_base/
├── documents/           # Original files
│   ├── teaching/       # Teaching strategies
│   ├── behavior/       # Student behaviors
│   └── content/        # Subject content
│
└── processed/          # Processed data
    ├── knowledge.db    # Vector store
    └── metadata.json   # File information
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## System Architecture

```mermaid
graph TD
    A[Knowledge Base] --> B[Knowledge Processor]
    B --> C[Chatbot Core]
    C --> D[User Interface]
    
    subgraph Knowledge Layer
    A --> |Teaching Strategies| A1[strategies.txt]
    A --> |Student Behaviors| A2[behaviors.json]
    A --> |Academic Content| A3[math_strategies.csv]
    end
    
    subgraph Processing Layer
    B --> |Vector Store| B1[Embeddings]
    B --> |Categories| B2[Document Store]
    end
    
    subgraph Interaction Layer
    C --> |Generate| C1[Scenarios]
    C --> |Evaluate| C2[Responses]
    C --> |Track| C3[Progress]
    end
    
    subgraph Interface Layer
    D --> |Display| D1[Scenario]
    D --> |Chat| D2[Interaction]
    D --> |Show| D3[Feedback]
    end
```

## Core Components

### 1. Knowledge Base
- **Teaching Strategies**: Pedagogical approaches and interventions
- **Student Behaviors**: Common behavioral patterns and responses
- **Academic Content**: Subject-specific challenges and solutions

### 2. Scenario Generation
```python
Scenario = {
    "subject": "math/reading",
    "time_of_day": "morning/after lunch/late afternoon",
    "student_context": {
        "learning_style": "visual/auditory/kinesthetic",
        "attention_span": 0.0-1.0,
        "social_confidence": 0.0-1.0,
        "seating": "front/middle/back row",
        "peer_interactions": "group/solo/distracted/shy"
    },
    "behavioral_context": {
        "type": "attention/frustration",
        "trigger": "specific event",
        "manifestation": "observable behavior"
    }
}
```

### 3. Response Evaluation
The system evaluates teacher responses based on four key criteria:

1. **Time-Appropriate Strategies** (20%)
   - Morning: structured start, clear expectations
   - After lunch: movement breaks, energy management
   - Late afternoon: short tasks, varied activities

2. **Learning Style Alignment** (20%)
   - Visual: show, draw, look at
   - Auditory: tell, listen, discuss
   - Kinesthetic: try, move, build

3. **Behavioral Management** (30%)
   - Attention: focus strategies, engagement techniques
   - Frustration: confidence building, support approaches

4. **Subject-Specific Support** (30%)
   - Math: step-by-step, manipulatives, visualization
   - Reading: phonics, comprehension strategies, guided practice

## Teacher Response Evaluation System

### Overview
The system uses a combination of LLM-based semantic understanding and rule-based scoring to evaluate teacher responses:
- Semantic similarity with known effective strategies
- Context-aware response evaluation
- Dynamic learning from the knowledge base
- Adaptive feedback generation

### Evaluation Architecture

```mermaid
flowchart TD
    A[Teacher Response] --> B[LLM Processor]
    K[Knowledge Base] --> B
    
    B --> C1[Semantic Analysis]
    B --> C2[Context Matching]
    B --> C3[Strategy Alignment]
    
    C1 --> D[Vector Similarity]
    C2 --> D
    C3 --> D
    
    D --> E[Score Generation]
    E --> F[Feedback Creation]
    
    subgraph "Knowledge Processing"
        K --> K1[Effective Strategies]
        K --> K2[Response Patterns]
        K --> K3[Context Rules]
    end
    
    subgraph "Semantic Analysis"
        C1 --> SA1[Intent Recognition]
        C1 --> SA2[Strategy Identification]
        C1 --> SA3[Tone Analysis]
    end
```

### LLM-Based Evaluation Process

1. **Semantic Understanding**
```python
def evaluate_semantic_similarity(response: str, context: dict) -> float:
    """
    Use LLM to understand the semantic meaning of teacher's response
    and compare it with known effective strategies.
    """
    # Encode teacher's response
    response_embedding = embedding_model.encode(response)
    
    # Get relevant strategies from knowledge base
    relevant_strategies = knowledge_base.get_strategies(
        subject=context["subject"],
        behavior=context["behavioral_context"]["type"],
        learning_style=context["student_context"]["learning_style"]
    )
    
    # Calculate semantic similarity
    similarities = []
    for strategy in relevant_strategies:
        strategy_embedding = embedding_model.encode(strategy["text"])
        similarity = cosine_similarity(response_embedding, strategy_embedding)
        similarities.append(similarity * strategy["effectiveness"])
    
    return max(similarities)
```

2. **Context Analysis**
```python
def analyze_context_alignment(response: str, context: dict) -> dict:
    """
    Use LLM to analyze how well the response aligns with the
    specific teaching context.
    """
    prompt = f"""
    Context:
    - Subject: {context['subject']}
    - Student Learning Style: {context['student_context']['learning_style']}
    - Behavior Type: {context['behavioral_context']['type']}
    - Time of Day: {context['time_of_day']}
    
    Teacher's Response: "{response}"
    
    Analyze how well this response addresses:
    1. Subject-specific needs
    2. Learning style alignment
    3. Behavioral management
    4. Time-appropriate strategy
    """
    
    analysis = llm.generate(prompt)
    return parse_llm_analysis(analysis)
```

3. **Strategy Identification**
```python
def identify_teaching_strategies(response: str) -> list:
    """
    Use LLM to identify specific teaching strategies used in the response.
    """
    prompt = f"""
    Identify teaching strategies in: "{response}"
    Consider:
    - Instructional techniques
    - Behavioral management
    - Student engagement
    - Emotional support
    """
    
    strategies = llm.generate(prompt)
    return extract_strategies(strategies)
```

### Comprehensive Evaluation Example

```python
Input Scenario:
{
    "subject": "math",
    "topic": "two-digit addition",
    "student_context": {
        "learning_style": "visual",
        "attention_span": 0.4,
        "current_state": "frustrated"
    }
}

Teacher Response:
"I see you're having trouble with this problem. Let's try something different.
I'll draw out the numbers using base-10 blocks on the board, so you can see
how regrouping works. Would you like to help me draw them?"

LLM Evaluation:
{
    "semantic_similarity": 0.85,  # High match with known effective strategies
    
    "context_alignment": {
        "subject_specific": 0.9,  # Strong math visualization
        "learning_style": 0.95,   # Excellent visual approach
        "behavioral": 0.8,        # Good frustration management
        "timing": 0.75           # Appropriate pacing
    },
    
    "identified_strategies": [
        {
            "type": "visualization",
            "effectiveness": 0.9,
            "context_appropriateness": 0.95
        },
        {
            "type": "student_engagement",
            "effectiveness": 0.85,
            "context_appropriateness": 0.8
        },
        {
            "type": "scaffolding",
            "effectiveness": 0.9,
            "context_appropriateness": 0.9
        }
    ],
    
    "overall_score": 0.88,
    
    "feedback": {
        "strengths": [
            "Excellent use of visual representation",
            "Good recognition of student frustration",
            "Effective engagement through participation"
        ],
        "suggestions": [
            "Consider adding explicit praise for effort",
            "Could incorporate previous successes reference"
        ]
    }
}
```

### Dynamic Learning

The system improves over time by:
1. Recording successful teaching strategies
2. Analyzing patterns in effective responses
3. Updating the knowledge base with new examples
4. Refining evaluation criteria based on outcomes

```python
def update_knowledge_base(response: str, effectiveness: float):
    """
    Add successful strategies to knowledge base for future reference.
    """
    if effectiveness > 0.8:
        new_strategy = {
            "text": response,
            "effectiveness": effectiveness,
            "context": current_context,
            "outcomes": student_reactions
        }
        knowledge_base.add_strategy(new_strategy)
```

## Workflow

```mermaid
sequenceDiagram
    participant T as Teacher
    participant UI as Interface
    participant C as Chatbot
    participant K as Knowledge Base

    K->>C: Load knowledge
    C->>UI: Initialize session
    UI->>T: Display scenario
    
    loop Interaction
        T->>UI: Teacher response
        UI->>C: Process response
        C->>K: Check against knowledge
        K->>C: Return evaluation
        C->>UI: Generate feedback
        UI->>T: Show student reaction
    end
```

## Usage Example

1. **Scenario Generation**:
```
Time: morning. Students are generally alert but may need time to settle.

Student Profile:
- Learning style: visual
- Seating: back row
- Peer interaction: easily distracted by peers
- Current challenges: number sense, staying focused

Situation:
During math class, while working on two-digit addition, 
the student is fidgeting after struggling with regrouping.
```

2. **Teacher Response**:
```
"Let's try this together. We can use these base-10 blocks to see how 
regrouping works. Watch as I show you step by step."
```

3. **Evaluation**:
```
Score: 0.9
✓ Good use of morning appropriate strategy
✓ Response matches visual learning style
✓ Appropriate behavioral support
✓ Good math-specific support
```

## File Structure
```
teacher_training_simulator/
├── app.py                 # Streamlit interface
├── chatbot.py            # Core chatbot logic
├── knowledge_processor.py # Knowledge processing
├── knowledge_base/       # Knowledge files
│   ├── teaching_strategies.txt
│   ├── student_behaviors.json
│   └── math_strategies.csv
└── processed_knowledge/   # Vector store
```

## Setup and Running

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
streamlit run app.py
```

## Contributing

Feel free to contribute by:
1. Adding more teaching scenarios
2. Enhancing evaluation criteria
3. Improving student responses
4. Adding new subjects/behaviors

## Interface Architecture

```mermaid
graph TB
    subgraph Current["Current Implementation"]
        direction TB
        T[Terminal Interface]
        TC[Terminal Controller]
        TU[Terminal UI]
        
        T --> TC
        TC --> TU
    end

    subgraph Future["Future Web Implementation"]
        direction TB
        S[Streamlit App]
        API[FastAPI Backend]
        WS[WebSocket Handler]
        
        S --> API
        S --> WS
    end

    subgraph Core["Core System"]
        direction TB
        CE[Chatbot Engine]
        KM[Knowledge Manager]
        LLM[LLM Handler]
        
        CE --> KM
        CE --> LLM
    end

    Current --> Core
    Future --> Core

    style Current fill:#bbf,stroke:#333,stroke-width:2px
    style Future fill:#fbb,stroke:#333,stroke-width:2px
    style Core fill:#bfb,stroke:#333,stroke-width:2px
```

### Current Terminal Implementation

The current implementation uses a terminal-based interface for optimal performance:

```mermaid
sequenceDiagram
    participant T as Teacher
    participant TI as Terminal Interface
    participant CE as Chatbot Engine
    participant LLM as LLM Handler
    
    T->>TI: Enter Response
    TI->>CE: Process Input
    CE->>LLM: Generate Analysis
    LLM-->>CE: Return Evaluation
    CE-->>TI: Format Output
    TI-->>T: Display Results
    
    Note over TI,CE: Direct Communication
    Note over CE,LLM: No Network Latency
```

#### Terminal Benefits
- **Performance**: Direct system access without web overhead
- **Low Latency**: Minimal communication layers
- **Resource Efficiency**: No additional web framework overhead
- **Rapid Development**: Faster iteration and testing
- **Focus on Core Logic**: Emphasis on AI and evaluation quality

### Future Web Implementation

The planned web interface using Streamlit will be implemented as a separate layer:

```mermaid
graph TB
    subgraph WebArch["Web Architecture"]
        direction TB
        subgraph FE["Frontend"]
            ST[Streamlit App]
            WC[Web Components]
        end
        
        subgraph BE["Backend"]
            API[FastAPI]
            WS[WebSocket]
            Cache[Redis Cache]
        end
        
        subgraph Core["Core System"]
            CE[Chatbot Engine]
            LLM[LLM Handler]
            KB[Knowledge Base]
        end
        
        ST --> API
        ST --> WS
        API --> Cache
        Cache --> CE
        CE --> LLM
        CE --> KB
    end

    style FE fill:#f9f,stroke:#333,stroke-width:2px
    style BE fill:#bbf,stroke:#333,stroke-width:2px
    style Core fill:#bfb,stroke:#333,stroke-width:2px
```

#### Performance Optimization Strategy

To maintain performance in the web implementation:

1. **Asynchronous Processing**
```mermaid
sequenceDiagram
    participant U as User
    participant S as Streamlit
    participant A as API
    participant C as Cache
    participant E as Engine
    
    U->>S: Submit Response
    S->>A: API Request
    A->>C: Check Cache
    
    alt Cache Hit
        C-->>A: Return Cached Result
        A-->>S: Quick Response
    else Cache Miss
        C->>E: Process New Request
        E-->>C: Store Result
        C-->>A: Return Result
        A-->>S: Full Response
    end
    
    S-->>U: Display Result
```

2. **Caching Strategy**
- Response caching for similar queries
- Vector embedding caching
- Session state management
- Incremental updates

3. **Resource Management**
```mermaid
graph LR
    subgraph Resources["Resource Allocation"]
        LLM[LLM Processing]
        Vec[Vector Operations]
        DB[Database Queries]
    end
    
    subgraph Optimization["Optimization Layer"]
        Cache[Redis Cache]
        Queue[Task Queue]
        Load[Load Balancer]
    end
    
    Queue --> LLM
    Queue --> Vec
    Load --> DB
    
    style Resources fill:#bbf,stroke:#333,stroke-width:2px
    style Optimization fill:#bfb,stroke:#333,stroke-width:2px
```

### Development Roadmap

1. **Phase 1: Terminal (Current)**
   - Core functionality implementation
   - LLM integration and optimization
   - Knowledge base development
   - Performance benchmarking

2. **Phase 2: API Development**
   - FastAPI backend implementation
   - WebSocket integration
   - Caching layer setup
   - Authentication system

3. **Phase 3: Web Interface**
   - Streamlit app development
   - Real-time updates
   - Interactive visualizations
   - User session management

4. **Phase 4: Optimization**
   - Performance tuning
   - Scale testing
   - Resource optimization
   - Monitoring implementation

## Usage

### Current Terminal Version
```bash
# Run the terminal version
python terminal_app.py
```

### Future Web Version (Coming Soon)
```bash
# Run the web version
streamlit run app.py
```