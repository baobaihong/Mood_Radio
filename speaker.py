from pydub import AudioSegment
import simpleaudio as sa
import pyaudio
import wave
import io

def play_audio(audio_bytes):
    # # Convert the bytes to an AudioSegment
    # audio_segment = AudioSegment.from_file(io.BytesIO(audio_bytes), format="wav")

    # # Play the audio
    # play_obj = sa.play_buffer(
    #     audio_segment.raw_data,
    #     num_channels=audio_segment.channels,
    #     bytes_per_sample=audio_segment.sample_width,
    #     sample_rate=audio_segment.frame_rate
    # )

    # # Wait for playback to finish before exiting
    # play_obj.wait_done()
     # Create a BytesIO object from the audio bytes
    audio_io = io.BytesIO(audio_bytes)
    
    # Open the audio file
    with wave.open(audio_io, 'rb') as wf:
        # Instantiate PyAudio
        p = pyaudio.PyAudio()
        
        # Open a stream
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)
        
        # Read data in chunks
        chunk = 1024
        data = wf.readframes(chunk)
        
        # Play the audio
        while data:
            stream.write(data)
            data = wf.readframes(chunk)
        
        # Stop and close the stream
        stream.stop_stream()
        stream.close()
        
        # Terminate PyAudio
        p.terminate()