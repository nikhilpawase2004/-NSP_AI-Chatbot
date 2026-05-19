from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


# SECRET OWNER KEY
OWNER_SECRET = "nspowner123"


def ask_groq(user_message):

    message = user_message.lower().strip()


    # =========================================
    # OWNER DETECTION
    # =========================================

    is_owner = False

    if OWNER_SECRET in message:

        is_owner = True


    # =========================================
    # OWNER RESPONSES
    # =========================================

    if is_owner:

        # HELLO RESPONSE
        if any(word in message for word in [
            "hello",
            "hi",
            "hey"
        ]):

            return """

👋 Welcome back Owner

NSP Chatbot is ready to help you.
"""


        # OWNER DETAILS
        if any(word in message for word in [
            "who am i",
            "about me",
            "my name",
            "do you know me"
        ]):

            return """

✅ Owner Verified

You are the developer of NSP-AI-Chatbot.

Tech Stack:
• Python Flask
• HTML/CSS/JS
• MySQL
• Groq AI

You are building a modern AI assistant project.
"""


    # =========================================
    # NORMAL AI RESPONSE
    # =========================================

    try:

        completion = client.chat.completions.create(

            model="llama-3.3-70b-versatile",

            messages=[

                {
                    "role": "system",

                    "content": """

You are NSP Chatbot AI Assistant.

Rules:

1. Understand spelling mistakes.

2. Understand shortcut words.

Example:
u = you
r = are
pls = please

3. For coding:
- give working code
- give formatted code
- avoid syntax errors

4. Behave professionally.

5. Give clean beautiful responses.

6. Keep answers user friendly.

"""
                },

                {
                    "role": "user",
                    "content": user_message
                }

            ]

        )

        reply = completion.choices[0].message.content

        return reply

    except Exception as e:

        print("GROQ ERROR:", e)

        return "AI is not responding."