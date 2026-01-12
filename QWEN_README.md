# Qwen LLM Integration - Real Offline Generative AI

Successfully integrated **Qwen2-0.5B** LLM into the voice AI assistant for true generative AI responses!

## 🎉 What's New

- ✅ **Real LLM** - Qwen2-0.5B running locally via Ollama
- ✅ **Fully Offline** - No internet required after model download
- ✅ **Voice Enabled** - Speaks responses using espeak-ng
- ✅ **Resource Efficient** - Runs in ~478MB RAM
- ✅ **Hybrid Mode** - Choose between Qwen LLM or pattern-based AI
- ✅ **Context Aware** - Maintains conversation history

## 📦 System Components

### New Files
1. **qwen_ai_brain.py** (10KB) - Qwen2 wrapper using Ollama API
2. **voice_ai_assistant.py** (updated) - Now supports `--qwen` flag

### Infrastructure
- **Ollama** - Lightweight LLM runtime (installed)
- **Qwen2-0.5B** - 352MB quantized model (downloaded)
- **System:** Cleaned up 2.6GB of unnecessary CUDA libraries

## 🚀 Quick Start

### Using Qwen LLM

```bash
# Interactive mode with Qwen
python3 voice_ai_assistant.py --qwen

# With robot voice
python3 voice_ai_assistant.py --qwen --preset robot

# Batch mode
python3 voice_ai_assistant.py --qwen --batch "What is AI?" "Tell me about robotics"

# Text-only (no voice)
python3 voice_ai_assistant.py --qwen --no-voice
```

### Using Pattern-Based AI (Default)

```bash
# Same commands without --qwen flag
python3 voice_ai_assistant.py
python3 voice_ai_assistant.py --preset excited
```

### Direct Qwen Test

```bash
# Test Qwen brain directly
python3 qwen_ai_brain.py

# Or use ollama CLI
ollama run qwen2:0.5b
```

## 💡 Usage Examples

### Example 1: Qwen Conversation

```bash
$ python3 voice_ai_assistant.py --qwen

You: What is Arduino?
AI: Arduino is a microcontroller system that allows you to control 
    electronic devices such as computers, smartphones, and robots.

You: How can I use it for robotics?
AI: You can use Arduino to control motors, sensors, and actuators to 
    build autonomous robots. It's great for beginners and hobbyists.
```

### Example 2: Comparison

```bash
# Pattern-based (fast, specific)
$ python3 voice_ai_assistant.py --batch "5 times 8"
AI: 5.0 times 8.0 equals 40.0.

# Qwen LLM (slower, more conversational)
$ python3 voice_ai_assistant.py --qwen --batch "5 times 8"
AI: The result of 5 times 8 is 40.
```

### Example 3: Robot Voice with Qwen

```bash
$ python3 voice_ai_assistant.py --qwen --preset robot

You: Initialize systems
AI: System initialization complete. All subsystems are operational. 
    How may I assist you today?
```

## 🎭 Qwen vs Pattern-Based

| Feature | Pattern-Based | Qwen LLM |
|---------|--------------|----------|
| Speed | ⚡ Instant (<100ms) | 🐢 2-10 seconds |
| RAM Usage | 💾 ~20MB | 💾 ~478MB |
| Responses | 🎯 Predictable | 🎲 Creative |
| Knowledge | 📚 Limited topics | 🌍 General knowledge |
| Math | ✅ Precise | ⚠️ Approximate |
| Conversation | 🔄 Context-aware | 🧠 Fully contextual |
| Best For | Quick queries | Complex discussions |

## 🔧 Technical Details

### Resource Usage

**With Qwen Running:**
- Ollama serve: 97MB
- Qwen runner: 478MB
- **Total:** ~575MB
- **Available RAM:** 375MB (out of 1.7GB)

**Pattern-Based:**
- AI brain: ~20MB
- **Available RAM:** 750MB

### Model Information

- **Model:** Qwen2-0.5B
- **Quantization:** Q4_0 (4-bit)
- **Size:** 352MB
- **Parameters:** 500 million
- **Context:** 32K tokens
- **Speed:** ~8-16 tokens/second
- **Location:** `~/.ollama/models/`

### Performance

```
Load time: ~7.7 seconds (first query)
Generation: ~10 seconds per response
Tokens/sec: 8-16 (varies by complexity)
```

## 🛠️ Installation (Already Done)

For reference, here's what was installed:

```bash
# 1. Clean up space (removed 2.6GB CUDA libs)
sudo rm -rf /usr/local/lib/ollama/cuda_v*

# 2. Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# 3. Start Ollama server
ollama serve &

# 4. Download Qwen2-0.5B
ollama pull qwen2:0.5b
```

## 📊 Disk Space

```
Before cleanup: 100% full (0 bytes free)
After cleanup:  77% used (2.2GB free)

Ollama install: ~50MB
Qwen model:     352MB
Total added:    ~400MB
```

## 🎯 Use Cases

### When to Use Qwen LLM
- Complex questions requiring reasoning
- Creative writing or brainstorming
- Explaining concepts in detail
- Open-ended conversations
- Learning and education

### When to Use Pattern-Based
- Quick math calculations
- Time/date queries
- Simple Q&A
- Fast response needed
- Low resource usage required

## 💻 API Usage

### Python - Qwen Brain

```python
from qwen_ai_brain import QwenAI

# Create Qwen instance
ai = QwenAI(
    model="qwen2:0.5b",
    temperature=0.7,      # 0.0-1.0 (creativity)
    max_tokens=150        # Response length
)

# Generate response
response = ai.process("Explain quantum computing")
print(response)

# With history disabled (faster)
response = ai.process("What is 2+2?", use_history=False)
```

### Python - Voice AI with Qwen

```python
from voice_ai_assistant import VoiceAI

# Create with Qwen
assistant = VoiceAI(
    use_qwen=True,
    voice_preset='normal',
    voice_enabled=True
)

# Chat with voice
response = assistant.chat("Tell me about Arduino")
# AI speaks the response

# Get stats
stats = assistant.ai.get_stats()
print(f"Model: {stats['model']}")
print(f"Messages: {stats['total_messages']}")
```

## 🔍 Troubleshooting

### Issue: "Ollama server not responding"
**Solution:**
```bash
# Start Ollama server
ollama serve > /tmp/ollama.log 2>&1 &

# Or add to startup
```

### Issue: Slow responses
**Solution:**
- Reduce max_tokens (default: 150)
- Disable conversation history for one-off queries
- Use pattern-based AI for quick responses

### Issue: Out of memory
**Solution:**
```bash
# Check RAM
free -h

# Stop Ollama when not in use
pkill ollama

# Use pattern-based mode
python3 voice_ai_assistant.py  # without --qwen
```

### Issue: Model not found
**Solution:**
```bash
# List installed models
ollama list

# Re-download if needed
ollama pull qwen2:0.5b
```

## 🚀 Advanced Usage

### Custom Qwen Settings

```bash
# Start with custom temperature (more random)
python3 -c "
from qwen_ai_brain import QwenAI
ai = QwenAI(temperature=0.9, max_tokens=200)
print(ai.process('Tell me a creative story'))
"
```

### Monitor Resource Usage

```bash
# Watch RAM usage
watch -n 1 'ps aux | grep ollama | grep -v grep'

# Check model info
ollama show qwen2:0.5b
```

### Manage Ollama

```bash
# List models
ollama list

# Remove model (free 352MB)
ollama rm qwen2:0.5b

# Stop server
pkill ollama

# View logs
tail -f /tmp/ollama.log
```

## 📈 Future Enhancements

- [ ] Streaming responses for real-time voice
- [ ] Fine-tune Qwen on Arduino-specific knowledge
- [ ] Hybrid mode (Qwen for complex, pattern for simple)
- [ ] GPU acceleration (if available)
- [ ] Larger models (Qwen2-1.5B, 7B)
- [ ] Multi-modal support (vision + voice)
- [ ] Voice-to-text input (complete voice loop)

## 🎉 Success Metrics

✅ **Qwen2-0.5B integrated and working**
✅ **Runs in available RAM (478MB)**
✅ **Voice synthesis working with LLM**
✅ **Hybrid mode (Qwen + Pattern-based)**
✅ **2.6GB disk space freed**
✅ **All tests passing**
✅ **Documentation complete**

## 🔗 Comparison Table

| Aspect | Before | After |
|--------|--------|-------|
| AI Type | Pattern matching | Real LLM |
| Model | Rule-based | Qwen2-0.5B |
| Response Quality | Scripted | Generative |
| Knowledge | Limited topics | General knowledge |
| Creativity | None | High |
| RAM Usage | 20MB | 478MB |
| Disk Usage | 25KB | 352MB |
| Speed | <0.1s | 2-10s |

## 📝 Commands Summary

```bash
# Qwen with voice
python3 voice_ai_assistant.py --qwen

# Qwen robot voice
python3 voice_ai_assistant.py --qwen --preset robot

# Pattern-based (default)
python3 voice_ai_assistant.py

# Test Qwen directly
python3 qwen_ai_brain.py

# Ollama CLI
ollama run qwen2:0.5b

# Check status
ollama list
ps aux | grep ollama
free -h
```

## 🙏 Acknowledgments

- **Alibaba Cloud** - Qwen2 model
- **Ollama** - Lightweight LLM runtime
- **Arduino UNO Q** - Powerful hybrid hardware
- **Community** - Open source AI tools

---

**Status:** ✅ **COMPLETE AND WORKING**

*Real offline generative AI with voice on Arduino UNO Q!*

Last Updated: January 12, 2026
