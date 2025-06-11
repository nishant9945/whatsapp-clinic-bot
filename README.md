# WhatsApp Clinic Bot

A Flask app for handling WhatsApp messages via Twilio + OpenAI.

## Deployment on Render

1. Choose **Public Git Repository** on Render.
2. Repo URL: `https://github.com/YOUR_USERNAME/whatsapp-clinic-bot`
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `gunicorn app:app`
5. Add environment variables:
   - `OPENAI_API_KEY`
   - `TWILIO_ACCOUNT_SID`
   - `TWILIO_AUTH_TOKEN`
   - `TWILIO_WHATSAPP_FROM`
