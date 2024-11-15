import pyaudio
import wave
import base64
import io

def start_recording():
    """Initialize recording and return the stream and frames list"""
    CHUNK = 4096
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100

    p = pyaudio.PyAudio()
    frames = []

    def callback(in_data, frame_count, time_info, status):
        frames.append(in_data)
        return (in_data, pyaudio.paContinue)

    try:
        stream = p.open(format=FORMAT,
                       channels=CHANNELS,
                       rate=RATE,
                       input=True,
                       frames_per_buffer=CHUNK,
                       stream_callback=callback)
        
        stream.start_stream()
        return stream, frames, p
    except Exception as e:
        print(f"An error occurred: {e}")
        p.terminate()
        return None, None, None

def stop_recording(stream, frames, p):
    """Stop recording and return the encoded audio"""
    try:
        stream.stop_stream()
        stream.close()
    finally:
        p.terminate()

    # Use BytesIO to avoid writing to a file
    audio_buffer = io.BytesIO()
    wf = wave.open(audio_buffer, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wf.setframerate(44100)
    wf.writeframes(b''.join(frames))
    wf.close()

    # Get the byte data from the buffer
    audio_buffer.seek(0)
    audio_bytes = audio_buffer.read()

    # Encode the byte data to base64 string
    encoded_string = base64.b64encode(audio_bytes).decode('utf-8')

    return audio_bytes, encoded_string