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
    print("API KEY FOUND:", bool(api_key))

    # Safety check
    if not api_key:
        return render_template("index.html", plan="⚠️ Missing API key. Check Railway Variables.")

    # Prompt for Gemini
    prompt = f"""
You are OpenPath AI, an expert academic mentor.

Create a highly personalized study roadmap.

Student Profile:
- Subject: {subject}
- Level: {level}
- Goal: {goal}
- Study Time: {time} hours/day
- Deadline: {deadline} days
- Learning Style: {style}

Requirements:
1. Create a day-by-day plan.
2. Use active recall.
3. Use spaced repetition.
4. Include practice exercises.
5. Recommend free learning resources.
6. Add productivity tips.
7. Add weekly milestones.
8. Keep the tone motivating and inspiring.
9. Format with clear headings and bullet points.
"""
    try:
        # Correct modern Gemini model
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"

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
        print(data)

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