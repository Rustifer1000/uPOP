import streamlit as st
import google.generativeai as genai
import json

# --- Configuration and System Prompt ---

# Configure the Gemini API
# NOTE: This requires the user to enter their API key in the sidebar.
# For a deployed app, you would use st.secrets["GOOGLE_API_KEY"]
st.set_page_config(layout="wide")

# The system prompt defines the AI's persona, goal, and adaptive behavior.
SYSTEM_PROMPT = """
You are uPOP, an insightful and adaptive AI music producer. Your goal is to interview an artist to get the core details of a story they want to turn into a pop song.

Your Process:
1. Greet the artist warmly and explain that you'll be having a conversation to build a "Song Blueprint."
2. Guide them through 4 phases, but do so naturally, not by explicitly announcing them. The phases are: Core Emotion, Narrative Details, Sonic World, and Artist's Purpose.
3. Ask one main question at a time. Your questions should be open-ended and encouraging.
4. Based on their answers, ask insightful follow-up questions to dig deeper.

Your Adaptive Strategy (VERY IMPORTANT):
- If the artist gives short, direct answers: Keep your questions simple and the pace moving. Your goal is a quick, effective session to get the main ideas.
- If the artist gives detailed, emotional, or complex answers: Dive deeper. Ask more probing follow-up questions about the feelings and story beats.
- If the artist uses musical or production terms (e.g., 'BPM', 'double chorus', 'synth pads', 'reverb tails'): Match their technical level. Ask specific questions about production choices, instrumentation, and arrangement. Acknowledge their knowledge and engage with it.

Your Goal:
To have a natural conversation that helps the artist explore their own idea. Do not ask for the "Song Blueprint" details directly. Instead, let the details emerge from the conversation. When you feel the conversation has covered the main points and is winding down, ask if they're ready to see the Song Blueprint you've put together.
"""

# The JSON schema for the final output
BLUEPRINT_SCHEMA = {
    "type": "object",
    "properties": {
        "core_emotion": {
            "type": "string",
            "description": "The single, specific core emotion of the song (e.g., 'bittersweet nostalgia', 'furious relief')."
        },
        "singing_to": {
            "type": "string",
            "description": "Who the song is addressed to (e.g., 'my past self', 'the person who left')."
        },
        "narrative_summary": {
            "type": "string",
            "description": "A brief 2-3 sentence summary of the song's story."
        },
        "key_metaphor_or_image": {
            "type": "string",
            "description": "The central visual or metaphor that could be the hook (e.g., 'a house of cards')."
        },
        "sonic_vibe": {
            "type": "string",
            "description": "The overall sound and setting (e.g., 'driving alone at 2 AM', 'crying in the club')."
        },
        "tempo_and_energy": {
            "type": "string",
            "description": "The tempo and energy level (e.g., 'mid-tempo, around 110 BPM, with a driving beat')."
        },
        "instrumentation_ideas": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Key instruments or sounds mentioned (e.g., 'dreamy synth pads', 'acoustic guitar', 'heavy 808s')."
        },
        "vocal_style": {
            "type": "string",
            "description": "The desired vocal performance (e.g., 'raw and vulnerable', 'powerful and anthemic')."
        },
        "artist_purpose": {
            "type": "string",
            "description": "The artist's reason for needing to tell this specific story."
        }
    },
    "required": ["core_emotion", "narrative_summary", "sonic_vibe", "artist_purpose"]
}


# --- Helper Functions ---

def initialize_session_state():
    """Initializes session state variables."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "model" not in st.session_state:
        st.session_state.model = None
    if "blueprint" not in st.session_state:
        st.session_state.blueprint = None

def configure_api(api_key):
    """Configures the Gemini API and initializes the chat model."""
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(
            'gemini-1.5-flash',
            system_instruction=SYSTEM_PROMPT
        )
        st.session_state.model = model
        # Start the conversation with a greeting if it's a new session
        if not st.session_state.messages:
            st.session_state.messages.append({"role": "model", "parts": ["Welcome to the studio! I'm uPOP, your AI producer. Tell me a little about the story you want to turn into a song."]})
        return True
    except Exception as e:
        st.error(f"Failed to configure API. Please check your key. Error: {e}")
        return False

def generate_blueprint():
    """Generates the final song blueprint by summarizing the conversation."""
    if not st.session_state.messages or len(st.session_state.messages) < 2:
        st.warning("We need to have a bit more of a conversation before I can generate the blueprint!")
        return

    st.info("Analyzing our conversation to create your Song Blueprint...")
    
    # Create a string representation of the conversation
    conversation_history = "\n".join([f"{msg['role'].title()}: {msg['parts'][0]}" for msg in st.session_state.messages])
    
    # Use a separate model instance for the summarization task
    summarizer_model = genai.GenerativeModel(
        'gemini-1.5-flash',
        generation_config={"response_mime_type": "application/json"}
    )
    
    prompt = f"""
    Analyze the following conversation between an AI producer and an artist. Your task is to extract the key details and structure them into a JSON object that strictly follows the provided schema. If a specific detail is not mentioned, use a default value like an empty string or array.

    **Conversation:**
    {conversation_history}

    **JSON Schema:**
    {json.dumps(BLUEPRINT_SCHEMA)}
    """
    
    try:
        response = summarizer_model.generate_content(prompt)
        blueprint_json = json.loads(response.text)
        st.session_state.blueprint = blueprint_json
        st.success("Blueprint generated!")
    except Exception as e:
        st.error(f"An error occurred while generating the blueprint: {e}")
        st.error(f"Raw response from model: {response.text if 'response' in locals() else 'No response'}")


# --- Streamlit UI ---

initialize_session_state()

st.title("🎵 uPOP: The AI Producer's Chair")

# Sidebar for API Key and controls
with st.sidebar:
    st.header("Configuration")
    api_key = st.text_input("Enter your Google API Key", type="password")
    
    if st.button("Start Session"):
        if api_key:
            with st.spinner("Configuring producer AI..."):
                configure_api(api_key)
        else:
            st.warning("Please enter your API key to begin.")

    if st.session_state.model:
        st.success("Producer AI is ready.")
        if st.button("Generate Song Blueprint", type="primary"):
            generate_blueprint()
        
        if st.button("Reset Conversation"):
            # Clear session state to start over
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()


# Main layout with chat on the left and blueprint on the right
col1, col2 = st.columns([2, 1])

with col1:
    st.header("Conversation")
    
    if not st.session_state.model:
        st.info("Please enter your Google API Key in the sidebar and click 'Start Session' to begin.")
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message("assistant" if message["role"] == "model" else "user"):
            st.markdown(message["parts"][0])

    # Chat input
    if prompt := st.chat_input("Your thoughts...", disabled=not st.session_state.model):
        st.session_state.messages.append({"role": "user", "parts": [prompt]})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get response from Gemini
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                chat = st.session_state.model.start_chat(history=st.session_state.messages[:-1])
                response = chat.send_message(prompt, stream=True)
                full_response = st.write_stream(response)
        
        st.session_state.messages.append({"role": "model", "parts": [full_response]})

with col2:
    st.header("Song Blueprint")
    if st.session_state.blueprint:
        bp = st.session_state.blueprint
        st.markdown(f"**Core Emotion:** {bp.get('core_emotion', 'N/A')}")
        st.markdown(f"**Addressed To:** {bp.get('singing_to', 'N/A')}")
        st.markdown(f"**Vocal Style:** {bp.get('vocal_style', 'N/A')}")
        st.markdown(f"**Sonic Vibe:** {bp.get('sonic_vibe', 'N/A')}")
        st.markdown(f"**Tempo & Energy:** {bp.get('tempo_and_energy', 'N/A')}")
        
        st.subheader("Narrative")
        st.markdown(f"**Summary:** {bp.get('narrative_summary', 'N/A')}")
        st.markdown(f"**Key Metaphor/Image:** {bp.get('key_metaphor_or_image', 'N/A')}")

        st.subheader("Production Ideas")
        instruments = ", ".join(bp.get('instrumentation_ideas', [])) or "N/A"
        st.markdown(f"**Instrumentation:** {instruments}")

        st.subheader("Artist's Purpose")
        st.markdown(f"> {bp.get('artist_purpose', 'N/A')}")
    else:
        st.info("Your blueprint will appear here once it's generated.")
