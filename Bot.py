import os

from telegram import (
    Update,
    InlineQueryResultArticle,
    InputTextMessageContent,
)
from telegram.ext import (
    Application,
    InlineQueryHandler,
)

TOKEN = os.environ["BOT_TOKEN"]


async def inline_query(update: Update, context):
    result = InlineQueryResultArticle(
        id="would-you-rather-test",
        title="🎮 Would You Rather",
        description="Start a 2-player game",
        input_message_content=InputTextMessageContent(
            "🎮 WOULD YOU RATHER\n\n"
            "2-player game\n\n"
            "Tap START GAME to begin."
        ),
    )

    await update.inline_query.answer(
        [result],
        cache_time=0,
        is_personal=True,
    )


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(
        InlineQueryHandler(inline_query)
    )

    print("BOT IS RUNNING")

    app.run_polling()


if __name__ == "__main__":
    main()
