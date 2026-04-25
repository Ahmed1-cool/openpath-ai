from flask import Flask, request, render_template
import requests

app = Flask(__name__)

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
    low_resource = request.args.get("low_resource")

    prompt = f"""
You are an elite study strategist.

Create a structured, step-by-step study plan.

Student Profile:
- Subject: {subject}
- Level: {level}
- Goal: {goal}
- Study time per day: {time} hours
- Deadline: {deadline} days
- Learning style: {style}
"""

    if low_resource:
        prompt += "\nMake it suitable for students with limited internet and no paid resources."

    prompt += """
Requirements:
1. Break into daily plan
2. Give clear tasks
3. Be realistic
4. Use bullet points
"""

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
    json={
        "model": "llama3.1",
        "prompt": prompt,
        "stream": False,
        "options": {
            "num_predict": 300
        }
    },
    timeout=60
            
        )

        ai_response = response.json()["response"]

        with open("plans.txt", "a", encoding="utf-8") as f:
            f.write(ai_response + "\n\n---\n\n")

        return render_template("index.html", plan=[ai_response])

    except Exception as e:
        return render_template("index.html", plan=[f"Error: {str(e)}"])

@app.route('/history')
def history():
    try:
        with open("plans.txt", "r", encoding="utf-8") as f:
            content = f.read()
    except:
        content = "No saved plans yet."

    return f"<pre>{content}</pre>"

if __name__ == '__main__':
    app.run(debug=True)