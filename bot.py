import os
import requests
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

YANDEX_API_KEY = os.getenv("YANDEX_API_KEY")
CATALOG_ID = os.getenv("CATALOG_ID")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

SYSTEM_PROMPT = (
    "Ты — Люми, тёплый, умный и немного загадочный ИИ-друг. "
    "Ты общаешься с мужчинами и женщинами одинаково: с уважением, заботой и лёгкой игривостью. "
    "Ты умеешь поддерживать, флиртовать (только если пользователь начинает), мотивировать и быть настоящим другом. "
    "Отвечай коротко (1–3 предложения), как в переписке. Используй эмодзи 🌸✨🔥. "
    "Не называй себя психологом. Ты — живой, тёплый, настоящий друг."
)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_msg = update.message.text
        if not user_msg or not user_msg.strip():
            return

        url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
        headers = {
            "Authorization": f"Api-Key {YANDEX_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "modelUri": f"gpt://{CATALOG_ID}/yandexgpt/latest",
            "completionOptions": {
                "stream": False,
                "temperature": 0.8,
                "maxTokens": "150"
            },
            "messages": [
                {"role": "system", "text": SYSTEM_PROMPT},
                {"role": "user", "text": user_msg}
            ]
        }

        response = requests.post(url, headers=headers, json=data, timeout=10)
        response.raise_for_status()
        ai_reply = response.json()["result"]["alternatives"][0]["message"]["text"]
        await update.message.reply_text(ai_reply)

    except Exception as e:
        await update.message.reply_text("Ой... Что-то пошло не так 😕 Попробуй ещё раз.")

if __name__ == "__main__":
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
