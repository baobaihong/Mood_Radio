import os
import sys
import pyaudio
import wave
import io

def play_audio(audio_bytes):
    # Redirect stderr temporarily to suppress ALSA errors
    stderr = sys.stderr
    sys.stderr = open(os.devnull, 'w')
    
    try:
        p = pyaudio.PyAudio()
        
        # Find the right audio device
        default_device_index = None
        for i in range(p.get_device_count()):
            device_info = p.get_device_info_by_index(i)
            if device_info['maxOutputChannels'] > 0:
                default_device_index = i
                break
        
        if default_device_index is None:
            print("No output device found")
            return

        audio_io = io.BytesIO(audio_bytes)
        with wave.open(audio_io, 'rb') as wf:
            stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                          channels=wf.getnchannels(),
                          rate=wf.getframerate(),
                          output=True,
                          output_device_index=default_device_index)
            
            chunk = 1024
            data = wf.readframes(chunk)
            
            while data:
                stream.write(data)
                data = wf.readframes(chunk)
            
            stream.stop_stream()
            stream.close()
    finally:
        p.terminate()
        # Restore stderr
        sys.stderr = stderr