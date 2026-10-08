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
    CommandHandler,
    InlineQueryHandler,
    CallbackQueryHandler,
)

TOKEN = os.environ["BOT_TOKEN"]

games = {}


# =========================================================
# QUESTIONS
# =========================================================

QUESTIONS = [
    ("Would you rather kiss your crush 😳",
     "or let your crush read your private messages 📱?"),

    ("Would you rather know who secretly likes you ❤️",
     "or know who secretly hates you 😈?"),

    ("Would you rather go on a date with your crush 💕",
     "or receive $1,000,000 💰?"),

    ("Would you rather accidentally text your crush 'I love you' 😭",
     "or accidentally send them your search history 💀?"),

    ("Would you rather be extremely attractive 😏",
     "or extremely rich 💰?"),

    ("Would you rather have your crush kiss you 💋",
     "or have your crush confess their feelings ❤️?"),

    ("Would you rather lose your phone for a week 📱",
     "or lose the internet for a month 🌐?"),

    ("Would you rather be able to read minds 🧠",
     "or become invisible 👻?"),

    ("Would you rather have your ex text 'I miss you' 😳",
     "or your crush text 'I want you' 🔥?"),

    ("Would you rather reveal your biggest secret 🤐",
     "or reveal your biggest crush 😳?"),

    ("Would you rather spend one night with your celebrity crush ⭐",
     "or receive $100,000 💰?"),

    ("Would you rather never be able to lie again 😇",
     "or have everyone know when you're lying 🤥?"),

    ("Would you rather have unlimited money 💰",
     "or unlimited free time 😎?"),

    ("Would you rather accidentally like your crush's old photo 😭",
     "or accidentally comment '😍' on it 💀?"),

    ("Would you rather have your crush call you at midnight 🌙",
     "or wake up to a romantic message ❤️?"),

    ("Would you rather be stuck in an elevator with your crush 😏",
     "or stuck in a car with your ex 😭?"),

    ("Would you rather date someone extremely jealous 😈",
     "or someone who never gets jealous 😐?"),

    ("Would you rather know your partner's entire past 👀",
     "or have them know yours?"),

    ("Would you rather get caught flirting 😳",
     "or get caught lying about flirting 💀?"),

    ("Would you rather have your crush see your private photos 😳",
     "or hear every thought you've had about them 🧠?"),

    ("Would you rather always know when someone is lying 🤥",
     "or always get away with lying 😈?"),

    ("Would you rather have your first kiss again 💋",
     "or your best kiss again 🔥?"),

    ("Would you rather be famous worldwide 🌎",
     "or anonymous but extremely rich 💰?"),

    ("Would you rather date your best friend ❤️",
     "or never date anyone again 😭?"),

    ("Would you rather receive a surprise kiss 💋",
     "or give someone a surprise kiss 😏?"),

    ("Would you rather have your crush call you beautiful 😍",
     "or tell you they can't stop thinking about you ❤️?"),

    ("Would you rather accidentally send a spicy photo to your family 😭",
     "or to your boss 💀?"),

    ("Would you rather have your partner know your passwords 🔐",
     "or your entire search history 📱?"),

    ("Would you rather spend Valentine's Day alone 😭",
     "or with someone you don't love 😐?"),

    ("Would you rather have your crush reject you 💔",
     "or never know if they liked you?"),

    ("Would you rather kiss someone you don't like 😳",
     "or never kiss anyone again?"),

    ("Would you rather have one perfect relationship ❤️",
     "or date lots of people but never fall in love?"),

    ("Would you rather have your crush walk in while you're changing 😳",
     "or walk in while they're changing 👀?"),

    ("Would you rather know exactly who your soulmate is ❤️",
     "or never know but eventually meet them?"),

    ("Would you rather teleport anywhere 🌎",
     "or pause time ⏸️?"),

    ("Would you rather have $10 million 💰",
     "or find your soulmate tomorrow ❤️?"),

    ("Would you rather always be 10 minutes late ⏰",
     "or always be 30 minutes early?"),

    ("Would you rather be extremely funny 😂",
     "or extremely attractive 😏?"),

    ("Would you rather have your crush call you every night 🌙",
     "or text you all day 📱?"),

    ("Would you rather confess your feelings first ❤️",
     "or wait for them to confess?"),
]


# =========================================================
# INLINE RESULT
# =========================================================

async def inline_query(update: Update, context):

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "🎮 START GAME",
                callback_data="START_GAME"
            )
        ]
    ])

    result = InlineQueryResultArticle(
        id=str(uuid.uuid4()),
        title="🎮 Would You Rather",
        description="Start a 2-player private game",
        input_message_content=InputTextMessageContent(
            "🎮 <b>WOULD YOU RATHER</b>\n\n"
            "👥 <b>2-player private game</b>\n\n"
            "Tap <b>START GAME</b> to create a game.",
            parse_mode="HTML",
        ),
        reply_markup=keyboard,
    )

    await update.inline_query.answer(
        [result],
        cache_time=0,
        is_personal=True,
    )


# =========================================================
# START GAME
# =========================================================

async def start_game(update: Update, context):

    query = update.callback_query
    await query.answer()

    game_id = str(uuid.uuid4())

    games[game_id] = {
        "player1": None,
        "player2": None,
        "turn": None,
        "question": None,
        "round": 0,
    }

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "👤 JOIN GAME",
                callback_data=f"JOIN:{game_id}"
            )
        ]
    ])

    await query.edit_message_text(
        "🎮 <b>WOULD YOU RATHER</b>\n\n"
        "🔥 <b>GAME CREATED!</b>\n\n"
        "👥 Waiting for 2 players...\n\n"
        "Anyone who wants to play can tap:\n\n"
        "👤 <b>JOIN GAME</b>",
        parse_mode="HTML",
        reply_markup=keyboard,
    )


# =========================================================
# JOIN GAME
# =========================================================

async def join_game(update: Update, context):

    query = update.callback_query
    await query.answer()

    game_id = query.data.split(":", 1)[1]

    if game_id not in games:
        await query.answer(
            "❌ Game no longer exists.",
            show_alert=True
        )
        return

    game = games[game_id]
    user = query.from_user

    name = user.first_name

    # Player 1
    if game["player1"] is None:

        game["player1"] = {
            "id": user.id,
            "name": name,
        }

        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "👤 JOIN GAME",
                    callback_data=f"JOIN:{game_id}"
                )
            ]
        ])

        await query.edit_message_text(
            "🎮 <b>WOULD YOU RATHER</b>\n\n"
            "🔥 <b>GAME CREATED!</b>\n\n"
            f"👤 Player 1: <b>{name}</b>\n"
            "👤 Player 2: <i>Waiting...</i>\n\n"
            "Send this game to your friend.\n"
            "They can tap <b>JOIN GAME</b>.",
            parse_mode="HTML",
            reply_markup=keyboard,
        )

        return

    # Same player
    if game["player1"]["id"] == user.id:
        await query.answer(
            "You already joined this game.",
            show_alert=True
        )
        return

    # Player 2
    if game["player2"] is None:

        game["player2"] = {
            "id": user.id,
            "name": name,
        }

        game["turn"] = game["player1"]["id"]

        await show_question(query, game_id)

        return

    await query.answer(
        "❌ This game already has 2 players.",
        show_alert=True
    )


# =========================================================
# SHOW QUESTION
# =========================================================

async def show_question(query, game_id):

    game = games[game_id]

    game["round"] += 1
    game["question"] = random.choice(QUESTIONS)

    p1 = game["player1"]
    p2 = game["player2"]

    current = p1 if game["turn"] == p1["id"] else p2

    a, b = game["question"]

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "🅰️ A",
                callback_data=f"ANSWER:A:{game_id}"
            ),
            InlineKeyboardButton(
                "🅱️ B",
                callback_data=f"ANSWER:B:{game_id}"
            )
        ],
        [
            InlineKeyboardButton(
                "❌ END GAME",
                callback_data=f"END:{game_id}"
            )
        ]
    ])

    await query.edit_message_text(
        "🎮 <b>WOULD YOU RATHER</b>\n\n"
        f"👤 {p1['name']}\n"
        f"👤 {p2['name']}\n\n"
        f"🔥 <b>ROUND {game['round']}</b>\n\n"
        f"<b>A.</b> {a}\n\n"
        "<b>OR</b>\n\n"
        f"<b>B.</b> {b}\n\n"
        f"🎯 <b>{current['name']}'s turn</b>",
        parse_mode="HTML",
        reply_markup=keyboard,
    )


# =========================================================
# ANSWER
# =========================================================

async def answer(update: Update, context):

    query = update.callback_query

    parts = query.data.split(":")
    choice = parts[1]
    game_id = parts[2]

    if game_id not in games:
        await query.answer(
            "❌ Game no longer exists.",
            show_alert=True
        )
        return

    game = games[game_id]
    user = query.from_user

    # TURN CHECK
    if user.id != game["turn"]:

        current = (
            game["player1"]
            if game["turn"] == game["player1"]["id"]
            else game["player2"]
        )

        await query.answer(
            f"⏳ It's {current['name']}'s turn!",
            show_alert=True
        )
        return

    await query.answer()

    p1 = game["player1"]
    p2 = game["player2"]

    current = p1 if user.id == p1["id"] else p2

    if choice == "A":
        chosen = game["question"][0]
    else:
        chosen = game["question"][1]

    # SWITCH TURN
    if user.id == p1["id"]:
        game["turn"] = p2["id"]
        next_player = p2
    else:
        game["turn"] = p1["id"]
        next_player = p1

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "🔥 NEXT QUESTION",
                callback_data=f"NEXT:{game_id}"
            )
        ],
        [
            InlineKeyboardButton(
                "❌ END GAME",
                callback_data=f"END:{game_id}"
            )
        ]
    ])

    await query.edit_message_text(
        "🎮 <b>WOULD YOU RATHER</b>\n\n"
        f"🔥 <b>{current['name']} chose:</b>\n\n"
        f"{chosen}\n\n"
        "━━━━━━━━━━━━━━\n\n"
        f"🎯 <b>{next_player['name']}'s turn!</b>",
        parse_mode="HTML",
        reply_markup=keyboard,
    )


# =========================================================
# NEXT QUESTION
# =========================================================

async def next_question(update: Update, context):

    query = update.callback_query

    game_id = query.data.split(":", 1)[1]

    if game_id not in games:
        await query.answer(
            "❌ Game no longer exists.",
            show_alert=True
        )
        return

    game = games[game_id]

    # Only current player can continue
    if query.from_user.id != game["turn"]:

        current = (
            game["player1"]
            if game["turn"] == game["player1"]["id"]
            else game["player2"]
        )

        await query.answer(
            f"⏳ It's {current['name']}'s turn.",
            show_alert=True
        )
        return

    await query.answer()

    await show_question(query, game_id)


# =========================================================
# END GAME
# =========================================================

async def end_game(update: Update, context):

    query = update.callback_query

    game_id = query.data.split(":", 1)[1]

    if game_id not in games:
        await query.answer()
        return

    game = games[game_id]

    user_id = query.from_user.id

    allowed = False

    if game["player1"] and game["player1"]["id"] == user_id:
        allowed = True

    if game["player2"] and game["player2"]["id"] == user_id:
        allowed = True

    if not allowed:
        await query.answer(
            "Only the players can end this game.",
            show_alert=True
        )
        return

    await query.answer()

    del games[game_id]

    await query.edit_message_text(
        "🎮 <b>WOULD YOU RATHER</b>\n\n"
        "❌ <b>GAME ENDED</b>\n\n"
        "Thanks for playing! 🔥",
        parse_mode="HTML",
    )


# =========================================================
# CALLBACK ROUTER
# =========================================================

async def callback_handler(update: Update, context):

    data = update.callback_query.data

    if data == "START_GAME":
        await start_game(update, context)

    elif data.startswith("JOIN:"):
        await join_game(update, context)

    elif data.startswith("ANSWER:"):
        await answer(update, context)

    elif data.startswith("NEXT:"):
        await next_question(update, context)

    elif data.startswith("END:"):
        await end_game(update, context)


# =========================================================
# /START
# =========================================================

async def start(update: Update, context):

    await update.message.reply_text(
        "🎮 <b>WOULD YOU RATHER</b>\n\n"
        "2-player Telegram game.\n\n"
        "Type @wouldyouratherobot in a chat "
        "to start a game.",
        parse_mode="HTML",
    )


# =========================================================
# MAIN
# =========================================================

def main():

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

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
