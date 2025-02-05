"""
Retrieval-Augmented Generation (RAG) pipeline for educational content.

This module implements a RAG pipeline that retrieves relevant educational
content to enhance the chatbot's responses with domain knowledge.
"""

from typing import List, Dict, Optional, Union
from pathlib import Path
import json
import yaml
import logging
from datetime import datetime

from .embedding import EmbeddingHandler

logger = logging.getLogger(__name__)

class RAGPipeline:
    def __init__(self,
                embedding_handler: EmbeddingHandler,
                resources_dir: Optional[Union[str, Path]] = None):
        """Initialize the RAG pipeline.
        
        Args:
            embedding_handler: Handler for generating embeddings
            resources_dir: Directory containing educational resources
        """
        self.embedding_handler = embedding_handler
        self.resources_dir = Path(resources_dir) if resources_dir else Path(__file__).parent.parent.parent / "data/education_resources"
        
        # Load and index resources
        self.resources = self._load_resources()
        self._index_resources()
        
    def _load_resources(self) -> Dict:
        """Load educational resources from various files."""
        resources = {
            "curriculum": {},
            "standards": {},
            "best_practices": {},
            "lesson_plans": {},
            "assessments": {}
        }
        
        try:
            # Load curriculum
            curriculum_path = self.resources_dir / "curriculum"
            for file in curriculum_path.glob("**/*.yaml"):
                with open(file, "r") as f:
                    resources["curriculum"][file.stem] = yaml.safe_load(f)
            
            # Load teaching standards
            standards_path = self.resources_dir / "standards"
            for file in standards_path.glob("**/*.json"):
                with open(file, "r") as f:
                    resources["standards"][file.stem] = json.load(f)
            
            # Load best practices
            practices_path = self.resources_dir / "best_practices"
            for file in practices_path.glob("**/*.yaml"):
                with open(file, "r") as f:
                    resources["best_practices"][file.stem] = yaml.safe_load(f)
            
            # Load lesson plans
            plans_path = self.resources_dir / "lesson_plans"
            for file in plans_path.glob("**/*.yaml"):
                with open(file, "r") as f:
                    resources["lesson_plans"][file.stem] = yaml.safe_load(f)
            
            # Load assessment rubrics
            assessment_path = self.resources_dir / "assessments"
            for file in assessment_path.glob("**/*.yaml"):
                with open(file, "r") as f:
                    resources["assessments"][file.stem] = yaml.safe_load(f)
                    
        except Exception as e:
            logger.error(f"Failed to load resources: {str(e)}")
            raise
            
        return resources

    def _index_resources(self):
        """Create searchable index of resources."""
        self.indexed_chunks = []
        
        # Process curriculum
        for subject, content in self.resources["curriculum"].items():
            self._process_resource(content, f"curriculum/{subject}")
        
        # Process standards
        for grade, standards in self.resources["standards"].items():
            self._process_resource(standards, f"standards/{grade}")
        
        # Process best practices
        for category, practices in self.resources["best_practices"].items():
            self._process_resource(practices, f"best_practices/{category}")
        
        # Process lesson plans
        for subject, plans in self.resources["lesson_plans"].items():
            self._process_resource(plans, f"lesson_plans/{subject}")
        
        # Process assessments
        for type_, rubrics in self.resources["assessments"].items():
            self._process_resource(rubrics, f"assessments/{type_}")

    def _process_resource(self, content: Union[Dict, List, str], source: str):
        """Process and chunk a resource for indexing."""
        if isinstance(content, dict):
            for key, value in content.items():
                self._process_resource(value, f"{source}/{key}")
        elif isinstance(content, list):
            for item in content:
                self._process_resource(item, source)
        elif isinstance(content, str):
            # Add the text chunk to indexed content
            self.indexed_chunks.append({
                "text": content,
                "source": source,
                "timestamp": datetime.now().isoformat()
            })

    def get_relevant_context(self,
                          query: str,
                          n_results: int = 3,
                          threshold: float = 0.7) -> List[Dict]:
        """Retrieve relevant educational context for a query.
        
        Args:
            query: Search query
            n_results: Number of results to return
            threshold: Minimum similarity threshold
            
        Returns:
            List of relevant context chunks with metadata
        """
        try:
            # Get text chunks
            texts = [chunk["text"] for chunk in self.indexed_chunks]
            
            # Find similar chunks
            similar = self.embedding_handler.get_similar_texts(
                query=query,
                texts=texts,
                n_results=n_results,
                threshold=threshold
            )
            
            # Add metadata to results
            results = []
            for match in similar:
                # Find the original chunk with metadata
                for chunk in self.indexed_chunks:
                    if chunk["text"] == match["text"]:
                        results.append({
                            **chunk,
                            "similarity": match["similarity"]
                        })
                        break
            
            return results
            
        except Exception as e:
            logger.error(f"Error retrieving context: {str(e)}")
            return []

    def get_resource_by_path(self, path: str) -> Optional[Dict]:
        """Retrieve a specific resource by its path.
        
        Args:
            path: Path to the resource (e.g., "curriculum/math/grade_5")
            
        Returns:
            Resource content if found, None otherwise
        """
        try:
            # Split path into components
            components = path.split("/")
            
            # Navigate through resource dictionary
            current = self.resources
            for component in components:
                if component in current:
                    current = current[component]
                else:
                    return None
            
            return current
            
        except Exception as e:
            logger.error(f"Error retrieving resource: {str(e)}")
            return None 