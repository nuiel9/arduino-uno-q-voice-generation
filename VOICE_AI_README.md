# Offline Voice AI Assistant for Arduino UNO Q

A complete offline generative AI system with voice responses, running entirely on Arduino UNO Q without internet connection.

## 🎯 Features

- ✅ **Fully Offline** - No internet required
- 🧠 **Conversational AI** - Pattern matching + context awareness
- 🔊 **Voice Responses** - Professional TTS using espeak-ng
- 🎭 **Multiple Voice Presets** - Robot, excited, calm, and more
- 💬 **Natural Conversations** - Remembers your name and context
- 🔢 **Basic Calculations** - Math operations built-in
- 😄 **Jokes & Fun** - Entertainment capabilities
- 📊 **Conversation History** - Track and save conversations
- 🎮 **Interactive & Batch Modes** - Flexible usage
- 💾 **Lightweight** - Optimized for 2GB RAM systems

## 📦 System Components

### 1. offline_ai_brain.py (15KB)
Lightweight AI engine with:
- Pattern-based response matching
- Conversation history management
- Context awareness
- Knowledge base system
- Name learning and personalization

### 2. voice_ai_assistant.py (9KB)
Main voice assistant interface:
- Integrates AI brain with TTS
- Interactive chat mode
- Batch processing mode
- Voice control (mute/unmute)
- Conversation statistics

### 3. espeak_tts.py (Existing)
Professional TTS engine for voice output

## 🚀 Quick Start

### Basic Usage

```bash
# Start interactive voice AI
python3 voice_ai_assistant.py

# Use robot voice
python3 voice_ai_assistant.py --preset robot

# Text-only mode (no voice)
python3 voice_ai_assistant.py --no-voice

# Batch mode
python3 voice_ai_assistant.py --batch "Hello" "What time is it?" "Goodbye"
```

### Interactive Commands

Once in interactive mode, you can use:
- `mute` - Disable voice output
- `unmute` - Enable voice output
- `stats` - Show conversation statistics
- `save` - Save conversation to JSON file
- `clear` - Clear conversation history
- `quit` or `exit` - End session

## 💡 Usage Examples

### Example 1: Basic Conversation

```bash
$ python3 voice_ai_assistant.py

You: hello
AI: Hi there! What would you like to know?

You: my name is John
AI: Nice to meet you, John! I'll remember your name.

You: what can you do?
AI: I can chat with you, answer questions, tell jokes, do math, 
    and provide information about various topics. Try asking me something!

You: 15 + 27
AI: The answer is 42.0.

You: thank you
AI: You're welcome!
```

### Example 2: Different Voice Presets

```bash
# Normal voice
python3 voice_ai_assistant.py --preset normal

# Robot voice (deep, mechanical)
python3 voice_ai_assistant.py --preset robot

# Excited voice (fast, high pitch)
python3 voice_ai_assistant.py --preset excited

# Calm voice (slow, soothing)
python3 voice_ai_assistant.py --preset calm

# Whisper voice (quiet)
python3 voice_ai_assistant.py --preset whisper
```

### Example 3: Custom Voice Settings

```bash
# Custom speed, pitch, and volume
python3 voice_ai_assistant.py --speed 200 --pitch 60 --volume 120

# Fast robot voice
python3 voice_ai_assistant.py --preset robot --speed 250
```

### Example 4: Batch Processing

```bash
# Process multiple questions at once
python3 voice_ai_assistant.py --batch \
  "What time is it?" \
  "Tell me a joke" \
  "What is 100 minus 37?" \
  "Thank you"
```

### Example 5: Save Conversation

```bash
# Save audio files and conversation history
python3 voice_ai_assistant.py --save-audio

# In interactive mode:
You: save
AI: Conversation saved to /tmp/conversation_12.json
```

## 🎭 Voice Presets

| Preset | Speed | Pitch | Volume | Description |
|--------|-------|-------|--------|-------------|
| normal | 175 | 50 | 100 | Default balanced voice |
| fast | 250 | 50 | 100 | Quick speaking |
| slow | 120 | 50 | 100 | Deliberate speaking |
| robot | 150 | 30 | 90 | Mechanical, robotic |
| deep | 160 | 20 | 110 | Deep, authoritative |
| high | 180 | 80 | 100 | High-pitched, cheerful |
| whisper | 140 | 40 | 60 | Quiet, soft |
| excited | 220 | 70 | 120 | Energetic, enthusiastic |
| calm | 150 | 45 | 85 | Soothing, relaxed |

## 🧠 AI Capabilities

### Supported Topics & Commands

**Greetings**
- "hello", "hi", "hey"
- Response: Friendly greeting

**Time & Date**
- "what time is it?"
- "what's the date?"
- Response: Current time/date

**System Information**
- "what are your specs?"
- "tell me about arduino"
- Response: Hardware information

**Mathematics**
- "5 + 3", "100 - 37", "12 * 8", "144 / 12"
- Response: Calculated result

**Jokes**
- "tell me a joke"
- Response: Random tech/programming joke

**Personal**
- "my name is [Name]"
- Response: Remembers and uses your name

**Help**
- "what can you do?"
- "help"
- Response: Capability list

**Topics**
- Arduino, Python, AI, Linux, Robotics, Programming
- Response: Information about the topic

## 📊 API Usage (Python)

### Using AI Brain Directly

```python
from offline_ai_brain import OfflineAI

# Create AI instance
ai = OfflineAI()

# Process text
response = ai.process("Hello!")
print(response)

# Get conversation stats
stats = ai.get_stats()
print(f"Messages: {stats['total_messages']}")

# Save conversation
ai.save_conversation("chat.json")
```

### Using Voice AI

```python
from voice_ai_assistant import VoiceAI

# Create voice AI
assistant = VoiceAI(
    voice_preset='robot',
    speed=180,
    pitch=50,
    voice_enabled=True
)

# Chat with voice response
response = assistant.chat("Hello, robot!")

# Chat without voice
response = assistant.chat("Silent message", speak=False)
```

### Batch Processing

```python
from voice_ai_assistant import VoiceAI

assistant = VoiceAI()

questions = [
    "What time is it?",
    "Tell me about Arduino",
    "What is 7 times 8?"
]

assistant.batch_mode(questions)
```

## 🔧 Command-Line Options

```
usage: voice_ai_assistant.py [-h] [--preset {normal,fast,slow,robot,deep,high,whisper,excited,calm}]
                              [--speed SPEED] [--pitch PITCH] [--volume VOLUME]
                              [--no-voice] [--save-audio] [--batch BATCH [BATCH ...]]

Options:
  -h, --help            Show help message
  --preset, -p          Voice preset (default: normal)
  --speed, -s           Speech speed 80-450 (default: 175)
  --pitch               Voice pitch 0-99 (default: 50)
  --volume, -v          Volume level 0-200 (default: 100)
  --no-voice            Text-only mode (disable voice)
  --save-audio          Save audio files to /tmp
  --batch, -b           Batch mode: process multiple questions
```

## 💻 System Requirements

- **Hardware:** Arduino UNO Q (or similar 2GB RAM system)
- **OS:** Debian Linux (or any Linux with apt)
- **Python:** 3.7+ (tested on 3.13.5)
- **Dependencies:**
  - espeak-ng (for voice synthesis)
  - aplay (for audio playback)
  - Standard Python libraries only

## 📥 Installation

### 1. Install System Dependencies

```bash
sudo apt-get update
sudo apt-get install -y espeak-ng espeak-ng-data
```

### 2. Make Scripts Executable

```bash
chmod +x offline_ai_brain.py voice_ai_assistant.py
```

### 3. Test Installation

```bash
# Test AI brain only
python3 offline_ai_brain.py

# Test voice AI
python3 voice_ai_assistant.py --batch "Hello" "Goodbye"
```

## 🎯 Use Cases

### 1. Voice Assistant for Robotics
Use the voice AI to make your robot talk and respond to commands.

```python
# Robot control example
assistant = VoiceAI(voice_preset='robot')
response = assistant.chat("Initializing robot systems")
```

### 2. Educational Tool
Teach kids about AI and voice synthesis.

```bash
python3 voice_ai_assistant.py --preset excited
# Ask: "What is programming?"
```

### 3. Accessibility Aid
Provide voice feedback for IoT projects.

```python
assistant = VoiceAI(voice_preset='calm')
assistant.chat("Temperature is 25 degrees")
```

### 4. Smart Home Notifications
Voice announcements for events.

```bash
python3 voice_ai_assistant.py --batch \
  "Motion detected at front door" \
  "Security system armed"
```

## 🔍 Technical Details

### Memory Usage
- AI Brain: ~5-10MB RAM
- TTS Engine: ~5-10MB RAM
- Total: ~15-20MB RAM
- Storage: ~25KB (scripts only)

### Performance
- Response time: <100ms (AI processing)
- Voice synthesis: ~500ms per sentence
- Concurrent operations: Supported

### Architecture

```
┌─────────────────────────────────┐
│   Voice AI Assistant            │
│   (voice_ai_assistant.py)       │
└────────────┬────────────────────┘
             │
     ┌───────┴───────┐
     │               │
┌────▼─────┐   ┌────▼──────┐
│ AI Brain │   │ TTS Engine│
│ (offline)│   │ (espeak)  │
└──────────┘   └───────────┘
     │               │
     └───────┬───────┘
             │
     ┌───────▼────────┐
     │ Audio Output   │
     │ (speakers)     │
     └────────────────┘
```

## 🐛 Troubleshooting

### Issue: "espeak-ng not found"
**Solution:** Install espeak-ng
```bash
sudo apt-get install espeak-ng espeak-ng-data
```

### Issue: No audio output
**Solution:** Check audio device
```bash
aplay -l  # List audio devices
speaker-test -t wav -c 2  # Test speakers
```

### Issue: "Permission denied"
**Solution:** Make scripts executable
```bash
chmod +x *.py
```

### Issue: Slow response
**Solution:** Reduce conversation history
```python
# In interactive mode, type:
clear
```

## 📈 Future Enhancements

### Planned Features
- [ ] Speech-to-text (voice input)
- [ ] Better context understanding
- [ ] Plugin system for custom commands
- [ ] Web interface for remote control
- [ ] Multi-language AI responses
- [ ] Emotion detection in responses
- [ ] Integration with Arduino sensors
- [ ] Custom knowledge base loading

### Potential Integrations
- [ ] Home Assistant integration
- [ ] MQTT support for IoT
- [ ] RESTful API server
- [ ] WebSocket real-time chat
- [ ] Serial command protocol expansion

## 🤝 Contributing

This is an open educational project. Feel free to:
- Add new response patterns
- Create new voice presets
- Expand the knowledge base
- Improve the AI logic
- Add new features

## 📝 Example Conversations

### Conversation 1: Getting Started
```
You: hello
AI: Hi there! What would you like to know?

You: who are you
AI: I'm an offline AI assistant running on Arduino UNO Q. 
    I can answer questions and have conversations without internet.

You: impressive
AI: Thank you! What else can I help you with?
```

### Conversation 2: Math & Practical Use
```
You: what time is it
AI: The current time is 02:45 PM.

You: calculate 234 + 567
AI: The answer is 801.0.

You: thank you
AI: Happy to help!
```

### Conversation 3: Fun & Personality
```
You: tell me a joke
AI: Why do programmers prefer dark mode? 
    Because light attracts bugs!

You: haha that's funny
AI: Great! What else can I help you with?

You: you're awesome
AI: Thank you! What else would you like to know?
```

## 📄 License

Educational project for Arduino UNO Q platform.
Free to use, modify, and share.

## 🙏 Acknowledgments

- espeak-ng team for excellent TTS engine
- Arduino UNO Q for powerful hybrid hardware
- Warp AI for development assistance

---

**Built with ❤️ for Arduino UNO Q**  
*Offline AI • Voice Synthesis • Educational Tool*

Last Updated: January 12, 2026
