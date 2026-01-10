#!/usr/bin/env python3
"""
Multi-language Text-to-Speech using Google TTS
Supports Thai and multiple other languages
"""

from gtts import gTTS
import subprocess
import argparse
import os


class MultiLangTTS:
    """Multi-language TTS using Google Text-to-Speech"""
    
    SUPPORTED_LANGUAGES = {
        'en': 'English',
        'th': 'Thai',
        'zh': 'Chinese',
        'ja': 'Japanese',
        'ko': 'Korean',
        'es': 'Spanish',
        'fr': 'French',
        'de': 'German',
        'it': 'Italian',
        'ru': 'Russian',
    }
    
    def __init__(self, language='en', slow=False):
        """
        Initialize TTS
        
        Args:
            language: Language code (e.g., 'en', 'th')
            slow: Speak slowly if True
        """
        self.language = language
        self.slow = slow
    
    def speak(self, text, play=True, output_file="/tmp/gtts_output.mp3"):
        """
        Synthesize and optionally play speech
        
        Args:
            text: Text to speak
            play: Whether to play audio
            output_file: Path to save audio file
        
        Returns:
            Path to output file
        """
        # Generate speech
        tts = gTTS(text=text, lang=self.language, slow=self.slow)
        tts.save(output_file)
        
        if play:
            try:
                # Try paplay with mpg123 for MP3 playback
                subprocess.run(['mpg123', output_file], check=True,
                             stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
            except FileNotFoundError:
                # Try ffplay as fallback
                try:
                    subprocess.run(['ffplay', '-nodisp', '-autoexit', output_file], 
                                 check=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
                except FileNotFoundError:
                    print(f"Audio file saved to: {output_file}")
                    print("Install 'mpg123' or 'ffplay' to play MP3 files")
        
        return output_file


def main():
    parser = argparse.ArgumentParser(
        description='Multi-language TTS using Google Text-to-Speech'
    )
    parser.add_argument('text', nargs='*', help='Text to synthesize')
    parser.add_argument('-l', '--lang', type=str, default='en',
                       help='Language code (en, th, zh, ja, etc.)')
    parser.add_argument('--slow', action='store_true',
                       help='Speak slowly')
    parser.add_argument('--output', type=str, default='/tmp/gtts_output.mp3',
                       help='Output MP3 file')
    parser.add_argument('--no-play', action='store_true',
                       help="Don't play audio, just save file")
    parser.add_argument('--list-langs', action='store_true',
                       help='List supported languages')
    
    args = parser.parse_args()
    
    # List languages if requested
    if args.list_langs:
        print("\nSupported languages:")
        for code, name in MultiLangTTS.SUPPORTED_LANGUAGES.items():
            print(f"  {code}: {name}")
        print("\nFor more languages, see: https://gtts.readthedocs.io/")
        return
    
    # Get text
    if args.text:
        text = ' '.join(args.text)
    else:
        # Default text based on language
        if args.lang == 'th':
            text = "สวัสดีครับ ยินดีต้อนรับสู่ Arduino UNO Q"
        elif args.lang == 'zh':
            text = "你好，欢迎使用 Arduino UNO Q"
        elif args.lang == 'ja':
            text = "こんにちは、Arduino UNO Q へようこそ"
        else:
            text = "Hello from Arduino UNO Q with multi-language support"
    
    # Initialize TTS
    tts = MultiLangTTS(language=args.lang, slow=args.slow)
    
    print(f"Language: {args.lang}")
    print(f"Synthesizing: {text}")
    
    # Speak
    output_file = tts.speak(text, play=not args.no_play, output_file=args.output)
    print(f"Audio saved to: {output_file}")


if __name__ == "__main__":
    main()
