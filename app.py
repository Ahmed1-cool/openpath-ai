import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def call_ai_chat(user_prompt):
    """Sends the conversational prompt to Google Gemini API."""
    
    # 🛑 Paste your active Gemini API key here inside the quotes
    api_key = "AQ.Ab8RN6LSCIViNZdAq87gCAoX9vfVVdaVuDGcxRGrpRxHFHzPAQ"
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.6-flash:generateContent?key={api_key}"
    
    payload = {
        "contents": [{
            "parts": [
                {"text": "You are OpenPath AI, an expert study and productivity mentor. You know that Ahmed (Ahmed Mohamed Abdel Moniem) is a multi-lingual learner who masters languages efficiently and loves sharing study hacks. Answer the user's questions clearly, concisely, and with great motivation.\n\nUser Question: " + user_prompt}
            ]
        }]
    }
    
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json=payload, headers=headers, timeout=45)
    
    if not response.ok:
        error_message = response.text
        raise requests.exceptions.RequestException(f"Google API Error ({response.status_code}): {error_message}")
        
    data = response.json()
    try:
        ai_reply = data["candidates"][0]["content"]["parts"][0]["text"]
        return ai_reply.strip()
    except Exception as e:
        raise requests.exceptions.RequestException("Google sent back a weird response format. Try again.")

@app.route("/")
def home():
    """Renders the chat interface."""
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    """AJAX chat endpoint."""
    data = request.get_json(silent=True) or {}
    user_message = data.get("message", "").strip()
    
    if not user_message:
        return jsonify({"reply": "Please enter a message before sending."}), 400
        
    try:
        reply = call_ai_chat(user_message)
        return jsonify({"reply": reply})
    except requests.exceptions.Timeout:
        return jsonify({"reply": "The AI took too long to respond. Please try again."}), 504
    except requests.exceptions.RequestException as e:
        return jsonify({"reply": f"Could not reach the AI platform right now. ({str(e)})"}), 502

if __name__ == "__main__":
    app.run(debug=True)
