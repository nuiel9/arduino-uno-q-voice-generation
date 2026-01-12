#!/usr/bin/env python3
"""
Offline AI Brain - Lightweight conversational AI for Arduino UNO Q
Uses pattern matching, templates, and basic NLP without heavy models
Optimized for 2GB RAM systems
"""

import re
import random
import json
from datetime import datetime
from typing import Dict, List, Tuple, Optional

class OfflineAI:
    """Lightweight offline AI with conversation capabilities"""
    
    def __init__(self):
        self.context = {}
        self.conversation_history = []
        self.user_name = None
        self.load_knowledge()
        
    def load_knowledge(self):
        """Load built-in knowledge base"""
        self.patterns = {
            # Greetings
            r'\b(hi|hello|hey|greetings)\b': [
                "Hello! How can I help you today?",
                "Hi there! What would you like to know?",
                "Greetings! I'm here to assist you.",
            ],
            
            # Introduction
            r'\b(who are you|what are you|your name)\b': [
                "I'm an offline AI assistant running on Arduino UNO Q. I can answer questions and have conversations without internet.",
                "I'm a lightweight AI designed for Arduino UNO Q. I work completely offline using efficient algorithms.",
            ],
            
            # Time/Date
            r'\b(time|what time|clock)\b': [
                self._get_time_response,
            ],
            r'\b(date|today|what day)\b': [
                self._get_date_response,
            ],
            
            # System info
            r'\b(system|hardware|specs|arduino)\b': [
                "This Arduino UNO Q has a Qualcomm QRB2210 processor with 2GB RAM, running Debian Linux. It's quite powerful for an Arduino!",
                "I'm running on Arduino UNO Q - a hybrid board with both MPU and MCU. The Linux side has 2GB RAM and runs Python.",
            ],
            
            # Help
            r'\b(help|what can you do|capabilities)\b': [
                "I can chat with you, answer questions, tell jokes, do math, and provide information about various topics. Try asking me something!",
                "I can help with conversations, basic questions, calculations, jokes, and general knowledge. What interests you?",
            ],
            
            # Math operations
            r'(\d+)\s*([\+\-\*/])\s*(\d+)': [
                self._calculate,
            ],
            r'(\d+)\s+(?:times|multiplied by)\s+(\d+)': [
                self._calculate_times,
            ],
            r'(\d+)\s+(?:plus|added to)\s+(\d+)': [
                self._calculate_plus,
            ],
            r'(\d+)\s+(?:minus|subtract)\s+(\d+)': [
                self._calculate_minus,
            ],
            r'(\d+)\s+(?:divided by)\s+(\d+)': [
                self._calculate_divide,
            ],
            
            # Jokes
            r'\b(joke|funny|laugh|humor)\b': [
                "Why did the Arduino cross the road? To get to the other IDE!",
                "What's an AI's favorite snack? Microchips!",
                "Why do programmers prefer dark mode? Because light attracts bugs!",
                "How many programmers does it take to change a light bulb? None, that's a hardware problem!",
            ],
            
            # Weather (local/simulated)
            r'\b(weather|temperature|forecast)\b': [
                "I don't have internet access, so I can't check live weather. But I hope it's nice where you are!",
                "As an offline AI, I can't fetch weather data. Try checking your local weather station!",
            ],
            
            # Feelings/Emotions
            r'\b(how are you|how do you feel)\b': [
                "I'm running smoothly! All my processes are working well. How are you?",
                "I'm doing great! My circuits are happy and my code is bug-free. How about you?",
            ],
            
            # Thank you
            r'\b(thank you|thanks|thx)\b': [
                "You're welcome!",
                "Happy to help!",
                "Anytime! That's what I'm here for.",
            ],
            
            # Goodbye
            r'\b(bye|goodbye|exit|quit)\b': [
                "Goodbye! It was nice talking with you.",
                "See you later! Feel free to come back anytime.",
                "Bye! Take care!",
            ],
            
            # Name learning
            r'my name is (\w+)': [
                self._learn_name,
            ],
            r'i am (\w+)': [
                self._learn_name,
            ],
            
            # Arduino/Robotics
            r'\b(robot|robotics|maker|diy)\b': [
                "Arduino is perfect for robotics! With the UNO Q, you can build intelligent robots with voice capabilities.",
                "I love robotics! The Arduino UNO Q combines MCU and MPU, making it ideal for advanced robotic projects.",
            ],
            
            # Programming
            r'\b(programming|code|python|c\+\+)\b': [
                "I'm written in Python! The Arduino UNO Q supports both Python on the Linux side and C++ on the MCU.",
                "Programming is fun! You can use Python for AI tasks and C++ for real-time control on the MCU.",
            ],
            
            # Voice/TTS
            r'\b(voice|speak|tts|text to speech)\b': [
                "I use espeak-ng for voice synthesis! It's a professional offline TTS engine that sounds great.",
                "My voice is generated using espeak-ng. It's completely offline and supports multiple languages!",
            ],
        }
        
        # Fallback responses for unknown inputs
        self.fallbacks = [
            "I'm not sure I understand. Could you rephrase that?",
            "Interesting question! I'm still learning, so I might not have the best answer.",
            "I don't have specific information about that, but I'm here to chat!",
            "That's a bit outside my knowledge base. Try asking something else?",
            "Hmm, I'm not quite sure about that. What else would you like to know?",
        ]
        
        # Topic-based knowledge
        self.knowledge = {
            'arduino': "Arduino is an open-source electronics platform. The UNO Q is special because it combines traditional Arduino with a powerful Linux processor.",
            'python': "Python is a versatile programming language. I'm written in Python and run on the Linux side of Arduino UNO Q.",
            'ai': "Artificial Intelligence involves creating systems that can perform tasks requiring human intelligence. I'm a lightweight offline AI!",
            'linux': "Linux is a free open-source operating system. The Arduino UNO Q runs Debian Linux on its MPU.",
        }
    
    def _get_time_response(self, match=None) -> str:
        """Generate time response"""
        now = datetime.now()
        return f"The current time is {now.strftime('%I:%M %p')}."
    
    def _get_date_response(self, match=None) -> str:
        """Generate date response"""
        now = datetime.now()
        return f"Today is {now.strftime('%A, %B %d, %Y')}."
    
    def _calculate(self, match) -> str:
        """Perform basic calculation"""
        try:
            num1 = float(match.group(1))
            operator = match.group(2)
            num2 = float(match.group(3))
            
            if operator == '+':
                result = num1 + num2
            elif operator == '-':
                result = num1 - num2
            elif operator == '*':
                result = num1 * num2
            elif operator == '/':
                if num2 == 0:
                    return "I can't divide by zero! That would break the universe."
                result = num1 / num2
            else:
                return "I don't recognize that operation."
            
            return f"The answer is {result}."
        except:
            return "I had trouble with that calculation."
    
    def _calculate_times(self, match) -> str:
        """Calculate multiplication with 'times' keyword"""
        num1 = float(match.group(1))
        num2 = float(match.group(2))
        result = num1 * num2
        return f"{num1} times {num2} equals {result}."
    
    def _calculate_plus(self, match) -> str:
        """Calculate addition with 'plus' keyword"""
        num1 = float(match.group(1))
        num2 = float(match.group(2))
        result = num1 + num2
        return f"{num1} plus {num2} equals {result}."
    
    def _calculate_minus(self, match) -> str:
        """Calculate subtraction with 'minus' keyword"""
        num1 = float(match.group(1))
        num2 = float(match.group(2))
        result = num1 - num2
        return f"{num1} minus {num2} equals {result}."
    
    def _calculate_divide(self, match) -> str:
        """Calculate division with 'divided by' keyword"""
        num1 = float(match.group(1))
        num2 = float(match.group(2))
        if num2 == 0:
            return "I can't divide by zero! That would break the universe."
        result = num1 / num2
        return f"{num1} divided by {num2} equals {result}."
    
    def _learn_name(self, match) -> str:
        """Learn and remember user's name"""
        self.user_name = match.group(1).capitalize()
        return f"Nice to meet you, {self.user_name}! I'll remember your name."
    
    def process(self, user_input: str) -> str:
        """Process user input and generate response"""
        if not user_input or not user_input.strip():
            return "I didn't catch that. Could you say something?"
        
        # Normalize input
        user_input = user_input.strip().lower()
        
        # Store in conversation history
        self.conversation_history.append({
            'role': 'user',
            'message': user_input,
            'timestamp': datetime.now().isoformat()
        })
        
        # Check for patterns
        for pattern, responses in self.patterns.items():
            match = re.search(pattern, user_input, re.IGNORECASE)
            if match:
                response_template = random.choice(responses)
                
                # If response is a function, call it
                if callable(response_template):
                    response = response_template(match)
                else:
                    response = response_template
                
                # Personalize with name if available
                if self.user_name and random.random() > 0.7:
                    response = f"{self.user_name}, {response.lower()}"
                
                self.conversation_history.append({
                    'role': 'assistant',
                    'message': response,
                    'timestamp': datetime.now().isoformat()
                })
                
                return response
        
        # Check knowledge base for topic keywords
        for topic, info in self.knowledge.items():
            if topic in user_input:
                response = info
                self.conversation_history.append({
                    'role': 'assistant',
                    'message': response,
                    'timestamp': datetime.now().isoformat()
                })
                return response
        
        # Use fallback response
        response = random.choice(self.fallbacks)
        
        # Add context awareness
        if len(self.conversation_history) > 2:
            if 'yes' in user_input or 'yeah' in user_input:
                response = "Great! What else can I help you with?"
            elif 'no' in user_input or 'nope' in user_input:
                response = "Okay, no problem. What would you like to talk about?"
        
        self.conversation_history.append({
            'role': 'assistant',
            'message': response,
            'timestamp': datetime.now().isoformat()
        })
        
        return response
    
    def get_conversation_history(self, last_n: Optional[int] = None) -> List[Dict]:
        """Get conversation history"""
        if last_n:
            return self.conversation_history[-last_n:]
        return self.conversation_history
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        self.context = {}
    
    def save_conversation(self, filename: str):
        """Save conversation to file"""
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
        }


def main():
    """Demo the offline AI"""
    print("=== Offline AI Brain Demo ===")
    print("Lightweight conversational AI for Arduino UNO Q")
    print("Type 'quit' to exit\n")
    
    ai = OfflineAI()
    
    while True:
        try:
            user_input = input("You: ").strip()
            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                response = ai.process(user_input)
                print(f"AI: {response}")
                break
            
            response = ai.process(user_input)
            print(f"AI: {response}\n")
            
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")
    
    # Show stats
    stats = ai.get_stats()
    print(f"\n--- Conversation Stats ---")
    print(f"Total exchanges: {stats['user_messages']}")
    print(f"Messages: {stats['total_messages']}")


if __name__ == '__main__':
    main()
