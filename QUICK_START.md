# Quick Start Guide - Arduino UNO Q Voice Generation

## 🚀 30-Second Test

```bash
cd /home/arduino/voice_ai_project
python3 simple_tts.py "Hello Arduino"
```

You should hear "Hello Arduino" spoken through your audio device!

## 📝 Common Use Cases

### 1. Speak Any Text
```bash
python3 advanced_tts.py "Your text here"
```

### 2. Interactive Mode
```bash
python3 demo.py
# Then select option 4 for interactive mode
```

### 3. Custom Voice Settings

**Robot Voice:**
```bash
python3 advanced_tts.py "I am a robot" --pitch 1.3 --speed 0.8
```

**Deep Voice:**
```bash
python3 advanced_tts.py "Deep voice mode" --pitch 0.6 --speed 0.9
```

**Fast Speech:**
```bash
python3 advanced_tts.py "Speaking quickly" --speed 1.8
```

### 4. Save Audio to File
```bash
python3 advanced_tts.py "Save this" --output ~/my_voice.wav --no-play
```

### 5. Use in Python Scripts

Create a file `my_script.py`:

```python
#!/usr/bin/env python3
from advanced_tts import AdvancedTTS

tts = AdvancedTTS(volume=0.7, speed=1.1)
tts.speak("System ready")
tts.speak("All sensors operational")
```

Run it:
```bash
python3 my_script.py
```

## 🎮 Run the Interactive Demo

```bash
python3 demo.py
```

Try each demo option to explore all features!

## 🤖 Arduino Integration

### For STM32 MCU Side:
1. Open `arduino_voice_trigger.ino` in Arduino IDE/App Lab
2. Upload to STM32U585
3. Connect button to pin 2 (optional)

### For Linux MPU Side:
```bash
python3 serial_voice_bridge.py
```

Press the button on your Arduino, and it will speak!

## 💡 Tips

- **Volume too low?** Increase `--volume` to 0.8 or 0.9
- **Speaking too fast?** Decrease `--speed` to 0.7 or 0.8
- **Voice too high/low?** Adjust `--pitch` between 0.5 and 2.0
- **Want better quality?** Try installing espeak-ng with sudo access

## 📁 Project Files

- `simple_tts.py` - Basic engine (good for testing)
- `advanced_tts.py` - Full-featured engine (recommended)
- `demo.py` - Interactive demo
- `serial_voice_bridge.py` - Arduino communication
- `README.md` - Complete documentation

## ❓ Troubleshooting

**No sound?**
```bash
aplay -l  # Check if audio device is detected
```

**Import errors?**
```bash
cd /home/arduino/voice_ai_project  # Make sure you're in the right directory
```

**Slow performance?**
- Try `simple_tts.py` instead of `advanced_tts.py`
- Reduce sample rate (edit the code to use 16000 instead of 22050)

## 🎯 Quick Examples

**Announce sensor data:**
```python
from advanced_tts import AdvancedTTS
tts = AdvancedTTS()
temperature = 25
tts.speak(f"Temperature is {temperature} degrees")
```

**Status notifications:**
```python
from advanced_tts import AdvancedTTS

def notify(message):
    tts = AdvancedTTS(volume=0.7, speed=1.2)
    tts.speak(message)

notify("Process complete")
notify("Error detected")
```

**Time announcements:**
```python
from advanced_tts import AdvancedTTS
from datetime import datetime

tts = AdvancedTTS()
now = datetime.now()
tts.speak(f"The time is {now.hour} {now.minute}")
```

---

**That's it! You now have offline voice generation on your Arduino UNO Q!** 🎉
