#!/usr/bin/env python3
"""
Thai Language Test - Offline TTS using espeak-ng

Demonstrates offline Thai text-to-speech without internet connection.
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from espeak_tts import EspeakTTS

def test_thai_basic():
    """Test basic Thai phrases"""
    print("=== Thai Language Test (Offline) ===\n")
    
    # Create Thai TTS engine
    tts = EspeakTTS(voice='th', speed=150, pitch=50, volume=100)
    
    # Test phrases
    phrases = [
        ("สวัสดีครับ", "Hello (male)"),
        ("สวัสดีค่ะ", "Hello (female)"),
        ("ขอบคุณครับ", "Thank you (male)"),
        ("ขอบคุณค่ะ", "Thank you (female)"),
        ("ยินดีต้อนรับ", "Welcome"),
        ("ลาก่อน", "Goodbye"),
        ("นี่คือการทดสอบเสียงภาษาไทยแบบออฟไลน์", "This is an offline Thai voice test"),
    ]
    
    for thai_text, translation in phrases:
        print(f"Speaking: {thai_text}")
        print(f"  Translation: {translation}")
        tts.speak(thai_text)
        print()

def test_thai_numbers():
    """Test Thai numbers"""
    print("\n=== Thai Numbers Test ===\n")
    
    tts = EspeakTTS(voice='th', speed=150, pitch=50, volume=100)
    
    numbers = [
        ("หนึ่ง", "One (1)"),
        ("สอง", "Two (2)"),
        ("สาม", "Three (3)"),
        ("สี่", "Four (4)"),
        ("ห้า", "Five (5)"),
        ("หก", "Six (6)"),
        ("เจ็ด", "Seven (7)"),
        ("แปด", "Eight (8)"),
        ("เก้า", "Nine (9)"),
        ("สิบ", "Ten (10)"),
    ]
    
    for thai_num, translation in numbers:
        print(f"{thai_num} = {translation}")
        tts.speak(thai_num)

def test_thai_custom():
    """Interactive Thai TTS test"""
    print("\n=== Interactive Thai Test ===\n")
    print("Enter Thai text to synthesize (or 'quit' to exit):\n")
    
    tts = EspeakTTS(voice='th', speed=150, pitch=50, volume=100)
    
    while True:
        text = input("Thai text > ")
        
        if text.lower() in ['quit', 'exit', 'q']:
            break
        
        if text.strip():
            tts.speak(text)

def main():
    """Main test program"""
    print("\nOffline Thai TTS Test")
    print("=" * 50)
    print("Engine: espeak-ng (offline)")
    print("Language: Thai (th)")
    print("Internet: NOT required")
    print("=" * 50)
    
    while True:
        print("\nSelect test:")
        print("  1. Basic Thai phrases")
        print("  2. Thai numbers (1-10)")
        print("  3. Interactive mode (type your own)")
        print("  0. Exit")
        
        choice = input("\nChoice: ").strip()
        
        if choice == '0':
            print("\nGoodbye!")
            break
        elif choice == '1':
            test_thai_basic()
            input("\nPress Enter to continue...")
        elif choice == '2':
            test_thai_numbers()
            input("\nPress Enter to continue...")
        elif choice == '3':
            test_thai_custom()
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nTest interrupted. Goodbye!")
    except Exception as e:
        print(f"\nError: {e}")
