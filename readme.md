# AI Music Compositer 🎶

## Overview
The **AI Music Compositer** is a web application that allows users to generate custom musical compositions based on their input. Using advanced AI language models and music generation libraries, users can describe the music they want, select a musical style, and receive a MIDI file of their composition.

## Features
- Generate melodies, harmonies, and rhythms based on user input.
- Adapt compositions to various musical styles.
- Play and download the generated MIDI files.
- Chatbot-like interface for user interaction about music composition.

## Technologies Used
- **Python**: The primary programming language for the application.
- **Streamlit**: Framework for creating the web application.
- **LangGraph**: Used for handling the state machine workflow.
- **LangChain**: For integrating AI language models.
- **music21**: For music generation and MIDI file creation.
- **pygame**: For playing MIDI files.
- **dotenv**: For managing environment variables.

## Installation
To run this application, follow these steps:

1. **Clone this repository**:
   ```bash
   git clone https://github.com/maryamsafdar/AI-Music-Compositor
   cd AI_Music_Compositor

2. **Create a virtual environment**:
   ```bash
   python -m venv venv

3. **On Windows, activate the virtual environment**:
   ```bash
   venv\Scripts\activate

4. **Install the required packages**:
   ```bash
   pip install -r requirements.txt

5. **Set up your Groq API key in a .env file**:
   ```bash
   GROQ_API_KEY=your_api_key_here


6. **Run the Streamlit application**:
   ```bash
   streamlit run AI_Music_Compositor.py


