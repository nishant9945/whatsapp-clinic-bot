import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import openai

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    incoming = request.values.get("Body", "").strip().lower()
    response = MessagingResponse()
    msg = response.message()

    # Logic tree
    if "book" in incoming or "appointment" in incoming:
        msg.body("Sure! What's your full name and preferred time?")
    elif "queue" in incoming or "wait" in incoming:
        msg.body("You're number 3 in line. Estimated wait time: ~20 mins.")
    elif "hours" in incoming or "timing" in incoming or "open" in incoming:
        msg.body("We are open daily from 9 AM to 9:30 PM.")
    else:
        try:
            gpt_reply = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": incoming}],
                temperature=0.5,
                max_tokens=100
            )
            msg.body(gpt_reply.choices[0].message.content.strip())
        except Exception as e:
            msg.body("Sorry, I'm having trouble replying right now.")

    return str(response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
