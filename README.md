# Arduino UNO Q - Voice Generation System

A complete text-to-speech (TTS) system for Arduino UNO Q with hybrid online/offline capabilities and **real generative AI** using Qwen2 LLM. Features multiple quality levels: professional espeak-ng integration (offline), Google TTS for multi-language support (online), enhanced pure Python TTS (offline), and basic zero-dependency TTS (offline). Includes Thai language support and offline conversational AI with voice responses.

## Features

🧠 **Generative AI** - Real offline LLM (Qwen2-0.5B) with voice responses 🆕
💬 **Conversational AI** - Pattern-based AI for fast responses  
🎵 **Neural TTS** - Piper high-quality neural voice synthesis 🆕  
👩 **Female Voice** - Multiple voice presets including female simulation 🆕  
🎮 **Interactive Menu** - Easy-to-use configuration menu 🆕  
✨ **Hybrid Online/Offline** - Works with or without internet  
🌍 **Multi-Language** - Thai language support (online via gTTS, offline via espeak-ng)  
🎵 **Voice Customization** - Control pitch, speed, volume, and voice presets  
🔊 **Real-time Generation** - Synthesize speech on-the-fly  
🤖 **Arduino Integration** - Serial communication with STM32 MCU  
🎮 **Interactive Demos** - Multiple demonstration modes including Thai and AI chat  
📦 **Multiple Quality Levels** - Neural (Piper), Professional (espeak-ng/gTTS), enhanced (pure Python), or basic (zero dependencies)  
⚖️ **Engine Comparison** - Built-in comparison tool for all engines

## System Requirements

- Arduino UNO Q (tested on 2GB RAM variant)
- Python 3.13+ (included with UNO Q)
- Audio output device (USB or built-in)
- ~350MB free storage space (for espeak-ng) or ~50KB (pure Python only)
- Optional: ~400MB for Qwen2 LLM (Ollama + model)

## Project Structure

```
voice_ai_project/
├── simple_tts.py              # Basic TTS engine (pure Python)
├── advanced_tts.py            # Advanced TTS with customization (pure Python)
├── espeak_tts.py              # Professional TTS using espeak-ng ⭐ RECOMMENDED
├── gtts_multilang.py          # Multi-language TTS tool (100+ languages)
├── thai_test.py               # Thai language test and demo script
├── compare_tts.py             # Compare all TTS engines
├── serial_voice_bridge.py     # Arduino MCU communication bridge
├── arduino_voice_trigger.ino  # Arduino sketch for STM32
├── demo.py                    # Interactive demo application
├── offline_ai_brain.py        # Pattern-based conversational AI 🆕
├── qwen_ai_brain.py           # Qwen2 LLM wrapper 🆕
├── voice_ai_assistant.py      # Voice-enabled AI assistant 🆕
├── demo_voice_ai.py           # AI voice demo 🆕
├── README.md                  # This file
├── QUICK_START.md             # Quick reference guide
├── VOICE_AI_README.md         # Voice AI documentation 🆕
└── QWEN_README.md             # Qwen LLM guide 🆕
```

## Quick Start

### 0. Interactive Menu (EASIEST! 🆕)

Use the interactive menu for easy configuration:

```bash
python3 voice_ai_menu.py
```

**Features:**
- Select AI model (Pattern-based, Qwen2)
- Choose TTS engine (espeak-ng, Piper Neural, Advanced, Simple)
- Pick voice presets (normal, female, robot, deep, etc.)
- Manage Ollama server
- Launch with your configuration

### 1. Voice AI Assistant (NEW! 🆕)

Use the AI assistant with voice responses:

```bash
# Pattern-based AI (fast, <0.1s responses)
python3 voice_ai_assistant.py

# Qwen2 LLM (real generative AI, 2-10s responses)
python3 voice_ai_assistant.py --qwen

# With different voices
python3 voice_ai_assistant.py --qwen --preset robot
python3 voice_ai_assistant.py --preset female
python3 voice_ai_assistant.py --preset excited

# With Piper neural TTS (high quality)
python3 voice_ai_assistant.py --qwen --piper
python3 voice_ai_assistant.py --piper --preset female

# Batch mode
python3 voice_ai_assistant.py --batch "Hello" "What time is it?"
python3 voice_ai_assistant.py --qwen --batch "What is Arduino?" "Tell me a joke"

# Text-only (no voice)
python3 voice_ai_assistant.py --no-voice
```

**Interactive commands:**
- `mute` / `unmute` - Control voice output
- `stats` - Show conversation statistics
- `save` - Save conversation history
- `quit` - Exit

See [VOICE_AI_README.md](VOICE_AI_README.md) and [QWEN_README.md](QWEN_README.md) for complete documentation.

### 2. Basic TTS Usage

Generate speech from command line:

```bash
# Professional quality with espeak-ng (RECOMMENDED)
python3 espeak_tts.py "Hello from Arduino UNO Q"

# With voice presets
python3 espeak_tts.py "Test message" --preset robot
python3 espeak_tts.py "Excited voice" --preset excited

# Custom settings
python3 espeak_tts.py "Custom" --speed 200 --pitch 60 --volume 120

# Pure Python TTS (no dependencies)
python3 simple_tts.py "Hello from Arduino UNO Q"
python3 advanced_tts.py "Test" --pitch 1.2 --speed 1.0 --volume 0.7

# Thai language (offline)
python3 espeak_tts.py "สวัสดีครับ" -v th

# Thai language test script
python3 thai_test.py
```

### 2. Compare TTS Engines

Compare all three TTS engines side-by-side:

```bash
python3 compare_tts.py
```

This tool demonstrates:
- Quality comparison of all three engines
- Speed and performance differences
- Feature availability
- Usage recommendations

### 3. Interactive Demo

Run the interactive demo to explore all features:

```bash
python3 demo.py
```

This provides:
- Basic text-to-speech examples
- Voice customization demonstrations
- Long text synthesis
- Interactive text input mode
- Special voice effects (robot, deep, chipmunk)
- Thai language demos (offline and online)

### 4. Arduino Integration

For projects combining the STM32 MCU with voice generation:

**Step 1:** Upload the Arduino sketch to your UNO Q MCU:
- Open `arduino_voice_trigger.ino` in Arduino IDE or App Lab
- Upload to the STM32U585 MCU side
- Connect a button to pin 2 (optional)

**Step 2:** Run the Python bridge on the Linux side:

```bash
python3 serial_voice_bridge.py
```

The bridge will:
- Auto-detect the Arduino serial port
- Listen for SPEAK: commands from the MCU
- Generate and play speech
- Send status feedback to MCU

## API Usage

### Espeak TTS (Recommended)

```python
from espeak_tts import EspeakTTS

# Create TTS with default settings
tts = EspeakTTS()
tts.speak("Hello world")

# With custom settings
tts = EspeakTTS(speed=180, pitch=50, volume=100)
tts.speak("Custom voice")

# Using voice presets
tts = EspeakTTS(preset="robot")
tts.speak("I am a robot")

# Available presets: normal, fast, slow, robot, deep, high, whisper, excited, calm
```

### Simple TTS

```python
from simple_tts import SimpleTTS

tts = SimpleTTS()
tts.speak("Hello world")
```

### Advanced TTS

```python
from advanced_tts import AdvancedTTS

# Create TTS with custom settings
tts = AdvancedTTS(
    pitch=1.2,    # 0.5 to 2.0 (default: 1.0)
    speed=1.0,    # 0.5 to 2.0 (default: 1.0)
    volume=0.6    # 0.0 to 1.0 (default: 0.5)
)

# Synthesize and play
tts.speak("This is custom voice")

# Save without playing
tts.speak("Save this", play=False, output_file="/tmp/output.wav")
```

### Thai Language Support

```python
# Offline Thai TTS with espeak-ng
from espeak_tts import EspeakTTS

tts = EspeakTTS(voice='th', speed=150, pitch=50)
tts.speak("สวัสดีครับ")  # Hello (male)
tts.speak("ขอบคุณค่ะ")  # Thank you (female)

# Online Thai TTS with Google (requires internet)
from gtts import gTTS
import subprocess

tts = gTTS(text="สวัสดีครับ", lang='th')
tts.save("/tmp/thai.mp3")
subprocess.run(['mpg123', '-q', '/tmp/thai.mp3'])
```

### Serial Bridge

```python
from serial_voice_bridge import SerialVoiceBridge

# Auto-detect port
bridge = SerialVoiceBridge()
bridge.run()

# Or specify port manually
bridge = SerialVoiceBridge(port="/dev/ttyACM0", baudrate=115200)
bridge.run()
```

## Voice Customization Examples

### Robot Voice
```python
tts = AdvancedTTS(pitch=1.3, speed=0.8, volume=0.4)
tts.speak("I am a robot")
```

### Deep Voice
```python
tts = AdvancedTTS(pitch=0.6, speed=0.9, volume=0.6)
tts.speak("Deep voice mode")
```

### Fast Narrator
```python
tts = AdvancedTTS(pitch=1.0, speed=1.5, volume=0.7)
tts.speak("Speaking very quickly now")
```

### Chipmunk Voice
```python
tts = AdvancedTTS(pitch=1.8, speed=1.4, volume=0.5)
tts.speak("High pitched voice")
```

## Command Line Options

### espeak_tts.py

```bash
python3 espeak_tts.py [text] [options]

Options:
  --speed INT        Speech speed (80-450, default: 175)
  --pitch INT        Voice pitch (0-99, default: 50)
  --volume INT       Volume level (0-200, default: 100)
  --preset NAME      Voice preset (normal/fast/slow/robot/deep/high/whisper/excited/calm)
  --output FILE      Output WAV file path
  --no-play          Don't play audio, just save file
```

### advanced_tts.py

```bash
python3 advanced_tts.py [text] [options]

Options:
  --pitch FLOAT      Voice pitch (0.5-2.0, default: 1.0)
  --speed FLOAT      Speech speed (0.5-2.0, default: 1.0)
  --volume FLOAT     Volume level (0.0-1.0, default: 0.5)
  --output FILE      Output WAV file path
  --no-play          Don't play audio, just save file
```

### serial_voice_bridge.py

```bash
python3 serial_voice_bridge.py [options]

Options:
  --port PORT        Serial port (auto-detect if not specified)
  --baudrate RATE    Serial baud rate (default: 115200)
```

## Arduino Serial Protocol

The bridge listens for simple text commands from the MCU:

```
SPEAK:<text to synthesize>
```

And sends status responses:

```
STATUS:OK
STATUS:ERROR
```

Example Arduino code:

```cpp
Serial.println("SPEAK:Hello from microcontroller");
```

## Technical Details

### Audio Synthesis

The TTS engine uses **formant synthesis**, a technique that generates speech by:

1. **Text to Phonemes** - Converting text to basic phoneme units
2. **Formant Frequencies** - Each phoneme has characteristic frequency ranges
3. **Sine Wave Generation** - Creating audio using mathematical waveforms
4. **Envelope Shaping** - Smoothing transitions to reduce clicks
5. **Harmonics** - Adding overtones for richer sound
6. **WAV Encoding** - Outputting 16-bit PCM audio at 22.05 kHz

### Resource Usage

- **Memory**: ~10-20MB RAM during synthesis
- **CPU**: Moderate (synthesizes in near real-time)
- **Storage**: ~72KB for all scripts + 314MB for espeak-ng (optional)
- **Audio**: 22.05 kHz, 16-bit mono WAV files

### Limitations

**espeak-ng TTS (Professional):**
- ✅ Natural pronunciation
- ✅ Multiple languages supported
- ✅ Professional quality
- ✅ Voice presets and customization
- ⚠️ Requires 314MB storage

**Pure Python TTS (Advanced/Simple):**
- ✅ Zero dependencies
- ✅ Minimal storage (~10KB)
- ✅ Good for embedded systems
- ⚠️ Robotic/synthetic voice
- ⚠️ Limited pronunciation accuracy
- ⚠️ English only

Choose espeak-ng for professional applications, or pure Python for ultra-lightweight deployments.

## Troubleshooting

### No Audio Output

```bash
# Check audio devices
aplay -l

# Test audio with a simple tone
speaker-test -t sine -f 440 -l 1
```

### Serial Port Issues

```bash
# List available ports
python3 -c "import serial.tools.list_ports; print([p.device for p in serial.tools.list_ports.comports()])"

# Check permissions
ls -l /dev/ttyACM*
```

### Python Import Errors

Make sure you're running scripts from the project directory:

```bash
cd /home/arduino/voice_ai_project
python3 demo.py
```

## Examples

### Example 1: Simple Announcement System

```python
from espeak_tts import EspeakTTS
import time

tts = EspeakTTS(volume=120, speed=180)

announcements = [
    "System startup complete.",
    "All sensors operational.",
    "Ready for operation."
]

for msg in announcements:
    tts.speak(msg)
    time.sleep(1)
```

### Example 2: Sensor Reading Announcer

```python
from espeak_tts import EspeakTTS
import random

tts = EspeakTTS(volume=100)

# Simulate sensor reading
temperature = random.randint(20, 30)
humidity = random.randint(40, 60)

tts.speak(f"Temperature is {temperature} degrees.")
tts.speak(f"Humidity is {humidity} percent.")
```

### Example 3: Status Alert System

```python
from espeak_tts import EspeakTTS

def alert_status(level, message):
    if level == "error":
        tts = EspeakTTS(preset="deep", speed=160)
    elif level == "warning":
        tts = EspeakTTS(preset="normal", volume=120)
    else:
        tts = EspeakTTS(preset="excited", speed=200)
    
    tts.speak(message)

alert_status("error", "Critical error detected")
alert_status("warning", "Low battery warning")
alert_status("info", "Operation complete")
```

## Future Enhancements

Possible improvements if resources allow:

- [ ] Better phoneme-to-text mapping
- [ ] Multi-language support
- [ ] SSML markup support
- [ ] Integration with Piper TTS for neural voices
- [ ] Web interface for remote control
- [ ] Voice recording and playback
- [ ] Emotion/intonation control

## License

This project is open source and available for use with Arduino UNO Q.

## Credits

Developed for Arduino UNO Q  
Uses formant synthesis techniques (pure Python) and espeak-ng integration  
Multiple quality levels: professional, enhanced, and zero-dependency options

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review the examples
3. Run the demo.py to verify installation
4. Check Arduino forums for UNO Q specific issues

---

**Enjoy offline voice generation on your Arduino UNO Q!** 🎙️🤖
