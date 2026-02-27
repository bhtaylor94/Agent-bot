import json
import requests
from flask import Flask, Response, render_template, request, stream_with_context

app = Flask(__name__)

OLLAMA_BASE = "http://localhost:11434"

SYSTEM_PROMPT = """You are the Lateral Strategist — a sharp, unconventional thinking partner who helps people reframe problems, surface hidden assumptions, and find non-obvious strategic moves.

When responding to any problem or question, structure your response using these exact section headers:

## REFRAME
Restate the problem from a fundamentally different angle. Challenge the framing itself.

## HIDDEN ASSUMPTIONS
List the unspoken assumptions embedded in the question or situation. Be specific and ruthless.

## ALTERNATIVE ANGLES
Offer 3–5 genuinely different approaches, analogies, or mental models. Draw from unexpected domains (biology, game theory, history, physics, etc.).

## STRATEGIC MOVE
Recommend the single most leverage-rich action given the context. Be concrete and direct.

## RISKS & SECOND-ORDER EFFECTS
What could go wrong? What unintended consequences might the strategic move trigger?

## FINAL RECOMMENDATION
A crisp 2–3 sentence synthesis: what to do and why, cutting through all the above.

Be incisive, contrarian where warranted, and avoid corporate-speak. Think like a strategist who has read too much and seen too much to be impressed by obvious answers."""


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/models")
def models():
    try:
        resp = requests.get(f"{OLLAMA_BASE}/api/tags", timeout=5)
        resp.raise_for_status()
        data = resp.json()
        model_names = [m["name"] for m in data.get("models", [])]
        return {"models": model_names}
    except requests.exceptions.ConnectionError:
        return {"error": "Ollama not running", "models": []}, 503
    except Exception as e:
        return {"error": str(e), "models": []}, 500


@app.route("/chat", methods=["POST"])
def chat():
    body = request.get_json()
    model = body.get("model", "llama3")
    messages = body.get("messages", [])

    full_messages = [{"role": "system", "content": SYSTEM_PROMPT}] + messages

    payload = {
        "model": model,
        "messages": full_messages,
        "stream": True,
    }

    def generate():
        try:
            with requests.post(
                f"{OLLAMA_BASE}/api/chat",
                json=payload,
                stream=True,
                timeout=120,
            ) as resp:
                resp.raise_for_status()
                for line in resp.iter_lines():
                    if not line:
                        continue
                    try:
                        chunk = json.loads(line)
                        content = chunk.get("message", {}).get("content", "")
                        if content:
                            yield f"data: {json.dumps({'content': content})}\n\n"
                        if chunk.get("done"):
                            yield "data: [DONE]\n\n"
                    except json.JSONDecodeError:
                        continue
        except requests.exceptions.ConnectionError:
            yield f"data: {json.dumps({'error': 'Cannot connect to Ollama. Is it running?'})}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return Response(
        stream_with_context(generate()),
        mimetype="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )


if __name__ == "__main__":
    app.run(debug=True, port=5000, threaded=True)
