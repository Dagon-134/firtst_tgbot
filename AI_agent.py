from openai import OpenAI

from dotenv import load_dotenv
import os

load_dotenv()

AI_token1 = os.getenv("AI_TOKEN1")
AI_token2 = os.getenv("AI_TOKEN2")


async def generate_response(user_message):
    for i in range(10):
        try:
            client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=AI_token1,
            )

            response = client.chat.completions.create(
                model="google/gemma-4-31b-it:free",
                messages=[
                    {
                        "role": "system",
                        "content": "Ты полезный ассистент. Отвечай на русском."
                    },
                    {
                        "role": "user",
                        "content": user_message,   # ← сообщение от пользователя Telegram
                    }
                ],
                extra_body={"reasoning": {"enabled": True}},
                stream=True
            )

            return response.choices[0].message.content
        except Exception as e:
            print(e)
            i += 1
    return 'Ответ от ии не пришёл'