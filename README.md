# Interactive Radio Host System

A Raspberry Pi-based interactive radio host system that combines RFID color detection, speech recognition, and dynamic music playback to create an engaging audio experience.

## Features

- **RFID Color Detection**: Uses RFID cards to set different themes and personalities for the radio host
- **Dynamic Music Selection**: AI-powered DJ that selects appropriate background music based on context
- **Voice Interaction**: Records and processes user voice input
- **Text-to-Speech Output**: Converts AI responses to natural-sounding speech
- **Spotify Integration**: Automated music playback through Spotify
- **Development Mode**: Includes mock implementations for non-Raspberry Pi development

## Hardware Requirements

- Raspberry Pi
- RFID-RC522 module
- Push button
- Speaker/Audio output device
- Microphone

## Software Requirements

- Python 3.x
- Spotify Premium account
- OpenAI API key
- Required Python packages (see Installation)

## Installation

1. Clone the repository
2. Install required packages: 
    pip install spotipy openai python-dotenv pyaudio wave gpiozero mfrc522
3. Create a `.env` file with the following configurations:
    OPENAI_API_KEY=your_openai_api_key
    SPOTIFY_CLIENT_ID=your_spotify_client_id
    SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
    SPOTIFY_REDIRECT_URI=your_spotify_redirect_uri
    YELLOW_PROMPT=your_yellow_theme_prompt
    BLUE_PROMPT=your_blue_theme_prompt

## Usage

1. Run the main program:
    python main.py
2. Present an RFID card to set the theme (yellow or blue)
3. The system will:
   - Select appropriate background music
   - Generate an opening remark
   - Begin listening for user input

## Development Mode

The system includes mock implementations for GPIO, RFID, and button interfaces when running on non-Raspberry Pi systems. This allows for development and testing on regular computers.

## Project Structure

- `main.py`: Main application entry point
- `rp_rfid.py`: RFID handling and color detection
- `dj.py`: Music selection and playback control
- `host.py`: AI host interaction and speech generation
- `recorder.py`: Audio recording functionality
- `speaker.py`: Audio playback functionality
- `openai_client.py`: OpenAI API client configuration

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- OpenAI for GPT and text-to-speech capabilities
- Spotify for music playback integration
- The Raspberry Pi community for GPIO and RFID libraries