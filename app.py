from flask import Flask, request, render_template
import requests
import os

app = Flask(__name__)


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/plan')
def plan():

    # Get user inputs safely
    subject = request.args.get("subject", "Not specified")
    level = request.args.get("level", "Not specified")
    goal = request.args.get("goal", "Not specified")
    time = request.args.get("time", "Not specified")
    deadline = request.args.get("deadline", "Not specified")
    style = request.args.get("style", "Not specified")

    # Get API key from Railway environment
    api_key = os.getenv("GEMINI_API_KEY")

    # Safety check
    if not api_key:
        return render_template("index.html", plan="⚠️ Missing API key. Check Railway Variables.")

    # Prompt for Gemini
    prompt = f"""
Create a structured daily study plan.

Subject: {subject}
Level: {level}
Goal: {goal}
Study time: {time} hours/day
Deadline: {deadline} days
Learning style: {style}

Make it clear, practical, and motivating.
"""

    try:
        # Correct modern Gemini model
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"

        response = requests.post(
            url,
            json={
                "contents": [
                    {
                        "parts": [
                            {"text": prompt}
                        ]
                    }
                ]
            }
        )

        data = response.json()

        # Extract response safely
        if "candidates" in data and len(data["candidates"]) > 0:
            ai_response = data["candidates"][0]["content"]["parts"][0]["text"]
        else:
            ai_response = f"⚠️ Gemini error:\n{data}"

    except Exception as e:
        ai_response = f"Error: {str(e)}"

    return render_template("index.html", plan=ai_response)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)