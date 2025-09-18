import { NextRequest, NextResponse } from 'next/server';
import { GoogleGenerativeAI } from '@google/generative-ai';

const BLUEPRINT_SCHEMA = {
  type: "object",
  properties: {
    core_emotion: {
      type: "string",
      description: "The single, specific core emotion of the song (e.g., 'bittersweet nostalgia', 'furious relief')."
    },
    singing_to: {
      type: "string",
      description: "Who the song is addressed to (e.g., 'my past self', 'the person who left')."
    },
    narrative_summary: {
      type: "string",
      description: "A brief 2-3 sentence summary of the song's story."
    },
    key_metaphor_or_image: {
      type: "string",
      description: "The central visual or metaphor that could be the hook (e.g., 'a house of cards')."
    },
    sonic_vibe: {
      type: "string",
      description: "The overall sound and setting (e.g., 'driving alone at 2 AM', 'crying in the club')."
    },
    tempo_and_energy: {
      type: "string",
      description: "The tempo and energy level (e.g., 'mid-tempo, around 110 BPM, with a driving beat')."
    },
    instrumentation_ideas: {
      type: "array",
      items: { type: "string" },
      description: "Key instruments or sounds mentioned (e.g., 'dreamy synth pads', 'acoustic guitar', 'heavy 808s')."
    },
    vocal_style: {
      type: "string",
      description: "The desired vocal performance (e.g., 'raw and vulnerable', 'powerful and anthemic')."
    },
    artist_purpose: {
      type: "string",
      description: "The artist's reason for needing to tell this specific story."
    }
  },
  required: ["core_emotion", "narrative_summary", "sonic_vibe", "artist_purpose"]
};

export async function POST(request: NextRequest) {
  try {
    const { conversation } = await request.json();

    if (!process.env.GOOGLE_API_KEY) {
      return NextResponse.json(
        { error: 'Google API key not configured' },
        { status: 500 }
      );
    }

    const genAI = new GoogleGenerativeAI(process.env.GOOGLE_API_KEY);
    const model = genAI.getGenerativeModel({
      model: 'gemini-2.0-flash',
      generationConfig: {
        responseMimeType: 'application/json',
      },
    });

    // Create a string representation of the conversation
    const conversationHistory = conversation
      .map((msg: any) => `${msg.role === 'assistant' ? 'Producer' : 'Artist'}: ${msg.content}`)
      .join('\n');

    const prompt = `
Analyze the following conversation between an AI producer and an artist. Your task is to extract the key details and structure them into a JSON object that strictly follows the provided schema. If a specific detail is not mentioned, use a default value like an empty string or array.

**Conversation:**
${conversationHistory}

**JSON Schema:**
${JSON.stringify(BLUEPRINT_SCHEMA, null, 2)}
`;

    const result = await model.generateContent(prompt);
    const response = await result.response;
    const text = response.text();

    const blueprint = JSON.parse(text);

    return NextResponse.json({ blueprint });
  } catch (error) {
    console.error('Error in blueprint API:', error);
    return NextResponse.json(
      { error: 'Failed to generate blueprint' },
      { status: 500 }
    );
  }
}
