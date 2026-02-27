# Lateral Strategist

A locally-hosted AI agent that reframes problems, surfaces hidden assumptions, and delivers structured strategic advice — all running on your machine via Ollama. No API keys, no cloud, no data leaving your device.

![Python](https://img.shields.io/badge/python-3.8+-blue) ![Flask](https://img.shields.io/badge/flask-latest-green) ![Ollama](https://img.shields.io/badge/ollama-local-orange)

---

## What it does

You describe a problem. The Lateral Strategist responds with a structured 6-section analysis:

| Section | Description |
|---|---|
| **Reframe** | Restates the problem from a fundamentally different angle |
| **Hidden Assumptions** | Surfaces the unspoken assumptions embedded in the situation |
| **Alternative Angles** | 3–5 non-obvious approaches drawn from unexpected domains |
| **Strategic Move** | The single most leverage-rich action to take |
| **Risks & Second-Order Effects** | What could go wrong and what the move might trigger |
| **Final Recommendation** | A crisp 2–3 sentence synthesis of what to do and why |

Responses stream live (typewriter effect) and each section is rendered with a distinct color-coded label.

---

## Requirements

- Python 3.8+
- [Ollama](https://ollama.com) running locally with at least one model pulled

---

## Setup

```bash
# 1. Clone the repo
git clone https://github.com/bhtaylor94/Agent-bot.git
cd Agent-bot

# 2. Install dependencies
pip install -r requirements.txt

# 3. Make sure Ollama is running and a model is available
ollama serve          # if not already running
ollama pull llama3    # or mistral, gemma2, etc.

# 4. Start the app
python app.py
```

Then open **http://localhost:5000** in your browser.

---

## Usage

- Type your problem or question in the input box and press **Enter** (or **Shift+Enter** for a new line)
- Use the model dropdown in the header to switch between any models you have installed in Ollama
- Click **↺ Reset** to clear the conversation and start fresh
- Multi-turn conversation is supported — context is maintained across messages

---

## Project Structure

```
├── app.py                  # Flask server + Ollama integration
├── requirements.txt        # flask, requests
└── templates/
    └── index.html          # Single-page dark-theme UI (vanilla JS)
```

### How it works

- **Backend**: Flask serves the UI and exposes two endpoints — `GET /models` (fetches available Ollama models) and `POST /chat` (streams responses via Server-Sent Events). The system prompt defining the Lateral Strategist persona is injected server-side and never exposed to the client.
- **Streaming**: Ollama's streaming API is piped through Flask as SSE chunks; the frontend reads them with the Fetch Streams API for a live typewriter effect.
- **Section parsing**: Once streaming completes, the raw response is parsed by regex into named sections and re-rendered with styled labels.

---

## Switching models

The model dropdown is populated automatically from whatever you have installed in Ollama. To add a new model:

```bash
ollama pull mistral
ollama pull gemma2
ollama pull phi3
```

Refresh the page and the new model will appear in the dropdown.

---

## License

MIT
