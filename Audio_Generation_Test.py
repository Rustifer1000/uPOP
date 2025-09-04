import streamlit as st
from elevenlabs.client import ElevenLabs

# --- Configuration ---
# Set page title and icon
st.set_page_config(page_title="Audio Sketchpad", page_icon="🎵")

# --- Helper Function ---
@st.cache_data
def generate_audio_sample(prompt_text, api_key):
    """
    Generates audio from a text prompt using the ElevenLabs API.
    Uses st.cache_data to avoid re-generating the same audio.
    """
    if not prompt_text or not api_key:
        return None, "Error: Prompt or API key is missing."

    try:
        # Initialize the ElevenLabs client
        client = ElevenLabs(api_key=api_key)

        # Generate the audio using the text_to_sound_effects model
        # This returns raw audio bytes
        audio_bytes = client.text_to_sound_effects.convert(
            text=prompt_text,
            duration_seconds=7,  # Keep it short for testing
            prompt_influence=0.7, # Controls how closely it follows the prompt
        )
        return audio_bytes, None
    except Exception as e:
        st.error(f"An error occurred with the ElevenLabs API: {e}")
        return None, str(e)

# --- Streamlit UI ---

st.title("🎵 Audio Generation Sketchpad")
st.markdown("This is a simple app to test the core functionality of generating instrumental audio from a text prompt using the ElevenLabs API.")

# --- API Key Input ---
# Use secrets if available, otherwise allow manual input
try:
    elevenlabs_api_key = st.secrets["ELEVENLABS_API_KEY"]
    st.success("ElevenLabs API Key found in secrets!")
except (KeyError, FileNotFoundError):
    st.warning("ElevenLabs API Key not found in secrets. Please enter it below.")
    elevenlabs_api_key = st.text_input("Enter your ElevenLabs API Key:", type="password")

st.markdown("---")

# --- Main Interaction ---
if elevenlabs_api_key:
    st.header("Create a Sound")
    
    # Text input for the audio prompt
    prompt = st.text_input(
        "Enter a descriptive prompt for the audio:",
        "A simple, melancholic piano melody, lo-fi, 85 BPM, dreamy and nostalgic."
    )

    # Button to trigger audio generation
    if st.button("Generate Audio Sketch", type="primary"):
        if prompt:
            with st.spinner("uPOP is dialing in a sound..."):
                # Call the function to get the audio bytes
                audio_data, error = generate_audio_sample(prompt, elevenlabs_api_key)

                if error:
                    st.error(f"Failed to generate audio: {error}")
                elif audio_data:
                    st.success("Audio generated successfully!")
                    # Display the audio player
                    st.audio(audio_data, format='audio/mpeg')
        else:
            st.warning("Please enter a prompt to generate audio.")
else:
    st.info("Please provide an ElevenLabs API key to begin.")
