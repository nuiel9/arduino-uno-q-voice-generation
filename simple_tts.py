#!/usr/bin/env python3
"""
Simple Text-to-Speech Engine for Arduino UNO Q
Pure Python implementation - no external dependencies
Generates audio using basic phoneme synthesis
"""

import wave
import struct
import math
import subprocess
import os

class SimpleTTS:
    def __init__(self, sample_rate=48000):
        self.sample_rate = sample_rate
        self.volume = 0.3
        
        # Simple phoneme to frequency mapping (formants)
        self.phonemes = {
            'a': [(700, 1220), (1220, 2600)],  # as in "father"
            'e': [(530, 1840), (1840, 2480)],  # as in "bed"
            'i': [(270, 2290), (2290, 3010)],  # as in "see"
            'o': [(570, 840), (840, 2410)],    # as in "go"
            'u': [(440, 1020), (1020, 2240)],  # as in "boot"
            'b': [(100, 200)],
            'd': [(150, 250)],
            'g': [(200, 300)],
            'k': [(250, 350)],
            'l': [(350, 1500)],
            'm': [(200, 1000)],
            'n': [(250, 1500)],
            'p': [(100, 150)],
            'r': [(300, 1600)],
            's': [(4000, 8000)],
            't': [(200, 300)],
            'w': [(300, 800)],
            'z': [(3000, 7000)],
            ' ': [],  # silence
        }
        
    def text_to_phonemes(self, text):
        """Convert text to simple phoneme representation"""
        text = text.lower()
        phonemes = []
        
        # Very basic text-to-phoneme conversion
        for char in text:
            if char in self.phonemes:
                phonemes.append(char)
            elif char.isalpha():
                # Default to 'e' for unknown letters
                phonemes.append('e')
            elif char in '.,!?':
                phonemes.append(' ')
                phonemes.append(' ')
        
        return phonemes
    
    def generate_tone(self, frequency, duration, fade=True):
        """Generate a sine wave tone"""
        num_samples = int(self.sample_rate * duration)
        samples = []
        
        for i in range(num_samples):
            t = float(i) / self.sample_rate
            
            # Generate sine wave
            value = math.sin(2 * math.pi * frequency * t)
            
            # Apply fade in/out to reduce clicks
            if fade:
                if i < 100:
                    value *= i / 100.0
                elif i > num_samples - 100:
                    value *= (num_samples - i) / 100.0
            
            # Scale to volume
            value *= self.volume
            
            # Convert to 16-bit PCM
            sample = int(value * 32767)
            samples.append(sample)
        
        return samples
    
    def generate_formant(self, formants, duration):
        """Generate sound with multiple formant frequencies"""
        num_samples = int(self.sample_rate * duration)
        samples = [0] * num_samples
        
        for freq_low, freq_high in formants:
            freq = (freq_low + freq_high) / 2
            tone_samples = self.generate_tone(freq, duration)
            
            for i in range(len(samples)):
                samples[i] += tone_samples[i] // len(formants)
        
        return samples
    
    def synthesize_speech(self, text, output_file):
        """Synthesize speech from text"""
        phonemes = self.text_to_phonemes(text)
        all_samples = []
        
        for phoneme in phonemes:
            if phoneme == ' ':
                # Add silence
                duration = 0.1
                silence = [0] * int(self.sample_rate * duration)
                all_samples.extend(silence)
            else:
                # Generate phoneme sound
                formants = self.phonemes.get(phoneme, [(500, 1500)])
                duration = 0.15  # Duration per phoneme
                samples = self.generate_formant(formants, duration)
                all_samples.extend(samples)
        
        # Write WAV file
        with wave.open(output_file, 'wb') as wav_file:
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(self.sample_rate)
            
            # Convert samples to bytes
            for sample in all_samples:
                wav_file.writeframes(struct.pack('<h', sample))
        
        return output_file
    
    def speak(self, text, play=True):
        """Synthesize and optionally play speech"""
        output_file = "/tmp/tts_output.wav"
        self.synthesize_speech(text, output_file)
        
        if play:
            try:
                # Try paplay first (PulseAudio/PipeWire for Bluetooth)
                subprocess.run(['paplay', output_file], check=True)
            except FileNotFoundError:
                # Fallback to aplay
                try:
                    subprocess.run(['aplay', output_file], check=True)
                except FileNotFoundError:
                    print(f"Audio file generated: {output_file}")
                    print("Install audio player to play automatically")
                except subprocess.CalledProcessError:
                    print(f"Error playing audio. File saved to: {output_file}")
        
        return output_file


def main():
    import sys
    
    tts = SimpleTTS()
    
    if len(sys.argv) > 1:
        text = ' '.join(sys.argv[1:])
    else:
        text = "Hello from Arduino UNO Q. This is offline voice generation."
    
    print(f"Synthesizing: {text}")
    output_file = tts.speak(text)
    print(f"Audio saved to: {output_file}")


if __name__ == "__main__":
    main()
