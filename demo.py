#!/usr/bin/env python3
"""
Arduino UNO Q Voice Generation Demo

Interactive demonstration of offline voice generation capabilities
"""

import os
import time
import subprocess
from espeak_tts import EspeakTTS, VoicePresets
from gtts import gTTS

# Optional Piper integration
PIPER_AVAILABLE = False
try:
    from piper_tts import synthesize as piper_synthesize, play_wav as piper_play
    PIPER_AVAILABLE = True
except Exception:
    PIPER_AVAILABLE = False

# Current TTS engine: 'espeak' or 'piper'
ENGINE = 'espeak'
# Current ESPEAK voice (supports MBROLA voices like 'mb-us1')
ESPEAK_VOICE = 'en'
# Global speed multiplier for all demos (0.5–2.0, 1.0 = normal)
SPEECH_SPEED = 1.0

def clear_screen():
    os.system('clear' if os.name != 'nt' else 'cls')

def _espeak_from_params(pitch=1.0, speed=1.0, volume=0.5, preset=None, voice_override=None):
    if preset:
        # Map preset names to VoicePresets
        presets = {
            'normal': VoicePresets.normal,
            'fast': VoicePresets.fast,
            'slow': VoicePresets.slow,
            'robot': VoicePresets.robot,
            'deep': VoicePresets.deep,
            'high': VoicePresets.high,
            'whisper': VoicePresets.whisper,
            'excited': VoicePresets.excited,
            'calm': VoicePresets.calm,
        }
        fn = presets.get(preset)
        return fn() if fn else EspeakTTS()
    # Convert normalized params to espeak-ng ranges
    es_speed = max(80, min(450, int(175 * speed)))
    es_pitch = max(0, min(99, int(50 * pitch)))
    es_volume = max(0, min(200, int(200 * volume)))
    voice = voice_override if voice_override else ESPEAK_VOICE
    return EspeakTTS(voice=voice, speed=es_speed, pitch=es_pitch, volume=es_volume)

def _engine_speak(text, pitch=1.0, speed=1.0, volume=0.5, preset=None, voice_override=None):
    global ENGINE, SPEECH_SPEED
    # Combine requested speed with global multiplier and clamp
    effective_speed = max(0.5, min(2.0, (speed or 1.0) * (SPEECH_SPEED or 1.0)))
    if ENGINE == 'espeak':
        tts = _espeak_from_params(pitch=pitch, speed=effective_speed, volume=volume, preset=preset, voice_override=voice_override)
        tts.speak(text)
    elif ENGINE == 'piper':
        if not PIPER_AVAILABLE:
            print("Piper not available; falling back to espeak-ng.")
            tts = _espeak_from_params(pitch=pitch, speed=effective_speed, volume=volume, preset=preset)
            tts.speak(text)
            return
        # Map speed to Piper length-scale (<1 faster)
        length_scale = max(0.6, min(1.6, 1.0 / effective_speed))
        # Basic presets mapping (very lightweight)
        noise_scale, noise_w = 0.667, 0.8
        if preset == 'robot':
            noise_scale, noise_w = 0.3, 0.2
        elif preset == 'deep':
            noise_scale, noise_w = 0.6, 0.6
        elif preset == 'excited':
            noise_scale, noise_w = 0.9, 1.0
        tmp = "/tmp/piper_demo.wav"
        piper_synthesize(text, tmp, length_scale=length_scale, noise_scale=noise_scale, noise_w=noise_w)
        piper_play(tmp)


def demo_basic_tts():
    """Demo 1: Basic text-to-speech"""
    print("\n=== Demo 1: Basic Text-to-Speech ===\n")
    
    texts = [
        "Hello, I am Arduino UNO Q.",
        "This is an offline voice generation system.",
        "No internet connection required.",
    ]
    
    for text in texts:
        print(f"Speaking: {text}")
        _engine_speak(text)
        time.sleep(0.5)

def demo_voice_customization():
    """Demo 2: Voice customization"""
    print("\n=== Demo 2: Voice Customization ===\n")
    
    text = "Voice customization test."
    
    # Normal voice
    print("Normal voice:")
    _engine_speak(text, pitch=1.0, speed=1.0, volume=0.5)
    time.sleep(0.5)
    
    # Low pitch (deeper voice)
    print("Low pitch:")
    _engine_speak(text, pitch=0.7, speed=1.0, volume=0.5, preset='deep')
    time.sleep(0.5)
    
    # High pitch
    print("High pitch:")
    _engine_speak(text, pitch=1.5, speed=1.0, volume=0.5)
    time.sleep(0.5)
    
    # Fast speed
    print("Fast speed:")
    _engine_speak(text, pitch=1.0, speed=1.5, volume=0.5)
    time.sleep(0.5)
    
    # Slow speed
    print("Slow speed:")
    _engine_speak(text, pitch=1.0, speed=0.7, volume=0.5)

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
    _engine_speak(text, speed=1.2, volume=0.6)

def demo_interactive():
    """Demo 4: Interactive mode"""
    print("\n=== Demo 4: Interactive Mode ===\n")
    print("Enter text to synthesize (or 'quit' to exit):\n")
    
    
    while True:
        text = input("> ")
        
        if text.lower() in ['quit', 'exit', 'q']:
            break
        
        if text.strip():
            _engine_speak(text, volume=0.6)

def demo_special_voices():
    """Demo 5: Special voice effects"""
    print("\n=== Demo 5: Special Voice Effects ===\n")
    
    text = "This is a special voice effect"
    
    # Robot voice (preset)
    print("Robot voice:")
    _engine_speak(text, preset='robot')
    time.sleep(0.5)
    
    # Deep voice (preset)
    print("Deep voice:")
    _engine_speak(text, preset='deep')
    time.sleep(0.5)
    
    # Chipmunk-like (high pitch, fast)
    print("Chipmunk voice:")
    _engine_speak(text, pitch=1.8, speed=1.4, volume=0.5)

def show_menu():
    """Display demo menu"""
    clear_screen()
    print("=" * 60)
    print("   Arduino UNO Q - Offline Voice Generation Demo")
    print("=" * 60)
    if ENGINE == 'espeak':
        print(f"Engine: ESPEAK (voice={ESPEAK_VOICE}, speed={SPEECH_SPEED:.2f}x)  | Toggle engine: option 7")
    else:
        print(f"Engine: PIPER (speed={SPEECH_SPEED:.2f}x)  | Toggle engine: option 7")
    print("\nAvailable Demos:\n")
    print("  1. Basic Text-to-Speech")
    print("  2. Voice Customization")
    print("  3. Long Text Synthesis")
    print("  4. Interactive Mode")
    print("  5. Special Voice Effects")
    print("  6. Run All Demos")
    print("  7. Switch Engine (espeak/piper)")
    print("  8. Select ESPEAK Voice (en/mb-us1/mb-us2/mb-us3)")
    print("  9. Set Global Speed (0.5–2.0, default 1.0)")
    print(" 10. Thai Quick Test (สวัสดี)")
    print(" 11. gTTS Thai Demo (Google TTS)")
    print("  0. Exit")
    print("\n" + "=" * 60)

def list_mbrola_voices():
    try:
        out = subprocess.check_output(['espeak-ng', '--voices=mb'], text=True)
        print(out)
    except Exception:
        print("Could not list MBROLA voices. Make sure mbrola voices are installed.")


def select_espeak_voice():
    global ESPEAK_VOICE
    print("\nSelect ESPEAK voice (examples: en, mb-us1, mb-us2, mb-us3).\n")
    try:
        list_mbrola_voices()
    except Exception:
        pass
    choice = input("Enter voice code (or press Enter to keep current): ").strip()
    if choice:
        ESPEAK_VOICE = choice
        print(f"Selected ESPEAK voice: {ESPEAK_VOICE}")
        time.sleep(1)


def select_speed():
    global SPEECH_SPEED
    print("\nSet global speed multiplier (0.5–2.0). 1.0 = normal, <1.0 faster for Piper, >1.0 slower.")
    val = input("Enter speed (e.g., 0.9, 1.0, 1.2): ").strip()
    try:
        sp = float(val)
        sp = max(0.5, min(2.0, sp))
        SPEECH_SPEED = sp
        print(f"Global speed set to {SPEECH_SPEED:.2f}x")
        time.sleep(1)
    except ValueError:
        print("Invalid number; keeping previous speed.")
        time.sleep(1)


def demo_gtts_thai():
    """Demo gTTS Thai language support"""
    print("\n=== gTTS Thai Language Demo ===\n")
    
    thai_text = "สวัสดีครับ นี่คือการทดสอบเสียงภาษาไทยด้วย Google Text to Speech"
    output_file = "/tmp/gtts_thai.mp3"
    
    try:
        print(f"Generating Thai speech: {thai_text}")
        tts = gTTS(text=thai_text, lang='th')
        tts.save(output_file)
        print(f"Saved to {output_file}")
        
        # Play the audio file
        print("Playing audio...")
        subprocess.run(['mpg123', '-q', output_file])
        print("Playback complete.")
    except Exception as e:
        print(f"Error: {e}")
        print("Note: Make sure mpg123 is installed for playback (sudo apt install mpg123)")


def main():
    """Main demo program"""
    global ENGINE, ESPEAK_VOICE, SPEECH_SPEED
    demos = {
        '1': demo_basic_tts,
        '2': demo_voice_customization,
        '3': demo_long_text,
        '4': demo_interactive,
        '5': demo_special_voices,
    }
    
    while True:
        show_menu()
        choice = input("\nSelect demo (0-11): ").strip()
        
        if choice == '0':
            print("\nGoodbye!")
            break
        elif choice == '6':
            # Run all demos
            for key in sorted(demos.keys()):
                demos[key]()
                time.sleep(1)
            
            input("\nPress Enter to continue...")
        elif choice == '7':
            if ENGINE == 'espeak':
                if not PIPER_AVAILABLE:
                    print("Piper not available. Run piper_tts.py once to initialize.")
                    time.sleep(1)
                else:
                    ENGINE = 'piper'
            else:
                ENGINE = 'espeak'
        elif choice == '8':
            if ENGINE != 'espeak':
                print("Switch to ESPEAK (option 7) to change ESPEAK voice.")
                time.sleep(1)
            else:
                select_espeak_voice()
        elif choice == '9':
            select_speed()
        elif choice == '10':
            thai_text = "สวัสดีครับ นี่คือการทดสอบเสียงภาษาไทยแบบออฟไลน์"
            if ENGINE == 'espeak':
                _engine_speak(thai_text, voice_override='th')
            else:
                print("Piper Thai voice not installed yet. I can set it up if you want.")
                time.sleep(2)
        elif choice == '11':
            demo_gtts_thai()
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
