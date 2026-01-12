#!/usr/bin/env python3
"""
Piper Neural TTS - High-quality neural voice synthesis
Using Amy voice model (60MB) for natural-sounding speech
"""

import subprocess
import argparse
import os
import sys

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(PROJECT_DIR, "voices/en_US-amy-medium/en_US-amy-medium.onnx")
PIPER_BIN = os.path.expanduser("~/.local/bin/piper")

def speak(text, speed=1.0, output_file=None, play=True):
    """
    Synthesize speech using Piper neural TTS
    
    Args:
        text: Text to synthesize
        speed: Speaking speed (0.5-2.0, default 1.0)
        output_file: Optional WAV file path
        play: Whether to play audio (default True)
    """
    if not os.path.exists(PIPER_BIN):
        print(f"Error: Piper not found at {PIPER_BIN}")
        print("Install with: pip3 install piper-tts --break-system-packages")
        sys.exit(1)
    
    if not os.path.exists(MODEL_PATH):
        print(f"Error: Voice model not found at {MODEL_PATH}")
        print("Download it first!")
        sys.exit(1)
    
    # Create temporary file if needed
    if output_file is None:
        output_file = "/tmp/piper_output.wav"
    
    try:
        # Run piper
        cmd = [
            PIPER_BIN,
            "--model", MODEL_PATH,
            "--output_file", output_file,
            "--length_scale", str(1.0 / speed)  # Piper uses inverse
        ]
        
        subprocess.run(cmd, input=text, text=True, check=True, 
                      stderr=subprocess.DEVNULL)
        
        # Play audio if requested
        if play:
            # Try different players in order of Bluetooth compatibility
            players = [
                ("pw-play", [output_file]),  # PipeWire native - best for Bluetooth
                ("play", [output_file]),  # sox
                ("paplay", [output_file]),  # PulseAudio
                ("aplay", [output_file])  # ALSA fallback
            ]
            
            played = False
            for player, args in players:
                if os.system(f"which {player} > /dev/null 2>&1") == 0:
                    try:
                        subprocess.run([player] + args, 
                                     stdout=subprocess.DEVNULL, 
                                     stderr=subprocess.DEVNULL,
                                     check=True)
                        played = True
                        break
                    except:
                        continue
            
            if not played:
                print(f"Audio saved to {output_file} but could not play.")
                print("Please check your audio configuration.")
        
        return output_file
        
    except subprocess.CalledProcessError as e:
        print(f"Error synthesizing speech: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print("Error: Audio player not found. Install aplay or paplay.")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description='Piper Neural TTS - High-quality voice synthesis',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 piper_neural_tts.py "Hello world"
  python3 piper_neural_tts.py "Faster speech" --speed 1.3
  python3 piper_neural_tts.py "Slower speech" --speed 0.8
  python3 piper_neural_tts.py "Save this" --output voice.wav
  python3 piper_neural_tts.py "No playback" --output voice.wav --no-play
        """
    )
    
    parser.add_argument('text', nargs='*', 
                       help='Text to synthesize')
    parser.add_argument('--speed', type=float, default=1.0,
                       help='Speaking speed (0.5-2.0, default: 1.0)')
    parser.add_argument('--output', type=str, default=None,
                       help='Output WAV file path')
    parser.add_argument('--no-play', action='store_true',
                       help='Do not play audio, only save')
    
    args = parser.parse_args()
    
    # Get text
    text = ' '.join(args.text) if args.text else \
           "Hello from Piper neural text to speech on Arduino UNO Q. This is high quality neural voice synthesis running completely offline."
    
    # Synthesize
    output = speak(text, speed=args.speed, output_file=args.output, 
                   play=not args.no_play)
    
    if args.no_play:
        print(f"Saved to: {output}")


if __name__ == '__main__':
    main()
