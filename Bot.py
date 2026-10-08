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
    ContextTypes,
)

# =========================================================
# SETTINGS
# =========================================================

TOKEN = os.environ["BOT_TOKEN"]

# Active games
games = {}

# =========================================================
# WOULD YOU RATHER QUESTIONS
# =========================================================

QUESTIONS = [
    ("Would you rather kiss your crush in front of everyone 😳",
     "or let your crush read your private messages 📱?"),

    ("Would you rather know who secretly likes you ❤️",
     "or know who secretly hates you 😈?"),

    ("Would you rather go on a date with your crush 💕",
     "or get $1,000,000 💰?"),

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
     "or accidentally comment on it '😍' 💀?"),

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

    ("Would you rather have your crush see you naked 😳",
     "or hear every thought you've ever had about them 🧠?"),

    ("Would you rather always know when someone is lying 🤥",
     "or always get away with lying 😈?"),

    ("Would you rather have your first kiss again 💋",
     "or your best kiss again 🔥?"),

    ("Would you rather be famous worldwide 🌎",
     "or completely anonymous but extremely rich 💰?"),

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

    ("Would you rather be able to teleport anywhere 🌎",
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
# START MESSAGE
# =========================================================

def start_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "🎮 START GAME",
                callback_data="create_game"
            )
        ]
    ])


# =========================================================
# INLINE MODE
# =========================================================

async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query

    game_id = str(uuid.uuid4())[:8]

    text = (
        "🎮 <b>WOULD YOU RATHER</b>\n\n"
        "👥 <b>2-player private game</b>\n\n"
        "Tap <b>START GAME</b> to create a game.\n\n"
        "🔥 Challenge a friend and see what they choose!"
    )

    result = InlineQueryResultArticle(
        id=game_id,
        title="🎮 Would You Rather",
        description="Start a 2-player private game",
        input_message_content=InputTextMessageContent(
            text=text,
            parse_mode="HTML"
        ),
        reply_markup=start_keyboard()
    )

    await update.inline_query.answer(
        [result],
        cache_time=0,
        is_personal=True
    )


# =========================================================
# CREATE GAME
# =========================================================

async def create_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    chat_id = query.message.chat_id
    message_id = query.message.message_id

    game_id = f"{chat_id}_{message_id}"

    games[game_id] = {
        "chat_id": chat_id,
        "message_id": message_id,
        "player1": None,
        "player2": None,
        "turn": None,
        "question": None,
        "question_number": 0,
    }

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "👤 JOIN GAME",
                callback_data=f"join:{game_id}"
            )
        ],
        [
            InlineKeyboardButton(
                "❌ CANCEL",
                callback_data=f"cancel:{game_id}"
            )
        ]
    ])

    await query.edit_message_text(
        "🎮 <b>WOULD YOU RATHER</b>\n\n"
        "🔥 <b>GAME CREATED!</b>\n\n"
        "👥 This game needs 2 players.\n\n"
        "Player 1: Waiting...\n"
        "Player 2: Waiting...\n\n"
        "Tap <b>JOIN GAME</b> to join.",
        parse_mode="HTML",
        reply_markup=keyboard
    )


# =========================================================
# JOIN GAME
# =========================================================

async def join_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data
    game_id = data.split(":", 1)[1]

    if game_id not in games:
        await query.answer(
            "❌ This game no longer exists.",
            show_alert=True
        )
        return

    game = games[game_id]

    user = query.from_user

    player = user.first_name

    # Player 1
    if game["player1"] is None:
        game["player1"] = {
            "id": user.id,
            "name": player
        }

        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "👤 JOIN GAME",
                    callback_data=f"join:{game_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    "❌ CANCEL",
                    callback_data=f"cancel:{game_id}"
                )
            ]
        ])

        await query.edit_message_text(
            "🎮 <b>WOULD YOU RATHER</b>\n\n"
            "🔥 <b>GAME CREATED!</b>\n\n"
            f"👤 Player 1: <b>{player}</b>\n"
            "👤 Player 2: <i>Waiting...</i>\n\n"
            "Send this game to your friend!\n"
            "They should tap <b>JOIN GAME</b>.",
            parse_mode="HTML",
            reply_markup=keyboard
        )

        return

    # Don't allow same player twice
    if game["player1"]["id"] == user.id:
        await query.answer(
            "You are already Player 1.",
            show_alert=True
        )
        return

    # Player 2
    if game["player2"] is None:
        game["player2"] = {
            "id": user.id,
            "name": player
        }

        game["turn"] = game["player1"]["id"]

        await start_round(query, game_id)

        return

    # Game full
    await query.answer(
        "❌ This game already has 2 players.",
        show_alert=True
    )


# =========================================================
# START ROUND
# =========================================================

async def start_round(query, game_id):
    game = games[game_id]

    question = random.choice(QUESTIONS)

    game["question"] = question
    game["question_number"] += 1

    player1 = game["player1"]
    player2 = game["player2"]

    if game["turn"] == player1["id"]:
        current_player = player1
    else:
        current_player = player2

    text = (
        "🎮 <b>WOULD YOU RATHER</b>\n\n"
        f"👤 <b>{player1['name']}</b>\n"
        f"👤 <b>{player2['name']}</b>\n\n"
        f"🔥 <b>ROUND {game['question_number']}</b>\n\n"
        f"<b>{question[0]}</b>\n\n"
        f"<b>OR</b>\n\n"
        f"<b>{question[1]}</b>\n\n"
        f"🎯 <b>{current_player['name']}'s turn</b>"
    )

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "🅰️ OPTION A",
                callback_data=f"answer:A:{game_id}"
            ),
            InlineKeyboardButton(
                "🅱️ OPTION B",
                callback_data=f"answer:B:{game_id}"
            )
        ],
        [
            InlineKeyboardButton(
                "❌ END GAME",
                callback_data=f"cancel:{game_id}"
            )
        ]
    ])

    await query.edit_message_text(
        text,
        parse_mode="HTML",
        reply_markup=keyboard
    )


# =========================================================
# ANSWER
# =========================================================

async def answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    data = query.data.split(":")

    choice = data[1]
    game_id = ":".join(data[2:])

    if game_id not in games:
        await query.answer(
            "❌ Game no longer exists.",
            show_alert=True
        )
        return

    game = games[game_id]

    user = query.from_user

    # Check whose turn
    if user.id != game["turn"]:
        current_player = (
            game["player1"]
            if game["turn"] == game["player1"]["id"]
            else game["player2"]
        )

        await query.answer(
            f"⏳ Wait! It's {current_player['name']}'s turn.",
            show_alert=True
        )
        return

    await query.answer()

    question = game["question"]

    if choice == "A":
        chosen = question[0]
    else:
        chosen = question[1]

    player1 = game["player1"]
    player2 = game["player2"]

    current_player = (
        player1
        if user.id == player1["id"]
        else player2
    )

    # Switch turn
    if user.id == player1["id"]:
        game["turn"] = player2["id"]
        next_player = player2
    else:
        game["turn"] = player1["id"]
        next_player = player1

    text = (
        "🎮 <b>WOULD YOU RATHER</b>\n\n"
        f"🔥 <b>{current_player['name']} chose:</b>\n\n"
        f"👉 {chosen}\n\n"
        "━━━━━━━━━━━━━━\n\n"
        f"🎯 <b>{next_player['name']}'s turn!</b>\n\n"
        "Get ready for the next question..."
    )

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "🔥 NEXT QUESTION",
                callback_data=f"next:{game_id}"
            )
        ],
        [
            InlineKeyboardButton(
                "❌ END GAME",
                callback_data=f"cancel:{game_id}"
            )
        ]
    ])

    await query.edit_message_text(
        text,
        parse_mode="HTML",
        reply_markup=keyboard
    )


# =========================================================
# NEXT QUESTION
# =========================================================

async def next_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    game_id = query.data.split(":", 1)[1]

    if game_id not in games:
        await query.answer(
            "❌ Game no longer exists.",
            show_alert=True
        )
        return

    game = games[game_id]

    if query.from_user.id != game["turn"]:
        current_player = (
            game["player1"]
            if game["turn"] == game["player1"]["id"]
            else game["player2"]
        )

        await query.answer(
            f"⏳ It's {current_player['name']}'s turn.",
            show_alert=True
        )
        return

    await query.answer()

    await start_round(query, game_id)


# =========================================================
# CANCEL GAME
# =========================================================

async def cancel_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    game_id = query.data.split(":", 1)[1]

    if game_id not in games:
        await query.answer()
        return

    game = games[game_id]

    user = query.from_user

    # Only players can end it
    if (
        game["player1"]
        and user.id != game["player1"]["id"]
        and game["player2"]
        and user.id != game["player2"]["id"]
    ):
        await query.answer(
            "❌ Only the players can end this game.",
            show_alert=True
        )
        return

    await query.answer()

    del games[game_id]

    await query.edit_message_text(
        "🎮 <b>WOULD YOU RATHER</b>\n\n"
        "❌ <b>GAME ENDED</b>\n\n"
        "Thanks for playing! 🔥",
        parse_mode="HTML"
    )


# =========================================================
# CALLBACK ROUTER
# =========================================================

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = update.callback_query.data

    if data == "create_game":
        await create_game(update, context)

    elif data.startswith("join:"):
        await join_game(update, context)

    elif data.startswith("answer:"):
        await answer(update, context)

    elif data.startswith("next:"):
        await next_question(update, context)

    elif data.startswith("cancel:"):
        await cancel_game(update, context)


# =========================================================
# START COMMAND
# =========================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎮 <b>WOULD YOU RATHER</b>\n\n"
        "This is a 2-player game.\n\n"
        "To play inside a Telegram chat, type:\n\n"
        "<code>@YourBotUsername</code>\n\n"
        "and select the Would You Rather game.",
        parse_mode="HTML"
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

    print("🔥 Would You Rather bot is running...")

    app.run_polling()


if __name__ == "__main__":
    main()
