from flask import Flask, request, render_template
import requests
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")


@app.route('/plan')
def plan():
    import os
    import requests

    subject = request.args.get("subject")
    level = request.args.get("level")
    goal = request.args.get("goal")
    time = request.args.get("time")
    deadline = request.args.get("deadline")
    style = request.args.get("style")

    api_key = os.getenv("AIzaSyAgq8aOGavEo4Uo2Q6cELsO89Ltb7j4oOU")

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
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"

        response = requests.post(
            url,
            json={
                "contents": [{"parts": [{"text": prompt}]}]
            }
        )

        data = response.json()

        if "candidates" in data:
            ai_response = data["candidates"][0]["content"]["parts"][0]["text"]
        else:
            ai_response = f"⚠️ Gemini error:\n{data}"

    except Exception as e:
        ai_response = f"Error: {str(e)}"

    return render_template("index.html", plan=ai_response)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
