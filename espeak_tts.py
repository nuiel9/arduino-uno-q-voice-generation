#!/usr/bin/env python3
"""
Enhanced Text-to-Speech using espeak-ng
Professional quality voice synthesis for Arduino UNO Q
"""

import subprocess
import argparse
import os

class EspeakTTS:
    def __init__(self, voice='en', speed=175, pitch=50, volume=100):
        """
        Initialize espeak-ng TTS
        
        Args:
            voice: Voice/language code (en, en-us, en-gb, etc.)
            speed: Words per minute (80-450, default: 175)
            pitch: Pitch adjustment (0-99, default: 50)
            volume: Volume (0-200, default: 100)
        """
        self.voice = voice
        self.speed = speed
        self.pitch = pitch
        self.volume = volume
        
        # Available voices
        self.voices = {
            'en': 'English',
            'en-us': 'English (US)',
            'en-gb': 'English (UK)',
            'en-scottish': 'English (Scottish)',
            'en-rp': 'English (Received Pronunciation)',
            'en-westindies': 'English (West Indies)',
        }
    
    def list_voices(self):
        """List all available voices"""
        try:
            result = subprocess.run(['espeak-ng', '--voices'], 
                                  capture_output=True, text=True)
            return result.stdout
        except FileNotFoundError:
            return "espeak-ng not found"
    
    def speak(self, text, play=True, output_file=None):
        """
        Synthesize speech from text
        
        Args:
            text: Text to synthesize
            play: Whether to play audio immediately
            output_file: Save to WAV file (optional)
        """
        cmd = ['espeak-ng']
        
        # Voice settings
        cmd.extend(['-v', self.voice])
        cmd.extend(['-s', str(self.speed)])
        cmd.extend(['-p', str(self.pitch)])
        cmd.extend(['-a', str(self.volume)])
        
        # Output file
        if output_file:
            cmd.extend(['-w', output_file])
        
        # Text to speak
        cmd.append(text)
        
        try:
            if not play and output_file:
                # Just save to file
                subprocess.run(cmd, check=True, stderr=subprocess.DEVNULL)
                return output_file
            elif output_file:
                # Save and play
                subprocess.run(cmd, check=True, stderr=subprocess.DEVNULL)
                try:
                    # Try paplay first (PulseAudio/PipeWire for Bluetooth)
                    subprocess.run(['paplay', output_file], 
                                 check=True, stderr=subprocess.DEVNULL)
                except FileNotFoundError:
                    # Fallback to aplay
                    subprocess.run(['aplay', output_file], 
                                 check=True, stderr=subprocess.DEVNULL)
                return output_file
            else:
                # Just play
                subprocess.run(cmd, check=True, stderr=subprocess.DEVNULL)
                return None
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
            return None
    
    def speak_file(self, filename):
        """Speak text from a file"""
        try:
            with open(filename, 'r') as f:
                text = f.read()
            self.speak(text)
        except FileNotFoundError:
            print(f"File not found: {filename}")
    
    def set_voice(self, voice):
        """Change voice"""
        self.voice = voice
    
    def set_speed(self, speed):
        """Change speaking speed (80-450 wpm)"""
        self.speed = max(80, min(450, speed))
    
    def set_pitch(self, pitch):
        """Change pitch (0-99)"""
        self.pitch = max(0, min(99, pitch))
    
    def set_volume(self, volume):
        """Change volume (0-200)"""
        self.volume = max(0, min(200, volume))


class VoicePresets:
    """Pre-configured voice presets"""
    
    @staticmethod
    def normal():
        return EspeakTTS(speed=175, pitch=50, volume=100)
    
    @staticmethod
    def thai():
        # Basic Thai voice using espeak-ng 'th'
        return EspeakTTS(voice='th', speed=175, pitch=50, volume=100)
    
    @staticmethod
    def fast():
        return EspeakTTS(speed=250, pitch=50, volume=100)
    
    @staticmethod
    def slow():
        return EspeakTTS(speed=120, pitch=50, volume=100)
    
    @staticmethod
    def robot():
        return EspeakTTS(speed=150, pitch=30, volume=90)
    
    @staticmethod
    def deep():
        return EspeakTTS(speed=160, pitch=20, volume=110)
    
    @staticmethod
    def high():
        return EspeakTTS(speed=180, pitch=80, volume=100)
    
    @staticmethod
    def whisper():
        return EspeakTTS(speed=140, pitch=40, volume=60)
    
    @staticmethod
    def excited():
        return EspeakTTS(speed=220, pitch=70, volume=120)
    
    @staticmethod
    def calm():
        return EspeakTTS(speed=150, pitch=45, volume=85)


def main():
    parser = argparse.ArgumentParser(
        description='Enhanced TTS using espeak-ng for Arduino UNO Q',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Voice Presets:
  normal, fast, slow, robot, deep, high, whisper, excited, calm

Examples:
  espeak_tts.py "Hello world"
  espeak_tts.py "Test" --speed 200 --pitch 60
  espeak_tts.py "Save this" --output voice.wav --no-play
  espeak_tts.py "Robot voice" --preset robot
  espeak_tts.py --list-voices
        """
    )
    
    parser.add_argument('text', nargs='*', help='Text to synthesize')
    parser.add_argument('-v', '--voice', type=str, default='en',
                       help='Voice code (default: en)')
    parser.add_argument('--speed', type=int, default=175,
                       help='Words per minute (80-450, default: 175)')
    parser.add_argument('--pitch', type=int, default=50,
                       help='Pitch (0-99, default: 50)')
    parser.add_argument('--volume', type=int, default=100,
                       help='Volume (0-200, default: 100)')
    parser.add_argument('--preset', type=str, choices=[
                       'normal', 'fast', 'slow', 'robot', 'deep', 
                       'high', 'whisper', 'excited', 'calm', 'thai'],
                       help='Use a voice preset')
    parser.add_argument('--output', type=str,
                       help='Save to WAV file')
    parser.add_argument('--no-play', action='store_true',
                       help='Don\'t play audio, just save')
    parser.add_argument('--file', type=str,
                       help='Read text from file')
    parser.add_argument('--list-voices', action='store_true',
                       help='List all available voices')
    
    args = parser.parse_args()
    
    # List voices
    if args.list_voices:
        tts = EspeakTTS()
        print(tts.list_voices())
        return
    
    # Create TTS with preset or custom settings
    if args.preset:
        tts = getattr(VoicePresets, args.preset)()
    else:
        tts = EspeakTTS(
            voice=args.voice,
            speed=args.speed,
            pitch=args.pitch,
            volume=args.volume
        )
    
    # Get text
    if args.file:
        tts.speak_file(args.file)
    elif args.text:
        text = ' '.join(args.text)
        print(f"Synthesizing: {text}")
        print(f"Settings: voice={tts.voice}, speed={tts.speed}, "
              f"pitch={tts.pitch}, volume={tts.volume}")
        
        output = tts.speak(text, play=not args.no_play, 
                          output_file=args.output)
        
        if output:
            print(f"Audio saved to: {output}")
    else:
        print("No text provided. Use --help for usage information.")


if __name__ == "__main__":
    main()
