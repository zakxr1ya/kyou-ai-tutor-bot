from flask import Flask, render_template, request
import smtplib
from email.mime.text import MIMEText
from groq import Groq

# Hardcoded config
client = Groq(api_key="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")
TUTOR_EMAIL = "zxkxriya@gmail.com"
FROM_EMAIL = "zakxriya.ali@gmail.com"
FROM_EMAIL_PASSWORD = "uuoq hlrl yryu ndll"  # ← Fix with Gmail App Password later

app = Flask(__name__)

SYSTEM_PROMPT = """
You are an assistant for a private tuition centre in Leicester.
You receive raw enquiry details from parents about tuition.

Your job:
1. Summarise the enquiry in 3–5 bullet points: child age/year, subject, level, goals, timing.
2. Decide if good fit for centre.
3. Draft short friendly email reply for tutor to send parent (UK English).
Be concise.
"""

def send_email(to_email, subject, body):
    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = FROM_EMAIL
    msg["To"] = to_email
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(FROM_EMAIL, FROM_EMAIL_PASSWORD)
        server.send_message(msg)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/enquiry", methods=["POST"])
def handle_enquiry():
    parent_name = request.form.get("parent_name", "")
    parent_email = request.form.get("parent_email", "")
    child_name = request.form.get("child_name", "")
    child_age = request.form.get("child_age", "")
    year_group = request.form.get("year_group", "")
    subject = request.form.get("subject", "")
    level = request.form.get("level", "")
    goals = request.form.get("goals", "")
    availability = request.form.get("availability", "")
    other_notes = request.form.get("other_notes", "")

    raw_text = f"""
Parent: {parent_name} ({parent_email})
Child: {child_name}, age {child_age}, year {year_group}
Subject: {subject}, level: {level}
Goals: {goals}
Availability: {availability}
Notes: {other_notes}
"""

    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": raw_text}
        ]
    )

    ai_output = completion.choices[0].message.content

    # PRINT AI OUTPUT TO TERMINAL (your demo proof)
    print("\n=== NEW ENQUIRY ===")
    print(raw_text)
    print("=== AI SUMMARY + REPLY ===")
    print(ai_output)
    print("=" * 50)

    # Email (uncomment when Gmail fixed)
    send_email(TUTOR_EMAIL, "New Tuition Enquiry (AI)", f"{raw_text}\n\nAI:\n{ai_output}")

    return render_template("thanks.html", parent_name=parent_name)

if __name__ == "__main__":
    app.run(debug=True)
