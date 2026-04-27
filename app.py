from flask import Flask, request, render_template
import requests
import os

app = Flask(__name__)

GEMINI_API_KEY = os.getenv("AIzaSyAgq8aOGavEo4Uo2Q6cELsO89Ltb7j4oOU")

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/plan')
def plan():
    subject = request.args.get("subject")
    level = request.args.get("level")
    goal = request.args.get("goal")
    time = request.args.get("time")
    deadline = request.args.get("deadline")
    style = request.args.get("style")

    prompt = f"""
You are an elite study strategist.

Create a clear, structured, daily study plan.

Subject: {subject}
Level: {level}
Goal: {goal}
Study time: {time} hours/day
Deadline: {deadline} days
Learning style: {style}

Make it:
- Organized by days
- Practical
- Motivating
"""

    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"

        response = requests.post(
            url,
            json={
                "contents": [
                    {"parts": [{"text": prompt}]}
                ]
            }
        )

        data = response.json()

        ai_response = data["candidates"][0]["content"]["parts"][0]["text"]

        return render_template("index.html", plan=ai_response)

    except Exception as e:
        return render_template("index.html", plan=f"Error: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True)