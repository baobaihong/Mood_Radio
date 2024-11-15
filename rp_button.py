import recorder

# Mock Button class for development on non-Raspberry Pi systems
class MockButton:
    def __init__(self, pin):
        self.pin = pin
        self.is_pressed = False
        print(f"Mock Button initialized on pin {pin}")
    
    def wait_for_press(self):
        input("Press Enter to simulate button press...")
        self.is_pressed = True
        return True

    def wait_for_release(self):
        input("Press Enter to simulate button release...")
        self.is_pressed = False
        return True

try:
    from gpiozero import Button
except ImportError:
    print("Running in development mode with mock Button")
    Button = MockButton

def handle_button_recording():
    """
    Handle button press/release for recording.
    Returns: The recorded audio
    """
    button = Button(21)
    stream = None
    frames = None
    p = None

    button.wait_for_press()
    print("Recording started...")
    stream, frames, p = recorder.start_recording()
    if stream is None:
        print("Failed to start recording")
        return None
    
    button.wait_for_release()
    print("Recording stopped...")
    if stream is not None:
        audio = recorder.stop_recording(stream, frames, p)
        return audio
    
