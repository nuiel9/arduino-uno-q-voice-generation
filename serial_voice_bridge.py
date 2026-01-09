#!/usr/bin/env python3
"""
Serial Voice Bridge for Arduino UNO Q

Listens for commands from the STM32 MCU via serial and triggers
voice generation on the Linux MPU side.
"""

import serial
import serial.tools.list_ports
import sys
import time
from advanced_tts import AdvancedTTS

class SerialVoiceBridge:
    def __init__(self, port=None, baudrate=115200):
        self.baudrate = baudrate
        self.ser = None
        self.tts = AdvancedTTS(volume=0.6, speed=1.2)
        
        # Auto-detect Arduino port if not specified
        if port is None:
            port = self.find_arduino_port()
        
        self.port = port
        
    def find_arduino_port(self):
        """Auto-detect Arduino serial port"""
        ports = serial.tools.list_ports.comports()
        
        # Look for common Arduino identifiers
        for port in ports:
            if 'Arduino' in port.description or 'STM32' in port.description:
                return port.device
            if 'ttyACM' in port.device or 'ttyUSB' in port.device:
                return port.device
        
        # Default fallback
        if ports:
            return ports[0].device
        
        return None
    
    def connect(self):
        """Connect to Arduino via serial"""
        if self.port is None:
            print("Error: No serial port found")
            print("Available ports:")
            for port in serial.tools.list_ports.comports():
                print(f"  {port.device}: {port.description}")
            return False
        
        try:
            self.ser = serial.Serial(self.port, self.baudrate, timeout=1)
            time.sleep(2)  # Wait for Arduino to reset
            print(f"Connected to Arduino on {self.port}")
            self.send_status("OK")
            return True
        except serial.SerialException as e:
            print(f"Error connecting to {self.port}: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from serial port"""
        if self.ser and self.ser.is_open:
            self.ser.close()
            print("Disconnected from Arduino")
    
    def send_status(self, status):
        """Send status message to Arduino"""
        if self.ser and self.ser.is_open:
            message = f"STATUS:{status}\n"
            self.ser.write(message.encode())
    
    def process_command(self, command):
        """Process command from Arduino"""
        if command.startswith("SPEAK:"):
            text = command[6:].strip()
            if text:
                print(f"Speaking: {text}")
                try:
                    self.tts.speak(text, play=True)
                    self.send_status("OK")
                except Exception as e:
                    print(f"Error synthesizing speech: {e}")
                    self.send_status("ERROR")
        else:
            print(f"Unknown command: {command}")
    
    def run(self):
        """Main loop - listen for commands"""
        if not self.connect():
            return
        
        print("Listening for commands from Arduino...")
        print("Press Ctrl+C to exit")
        
        try:
            while True:
                if self.ser.in_waiting > 0:
                    line = self.ser.readline().decode('utf-8', errors='ignore').strip()
                    if line:
                        print(f"Received: {line}")
                        self.process_command(line)
                
                time.sleep(0.01)
                
        except KeyboardInterrupt:
            print("\nShutting down...")
        finally:
            self.disconnect()


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Serial Voice Bridge for Arduino UNO Q'
    )
    parser.add_argument('--port', type=str, default=None,
                       help='Serial port (auto-detect if not specified)')
    parser.add_argument('--baudrate', type=int, default=115200,
                       help='Serial baud rate (default: 115200)')
    
    args = parser.parse_args()
    
    bridge = SerialVoiceBridge(port=args.port, baudrate=args.baudrate)
    bridge.run()


if __name__ == "__main__":
    main()
