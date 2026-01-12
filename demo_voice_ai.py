#!/usr/bin/env python3
"""
Quick Demo of Offline Voice AI Assistant
Shows various capabilities with voice responses
"""

from voice_ai_assistant import VoiceAI
import time

def demo():
    """Run comprehensive demo of voice AI"""
    print("=" * 60)
    print("OFFLINE VOICE AI ASSISTANT DEMO")
    print("Arduino UNO Q - Fully Offline Generative AI with Voice")
    print("=" * 60)
    print()
    
    # Demo 1: Normal voice
    print("Demo 1: Normal Voice")
    print("-" * 40)
    assistant = VoiceAI(voice_preset='normal')
    
    demos = [
        ("Hello!", "Basic greeting"),
        ("What time is it?", "Time inquiry"),
        ("Tell me a joke", "Entertainment"),
        ("What is 25 + 17?", "Math calculation"),
    ]
    
    for question, description in demos:
        print(f"\n[{description}]")
        print(f"You: {question}")
        response = assistant.chat(question)
        print(f"AI: {response}")
        time.sleep(1)
    
    print("\n" + "=" * 60)
    
    # Demo 2: Robot voice
    print("\nDemo 2: Robot Voice")
    print("-" * 40)
    robot = VoiceAI(voice_preset='robot')
    
    robot_demos = [
        "I am a robot assistant",
        "Initializing systems",
        "All systems operational",
    ]
    
    for msg in robot_demos:
        print(f"Robot: {msg}")
        robot.chat(msg)
        time.sleep(0.5)
    
    print("\n" + "=" * 60)
    
    # Demo 3: Excited voice
    print("\nDemo 3: Excited Voice")
    print("-" * 40)
    excited = VoiceAI(voice_preset='excited')
    
    print("You: Who are you?")
    response = excited.chat("Who are you?")
    print(f"AI: {response}")
    time.sleep(1)
    
    print("\nYou: Tell me about Arduino")
    response = excited.chat("Tell me about Arduino")
    print(f"AI: {response}")
    
    print("\n" + "=" * 60)
    
    # Demo 4: Conversation with memory
    print("\nDemo 4: Conversation with Memory")
    print("-" * 40)
    memory_ai = VoiceAI(voice_preset='calm')
    
    conversation = [
        "My name is Alice",
        "What can you do?",
        "Thank you",
    ]
    
    for msg in conversation:
        print(f"You: {msg}")
        response = memory_ai.chat(msg)
        print(f"AI: {response}")
        time.sleep(1)
    
    # Show stats
    stats = memory_ai.ai.get_stats()
    print(f"\nConversation stats:")
    print(f"  Messages exchanged: {stats['user_messages']}")
    print(f"  User name remembered: {stats['user_name']}")
    
    print("\n" + "=" * 60)
    print("\nDEMO COMPLETE!")
    print("\nTry it yourself:")
    print("  python3 voice_ai_assistant.py")
    print("\nOr with different voice:")
    print("  python3 voice_ai_assistant.py --preset robot")
    print("  python3 voice_ai_assistant.py --preset excited")
    print("=" * 60)

if __name__ == '__main__':
    demo()
