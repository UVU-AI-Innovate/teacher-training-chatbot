"""Knowledge management system for the teacher training simulator."""
import os
from typing import List, Dict, Any
import json
import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

class KnowledgeManager:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        self.embedding_model = SentenceTransformer(model_name)
        self.vector_dim = 384  # Dimension for this model
        self.index = faiss.IndexFlatL2(self.vector_dim)
        self.documents = []
        self.categories = {
            "student_behavior": [],
            "teaching_strategies": [],
            "academic_content": [],
            "developmental_psychology": [],
            "classroom_management": []
        }

    def add_document(self, text: str, metadata: Dict[str, Any] = None):
        """Add a document to the vector store."""
        embedding = self.embedding_model.encode([text])[0]
        self.index.add(np.array([embedding]).astype('float32'))
        self.documents.append({
            'text': text,
            'metadata': metadata or {}
        })

    def add_educational_resource(self, file_path: str, category: str):
        """Process and add educational resource files."""
        _, ext = os.path.splitext(file_path)
        
        if ext == '.txt':
            with open(file_path, 'r') as f:
                content = f.read()
                sections = content.split('\n\n')
                for section in sections:
                    self.add_document(section, {
                        'category': category,
                        'source': file_path
                    })
                    self.categories[category].append(section)
        
        elif ext == '.csv':
            df = pd.read_csv(file_path)
            for _, row in df.iterrows():
                text = ' '.join(str(v) for v in row.values)
                self.add_document(text, {
                    'category': category,
                    'source': file_path,
                    'row_data': row.to_dict()
                })
                self.categories[category].append(text)
        
        elif ext == '.json':
            with open(file_path, 'r') as f:
                data = json.load(f)
                self._process_json_data(data, category, file_path)

    def _process_json_data(self, data: Any, category: str, source: str):
        """Recursively process JSON data."""
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, (str, int, float)):
                    text = f"{key}: {value}"
                    self.add_document(text, {
                        'category': category,
                        'source': source,
                        'key': key
                    })
                    self.categories[category].append(text)
                else:
                    self._process_json_data(value, category, source)
        elif isinstance(data, list):
            for item in data:
                self._process_json_data(item, category, source)

    def search(self, query: str, k: int = 3) -> List[Dict]:
        """Search for relevant knowledge."""
        query_vector = self.embedding_model.encode([query])[0]
        distances, indices = self.index.search(
            np.array([query_vector]).astype('float32'), k
        )
        
        return [
            {
                'text': self.documents[idx]['text'],
                'metadata': self.documents[idx]['metadata'],
                'relevance': float(1 / (1 + dist))
            }
            for dist, idx in zip(distances[0], indices[0])
            if idx != -1
        ]

    def get_teaching_context(self, scenario: Dict) -> Dict[str, List[str]]:
        """Get relevant teaching context for a scenario."""
        context = {
            "student_behavior": [],
            "teaching_strategies": [],
            "academic_content": []
        }
        
        # Search for relevant behavior information
        behavior_query = f"{scenario['behavioral_context']['type']} behavior in {scenario['subject']} class"
        behavior_results = self.search(behavior_query)
        context["student_behavior"] = [r['text'] for r in behavior_results]
        
        # Search for teaching strategies
        strategy_query = f"teaching strategies for {scenario['difficulty']} in {scenario['subject']}"
        strategy_results = self.search(strategy_query)
        context["teaching_strategies"] = [r['text'] for r in strategy_results]
        
        # Search for academic content
        content_query = f"{scenario['subject']} {scenario['difficulty']} second grade"
        content_results = self.search(content_query)
        context["academic_content"] = [r['text'] for r in content_results]
        
        return context

    def evaluate_response(self, response: str, scenario: Dict) -> Dict:
        """Evaluate teacher's response using knowledge base."""
        # Search for relevant teaching strategies
        relevant_strategies = self.search(
            f"effective teaching strategies for {scenario['behavioral_context']['type']} "
            f"in {scenario['subject']} {scenario['difficulty']}"
        )
        
        # Search for behavioral interventions
        relevant_interventions = self.search(
            f"interventions for {scenario['behavioral_context']['manifestation']} "
            f"in second grade"
        )
        
        # Calculate scores
        strategy_score = self._calculate_strategy_score(response, relevant_strategies)
        intervention_score = self._calculate_intervention_score(response, relevant_interventions)
        
        return {
            "strategy_score": strategy_score,
            "intervention_score": intervention_score,
            "total_score": (strategy_score + intervention_score) / 2,
            "relevant_strategies": [s['text'] for s in relevant_strategies],
            "relevant_interventions": [i['text'] for i in relevant_interventions]
        }

    def _calculate_strategy_score(self, response: str, strategies: List[Dict]) -> float:
        """Calculate how well the response uses recommended strategies."""
        score = 0.0
        response_embedding = self.embedding_model.encode([response])[0]
        
        for strategy in strategies:
            strategy_embedding = self.embedding_model.encode([strategy['text']])[0]
            similarity = float(faiss.pairwise_distances(
                response_embedding.reshape(1, -1),
                strategy_embedding.reshape(1, -1)
            ))
            score += similarity * strategy['relevance']
        
        return min(1.0, score / len(strategies) if strategies else 0.0)

    def _calculate_intervention_score(self, response: str, interventions: List[Dict]) -> float:
        """Calculate how well the response implements interventions."""
        score = 0.0
        response_embedding = self.embedding_model.encode([response])[0]
        
        for intervention in interventions:
            intervention_embedding = self.embedding_model.encode([intervention['text']])[0]
            similarity = float(faiss.pairwise_distances(
                response_embedding.reshape(1, -1),
                intervention_embedding.reshape(1, -1)
            ))
            score += similarity * intervention['relevance']
        
        return min(1.0, score / len(interventions) if interventions else 0.0)

    def save(self, directory: str = 'data/knowledge_base'):
        """Save the knowledge base."""
        os.makedirs(directory, exist_ok=True)
        
        # Save index
        faiss.write_index(self.index, f'{directory}/vectors.index')
        
        # Save documents and categories
        with open(f'{directory}/documents.json', 'w') as f:
            json.dump({
                'documents': self.documents,
                'categories': self.categories
            }, f)

    def load(self, directory: str = 'data/knowledge_base'):
        """Load the knowledge base."""
        # Load index
        self.index = faiss.read_index(f'{directory}/vectors.index')
        
        # Load documents and categories
        with open(f'{directory}/documents.json', 'r') as f:
            data = json.load(f)
            self.documents = data['documents']
            self.categories = data['categories']

    def load_default_knowledge(self):
        """Load default knowledge base files."""
        default_dir = "default_knowledge"
        
        try:
            # Load teaching strategies
            self.add_educational_resource(
                f"{default_dir}/teaching_strategies.txt",
                "teaching_strategies"
            )
            
            # Load student behaviors
            self.add_educational_resource(
                f"{default_dir}/student_behaviors.json",
                "student_behavior"
            )
            
            # Load academic content
            self.add_educational_resource(
                f"{default_dir}/math_strategies.csv",
                "academic_content"
            )
            
            print("Default knowledge base loaded successfully")
        except Exception as e:
            print(f"Error loading default knowledge: {e}")

    def get_stats(self) -> dict:
        """Get statistics about the knowledge base."""
        return {
            category: len(items) 
            for category, items in self.categories.items()
            if items  # Only show categories with items
        }

    def is_loaded(self) -> bool:
        """Check if knowledge base has content."""
        return any(len(items) > 0 for items in self.categories.values())

    def get_category_sample(self, category: str, n: int = 3) -> list:
        """Get sample entries from a category."""
        items = self.categories.get(category, [])
        return items[:n] if items else [] 