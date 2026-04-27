from flask import Flask, request, render_template
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/plan')
def plan():
    subject = request.args.get("subject")

    ai_response = f"""
Your Study Plan for {subject}:

Day 1:
- Learn basics
- Watch simple videos

Day 2:
- Practice exercises

Day 3:
- Review everything
"""

    return render_template("index.html", plan=ai_response)
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