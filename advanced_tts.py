#!/usr/bin/env python3
"""
Advanced Text-to-Speech Engine for Arduino UNO Q
Enhanced phoneme synthesis with voice customization
"""

import wave
import struct
import math
import subprocess
import argparse

class AdvancedTTS:
    def __init__(self, sample_rate=22050, pitch=1.0, speed=1.0, volume=0.5):
        self.sample_rate = sample_rate
        self.pitch = pitch  # 0.5 to 2.0
        self.speed = speed  # 0.5 to 2.0
        self.volume = volume  # 0.0 to 1.0
        
        # Enhanced phoneme mappings with better formant frequencies
        self.vowel_formants = {
            'a': [(730, 1090), (1220, 2440)],
            'e': [(530, 1840), (1840, 2480)],
            'i': [(270, 2290), (2290, 3010)],
            'o': [(570, 840), (840, 2410)],
            'u': [(440, 1020), (1020, 2240)],
        }
        
        self.consonant_formants = {
            'b': [(150, 300)],
            'c': [(200, 400)],
            'd': [(150, 300)],
            'f': [(3000, 6000)],
            'g': [(200, 400)],
            'h': [(500, 2000)],
            'j': [(200, 500)],
            'k': [(250, 500)],
            'l': [(400, 1500)],
            'm': [(250, 1000)],
            'n': [(300, 1500)],
            'p': [(150, 300)],
            'q': [(200, 400)],
            'r': [(350, 1600)],
            's': [(4000, 8000)],
            't': [(200, 400)],
            'v': [(200, 600)],
            'w': [(300, 900)],
            'x': [(200, 400)],
            'y': [(300, 2200)],
            'z': [(3000, 7000)],
        }
        
        # Common word mappings for better pronunciation
        self.word_mappings = {
            'hello': 'helo',
            'world': 'werld',
            'arduino': 'ardeeno',
            'voice': 'voys',
            'text': 'tekst',
            'speech': 'speech',
            'the': 'thu',
            'is': 'iz',
            'are': 'ar',
            'you': 'yu',
            'this': 'this',
        }
    
    def preprocess_text(self, text):
        """Preprocess text for better pronunciation"""
        text = text.lower().strip()
        words = text.split()
        processed = []
        
        for word in words:
            # Remove punctuation but keep it for pauses
            clean_word = ''.join(c for c in word if c.isalnum())
            if clean_word in self.word_mappings:
                processed.append(self.word_mappings[clean_word])
            else:
                processed.append(clean_word)
            
            # Add pause for punctuation
            if word and word[-1] in '.,!?;:':
                processed.append('_')
        
        return ' '.join(processed)
    
    def text_to_phonemes(self, text):
        """Convert text to phonemes with better rules"""
        text = self.preprocess_text(text)
        phonemes = []
        
        i = 0
        while i < len(text):
            char = text[i]
            
            if char == ' ':
                phonemes.append('_')
            elif char == '_':
                phonemes.append('_')
                phonemes.append('_')
            elif char.isalpha():
                # Check for vowel vs consonant
                if char in self.vowel_formants:
                    phonemes.append(('v', char))
                elif char in self.consonant_formants:
                    phonemes.append(('c', char))
                else:
                    phonemes.append(('v', 'e'))  # Default vowel
            
            i += 1
        
        return phonemes
    
    def generate_tone(self, frequency, duration, envelope='smooth'):
        """Generate a tone with specified envelope"""
        frequency = frequency * self.pitch
        num_samples = int(self.sample_rate * duration / self.speed)
        samples = []
        
        for i in range(num_samples):
            t = float(i) / self.sample_rate
            
            # Generate sine wave
            value = math.sin(2 * math.pi * frequency * t)
            
            # Apply envelope
            if envelope == 'smooth':
                fade_samples = min(200, num_samples // 4)
                if i < fade_samples:
                    value *= i / fade_samples
                elif i > num_samples - fade_samples:
                    value *= (num_samples - i) / fade_samples
            elif envelope == 'sharp':
                fade_samples = 50
                if i < fade_samples:
                    value *= i / fade_samples
                elif i > num_samples - fade_samples:
                    value *= (num_samples - i) / fade_samples
            
            # Add slight harmonics for richness
            value += 0.2 * math.sin(2 * math.pi * frequency * 2 * t)
            value += 0.1 * math.sin(2 * math.pi * frequency * 3 * t)
            
            # Normalize and scale to volume
            value *= self.volume * 0.4
            
            # Convert to 16-bit PCM
            sample = int(max(-32767, min(32767, value * 32767)))
            samples.append(sample)
        
        return samples
    
    def generate_phoneme_sound(self, phoneme_type, phoneme_char):
        """Generate sound for a phoneme"""
        duration = 0.12 / self.speed
        
        if phoneme_type == 'v':
            # Vowel - use formant synthesis
            formants = self.vowel_formants.get(phoneme_char, [(500, 1500)])
            return self.generate_formant_sound(formants, duration, 'smooth')
        else:
            # Consonant - use noise or simple tone
            formants = self.consonant_formants.get(phoneme_char, [(500, 1000)])
            duration *= 0.7  # Consonants are shorter
            
            if phoneme_char in 'szhf':
                # Fricatives - use higher frequencies
                return self.generate_noise_sound(formants[0], duration)
            else:
                return self.generate_formant_sound(formants, duration, 'sharp')
    
    def generate_formant_sound(self, formants, duration, envelope):
        """Generate sound with multiple formants"""
        num_samples = int(self.sample_rate * duration / self.speed)
        samples = [0] * num_samples
        
        for freq_low, freq_high in formants:
            freq = (freq_low + freq_high) / 2
            tone_samples = self.generate_tone(freq, duration, envelope)
            
            # Mix formants
            for i in range(min(len(samples), len(tone_samples))):
                samples[i] += tone_samples[i] // len(formants)
        
        return samples
    
    def generate_noise_sound(self, freq_range, duration):
        """Generate noise for fricatives"""
        import random
        num_samples = int(self.sample_rate * duration / self.speed)
        samples = []
        
        for i in range(num_samples):
            # Generate filtered noise
            value = random.uniform(-1, 1)
            
            # Simple fade envelope
            fade_samples = 100
            if i < fade_samples:
                value *= i / fade_samples
            elif i > num_samples - fade_samples:
                value *= (num_samples - i) / fade_samples
            
            value *= self.volume * 0.3
            sample = int(value * 32767)
            samples.append(sample)
        
        return samples
    
    def synthesize_speech(self, text, output_file):
        """Synthesize speech from text"""
        phonemes = self.text_to_phonemes(text)
        all_samples = []
        
        for phoneme in phonemes:
            if phoneme == '_':
                # Silence/pause
                duration = 0.15 / self.speed
                silence = [0] * int(self.sample_rate * duration)
                all_samples.extend(silence)
            else:
                phoneme_type, phoneme_char = phoneme
                samples = self.generate_phoneme_sound(phoneme_type, phoneme_char)
                all_samples.extend(samples)
        
        # Write WAV file
        with wave.open(output_file, 'wb') as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(self.sample_rate)
            
            for sample in all_samples:
                wav_file.writeframes(struct.pack('<h', sample))
        
        return output_file
    
    def speak(self, text, play=True, output_file="/tmp/tts_output.wav"):
        """Synthesize and optionally play speech"""
        self.synthesize_speech(text, output_file)
        
        if play:
            try:
                subprocess.run(['aplay', output_file], check=True, 
                             stderr=subprocess.DEVNULL)
            except (FileNotFoundError, subprocess.CalledProcessError):
                print(f"Audio file saved to: {output_file}")
        
        return output_file


def main():
    parser = argparse.ArgumentParser(description='Advanced TTS for Arduino UNO Q')
    parser.add_argument('text', nargs='*', help='Text to synthesize')
    parser.add_argument('--pitch', type=float, default=1.0, 
                       help='Pitch (0.5-2.0, default: 1.0)')
    parser.add_argument('--speed', type=float, default=1.0, 
                       help='Speed (0.5-2.0, default: 1.0)')
    parser.add_argument('--volume', type=float, default=0.5, 
                       help='Volume (0.0-1.0, default: 0.5)')
    parser.add_argument('--output', type=str, default='/tmp/tts_output.wav',
                       help='Output WAV file')
    parser.add_argument('--no-play', action='store_true',
                       help='Don\'t play audio, just save file')
    
    args = parser.parse_args()
    
    if args.text:
        text = ' '.join(args.text)
    else:
        text = "Hello from Arduino UNO Q. Advanced offline voice generation system."
    
    tts = AdvancedTTS(pitch=args.pitch, speed=args.speed, volume=args.volume)
    
    print(f"Synthesizing: {text}")
    print(f"Settings: pitch={args.pitch}, speed={args.speed}, volume={args.volume}")
    
    output_file = tts.speak(text, play=not args.no_play, output_file=args.output)
    print(f"Audio saved to: {output_file}")


if __name__ == "__main__":
    main()
