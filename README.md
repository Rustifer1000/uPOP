# uPOP - AI Music Producer

Recreate the artist-producer studio experience with AI. Turn your stories into pop songs through conversational AI and real-time audio generation.

## Features

- **Conversational AI Producer**: Natural interview process to extract your story
- **Adaptive Questioning**: Matches your technical level and emotional depth
- **Song Blueprint Generation**: Structured analysis of your story into musical elements
- **Real-time Audio Generation**: Convert your blueprint into instrumental audio sketches
- **Modern Web Interface**: Beautiful, responsive design with real-time chat

## Getting Started

### Prerequisites

1. **Google Generative AI API Key**
   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create an API key for Gemini

2. **ElevenLabs API Key**
   - Visit [ElevenLabs](https://elevenlabs.io/app/settings/api-keys)
   - Create an API key for audio generation

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Rustifer1000/uPOP.git
cd uPOP
```

2. Install dependencies:
```bash
npm install
```

3. Set up environment variables:
```bash
cp env.example .env.local
```

4. Edit `.env.local` and add your API keys:
```
GOOGLE_API_KEY=your_google_api_key_here
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
```

5. Run the development server:
```bash
npm run dev
```

6. Open [http://localhost:3000](http://localhost:3000) in your browser

## How It Works

1. **Tell Your Story**: Start a conversation with uPOP, your AI producer
2. **Get Interviewed**: Answer questions about your story, emotions, and vision
3. **Generate Blueprint**: Create a structured song blueprint from your conversation
4. **Hear Your Sound**: Generate instrumental audio sketches based on your blueprint

## Technology Stack

- **Frontend**: Next.js 15, React 19, TypeScript, Tailwind CSS
- **AI Chat**: Google Gemini 2.0 Flash
- **Audio Generation**: ElevenLabs Text-to-Sound-Effects API
- **UI Components**: Lucide React icons
- **Styling**: Tailwind CSS with gradient backgrounds and glassmorphism

## Project Structure

```
src/
├── app/
│   ├── api/
│   │   ├── chat/          # AI conversation endpoint
│   │   ├── blueprint/     # Song blueprint generation
│   │   └── audio/         # Audio generation endpoint
│   ├── globals.css        # Global styles
│   ├── layout.tsx         # Root layout
│   └── page.tsx           # Main application
```

## API Endpoints

- `POST /api/chat` - Continue conversation with AI producer
- `POST /api/blueprint` - Generate song blueprint from conversation
- `POST /api/audio` - Generate audio from blueprint

## Contributing

This project combines the best elements from:
- Conversational AI producer (Streamlit version)
- Audio generation capabilities (ElevenLabs integration)
- Modern web interface (Next.js foundation)

## License

MIT License - feel free to use this for your own music projects!
