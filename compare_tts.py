#!/usr/bin/env python3
"""
TTS Engine Comparison Demo
Compare simple, advanced, and espeak TTS quality
"""

import time
import sys

def test_simple_tts():
    """Test simple pure Python TTS"""
    print("\n" + "="*60)
    print("1. SIMPLE TTS (Pure Python, Zero Dependencies)")
    print("="*60)
    print("Quality: Basic")
    print("Speed: Fast")
    print("Size: Smallest (~5KB)")
    print()
    
    try:
        from simple_tts import SimpleTTS
        tts = SimpleTTS()
        print("Speaking with Simple TTS...")
        tts.speak("This is the simple text to speech engine.")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_advanced_tts():
    """Test advanced pure Python TTS"""
    print("\n" + "="*60)
    print("2. ADVANCED TTS (Pure Python with Enhancements)")
    print("="*60)
    print("Quality: Better")
    print("Speed: Moderate")
    print("Features: Voice customization, harmonics")
    print()
    
    try:
        from advanced_tts import AdvancedTTS
        tts = AdvancedTTS(volume=0.6, speed=1.2)
        print("Speaking with Advanced TTS...")
        tts.speak("This is the advanced text to speech engine with customization.")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_espeak_tts():
    """Test espeak-ng TTS"""
    print("\n" + "="*60)
    print("3. ESPEAK-NG TTS (Professional Quality)")
    print("="*60)
    print("Quality: Professional ⭐")
    print("Speed: Fast")
    print("Features: Multiple voices, languages, best pronunciation")
    print()
    
    try:
        from espeak_tts import EspeakTTS
        tts = EspeakTTS(speed=175, pitch=50, volume=100)
        print("Speaking with espeak-ng TTS...")
        tts.speak("This is the espeak text to speech engine with professional quality.")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def demo_voice_presets():
    """Demo espeak voice presets"""
    print("\n" + "="*60)
    print("4. ESPEAK VOICE PRESETS")
    print("="*60)
    
    try:
        from espeak_tts import VoicePresets
        
        presets = [
            ('normal', 'Normal voice'),
            ('robot', 'Robot voice'),
            ('deep', 'Deep voice'),
            ('excited', 'Excited voice'),
            ('whisper', 'Whisper voice'),
        ]
        
        text = "Voice preset demonstration."
        
        for preset_name, description in presets:
            print(f"\n{description}:")
            tts = getattr(VoicePresets, preset_name)()
            tts.speak(text)
            time.sleep(0.5)
        
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def show_recommendations():
    """Show usage recommendations"""
    print("\n" + "="*60)
    print("RECOMMENDATIONS")
    print("="*60)
    print()
    print("✅ For best quality: Use espeak_tts.py")
    print("   - Professional voice quality")
    print("   - Multiple languages and voices")
    print("   - Fast and efficient")
    print()
    print("⚡ For minimal resources: Use simple_tts.py")
    print("   - No dependencies")
    print("   - Smallest footprint")
    print("   - Works anywhere")
    print()
    print("🎨 For customization: Use advanced_tts.py")
    print("   - More voice control")
    print("   - Better than simple")
    print("   - Still pure Python")
    print()
    print("🔧 For Arduino projects: Use espeak with serial bridge")
    print("   - Best quality for announcements")
    print("   - Easy MCU integration")
    print()

def main():
    print("\n" + "="*60)
    print("   Arduino UNO Q - TTS Engine Comparison")
    print("="*60)
    
    if len(sys.argv) > 1 and sys.argv[1] == '--all':
        # Run all tests
        test_simple_tts()
        time.sleep(1)
        test_advanced_tts()
        time.sleep(1)
        test_espeak_tts()
        time.sleep(1)
        demo_voice_presets()
        show_recommendations()
    else:
        print("\nThis demo compares three TTS engines:")
        print("1. Simple TTS (pure Python)")
        print("2. Advanced TTS (pure Python with enhancements)")
        print("3. espeak-ng TTS (professional quality)")
        print()
        print("Options:")
        print("  1 - Test Simple TTS")
        print("  2 - Test Advanced TTS")
        print("  3 - Test espeak-ng TTS")
        print("  4 - Demo espeak voice presets")
        print("  5 - Run all tests")
        print("  0 - Exit")
        print()
        
        while True:
            choice = input("Select option (0-5): ").strip()
            
            if choice == '0':
                break
            elif choice == '1':
                test_simple_tts()
                input("\nPress Enter to continue...")
            elif choice == '2':
                test_advanced_tts()
                input("\nPress Enter to continue...")
            elif choice == '3':
                test_espeak_tts()
                input("\nPress Enter to continue...")
            elif choice == '4':
                demo_voice_presets()
                input("\nPress Enter to continue...")
            elif choice == '5':
                test_simple_tts()
                time.sleep(1)
                test_advanced_tts()
                time.sleep(1)
                test_espeak_tts()
                time.sleep(1)
                demo_voice_presets()
                show_recommendations()
                input("\nPress Enter to continue...")
            else:
                print("Invalid choice")
    
    print("\n✅ Comparison complete!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nComparison interrupted.")
