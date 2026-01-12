#!/usr/bin/env python3
"""
Interactive Menu for Voice AI Assistant
Allows easy selection of AI models and TTS engines
"""

import subprocess
import sys
import os

def clear_screen():
    """Clear terminal screen"""
    os.system('clear' if os.name != 'nt' else 'cls')

def print_header():
    """Print menu header"""
    clear_screen()
    print("=" * 60)
    print("     VOICE AI ASSISTANT - Configuration Menu")
    print("=" * 60)
    print()

def check_ollama_status():
    """Check if Ollama server is running"""
    try:
        result = subprocess.run(
            ['curl', '-s', 'http://localhost:11434/api/tags'],
            capture_output=True,
            timeout=2
        )
        return result.returncode == 0
    except:
        return False

def get_available_models():
    """Get list of installed Ollama models"""
    try:
        result = subprocess.run(
            ['/usr/local/bin/ollama', 'list'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')[1:]  # Skip header
            models = []
            for line in lines:
                if line.strip():
                    model_name = line.split()[0]
                    models.append(model_name)
            return models
    except:
        pass
    return []

def select_ai_model():
    """Select AI model"""
    print_header()
    print("📱 SELECT AI MODEL:")
    print()
    print("  1. Pattern-based AI (fast, 20MB RAM)")
    print("  2. Qwen2 0.5B (generative, 478MB RAM) ⭐")
    print("  3. SmolLM 360M (generative, 300MB RAM)")
    print("  4. SmolLM 1.7B (generative, 1.2GB RAM)")
    print()
    print("  0. Back")
    print()
    
    choice = input("Choose AI model (1-4, 0=back): ").strip()
    
    model_map = {
        '1': ('pattern', 'Pattern-based AI'),
        '2': ('qwen2:0.5b', 'Qwen2 0.5B'),
        '3': ('smollm:360m', 'SmolLM 360M'),
        '4': ('smollm:1.7b', 'SmolLM 1.7B'),
    }
    
    if choice in model_map:
        model_id, model_name = model_map[choice]
        
        # Check if model is installed (for Ollama models)
        if model_id != 'pattern':
            available_models = get_available_models()
            if model_id not in available_models:
                print(f"\n⚠️  Model '{model_id}' is not installed.")
                print(f"   Install with: /usr/local/bin/ollama pull {model_id}")
                input("\nPress Enter to continue...")
                return None
        
        return (model_id, model_name)
    
    return None

def select_tts_engine():
    """Select TTS engine"""
    print_header()
    print("🔊 SELECT VOICE ENGINE:")
    print()
    print("  1. espeak-ng (fast, lightweight) ⭐")
    print("  2. Piper Neural TTS (high quality)")
    print("  3. Advanced Python TTS (offline, no deps)")
    print("  4. Simple Python TTS (basic)")
    print()
    print("  0. Back")
    print()
    
    choice = input("Choose TTS engine (1-4, 0=back): ").strip()
    
    tts_map = {
        '1': ('espeak', 'espeak-ng'),
        '2': ('piper', 'Piper Neural TTS'),
        '3': ('advanced', 'Advanced Python TTS'),
        '4': ('simple', 'Simple Python TTS'),
    }
    
    if choice in tts_map:
        return tts_map[choice]
    
    return None

def select_voice_preset():
    """Select voice preset (for espeak)"""
    print_header()
    print("🎭 SELECT VOICE PRESET:")
    print()
    print("  1. Normal (male)")
    print("  2. Female")
    print("  3. Robot")
    print("  4. Deep (male)")
    print("  5. Fast")
    print("  6. Slow")
    print("  7. Excited")
    print("  8. Whisper")
    print("  9. Calm")
    print()
    print("  0. Skip (use default)")
    print()
    
    choice = input("Choose voice preset (1-9, 0=default): ").strip()
    
    preset_map = {
        '1': 'normal',
        '2': 'female',
        '3': 'robot',
        '4': 'deep',
        '5': 'fast',
        '6': 'slow',
        '7': 'excited',
        '8': 'whisper',
        '9': 'calm',
    }
    
    return preset_map.get(choice, 'normal')

def build_command(ai_model, tts_engine, voice_preset):
    """Build the command to run voice assistant"""
    cmd = ['python3', 'voice_ai_assistant.py']
    
    # Add AI model flag
    if ai_model[0] != 'pattern':
        cmd.append('--qwen')
        # Note: Currently voice_ai_assistant.py doesn't support custom model selection
        # You would need to modify qwen_ai_brain.py to accept model parameter
    
    # Add TTS engine flag
    if tts_engine[0] == 'piper':
        cmd.append('--piper')
    elif tts_engine[0] == 'advanced':
        # Would need to add support in voice_ai_assistant.py
        pass
    elif tts_engine[0] == 'simple':
        # Would need to add support in voice_ai_assistant.py
        pass
    
    # Add voice preset
    if voice_preset != 'normal':
        cmd.extend(['--preset', voice_preset])
    
    return cmd

def show_config_summary(ai_model, tts_engine, voice_preset):
    """Show configuration summary"""
    print_header()
    print("📋 CONFIGURATION SUMMARY:")
    print()
    print(f"  AI Model:     {ai_model[1]}")
    print(f"  TTS Engine:   {tts_engine[1]}")
    print(f"  Voice Preset: {voice_preset}")
    print()

def main_menu():
    """Main menu loop"""
    ai_model = ('qwen2:0.5b', 'Qwen2 0.5B')  # Default
    tts_engine = ('espeak', 'espeak-ng')      # Default
    voice_preset = 'normal'                    # Default
    
    while True:
        print_header()
        
        # Check Ollama status
        ollama_running = check_ollama_status()
        ollama_status = "🟢 Running" if ollama_running else "🔴 Stopped"
        
        print(f"Ollama Server: {ollama_status}")
        print()
        print("CURRENT CONFIGURATION:")
        print(f"  • AI Model:     {ai_model[1]}")
        print(f"  • TTS Engine:   {tts_engine[1]}")
        print(f"  • Voice Preset: {voice_preset}")
        print()
        print("─" * 60)
        print()
        print("OPTIONS:")
        print()
        print("  1. Change AI Model")
        print("  2. Change TTS Engine")
        print("  3. Change Voice Preset")
        print()
        print("  4. Start Voice Assistant")
        print("  5. Start with Text-Only Mode (no voice)")
        print("  6. Start with Audio Saving")
        print()
        print("  7. Start Ollama Server")
        print("  8. Stop Ollama Server")
        print("  9. Check Ollama Models")
        print()
        print("  0. Exit")
        print()
        
        choice = input("Select option (0-9): ").strip()
        
        if choice == '1':
            result = select_ai_model()
            if result:
                ai_model = result
        
        elif choice == '2':
            result = select_tts_engine()
            if result:
                tts_engine = result
        
        elif choice == '3':
            voice_preset = select_voice_preset()
        
        elif choice == '4':
            # Start voice assistant
            show_config_summary(ai_model, tts_engine, voice_preset)
            
            if not ollama_running and ai_model[0] != 'pattern':
                print("⚠️  Ollama server is not running!")
                print("   Starting Ollama server...")
                subprocess.Popen(
                    ['/usr/local/bin/ollama', 'serve'],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                print("   Waiting 3 seconds...")
                import time
                time.sleep(3)
            
            cmd = build_command(ai_model, tts_engine, voice_preset)
            
            print(f"\nStarting: {' '.join(cmd)}")
            print("\nPress Ctrl+C to stop and return to menu")
            print("=" * 60)
            print()
            
            try:
                subprocess.run(cmd)
            except KeyboardInterrupt:
                print("\n\nReturning to menu...")
                import time
                time.sleep(1)
        
        elif choice == '5':
            # Text-only mode
            cmd = build_command(ai_model, tts_engine, voice_preset)
            cmd.append('--no-voice')
            
            print(f"\nStarting (text-only): {' '.join(cmd)}")
            print()
            
            try:
                subprocess.run(cmd)
            except KeyboardInterrupt:
                print("\n\nReturning to menu...")
        
        elif choice == '6':
            # Audio saving mode
            cmd = build_command(ai_model, tts_engine, voice_preset)
            cmd.append('--save-audio')
            
            print(f"\nStarting (saving audio): {' '.join(cmd)}")
            print()
            
            try:
                subprocess.run(cmd)
            except KeyboardInterrupt:
                print("\n\nReturning to menu...")
        
        elif choice == '7':
            # Start Ollama
            print("\nStarting Ollama server...")
            subprocess.Popen(
                ['/usr/local/bin/ollama', 'serve'],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            print("Ollama server started in background.")
            input("\nPress Enter to continue...")
        
        elif choice == '8':
            # Stop Ollama
            print("\nStopping Ollama server...")
            subprocess.run(['killall', 'ollama'], stderr=subprocess.DEVNULL)
            print("Ollama server stopped.")
            input("\nPress Enter to continue...")
        
        elif choice == '9':
            # Check models
            print("\nInstalled Ollama models:")
            print()
            models = get_available_models()
            if models:
                for model in models:
                    print(f"  • {model}")
            else:
                print("  No models found or Ollama not available.")
            print()
            input("Press Enter to continue...")
        
        elif choice == '0':
            print("\nGoodbye!")
            sys.exit(0)
        
        else:
            print("\nInvalid option. Try again.")
            import time
            time.sleep(1)

if __name__ == '__main__':
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\nGoodbye!")
        sys.exit(0)
