# 🎶 AI Music Compositor
AI Music Compositor is an interactive, Streamlit-based application that uses the power of LLMs and the music21 library to generate original music compositions based on user input. Whether you're inspired by classical, jazz, pop, or romantic styles, this tool lets you compose melodies, harmonies, and rhythms—and even convert them into playable and downloadable MIDI files.

# 🚀 Features
✍️ Natural Language Music Input – Describe your desired musical feel, and AI will take care of the rest.

🎼 Melody, Harmony, and Rhythm Generation using LLM (LLaMA-3 via Groq).

🎹 Stylistic Adaptation – Choose from Classical, Romantic, Jazz, or Pop styles.

🎵 Auto MIDI Conversion – Convert compositions into real MIDI files for download or playback.

🖥️ Streamlit Web App – Easy-to-use interface with live interaction.

🧠 Graph-based Workflow – Built with LangGraph to model sequential steps in music generation.

# 🧰 Built With
Python

music21

Streamlit

LangGraph

LangChain

ChatGroq (LLaMA-3)

pygame (for local MIDI playback)

# ⚙️ How It Works
Enter a musical description (e.g., "A calm piano tune in minor scale").

Choose a style from the sidebar (Classical, Romantic, Jazz, Pop).

The system:

Generates a melody

Creates harmony

Suggests rhythm

Adapts to your chosen style

Converts everything into a MIDI file

🎧 Play, 🔽 Download, or 🎼 Share your AI-generated music!

# 🖥️ Getting Started
Requirements
bash
Copy
Edit
pip install streamlit music21 pygame langgraph langchain langchain_groq python-dotenv
Run the app
bash
Copy
Edit
streamlit run AI_Music_Compositor.py
# 📁 Environment Variables
You’ll need a .env file with your Groq API key like so:

ini
Copy
Edit
GROQ_API_KEY=your_api_key_here
# 📦 Output
MIDI file saved temporarily and available for download or playback.

Display of your input and selected style for transparency.

# 📌 To-Do / Future Ideas
Add support for saving and sharing compositions

Export to sheet music (PDF)

Advanced instrument selection

User profiles with saved history

# 🧠 AI Model Info
Uses LLaMA 3.1 - 70B (via Groq) with temperature control for deterministic output.
