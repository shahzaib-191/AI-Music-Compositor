# Import required libraries
from typing import Dict, TypedDict
from langgraph.graph import StateGraph, END
from langchain.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
import music21
import pygame
import tempfile
import os
import random
from dotenv import load_dotenv
import streamlit as st

# Load environment variables
load_dotenv()
api_key: str = os.getenv('GROQ_API_KEY')

llm = ChatGroq( model="llama-3.1-70b-versatile", temperature=0,api_key=api_key)
# State Definition
class MusicState(TypedDict):
    """Define the structure of the state for the music generation workflow."""
    musician_input: str  # User's input describing the desired music
    melody: str          # Generated melody
    harmony: str         # Generated harmony
    rhythm: str          # Generated rhythm
    style: str           # Desired musical style
    composition: str     # Complete musical composition
    midi_file: str       # Path to the generated MIDI file

# Initialize the Language Model (LLM) for generating musical components
# llm = ChatGroq(
#     model="llama-3.1-70b-versatile",
#     temperature=0.0,
# )

# Component Functions
def melody_generator(state: MusicState) -> Dict:
    """Generate a melody based on the user's input."""
    prompt = ChatPromptTemplate.from_template(
        "Generate a melody based on this input: {input}. Represent it as a string of notes in music21 format."
    )
    chain = prompt | llm
    melody = chain.invoke({"input": state["musician_input"]})
    return {"melody": melody.content}

def harmony_creator(state: MusicState) -> Dict:
    """Create harmony for the generated melody."""
    prompt = ChatPromptTemplate.from_template(
        "Create harmony for this melody: {melody}. Represent it as a string of chords in music21 format."
    )
    chain = prompt | llm
    harmony = chain.invoke({"melody": state["melody"]})
    return {"harmony": harmony.content}

def rhythm_analyzer(state: MusicState) -> Dict:
    """Analyze and suggest a rhythm for the melody and harmony."""
    prompt = ChatPromptTemplate.from_template(
        "Analyze and suggest a rhythm for this melody and harmony: {melody}, {harmony}. Represent it as a string of durations in music21 format."
    )
    chain = prompt | llm
    rhythm = chain.invoke({"melody": state["melody"], "harmony": state["harmony"]})
    return {"rhythm": rhythm.content}

def style_adapter(state: MusicState) -> Dict:
    """Adapt the composition to the specified musical style."""
    prompt = ChatPromptTemplate.from_template(
        "Adapt this composition to the {style} style: Melody: {melody}, Harmony: {harmony}, Rhythm: {rhythm}. Provide the result in music21 format."
    )
    chain = prompt | llm
    adapted = chain.invoke({
        "style": state["style"],
        "melody": state["melody"],
        "harmony": state["harmony"],
        "rhythm": state["rhythm"]
    })
    return {"composition": adapted.content}

def midi_converter(state: MusicState) -> Dict:
    """Convert the composition to MIDI format and save it as a file."""
    piece = music21.stream.Score()

    # Define a wide variety of scales and chords
    scales = {
        'C major': ['C', 'D', 'E', 'F', 'G', 'A', 'B'],
        'C minor': ['C', 'D', 'Eb', 'F', 'G', 'Ab', 'Bb'],
    }

    chords = {
        'C major': ['C4', 'E4', 'G4'],
        'C minor': ['C4', 'Eb4', 'G4'],
    }

    def create_melody(scale_name, duration):
        """Create a melody based on a given scale."""
        melody = music21.stream.Part()
        scale = scales[scale_name]
        for _ in range(duration):
            note = music21.note.Note(random.choice(scale) + '4')
            note.quarterLength = 1
            melody.append(note)
        return melody

    def create_chord_progression(duration):
        """Create a chord progression."""
        harmony = music21.stream.Part()
        for _ in range(duration):
            chord_name = random.choice(list(chords.keys()))
            chord = music21.chord.Chord(chords[chord_name])
            chord.quarterLength = 1
            harmony.append(chord)
        return harmony

    # Parse the user input to determine scale and style
    user_input = state['musician_input'].lower()
    scale_name = 'C major' if 'major' in user_input else 'C minor'

    # Create a 7-second piece (7 beats at 60 BPM)
    melody = create_melody(scale_name, 7)
    harmony = create_chord_progression(7)

    # Add the melody and harmony to the piece
    piece.append(melody)
    piece.append(harmony)

    # Set the tempo to 60 BPM
    piece.insert(0, music21.tempo.MetronomeMark(number=60))

    # Create a temporary MIDI file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mid') as temp_midi:
        piece.write('midi', temp_midi.name)
    
    return {"midi_file": temp_midi.name}

# Graph Construction
workflow = StateGraph(MusicState)

# Add nodes to the graph
workflow.add_node("melody_generator", melody_generator)
workflow.add_node("harmony_creator", harmony_creator)
workflow.add_node("rhythm_analyzer", rhythm_analyzer)
workflow.add_node("style_adapter", style_adapter)
workflow.add_node("midi_converter", midi_converter)

# Set the entry point of the graph
workflow.set_entry_point("melody_generator")

# Add edges to connect the nodes
workflow.add_edge("melody_generator", "harmony_creator")
workflow.add_edge("harmony_creator", "rhythm_analyzer")
workflow.add_edge("rhythm_analyzer", "style_adapter")
workflow.add_edge("style_adapter", "midi_converter")
workflow.add_edge("midi_converter", END)

# Compile the graph
app = workflow.compile()

# Streamlit Interface
st.set_page_config(page_title="🎶 AI Music Compositor 🎶", page_icon="🎵", layout="wide")

# Header section
st.header("🎶 AI Music Compositor 🎶")
st.write("🎼 Create Your Own Musical Composition with AI!")

# Sidebar with style selection
style = st.sidebar.selectbox("Select a Musical Style:", ["Classical", "Romantic", "Jazz", "Pop"])

# User input for music description
musician_input = st.text_input("Describe your desired music:")

# Button to generate composition
if st.button("Generate Composition"):
    if musician_input:
        inputs = {
            "musician_input": musician_input,
            "style": style
        }

        # Invoke the workflow
        result = app.invoke(inputs)
        
        st.write(f"**Your Input:** {musician_input}")
        st.write(f"**Selected Music Style:** {style}")
        st.success("🎵 Composition created successfully!")
        

        # Show the generated MIDI file
        st.write(f"MIDI file saved at: {result['midi_file']}")

        # Play button for MIDI file
        if st.button("Play Composition"):
            def play_midi(midi_file_path):
                """Play the generated MIDI file."""
                pygame.mixer.init()
                pygame.mixer.music.load(midi_file_path)
                pygame.mixer.music.play()

                # Wait for playback to finish
                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(10)

                # Clean up
                pygame.mixer.quit()

            play_midi(result["midi_file"])

        # Provide a download button for the generated MIDI file
        st.download_button(
            label="Download MIDI File",
            data=open(result['midi_file'], "rb").read(),
            file_name="generated_music.mid",
            mime="audio/midi"
        )
    else:
        st.error("Please enter a description for your music!")
