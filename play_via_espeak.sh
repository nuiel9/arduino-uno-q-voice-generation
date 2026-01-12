#!/bin/bash
# Play WAV file using espeak's audio backend (works with Bluetooth)
# Usage: ./play_via_espeak.sh <wav_file>

WAV_FILE="$1"

if [ ! -f "$WAV_FILE" ]; then
    echo "Error: File $WAV_FILE not found"
    exit 1
fi

# Convert WAV to raw audio and pipe to espeak's audio output
# This uses espeak's working audio system
sox "$WAV_FILE" -t raw -r 22050 -e signed -b 16 -c 1 - | aplay -r 22050 -f S16_LE -c 1
