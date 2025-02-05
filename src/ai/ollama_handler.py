"""
Handler for Ollama LLM models with advanced functionality and error handling.

This module provides a robust interface to interact with Ollama models,
implementing consistent API methods and proper error handling.
"""

from typing import Dict, List, Optional, Union
import json
import requests
import logging
from tenacity import retry, stop_after_attempt, wait_exponential

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OllamaHandler:
    def __init__(
        self,
        model_name: str = "mistral",
        base_url: str = "http://localhost:11434",
        temperature: float = 0.7,
        top_p: float = 0.9,
        max_tokens: int = 2048,
    ):
        """Initialize Ollama model handler.
        
        Args:
            model_name: Name of the Ollama model to use
            base_url: Base URL for Ollama API
            temperature: Sampling temperature (0.0 to 1.0)
            top_p: Top-p sampling parameter
            max_tokens: Maximum tokens to generate
        """
        self.model_name = model_name
        self.base_url = base_url.rstrip("/")
        self.temperature = temperature
        self.top_p = top_p
        self.max_tokens = max_tokens
        
        # Verify connection and model availability
        self._verify_connection()

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        reraise=True
    )
    def _verify_connection(self) -> None:
        """Verify connection to Ollama server and model availability."""
        try:
            response = requests.get(f"{self.base_url}/api/tags")
            response.raise_for_status()
            
            models = response.json().get("models", [])
            if not any(model["name"] == self.model_name for model in models):
                logger.warning(f"Model {self.model_name} not found. Available models: {[m['name'] for m in models]}")
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to connect to Ollama server: {str(e)}")
            raise

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        reraise=True
    )
    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        stream: bool = False
    ) -> Union[str, Dict]:
        """Generate text using the Ollama model.
        
        Args:
            prompt: Input text prompt
            system_prompt: Optional system prompt for context
            temperature: Optional override for temperature
            max_tokens: Optional override for max_tokens
            stream: Whether to stream the response
            
        Returns:
            Generated text response or streaming response object
        """
        url = f"{self.base_url}/api/generate"
        
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "system": system_prompt if system_prompt else "",
            "temperature": temperature if temperature is not None else self.temperature,
            "max_tokens": max_tokens if max_tokens is not None else self.max_tokens,
            "stream": stream
        }
        
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            
            if stream:
                return response
            
            return response.json().get("response", "")
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to generate response: {str(e)}")
            raise

    def chat(
        self,
        messages: List[Dict[str, str]],
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        stream: bool = False
    ) -> Union[str, Dict]:
        """Chat with the Ollama model using a message list format.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            system_prompt: Optional system prompt for context
            temperature: Optional override for temperature
            max_tokens: Optional override for max_tokens
            stream: Whether to stream the response
            
        Returns:
            Generated response or streaming response object
        """
        formatted_prompt = "\n".join([
            f"{msg['role']}: {msg['content']}"
            for msg in messages
        ])
        
        return self.generate(
            prompt=formatted_prompt,
            system_prompt=system_prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=stream
        )

    def embed(self, text: str) -> List[float]:
        """Get embeddings for the input text.
        
        Args:
            text: Input text to embed
            
        Returns:
            List of embedding values
        """
        url = f"{self.base_url}/api/embeddings"
        
        try:
            response = requests.post(url, json={
                "model": self.model_name,
                "prompt": text
            })
            response.raise_for_status()
            
            return response.json().get("embedding", [])
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to generate embeddings: {str(e)}")
            raise 