import os
import random
import uuid

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQueryResultArticle,
    InputTextMessageContent,
)
from telegram.ext import (
    Application,
    InlineQueryHandler,
    CallbackQueryHandler,
)

TOKEN = os.environ["BOT_TOKEN"]

# Active games
games = {}


# =========================================================
# WOULD YOU RATHER QUESTIONS
# =========================================================

QUESTIONS = [
    ("have no legs", "have no arms"),
    ("be extremely rich but ugly", "be extremely attractive but poor"),
    ("read minds", "be invisible"),
    ("never use your phone again", "never use the internet again"),
    ("always be 10 minutes late", "always be 30 minutes early"),
    ("know when someone is lying", "always get away with lying"),
    ("have your crush read your messages", "have your crush read your search history"),
    ("lose your phone for a month", "lose your wallet for a month"),
    ("be famous but hated", "be unknown but loved"),
    ("have unlimited money", "have unlimited free time"),
    ("never fall in love", "fall in love but get your heart broken"),
    ("kiss your crush", "hug your crush for 10 minutes"),
    ("text your crush 'I love you' by accident", "call your crush by accident"),
    ("have your ex come back", "have your crush confess their feelings"),
    ("know your future", "change your past"),
    ("be able to teleport", "be able to pause time"),
    ("have no music", "have no movies"),
    ("give up coffee forever", "give up your favorite food forever"),
    ("be stuck with your ex for a week", "be stuck with your boss for a week"),
    ("have your private photos leaked", "have your private messages leaked"),
    ("always say exactly what you think", "never speak your mind again"),
    ("be loved by everyone", "be feared by everyone"),
    ("have your dream job with low pay", "hate your job but be extremely rich"),
    ("live without air conditioning", "live without heating"),
    ("have one true love", "have many exciting relationships"),
    ("be able to fly", "be able to breathe underwater"),
    ("lose all your memories", "never make new memories"),
    ("be trapped in an elevator with your crush", "be trapped in an elevator with your ex"),
    ("have your crush call you every night", "have your crush text you all day"),
    ("always know what people think of you", "never know what anyone thinks"),
    ("have perfect skin", "have perfect hair"),
    ("be extremely funny", "be extremely attractive"),
    ("have $10 million today", "have your dream life in 10 years"),
    ("never get rejected", "never get ghosted"),
    ("have your crush like your old photo", "have your crush watch all your stories"),
    ("be caught flirting", "be caught lying"),
    ("have your crush see your embarrassing photos", "have your crush hear your embarrassing stories"),
    ("date your best friend", "date a complete stranger"),
    ("have a perfect relationship", "have a perfect career"),
    ("be able to erase one embarrassing moment", "be able to relive one perfect moment"),
    ("always know who likes you", "always know who dislikes you"),
    ("get a surprise kiss", "get a surprise date"),
    ("have your crush say 'I miss you'", "have your crush say 'I want you'"),
    ("be alone for a year", "be surrounded by people you don't like for a year"),
    ("have your partner know your password", "have your partner know your search history"),
    ("never be jealous", "have a partner who is never jealous"),
    ("be able to control dreams", "never need to sleep"),
    ("have one wish", "have three wishes but they are random"),
]


# =========================================================
# FORMAT QUESTION
# =========================================================

def question_text(question, status_text=None):
    a, b = question

    text = (
        "🎮 <b>WOULD YOU RATHER</b>\n\n"
        f"🔴 <b>{a}</b>\n\n"
        f"🔵 <b>{b}</b>"
    )

    if status_text:
        text += f"\n\n🔥 <b>{status_text}</b>"

    return text


# =========================================================
# ANSWER BUTTONS
# =========================================================

def answer_keyboard(game_id):

    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "🔴",
                callback_data=f"ANSWER:R:{game_id}"
            ),
            InlineKeyboardButton(
                "🔵",
                callback_data=f"ANSWER:B:{game_id}"
            ),
        ]
    ])


# =========================================================
# NEXT QUESTION BUTTON
# =========================================================

def next_question_keyboard():

    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "🔥 NEXT QUESTION",
                switch_inline_query_current_chat=""
            )
        ]
    ])


# =========================================================
# INLINE MODE
# =========================================================

async def inline_query(update: Update, context):

    game_id = str(uuid.uuid4())

    question = random.choice(QUESTIONS)

    games[game_id] = {
        "question": question,
        "answers": {},
    }

    result = InlineQueryResultArticle(
        id=game_id,
        title="🎮 Would You Rather",
        description=f"🔴 {question[0]}  |  🔵 {question[1]}",

        input_message_content=InputTextMessageContent(
            question_text(question),
            parse_mode="HTML",
        ),

        reply_markup=answer_keyboard(game_id),
    )

    await update.inline_query.answer(
        [result],
        cache_time=0,
        is_personal=True,
    )


# =========================================================
# ANSWER
# =========================================================

async def answer(update: Update, context):

    query = update.callback_query

    parts = query.data.split(":")

    choice = parts[1]
    game_id = parts[2]

    # -----------------------------------------------------
    # CHECK GAME
    # -----------------------------------------------------

    if game_id not in games:

        await query.answer(
            "❌ This game has expired.",
            show_alert=True,
        )

        return

    game = games[game_id]

    user = query.from_user

    # -----------------------------------------------------
    # PREVENT DOUBLE ANSWER
    # -----------------------------------------------------

    if user.id in game["answers"]:

        await query.answer(
            "You already answered this question! 😄",
            show_alert=True,
        )

        return

    # -----------------------------------------------------
    # SAVE ANSWER
    # -----------------------------------------------------

    game["answers"][user.id] = {
        "name": user.first_name,
        "choice": choice,
    }

    await query.answer(
        "🔴" if choice == "R" else "🔵"
    )

    # -----------------------------------------------------
    # ONLY ONE PLAYER ANSWERED
    # -----------------------------------------------------

    if len(game["answers"]) == 1:

        player_name = user.first_name

        await query.edit_message_text(
            question_text(
                game["question"],
                f"{player_name} chose their answer"
            ),
            parse_mode="HTML",
            reply_markup=answer_keyboard(game_id),
        )

        return

    # -----------------------------------------------------
    # BOTH PLAYERS ANSWERED
    # -----------------------------------------------------

    answers = list(game["answers"].values())

    player1 = answers[0]
    player2 = answers[1]

    choice1 = (
        "🔴"
        if player1["choice"] == "R"
        else "🔵"
    )

    choice2 = (
        "🔴"
        if player2["choice"] == "R"
        else "🔵"
    )

    result_text = (
        "🎮 <b>WOULD YOU RATHER</b>\n\n"

        f"🔴 <b>{game['question'][0]}</b>\n\n"

        f"🔵 <b>{game['question'][1]}</b>\n\n"

        "━━━━━━━━━━━━━━\n\n"

        f"<b>{player1['name']}</b> {choice1}\n"
        f"<b>{player2['name']}</b> {choice2}\n\n"

        "🔥 <b>Both answered!</b>"
    )

    # -----------------------------------------------------
    # SHOW RESULT + NEW QUESTION BUTTON
    # -----------------------------------------------------

    await query.edit_message_text(
        result_text,
        parse_mode="HTML",
        reply_markup=next_question_keyboard(),
    )


# =========================================================
# CALLBACK ROUTER
# =========================================================

async def callback_handler(update: Update, context):

    data = update.callback_query.data

    if data.startswith("ANSWER:"):

        await answer(update, context)


# =========================================================
# MAIN
# =========================================================

def main():

    app = Application.builder().token(TOKEN).build()

    app.add_handler(
        InlineQueryHandler(inline_query)
    )

    app.add_handler(
        CallbackQueryHandler(callback_handler)
    )

    print("🔥 WOULD YOU RATHER BOT IS RUNNING")

    app.run_polling()


if __name__ == "__main__":
    main()
