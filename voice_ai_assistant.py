#!/usr/bin/env python3
"""
Voice AI Assistant - Offline Generative AI with Voice Response
Combines lightweight AI brain with espeak-ng TTS for Arduino UNO Q
Fully offline operation - no internet required
"""

import sys
import argparse
from pathlib import Path

# Import the AI brains
from offline_ai_brain import OfflineAI
try:
    from qwen_ai_brain import QwenAI
    QWEN_AVAILABLE = True
except Exception as e:
    QWEN_AVAILABLE = False
    print(f"Qwen not available: {e}")

# Import the TTS engines
from espeak_tts import EspeakTTS, VoicePresets
try:
    from piper_neural_tts import speak as piper_speak
    PIPER_AVAILABLE = True
except:
    PIPER_AVAILABLE = False


class VoiceAI:
    """Voice-enabled AI assistant"""
    
    def __init__(self, voice_preset='normal', speed=175, pitch=50, volume=100, 
                 voice_enabled=True, save_audio=False, use_qwen=False, use_piper=False):
        """Initialize voice AI assistant
        
        Args:
            voice_preset: Voice preset (normal, robot, excited, calm, etc.)
            speed: Speech speed (80-450)
            pitch: Voice pitch (0-99)
            volume: Volume level (0-200)
            voice_enabled: Enable voice output
            save_audio: Save audio files
        """
        print("Initializing Offline Voice AI Assistant...")
        
        # Initialize AI brain
        self.use_qwen = use_qwen and QWEN_AVAILABLE
        
        if self.use_qwen:
            self.ai = QwenAI()
            print("✓ Qwen LLM loaded (Qwen2-0.5B)")
        else:
            self.ai = OfflineAI()
            print("✓ Pattern-based AI brain loaded")
            if use_qwen and not QWEN_AVAILABLE:
                print("  Note: Qwen requested but not available, using pattern-based AI")
        
        # Initialize TTS engine
        self.voice_enabled = voice_enabled
        self.save_audio = save_audio
        self.use_piper = use_piper and PIPER_AVAILABLE
        self.tts_speed = speed
        
        if voice_enabled:
            if self.use_piper:
                # Use Piper neural TTS
                self.tts = None  # Piper uses function, not class
                print("✓ Piper Neural TTS loaded (high quality)")
            else:
                # Use espeak-ng
                if voice_preset != 'normal' or (speed == 175 and pitch == 50 and volume == 100):
                    # Try to use preset
                    preset_method = getattr(VoicePresets, voice_preset, None)
                    if preset_method:
                        self.tts = preset_method()
                        print(f"✓ Voice engine loaded (preset: {voice_preset})")
                    else:
                        self.tts = EspeakTTS(speed=speed, pitch=pitch, volume=volume)
                        print(f"✓ Voice engine loaded (custom settings)")
                else:
                    self.tts = EspeakTTS(speed=speed, pitch=pitch, volume=volume)
                    print(f"✓ Voice engine loaded")
        else:
            self.tts = None
            print("✓ Text-only mode")
        
        self.audio_counter = 0
        print("Ready!\n")
    
    def speak_response(self, text: str):
        """Speak the response using TTS"""
        if not self.voice_enabled:
            return
        
        try:
            if self.use_piper:
                # Use Piper neural TTS
                output_file = f"/tmp/voice_ai_{self.audio_counter:03d}.wav" if self.save_audio else None
                piper_speak(text, speed=self.tts_speed/175.0, 
                          output_file=output_file, 
                          play=not self.save_audio)
                if self.save_audio:
                    self.audio_counter += 1
            else:
                # Use espeak-ng
                if self.save_audio:
                    filename = f"/tmp/voice_ai_{self.audio_counter:03d}.wav"
                    self.tts.speak(text, output_file=filename)
                    self.audio_counter += 1
                else:
                    self.tts.speak(text)
        except Exception as e:
            print(f"Voice output error: {e}")
    
    def chat(self, user_input: str, speak=True) -> str:
        """Process input and generate voice response
        
        Args:
            user_input: User's text input
            speak: Whether to speak the response
            
        Returns:
            AI's text response
        """
        # Get AI response
        response = self.ai.process(user_input)
        
        # Speak it
        if speak and self.voice_enabled:
            self.speak_response(response)
        
        return response
    
    def interactive_mode(self):
        """Run interactive chat session with voice"""
        print("=== Voice AI Assistant ===")
        print("Offline AI with voice responses")
        print("Type 'quit' or 'exit' to end session")
        print("Type 'mute' to disable voice")
        print("Type 'unmute' to enable voice")
        print("Type 'stats' to see conversation statistics")
        print("Type 'save' to save conversation history")
        print("-" * 40)
        
        # Greeting
        greeting = "Hello! I'm your offline AI assistant. How can I help you today?"
        print(f"\nAI: {greeting}")
        if self.voice_enabled:
            self.speak_response(greeting)
        
        print()
        
        # Main loop
        while True:
            try:
                # Get user input
                user_input = input("You: ").strip()
                
                if not user_input:
                    continue
                
                # Handle special commands
                if user_input.lower() in ['quit', 'exit', 'bye', 'goodbye']:
                    response = self.chat(user_input)
                    print(f"AI: {response}\n")
                    break
                
                elif user_input.lower() == 'mute':
                    self.voice_enabled = False
                    print("AI: [Voice output disabled]\n")
                    continue
                
                elif user_input.lower() == 'unmute':
                    self.voice_enabled = True
                    print("AI: [Voice output enabled]\n")
                    continue
                
                elif user_input.lower() == 'stats':
                    stats = self.ai.get_stats()
                    print(f"\n--- Conversation Statistics ---")
                    print(f"Total messages: {stats['total_messages']}")
                    print(f"Your messages: {stats['user_messages']}")
                    print(f"AI messages: {stats['assistant_messages']}")
                    if stats['user_name']:
                        print(f"Your name: {stats['user_name']}")
                    print()
                    continue
                
                elif user_input.lower() == 'save':
                    filename = f"/tmp/conversation_{self.ai.get_stats()['total_messages']}.json"
                    self.ai.save_conversation(filename)
                    print(f"AI: Conversation saved to {filename}\n")
                    continue
                
                elif user_input.lower() == 'clear':
                    self.ai.clear_history()
                    print("AI: Conversation history cleared.\n")
                    continue
                
                # Normal conversation
                response = self.chat(user_input)
                print(f"AI: {response}\n")
                
            except KeyboardInterrupt:
                print("\n\nInterrupted. Goodbye!")
                break
            
            except Exception as e:
                print(f"Error: {e}\n")
        
        # Show final stats
        stats = self.ai.get_stats()
        print("\n--- Session Summary ---")
        print(f"Total exchanges: {stats['user_messages']}")
        print(f"Audio files saved: {self.audio_counter}" if self.save_audio else "Audio not saved")
        print("\nThank you for using Voice AI Assistant!")
    
    def batch_mode(self, questions: list):
        """Process batch of questions"""
        print("=== Batch Mode ===\n")
        
        for i, question in enumerate(questions, 1):
            print(f"[{i}/{len(questions)}] You: {question}")
            response = self.chat(question)
            print(f"AI: {response}\n")
        
        print("Batch complete.")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Offline Voice AI Assistant for Arduino UNO Q',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode with default voice
  python3 voice_ai_assistant.py
  
  # Robot voice
  python3 voice_ai_assistant.py --preset robot
  
  # Excited voice, faster
  python3 voice_ai_assistant.py --preset excited --speed 200
  
  # Text-only mode (no voice)
  python3 voice_ai_assistant.py --no-voice
  
  # Save audio files
  python3 voice_ai_assistant.py --save-audio
  
  # Batch mode
  python3 voice_ai_assistant.py --batch "What time is it?" "Tell me a joke"
        """
    )
    
    parser.add_argument('--preset', '-p', 
                       choices=['normal', 'female', 'fast', 'slow', 'robot', 'deep', 
                               'high', 'whisper', 'excited', 'calm'],
                       default='normal',
                       help='Voice preset')
    
    parser.add_argument('--speed', '-s', type=int, default=175,
                       help='Speech speed (80-450, default: 175)')
    
    parser.add_argument('--pitch', type=int, default=50,
                       help='Voice pitch (0-99, default: 50)')
    
    parser.add_argument('--volume', '-v', type=int, default=100,
                       help='Volume level (0-200, default: 100)')
    
    parser.add_argument('--no-voice', action='store_true',
                       help='Text-only mode (disable voice)')
    
    parser.add_argument('--save-audio', action='store_true',
                       help='Save audio files to /tmp')
    
    parser.add_argument('--batch', '-b', nargs='+',
                       help='Batch mode: process multiple questions')
    
    parser.add_argument('--qwen', action='store_true',
                       help='Use Qwen LLM instead of pattern-based AI')
    
    parser.add_argument('--piper', action='store_true',
                       help='Use Piper neural TTS instead of espeak-ng')
    
    args = parser.parse_args()
    
    # Create voice AI assistant
    try:
        assistant = VoiceAI(
            voice_preset=args.preset,
            speed=args.speed,
            pitch=args.pitch,
            volume=args.volume,
            voice_enabled=not args.no_voice,
            save_audio=args.save_audio,
            use_qwen=args.qwen,
            use_piper=args.piper
        )
        
        # Run in appropriate mode
        if args.batch:
            assistant.batch_mode(args.batch)
        else:
            assistant.interactive_mode()
    
    except KeyboardInterrupt:
        print("\n\nGoodbye!")
        sys.exit(0)
    
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
