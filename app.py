import os
import json
import re
import gradio as gr
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from googleapiclient.discovery import build
from google import genai
from openai import AsyncOpenAI
from agents import (
    Agent,
    Runner,
    OpenAIChatCompletionsModel,
    function_tool,
    trace,
    ModelSettings
)

# ─────────────────────────────────────────────────────────────
# GEMINI CLIENT SETUP
# ─────────────────────────────────────────────────────────────

google_api_key = os.getenv("GEMINI_API_KEY")

GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"

gemini_client = AsyncOpenAI(
    base_url=GEMINI_BASE_URL,
    api_key=google_api_key,
)

gemini_model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash-lite",
    openai_client=gemini_client,
)

GEMINI_MODEL = gemini_model

gemini_search_client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)
# ─────────────────────────────────────────────────────────────
# SPOTIFY CLIENT
# ─────────────────────────────────────────────────────────────
spotify_client = spotipy.Spotify(
    auth_manager=SpotifyClientCredentials(
        client_id=os.getenv("SPOTIFY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIFY_CLIENT_SECRET")
    )
)
# ─────────────────────────────────────────────────────────────
# Youtube CLIENT
# ─────────────────────────────────────────────────────────────
youtube = build(
    "youtube",
    "v3",
    developerKey=os.getenv("YOUTUBE_API_KEY")
)
# ─────────────────────────────────────────────────────────────
# TOOLS
# ─────────────────────────────────────────────────────────────
@function_tool
def google_search(query: str) -> str:
    """
    Search the web using Gemini Google Search grounding.
    """

    try:

        response = gemini_search_client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=query,
            config={
                "tools": [
                    {
                        "google_search": {}
                    }
                ]
            }
        )

        return response.text

    except Exception as e:
        return f"Search Error: {str(e)}"
    
def get_spotify_track(song, artist):

    try:

        query = f"track:{song} artist:{artist}"

        results = spotify_client.search(
            q=query,
            type="track",
            limit=1
        )

        tracks = results.get("tracks", {}).get("items", [])

        if tracks:

            return tracks[0]["external_urls"]["spotify"]

    except Exception as e:
        print("Spotify Error:", e)

    return ""

def get_youtube_video(song, artist):

    try:

        query = f"{song} {artist} official video"

        request = youtube.search().list(
            q=query,
            part="snippet",
            maxResults=1,
            type="video"
        )

        response = request.execute()

        items = response.get("items", [])

        if items:

            video_id = items[0]["id"]["videoId"]

            return (
                f"https://www.youtube.com/watch?v={video_id}"
            )

    except Exception as e:
        print("YouTube Error:", e)

    return ""



# ─────────────────────────────────────────────────────────────
# MUSIC AGENT
# ─────────────────────────────────────────────────────────────

music_agent = Agent(
    name="MelodyAI",

    instructions="""
You are an expert music recommendation AI.

Recommend EXACTLY 5 songs.

Return ONLY JSON.

Format:

[
 {
   "song":"...",
   "artist":"...",
   "reason":"..."
 }
]

Do NOT include Spotify URLs.
Do NOT include YouTube URLs.

Never invent URLs.

""",
    model=GEMINI_MODEL,

)

# ─────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────

def extract_json(text: str):

    try:
        return json.loads(text)

    except:
        pass

    # Remove markdown if exists
    text = text.replace("```json", "").replace("```", "").strip()

    try:
        return json.loads(text)

    except:
        pass

    # Regex extraction
    match = re.search(r"\[.*\]", text, re.DOTALL)

    if match:

        try:
            return json.loads(match.group(0))
        except:
            pass

    return None


# ─────────────────────────────────────────────────────────────
# HTML CARD GENERATOR
# ─────────────────────────────────────────────────────────────

def generate_music_cards(songs):

    cards = ""

    for song in songs:

        song_name = song.get("song", "Unknown")
        artist = song.get("artist", "Unknown")
        reason = song.get("reason", "")

        spotify = song.get("spotify", "")
        youtube = song.get("youtube", "")

        # ───────────────── Spotify Embed ─────────────────

        spotify_embed = ""

        if spotify and "open.spotify.com/track/" in spotify:

            try:

                track_id = spotify.split("/track/")[1].split("?")[0]

                spotify_embed = f"""
                <iframe
                    style="border-radius:12px"
                    src="https://open.spotify.com/embed/track/{track_id}"
                    width="100%"
                    height="90"
                    frameBorder="0"
                    allowfullscreen=""
                    allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture">
                </iframe>
                """

            except:
                spotify_embed = ""

        # ───────────────── YouTube Embed ─────────────────

        youtube_embed = ""

        if youtube and "watch?v=" in youtube:

            try:

                video_id = youtube.split("watch?v=")[1].split("&")[0]

                youtube_embed = f"""
                <iframe
                    width="100%"
                    height="350"
                    src="https://www.youtube.com/embed/{video_id}"
                    title="YouTube video player"
                    frameborder="0"
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                    referrerpolicy="strict-origin-when-cross-origin"
                    allowfullscreen>
                </iframe>
                """

            except:
                youtube_embed = ""

        # ───────────────── Buttons ─────────────────

        spotify_button = ""

        if spotify:
            spotify_button = f"""
            <a
                href="{spotify}"
                target="_blank"
                style="
                    background:#1DB954;
                    color:white;
                    padding:12px 18px;
                    border-radius:10px;
                    text-decoration:none;
                    font-weight:bold;
                "
            >
                🎧 Open Spotify
            </a>
            """

        youtube_button = ""

        if youtube:
            youtube_button = f"""
            <a
                href="{youtube}"
                target="_blank"
                style="
                    background:#FF0000;
                    color:white;
                    padding:12px 18px;
                    border-radius:10px;
                    text-decoration:none;
                    font-weight:bold;
                "
            >
                ▶ Open YouTube
            </a>
            """

        # ───────────────── Card UI ─────────────────

        cards += f"""

        <div style="
            background: linear-gradient(145deg,#1f1f2e,#27293d);
            padding: 24px;
            border-radius: 22px;
            margin-bottom: 35px;
            color: white;
            box-shadow: 0 8px 30px rgba(0,0,0,0.35);
            border: 1px solid rgba(255,255,255,0.08);
        ">

            <h2 style="
                margin-bottom:8px;
                font-size:32px;
            ">
                🎵 {song_name}
            </h2>

            <h3 style="
                color:#c9c9d6;
                margin-top:0;
            ">
                👤 {artist}
            </h3>

            <p style="
                font-size:17px;
                line-height:1.7;
                color:#f0f0f0;
            ">
                ✨ {reason}
            </p>

            <div style="margin-top:25px;">
                {spotify_embed}
            </div>

            <div style="margin-top:25px;">
                {youtube_embed}
            </div>

            <div style="
                margin-top:20px;
                display:flex;
                gap:15px;
                flex-wrap:wrap;
            ">
                {spotify_button}
                {youtube_button}
            </div>

        </div>
        """

    return cards


# ─────────────────────────────────────────────────────────────
# MAIN FUNCTION
# ─────────────────────────────────────────────────────────────

async def recommend_songs(
    mood,
    language,
    energy,
    situation,
):

    user_prompt = f"""
Mood: {mood}
Language: {language}
Energy Level: {energy}
Listening Situation: {situation}

Recommend EXACTLY 5 songs.

For each song provide:
- song
- artist
- reason
- spotify
- youtube

Return ONLY JSON.
"""

    try:

        with trace("Music Recommendation"):

            result = await Runner.run(
                music_agent,
                input=user_prompt,
            )

        response = result.final_output

        print("\n========== RAW MODEL OUTPUT ==========\n")
        print(response)
        print("\n======================================\n")

        if not response:

            return """
            <div style='color:red;font-size:24px;'>
                ❌ Empty response from model.
            </div>
            """

        response = str(response).strip()

        # Remove markdown code blocks if Gemini adds them
        response = response.replace("```json", "")
        response = response.replace("```", "")
        response = response.strip()

        songs = extract_json(response)
        for song in songs:

            song_name = song["song"]
            artist = song["artist"]

            song["spotify"] = get_spotify_track(
                song_name,
                artist
            )

            song["youtube"] = get_youtube_video(
                song_name,
                artist
            )

            print("\n===== VERIFIED LINKS =====")
            print(song_name)
            print(song["spotify"])
            print(song["youtube"])

        if not songs:

            return f"""
            <div style='color:red;font-size:20px;'>

                ❌ Failed to parse model response.

                <br><br>

                <b>Raw Output:</b>

                <pre style="
                    white-space: pre-wrap;
                    background:#111;
                    color:white;
                    padding:15px;
                    border-radius:12px;
                    overflow:auto;
                ">{response}</pre>

            </div>
            """

        # Gemini sometimes returns a dict instead of a list
        if isinstance(songs, dict):
            songs = [songs]

        if len(songs) == 0:

            return """
            <div style='color:red;font-size:20px;'>
                ❌ No songs were returned.
            </div>
            """
        print("\n========== SONG DATA ==========\n")
        for song in songs:

            spotify = song.get("spotify","")
            youtube = song.get("youtube","")

            if not spotify.startswith("https://open.spotify.com/"):
                song["spotify"] = ""

            if not (
                youtube.startswith("https://www.youtube.com/")
                or
                youtube.startswith("https://youtu.be/")
            ):
                song["youtube"] = ""
        print("\n===============================\n")
        html_output = generate_music_cards(songs)

        return html_output

    except Exception as e:

        import traceback

        print("\n========== EXCEPTION ==========\n")
        traceback.print_exc()
        print("\n===============================\n")

        return f"""
        <div style="
            color:red;
            font-size:22px;
            padding:20px;
        ">
            ❌ Error:
            <br><br>
            {str(e)}
        </div>
        """


# ─────────────────────────────────────────────────────────────
# UI
# ─────────────────────────────────────────────────────────────

with gr.Blocks(
    theme=gr.themes.Soft(
        primary_hue="violet",
        secondary_hue="pink",
    )
) as ui:

    gr.Markdown(
        """
# 🎵 Melody AI — Personal Music Curator

Choose your vibe and get 5 personalized song recommendations with Spotify + YouTube playback.
"""
    )

    with gr.Row():

        mood = gr.Radio(
            choices=[
                "Happy 😊",
                "Sad 😔",
                "Relaxed 🌙",
            ],
            label="What's your mood?",
            value="Happy 😊",
        )

        language = gr.Dropdown(
            choices=[
                "Hindi",
                "English",
                "Punjabi",
                "Tamil",
                "Telugu",
                "Korean",
            ],
            label="Choose language",
            value="Hindi",
        )

    with gr.Row():

        energy = gr.Radio(
            choices=[
                "Calm",
                "Medium",
                "High Energy",
            ],
            label="Energy level",
            value="Medium",
        )

        situation = gr.Dropdown(
            choices=[
                "Workout",
                "Study",
                "Late Night",
                "Travel",
                "Party",
                "Relaxing Alone",
            ],
            label="Where will you listen?",
            value="Travel",
        )

    recommend_btn = gr.Button(
        "🎶 Recommend Songs",
        variant="primary",
    )

    output = gr.HTML()

    recommend_btn.click(
        fn=recommend_songs,
        inputs=[
            mood,
            language,
            energy,
            situation,
        ],
        outputs=output,
    )

# ─────────────────────────────────────────────────────────────
# RUN
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":

    ui.launch(
        server_name="0.0.0.0",
        server_port=7860,
    )