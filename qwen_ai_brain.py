#!/usr/bin/env python3
"""
Qwen AI Brain - Real offline LLM using Qwen2-0.5B via Ollama
Provides true generative AI responses for Arduino UNO Q
"""

import subprocess
import json
from datetime import datetime
from typing import Dict, List, Optional
import sys


class QwenAI:
    """Qwen2-based conversational AI using Ollama"""
    
    def __init__(self, model="qwen2:0.5b", temperature=0.7, max_tokens=150):
        """Initialize Qwen AI
        
        Args:
            model: Ollama model name (default: qwen2:0.5b)
                   Supported: qwen2:0.5b, smollm:360m, smollm:135m, smollm:1.7b
            temperature: Response randomness 0.0-1.0 (default: 0.7)
            max_tokens: Maximum response length (default: 150)
        """
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.conversation_history = []
        self.user_name = None
        
        # System prompt to give Qwen context
        self.system_prompt = """You are a helpful AI assistant running on Arduino UNO Q. 
You are offline and running locally using the Qwen2-0.5B model.
Keep responses concise and friendly. Answer questions directly and helpfully.
You can discuss Arduino, programming, robotics, and general knowledge topics."""
        
        # Check if Ollama is available
        self._check_ollama()
    
    def _check_ollama(self):
        """Check if Ollama server is running"""
        try:
            result = subprocess.run(
                ['ollama', 'list'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if self.model.split(':')[0] not in result.stdout:
                print(f"Warning: Model {self.model} not found. Run: ollama pull {self.model}")
        except FileNotFoundError:
            print("Error: Ollama not found. Install it first.")
            sys.exit(1)
        except subprocess.TimeoutExpired:
            print("Warning: Ollama server may not be running. Run: ollama serve")
        except Exception as e:
            print(f"Warning: Could not verify Ollama: {e}")
    
    def process(self, user_input: str, use_history=True) -> str:
        """Process user input and generate AI response
        
        Args:
            user_input: User's message
            use_history: Whether to include conversation history
            
        Returns:
            AI's response text
        """
        if not user_input or not user_input.strip():
            return "I didn't catch that. Could you say something?"
        
        # Store in history
        self.conversation_history.append({
            'role': 'user',
            'message': user_input,
            'timestamp': datetime.now().isoformat()
        })
        
        # Build prompt with context
        if use_history and len(self.conversation_history) > 1:
            # Include last few exchanges for context
            context_messages = self.conversation_history[-6:]  # Last 3 exchanges
            prompt = self.system_prompt + "\n\n"
            for msg in context_messages[:-1]:  # Exclude the current message
                if msg['role'] == 'user':
                    prompt += f"User: {msg['message']}\n"
                else:
                    prompt += f"Assistant: {msg['message']}\n"
            prompt += f"User: {user_input}\nAssistant:"
        else:
            prompt = f"{self.system_prompt}\n\nUser: {user_input}\nAssistant:"
        
        # Call Ollama
        try:
            response = self._call_ollama(prompt)
            
            # Store response
            self.conversation_history.append({
                'role': 'assistant',
                'message': response,
                'timestamp': datetime.now().isoformat()
            })
            
            return response
            
        except Exception as e:
            error_msg = f"Sorry, I encountered an error: {str(e)[:50]}"
            self.conversation_history.append({
                'role': 'assistant',
                'message': error_msg,
                'timestamp': datetime.now().isoformat()
            })
            return error_msg
    
    def _call_ollama(self, prompt: str) -> str:
        """Call Ollama API to generate response"""
        try:
            # Prepare API request
            api_data = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": self.temperature,
                    "num_predict": self.max_tokens,
                }
            }
            
            # Call Ollama HTTP API
            result = subprocess.run(
                ['curl', '-s', 'http://localhost:11434/api/generate',
                 '-d', json.dumps(api_data)],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                response_data = json.loads(result.stdout)
                response_text = response_data.get('response', '').strip()
                
                # Clean up the response
                response_text = self._clean_response(response_text)
                
                return response_text if response_text else "I'm not sure how to respond to that."
            else:
                return "Sorry, I couldn't generate a response."
                
        except subprocess.TimeoutExpired:
            return "Sorry, the response took too long. Try a simpler question."
        except json.JSONDecodeError:
            return "Sorry, I got confused. Could you rephrase that?"
        except Exception as e:
            return f"Error: {str(e)[:50]}"
    
    def _clean_response(self, text: str) -> str:
        """Clean up AI response"""
        # Remove common artifacts
        text = text.strip()
        
        # Remove "Assistant:" prefix if present
        if text.lower().startswith('assistant:'):
            text = text[10:].strip()
        
        # Take only the first paragraph for conciseness
        paragraphs = text.split('\n\n')
        if paragraphs:
            text = paragraphs[0]
        
        # Limit length
        if len(text) > 300:
            # Try to cut at sentence boundary
            sentences = text[:300].split('. ')
            if len(sentences) > 1:
                text = '. '.join(sentences[:-1]) + '.'
            else:
                text = text[:297] + '...'
        
        return text
    
    def get_conversation_history(self, last_n: Optional[int] = None) -> List[Dict]:
        """Get conversation history"""
        if last_n:
            return self.conversation_history[-last_n:]
        return self.conversation_history
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
    
    def save_conversation(self, filename: str):
        """Save conversation to JSON file"""
        with open(filename, 'w') as f:
            json.dump(self.conversation_history, f, indent=2)
    
    def get_stats(self) -> Dict:
        """Get conversation statistics"""
        total_messages = len(self.conversation_history)
        user_messages = sum(1 for m in self.conversation_history if m['role'] == 'user')
        assistant_messages = total_messages - user_messages
        
        return {
            'total_messages': total_messages,
            'user_messages': user_messages,
            'assistant_messages': assistant_messages,
            'user_name': self.user_name,
            'model': self.model,
        }


def main():
    """Demo the Qwen AI"""
    print("=== Qwen AI Brain Demo ===")
    print(f"Using Qwen2-0.5B via Ollama")
    print("Type 'quit' to exit\n")
    
    ai = QwenAI()
    
    while True:
        try:
            user_input = input("You: ").strip()
            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("AI: Goodbye! It was nice chatting with you.")
                break
            
            print("AI: ", end='', flush=True)
            response = ai.process(user_input)
            print(response + "\n")
            
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")
    
    # Show stats
    stats = ai.get_stats()
    print(f"\n--- Conversation Stats ---")
    print(f"Total exchanges: {stats['user_messages']}")
    print(f"Model: {stats['model']}")


if __name__ == '__main__':
    main()
