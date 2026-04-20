from groq import Groq
from config import GROQ_API_KEY, GROQ_MODEL

client = Groq(api_key=GROQ_API_KEY)

class Brain:
    def __init__(self):
        self.history = [
            {"role": "system", "content": "You are a helpful assistant living in a floating orb on the user's desktop. Be concise and friendly."}
        ]

    def ask(self, user_message):
        self.history.append({"role": "user", "content": user_message})
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=self.history
        )
        reply = response.choices[0].message.content
        self.history.append({"role": "assistant", "content": reply})
        return reply

    def get_history(self):
        # return only user/assistant turns, skip system
        return [m for m in self.history if m["role"] != "system"]

    def greet(self):
        self.history.append({"role": "system", "content": f"User's name is sir. Say hello to them."})
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=self.history
        )
        reply = response.choices[0].message.content
        self.history.append({"role": "assistant", "content": reply})
        return reply
