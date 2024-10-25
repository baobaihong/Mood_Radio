import pyaudio
import wave
import base64
import keyboard
import io

def record_audio():
    CHUNK = 4096
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100

    p = pyaudio.PyAudio()

    try:
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

        print("Press and hold the space key to start recording...")

        frames = []

        while True:
            if keyboard.is_pressed('space'):
                print("Recording...")
                while keyboard.is_pressed('space'):
                    try:
                        data = stream.read(CHUNK, exception_on_overflow=False)
                        frames.append(data)
                    except IOError as e:
                        print(f"Error recording: {e}")
                break

        print("Recording stopped.")

        stream.stop_stream()
        stream.close()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        p.terminate()

    # Use BytesIO to avoid writing to a file
    audio_buffer = io.BytesIO()
    wf = wave.open(audio_buffer, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    # Get the byte data from the buffer
    audio_buffer.seek(0)
    audio_bytes = audio_buffer.read()

    # Encode the byte data to a base64 string
    encoded_string = base64.b64encode(audio_bytes).decode('utf-8')

    return encoded_string

# print(record_audio())