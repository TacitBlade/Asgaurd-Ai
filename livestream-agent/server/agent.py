import anthropic
from server.config import config, ANTHROPIC_API_KEY

class Agent:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        self.personality = config.get("agent", {}).get("personality", "You are a helpful AI.")
        self.name = config.get("agent", {}).get("name", "StreamBot")
        self.conversation_history = []
        self.system_prompt = f"Your name is {self.name}. {self.personality}\nRespond concisely for a live stream."

    def process_message(self, user, message, is_host=False):
        # Add to history
        role = "Host" if is_host else f"Chatter ({user})"
        self.conversation_history.append({"role": "user", "content": f"[{role}]: {message}"})

        # Keep history short (e.g. last 10 messages)
        if len(self.conversation_history) > 10:
            self.conversation_history = self.conversation_history[-10:]

        try:
            response = self.client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=150,
                system=self.system_prompt,
                messages=self.conversation_history
            )
            
            ai_text = response.content[0].text
            self.conversation_history.append({"role": "assistant", "content": ai_text})
            return ai_text
        except Exception as e:
            print(f"Error calling Anthropic API: {e}")
            return None
