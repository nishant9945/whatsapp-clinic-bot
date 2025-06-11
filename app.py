import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from openai import OpenAI

# Set up Flask app and OpenAI client
app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    incoming = request.values.get("Body", "").strip().lower()
    response = MessagingResponse()
    msg = response.message()

    # Intent-based response logic
    if "book" in incoming or "appointment" in incoming:
        msg.body("Sure! Please share your full name and preferred time for the appointment.")
    elif "queue" in incoming or "wait" in incoming:
        msg.body("You are currently number 3 in the queue. Estimated wait time is about 20 minutes.")
    elif "hours" in incoming or "timing" in incoming or "open" in incoming:
        msg.body("Our clinic is open daily from 9 AM to 9:30 PM.")
    else:
        # Fallback to ChatGPT via OpenAI API
        try:
            gpt_reply = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": incoming}],
                temperature=0.5,
                max_tokens=100
            )
            msg.body(gpt_reply.choices[0].message.content.strip())
        except Exception as e:
            print("OpenAI error:", e)
            msg.body("Sorry, I'm having trouble replying right now. Please try again later.")

    return str(response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
