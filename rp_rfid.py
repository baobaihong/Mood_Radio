# Mock GPIO for development on non-Raspberry Pi systems
class MockGPIO:
    @staticmethod
    def cleanup():
        print("Mock GPIO cleanup")

class MockSimpleMFRC522:
    def read_id(self):
        import random
        return random.choice(["12345", "54321"])  # Randomly return one of the two IDs
    
    def write(self, text):
        print(f"Mock writing: {text}")

# Try to import the real GPIO and SimpleMFRC522
try:
    import RPi.GPIO as GPIO
    from mfrc522 import SimpleMFRC522
except ImportError:
    print("Running in development mode with mock GPIO")
    GPIO = MockGPIO
    SimpleMFRC522 = MockSimpleMFRC522

# Read RFID and return color string
def read_color():
    reader = SimpleMFRC522()
    ## Read functionality
    try:
        id = reader.read_id()
        if id == "12345":
            return "yellow"
        elif id == "54321":
            return "blue"
        else:
            return None
    ## Write functionality
    # try:
    #     text = input('New data:')
    #     print("Now place your tag to write")
    #     reader.write(text)
    #     print("Written")
    ## Common ending for read/write
    finally:
        GPIO.cleanup()