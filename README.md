# 🎵 Melody AI - Personal Music Curator

Melody AI is an Agentic AI-powered music recommendation application that generates personalized song recommendations based on a user's mood, language, energy level, and listening situation.

The application uses Google's Gemini models through the OpenAI-compatible API along with Spotify and YouTube integrations to provide an interactive music discovery experience.

---

## 🚀 Features

* Personalized music recommendations
* Mood-based song discovery
* Language-specific recommendations
* Energy-level filtering
* Listening-context recommendations
* Spotify track embedding
* YouTube video embedding
* Direct Spotify and YouTube links
* Modern Gradio user interface
* Agentic AI architecture using OpenAI Agents SDK

---

# 🏗️ Architecture

```text
User Input
     │
     ▼
┌────────────────────┐
│    Gradio UI       │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│   Melody AI Agent  │
│  (Gemini 2.5 Flash)│
└─────────┬──────────┘
          │
          ▼
 Generates 5 Songs
          │
          ▼
┌────────────────────┐
│ Spotify API        │
│ Track Lookup       │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│ YouTube Data API   │
│ Video Lookup       │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│ Card Renderer      │
│ Spotify Embed      │
│ YouTube Embed      │
└─────────┬──────────┘
          │
          ▼
      Final UI
```

---

# 🧠 Agent Workflow

### Step 1

User selects:

* Mood
* Language
* Energy Level
* Listening Situation

### Step 2

Melody AI Agent generates:

* Song Name
* Artist
* Recommendation Reason

### Step 3

Backend searches:

* Spotify Track URL
* YouTube Video URL

### Step 4

Application renders:

* Song card
* Spotify player
* YouTube player
* Direct links

---

# 🛠 Tech Stack

### AI / LLM

* Gemini 2.5 Flash Lite
* Google Generative AI

### Agent Framework

* OpenAI Agents SDK

### Backend

* Python 3.11+

### Frontend

* Gradio

### Music Platforms

* Spotify Web API
* YouTube Data API v3

### Deployment

* Hugging Face Spaces

---

# 📂 Project Structure

```text
music_agent/
│
├── app.py
├── requirements.txt
├── .gitignore
├── README.md
├── .env
│
└── assets/
```

---

# ⚙️ Installation

## 1. Clone Repository

```bash
git clone https://github.com/abhishekpoddar29/Melody-AI.git

cd Melody-AI
```

---

## 2. Create Virtual Environment

### Windows

```bash
python -m venv .venv

.venv\Scripts\activate
```

### Linux / Mac

```bash
python3 -m venv .venv

source .venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file in the root directory.

```env
GEMINI_API_KEY=your_gemini_api_key

SPOTIFY_CLIENT_ID=your_spotify_client_id

SPOTIFY_CLIENT_SECRET=your_spotify_client_secret

YOUTUBE_API_KEY=your_youtube_api_key
```

---

# 🔐 Getting API Keys

## Gemini API

1. Visit Google AI Studio
2. Create API Key
3. Copy into `.env`

---

## Spotify API

1. Visit Spotify Developer Dashboard
2. Create App
3. Get:

* Client ID
* Client Secret

---

## YouTube Data API

1. Open Google Cloud Console
2. Enable:

```text
YouTube Data API v3
```

3. Create API Key

---

# ▶️ Run Application

```bash
python app.py
```

Application will start on:

```text
http://localhost:7860
```

---

# 📦 Requirements

Example dependencies:

```text
gradio
openai
openai-agents
google-genai
spotipy
google-api-python-client
python-dotenv
```

Install all using:

```bash
pip install -r requirements.txt
```

---

# 🖼 Example Usage

### Input

```text
Mood: Relaxed 🌙

Language: Hindi

Energy: Calm

Situation: Travel
```

### Output

```text
1. Tum Se Hi
2. Kun Faya Kun
3. Kabira (Encore)
4. Dil Diyan Gallan
5. Shayad
```

With:

* Spotify Player
* YouTube Video
* Direct Streaming Links

---

# 🚀 Deployment

This project can be deployed on:

* Hugging Face Spaces
* Render
* Railway
* AWS EC2
* Azure
* Google Cloud Run

---

# 🧩 Future Improvements

* Playlist generation
* Multi-agent architecture
* Spotify playlist creation
* User authentication
* Music similarity search
* RAG-based music recommendation
* Genre-aware recommendations
* User recommendation history

---

# 👨‍💻 Author

**Abhishek Poddar**

* LinkedIn: https://www.linkedin.com/in/abhishek-poddar5829/
* GitHub: https://github.com/abhishekpoddar29

---

# 📄 License

MIT License

Feel free to fork, modify, and contribute.
