#!/usr/bin/env python3
"""
Arduino UNO Q Voice Generation Demo

Interactive demonstration of offline voice generation capabilities
"""

import os
import time
from advanced_tts import AdvancedTTS

def clear_screen():
    os.system('clear' if os.name != 'nt' else 'cls')

def demo_basic_tts():
    """Demo 1: Basic text-to-speech"""
    print("\n=== Demo 1: Basic Text-to-Speech ===\n")
    tts = AdvancedTTS()
    
    texts = [
        "Hello, I am Arduino UNO Q.",
        "This is an offline voice generation system.",
        "No internet connection required.",
    ]
    
    for text in texts:
        print(f"Speaking: {text}")
        tts.speak(text)
        time.sleep(0.5)

def demo_voice_customization():
    """Demo 2: Voice customization"""
    print("\n=== Demo 2: Voice Customization ===\n")
    
    text = "Voice customization test."
    
    # Normal voice
    print("Normal voice:")
    tts = AdvancedTTS(pitch=1.0, speed=1.0, volume=0.5)
    tts.speak(text)
    time.sleep(0.5)
    
    # Low pitch (deeper voice)
    print("Low pitch:")
    tts = AdvancedTTS(pitch=0.7, speed=1.0, volume=0.5)
    tts.speak(text)
    time.sleep(0.5)
    
    # High pitch
    print("High pitch:")
    tts = AdvancedTTS(pitch=1.5, speed=1.0, volume=0.5)
    tts.speak(text)
    time.sleep(0.5)
    
    # Fast speed
    print("Fast speed:")
    tts = AdvancedTTS(pitch=1.0, speed=1.5, volume=0.5)
    tts.speak(text)
    time.sleep(0.5)
    
    # Slow speed
    print("Slow speed:")
    tts = AdvancedTTS(pitch=1.0, speed=0.7, volume=0.5)
    tts.speak(text)

def demo_long_text():
    """Demo 3: Long text synthesis"""
    print("\n=== Demo 3: Long Text Synthesis ===\n")
    
    text = """
    The Arduino UNO Q is a powerful single board computer.
    It features a quad core processor and a real time microcontroller.
    This makes it perfect for edge AI applications.
    Voice generation works completely offline.
    """
    
    print(f"Speaking long text:\n{text}")
    tts = AdvancedTTS(speed=1.2, volume=0.6)
    tts.speak(text)

def demo_interactive():
    """Demo 4: Interactive mode"""
    print("\n=== Demo 4: Interactive Mode ===\n")
    print("Enter text to synthesize (or 'quit' to exit):\n")
    
    tts = AdvancedTTS(volume=0.6)
    
    while True:
        text = input("> ")
        
        if text.lower() in ['quit', 'exit', 'q']:
            break
        
        if text.strip():
            tts.speak(text)

def demo_special_voices():
    """Demo 5: Special voice effects"""
    print("\n=== Demo 5: Special Voice Effects ===\n")
    
    text = "This is a special voice effect"
    
    # Robot voice (high pitch, slow speed)
    print("Robot voice:")
    tts = AdvancedTTS(pitch=1.3, speed=0.8, volume=0.4)
    tts.speak(text)
    time.sleep(0.5)
    
    # Deep voice (low pitch, slow)
    print("Deep voice:")
    tts = AdvancedTTS(pitch=0.6, speed=0.9, volume=0.6)
    tts.speak(text)
    time.sleep(0.5)
    
    # Chipmunk voice (very high pitch, fast)
    print("Chipmunk voice:")
    tts = AdvancedTTS(pitch=1.8, speed=1.4, volume=0.5)
    tts.speak(text)

def show_menu():
    """Display demo menu"""
    clear_screen()
    print("=" * 60)
    print("   Arduino UNO Q - Offline Voice Generation Demo")
    print("=" * 60)
    print("\nAvailable Demos:\n")
    print("  1. Basic Text-to-Speech")
    print("  2. Voice Customization")
    print("  3. Long Text Synthesis")
    print("  4. Interactive Mode")
    print("  5. Special Voice Effects")
    print("  6. Run All Demos")
    print("  0. Exit")
    print("\n" + "=" * 60)

def main():
    """Main demo program"""
    demos = {
        '1': demo_basic_tts,
        '2': demo_voice_customization,
        '3': demo_long_text,
        '4': demo_interactive,
        '5': demo_special_voices,
    }
    
    while True:
        show_menu()
        choice = input("\nSelect demo (0-6): ").strip()
        
        if choice == '0':
            print("\nGoodbye!")
            break
        elif choice == '6':
            # Run all demos
            for key in sorted(demos.keys()):
                demos[key]()
                time.sleep(1)
            
            input("\nPress Enter to continue...")
        elif choice in demos:
            demos[choice]()
            input("\nPress Enter to continue...")
        else:
            print("Invalid choice. Please try again.")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nDemo interrupted. Goodbye!")
    except Exception as e:
        print(f"\nError: {e}")
