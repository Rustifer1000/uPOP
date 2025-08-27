import streamlit as st

def initialize_session_state():
    """Initializes all the necessary variables in the session state."""
    if 'phase' not in st.session_state:
        st.session_state.phase = 1
    
    # Phase 1 variables
    if 'core_emotion' not in st.session_state:
        st.session_state.core_emotion = ""
    if 'singing_to' not in st.session_state:
        st.session_state.singing_to = ""
    if 'listener_feeling' not in st.session_state:
        st.session_state.listener_feeling = ""
    if 'movie_weather' not in st.session_state:
        st.session_state.movie_weather = ""
        
    # Phase 2 variables
    if 'turning_point' not in st.session_state:
        st.session_state.turning_point = ""
    if 'story_start' not in st.session_state:
        st.session_state.story_start = ""
    if 'words_said' not in st.session_state:
        st.session_state.words_said = ""
    if 'words_unsaid' not in st.session_state:
        st.session_state.words_unsaid = ""
    if 'central_metaphor' not in st.session_state:
        st.session_state.central_metaphor = ""
    if 'realization_moment' not in st.session_state:
        st.session_state.realization_moment = ""

    # Phase 3 variables
    if 'song_venue' not in st.session_state:
        st.session_state.song_venue = "Stadium"
    if 'bpm' not in st.session_state:
        st.session_state.bpm = 120
    if 'song_purpose' not in st.session_state:
        st.session_state.song_purpose = []
    if 'reference_tracks' not in st.session_state:
        st.session_state.reference_tracks = ""
    if 'instrumentation' not in st.session_state:
        st.session_state.instrumentation = []
    if 'vocal_style' not in st.session_state:
        st.session_state.vocal_style = ""
        
    # Phase 4 variables
    if 'why_this_story' not in st.session_state:
        st.session_state.why_this_story = ""


def display_phase_1():
    """Displays the questions for Phase 1: The Core Emotion."""
    st.header("Phase 1: Finding the Core Emotion (The 'Why')")
    st.info("Let's start with the foundation. Forget lyrics for a second, just focus on the feeling.")
    
    st.text_input(
        "Before you tell me the whole story, what's the single core emotion? (e.g., 'bittersweet nostalgia,' 'furious relief,' 'nervous hope')", 
        key="core_emotion"
    )

    if st.session_state.core_emotion:
        st.text_input("Who is this song *to*? (e.g., the other person, your past self, everyone who's felt this way)", key="singing_to")
    
    if st.session_state.singing_to:
        st.text_input("When the song ends, what do you want the listener to feel?", key="listener_feeling")
        
    if st.session_state.listener_feeling:
        st.text_input("If this story were a movie scene, what's the weather like?", key="movie_weather")

    if st.session_state.movie_weather:
        if st.button("Next: Unpack the Narrative"):
            st.session_state.phase = 2
            st.rerun()


def display_phase_2():
    """Displays the questions for Phase 2: The Narrative."""
    st.header("Phase 2: Unpacking the Narrative (The 'What' and 'How')")
    st.info("Now we find the lyrics. As a writer, focus on sensory details and concrete images.")
    
    st.text_area("Describe the most important moment—the turning point. Where are you, what do you see, smell, feel?", key="turning_point", height=150)
    
    if st.session_state.turning_point:
        st.text_area("Where does the story *start*? Paint the 'before' picture.", key="story_start", height=100)
    
    if st.session_state.story_start:
        st.text_area("What was the single most important thing that was said? Use the exact words if you can.", key="words_said", height=100)
    
    if st.session_state.words_said:
        st.text_area("What was the most important thing that was *left unsaid*?", key="words_unsaid", height=100)
        
    if st.session_state.words_unsaid:
        st.text_input("What's the central metaphor for the conflict? (e.g., 'a house of cards,' 'a runaway train'). This could be your hook.", key="central_metaphor")
        
    if st.session_state.central_metaphor:
        st.text_area("What was the moment of realization or perspective shift? This is our bridge.", key="realization_moment", height=100)

    if st.session_state.realization_moment:
        if st.button("Next: Build the Sonic World"):
            st.session_state.phase = 3
            st.rerun()


def display_phase_3():
    """Displays the questions for Phase 3: The Sonic World."""
    st.header("Phase 3: Building the Sonic World (The 'Sound')")
    st.info("We have the emotion and the story. Now, what does it *sound* like?")
    
    st.radio("When you imagine this song, where are you?", ("A massive, sold-out stadium", "Alone in a car at 2 AM", "A small, intimate club"), key="song_venue")
    
    st.slider("What's the song's heartbeat? (Beats Per Minute)", min_value=60, max_value=180, key="bpm")
    
    st.multiselect("What do you want people to do when they hear this?", ["Dance", "Cry", "Think", "Drive", "Get Angry"], key="song_purpose")
    
    st.text_input("List 2-3 reference artists or songs that have the right *feeling*.", key="reference_tracks")
    
    st.multiselect("Is the music more organic or electronic?", ["Organic (Piano, Acoustic Guitar, Live Drums)", "Electronic (Synths, 808s, Programmed Drums)", "A blend of both"], key="instrumentation")
    
    st.selectbox("How is your vocal performance?", ["Raw and vulnerable", "Powerful and anthemic", "Breathy and intimate", "Slick and produced"], key="vocal_style")

    if st.session_state.vocal_style:
        if st.button("Next: The Final Touch"):
            st.session_state.phase = 4
            st.rerun()


def display_phase_4():
    """Displays the final question of the interview."""
    st.header("Phase 4: The Final Touch (The 'Who')")
    st.info("This is about you, the artist. How does this story live in your voice?")
    
    st.text_area("After all that, let's go back to the beginning. Why *this* story? Why do you need to sing this, right now?", key="why_this_story", height=150)
    
    if st.session_state.why_this_story:
        st.success("Interview Complete! See your summary below.")
        if st.button("Start Over"):
            # Clear all session state keys to reset the app
            for key in st.session_state.keys():
                del st.session_state[key]
            st.rerun()

def display_summary():
    """Displays a summary of all the user's answers."""
    if st.session_state.phase == 4 and st.session_state.why_this_story:
        st.markdown("---")
        st.header("Your Song Blueprint")
        
        st.subheader("Phase 1: Core Emotion")
        st.write(f"**Core Emotion:** {st.session_state.core_emotion}")
        st.write(f"**Singing To:** {st.session_state.singing_to}")
        st.write(f"**Listener Leaves Feeling:** {st.session_state.listener_feeling}")
        st.write(f"**The 'Weather':** {st.session_state.movie_weather}")
        
        st.subheader("Phase 2: Narrative")
        st.write(f"**The Turning Point:** {st.session_state.turning_point}")
        st.write(f"**The Beginning (Verse Idea):** {st.session_state.story_start}")
        st.write(f"**Words Said:** {st.session_state.words_said}")
        st.write(f"**Words Unsaid:** {st.session_state.words_unsaid}")
        st.write(f"**Central Metaphor (Chorus/Hook Idea):** {st.session_state.central_metaphor}")
        st.write(f"**The Realization (Bridge Idea):** {st.session_state.realization_moment}")
        
        st.subheader("Phase 3: Sonic World")
        st.write(f"**The Vibe:** {st.session_state.song_venue}")
        st.write(f"**Tempo:** {st.session_state.bpm} BPM")
        st.write(f"**Listener Action:** {', '.join(st.session_state.song_purpose)}")
        st.write(f"**Reference Tracks:** {st.session_state.reference_tracks}")
        st.write(f"**Instrumentation:** {', '.join(st.session_state.instrumentation)}")
        st.write(f"**Vocal Style:** {st.session_state.vocal_style}")
        
        st.subheader("Phase 4: Artist's Purpose")
        st.write(f"**Why this story needs to be told:** {st.session_state.why_this_story}")

# --- Main App Logic ---
st.title("🎵 The Producer's Chair: Songwriting Interview")
st.markdown("Welcome to the studio. You've got a story, and I'm here to help you turn it into a pop song. Let's find the truth in it together.")

initialize_session_state()

# Display the current phase
if st.session_state.phase == 1:
    display_phase_1()
elif st.session_state.phase == 2:
    display_phase_2()
elif st.session_state.phase == 3:
    display_phase_3()
elif st.session_state.phase == 4:
    display_phase_4()

# Display the summary at the end
display_summary()
