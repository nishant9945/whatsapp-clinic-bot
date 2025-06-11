import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import openai

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    incoming = request.values.get("Body", "").strip()
    resp = MessagingResponse()
    reply = resp.message()

    text = incoming.lower()
    if "book" in text:
        reply.body("Sure—what's your full name?")
    elif "queue" in text:
        reply.body("You're currently #3 in line. Wait ~20 mins.")
    elif "hours" in text or "time" in text:
        reply.body("Open daily 9 AM–9:30 PM.")
    else:
        gpt = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role":"user","content":incoming}]
        )
        reply.body(gpt.choices[0].message.content)

    return str(resp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
