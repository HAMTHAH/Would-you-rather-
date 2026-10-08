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
    ("Kiss your crush 😳", "Get $1,000,000 💰"),
    ("Know who secretly likes you ❤️", "Know who secretly hates you 😈"),
    ("Go on a date with your crush 💕", "Get $100,000 💰"),
    ("Text your crush 'I love you' by accident 😭", "Send them your search history 💀"),
    ("Be extremely attractive 😏", "Be extremely rich 💰"),
    ("Have your crush kiss you 💋", "Have your crush confess their feelings ❤️"),
    ("Lose your phone for a week 📱", "Lose the internet for a month 🌐"),
    ("Read minds 🧠", "Become invisible 👻"),
    ("Your ex says 'I miss you' 😳", "Your crush says 'I want you' 🔥"),
    ("Reveal your biggest secret 🤐", "Reveal your biggest crush 😳"),
    ("Spend a night with your celebrity crush ⭐", "Receive $100,000 💰"),
    ("Never lie again 😇", "Everyone knows when you're lying 🤥"),
    ("Have unlimited money 💰", "Have unlimited free time 😎"),
    ("Accidentally like your crush's old photo 😭", "Accidentally comment '😍' on it 💀"),
    ("Your crush calls you at midnight 🌙", "Wake up to a romantic message ❤️"),
    ("Be stuck in an elevator with your crush 😏", "Be stuck in a car with your ex 😭"),
    ("Date someone extremely jealous 😈", "Date someone who never gets jealous 😐"),
    ("Know your partner's entire past 👀", "Let them know yours 👀"),
    ("Get caught flirting 😳", "Get caught lying about flirting 💀"),
    ("Your crush sees your private photos 😳", "Your crush hears your thoughts 🧠"),
    ("Always know when someone is lying 🤥", "Always get away with lying 😈"),
    ("Have your first kiss again 💋", "Have your best kiss again 🔥"),
    ("Become famous worldwide 🌎", "Be anonymous but extremely rich 💰"),
    ("Date your best friend ❤️", "Never date anyone again 😭"),
    ("Receive a surprise kiss 💋", "Give someone a surprise kiss 😏"),
    ("Your crush calls you beautiful 😍", "Your crush says they can't stop thinking about you ❤️"),
    ("Send a spicy photo to your family by accident 😭", "Send it to your boss 💀"),
    ("Give your partner your passwords 🔐", "Give them your entire search history 📱"),
    ("Spend Valentine's Day alone 😭", "Spend it with someone you don't love 😐"),
    ("Have your crush reject you 💔", "Never know if they liked you"),
    ("Kiss someone you don't like 😳", "Never kiss anyone again"),
    ("Have one perfect relationship ❤️", "Date lots of people but never fall in love"),
    ("Walk in while your crush is changing 👀", "Have your crush walk in while you're changing 😳"),
    ("Know exactly who your soulmate is ❤️", "Never know but eventually meet them"),
    ("Teleport anywhere 🌎", "Pause time ⏸️"),
    ("Have $10 million 💰", "Find your soulmate tomorrow ❤️"),
    ("Always be 10 minutes late ⏰", "Always be 30 minutes early"),
    ("Be extremely funny 😂", "Be extremely attractive 😏"),
    ("Have your crush call you every night 🌙", "Have them text you all day 📱"),
    ("Confess your feelings first ❤️", "Wait for them to confess"),
    ("Have your crush secretly stalk your profile 👀", "Have them secretly ask their friends about you 😏"),
    ("Know your partner's biggest secret 🤫", "Have them know yours"),
    ("Get one unforgettable kiss 💋", "Get one unforgettable date ❤️"),
    ("Flirt with your crush for a year 😏", "Date them for one month ❤️"),
    ("Have your crush compliment you every day 😍", "Have them hug you every day 🤗"),
    ("Never get rejected again 😎", "Never get ghosted again 👻"),
    ("Have your crush call you at 3 AM 🌙", "Receive a 'I miss you' text at 3 AM 📱"),
    ("Be able to see your future 🔮", "Be able to change your past ⏳"),
]


# =========================================================
# INLINE GAME
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
        description="Start a 2-player game",
        input_message_content=InputTextMessageContent(
            "🎮 <b>WOULD YOU RATHER</b>\n\n"
            "👥 <b>2-player game</b>\n\n"
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
# CREATE GAME
# =========================================================

async def start_game(update: Update, context):

    query = update.callback_query
    await query.answer()

    game_id = str(uuid.uuid4())

    games[game_id] = {
        "player1": None,
        "player2": None,
        "question": None,
        "round": 0,
        "answers": {},
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
        "Both players can join by tapping:\n\n"
        "👤 <b>JOIN GAME</b>",
        parse_mode="HTML",
        reply_markup=keyboard,
    )


# =========================================================
# JOIN GAME
# =========================================================

async def join_game(update: Update, context):

    query = update.callback_query
    user = query.from_user

    game_id = query.data.split(":", 1)[1]

    if game_id not in games:
        await query.answer(
            "❌ Game no longer exists.",
            show_alert=True
        )
        return

    game = games[game_id]

    # PLAYER 1
    if game["player1"] is None:

        game["player1"] = {
            "id": user.id,
            "name": user.first_name,
        }

        await query.answer("✅ You joined as Player 1!")

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
            f"👤 Player 1: <b>{user.first_name}</b>\n"
            "👤 Player 2: <i>Waiting...</i>\n\n"
            "Send the game to your friend.",
            parse_mode="HTML",
            reply_markup=keyboard,
        )

        return

    # SAME PLAYER
    if game["player1"]["id"] == user.id:

        await query.answer(
            "You already joined the game.",
            show_alert=True
        )
        return

    # PLAYER 2
    if game["player2"] is None:

        game["player2"] = {
            "id": user.id,
            "name": user.first_name,
        }

        await query.answer("🔥 You joined as Player 2!")

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

    # Clear answers for new round
    game["answers"] = {}

    p1 = game["player1"]
    p2 = game["player2"]

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
        f"👤 <b>{p1['name']}</b>\n"
        f"👤 <b>{p2['name']}</b>\n\n"
        f"🔥 <b>ROUND {game['round']}</b>\n\n"
        f"<b>🅰️ A:</b> {a}\n\n"
        f"<b>🅱️ B:</b> {b}\n\n"
        "👇 <b>BOTH PLAYERS CHOOSE!</b>",
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

    p1 = game["player1"]
    p2 = game["player2"]

    # CHECK PLAYER
    if user.id not in [p1["id"], p2["id"]]:

        await query.answer(
            "❌ You are not one of the players.",
            show_alert=True
        )
        return

    # ALREADY ANSWERED
    if user.id in game["answers"]:

        await query.answer(
            "✅ You already answered!",
            show_alert=True
        )
        return

    # SAVE ANSWER
    game["answers"][user.id] = choice

    await query.answer(
        f"✅ You chose {'A' if choice == 'A' else 'B'}!"
    )

    # =====================================================
    # ONLY ONE PLAYER ANSWERED
    # =====================================================

    if len(game["answers"]) == 1:

        answered_player = (
            p1 if user.id == p1["id"] else p2
        )

        waiting_player = (
            p2 if user.id == p1["id"] else p1
        )

        await query.edit_message_text(
            "🎮 <b>WOULD YOU RATHER</b>\n\n"
            f"🔥 <b>ROUND {game['round']}</b>\n\n"
            f"✅ {answered_player['name']} has answered!\n"
            f"⏳ Waiting for {waiting_player['name']}...\n\n"
            "The other player can choose now.",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([
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
        )

        return

    # =====================================================
    # BOTH PLAYERS ANSWERED
    # =====================================================

    answer1 = game["answers"][p1["id"]]
    answer2 = game["answers"][p2["id"]]

    a1 = "🅰️ A" if answer1 == "A" else "🅱️ B"
    a2 = "🅰️ A" if answer2 == "A" else "🅱️ B"

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
        f"🔥 <b>ROUND {game['round']} RESULTS</b>\n\n"
        f"👤 <b>{p1['name']}</b>\n"
        f"👉 {a1}\n\n"
        f"👤 <b>{p2['name']}</b>\n"
        f"👉 {a2}\n\n"
        "━━━━━━━━━━━━━━\n\n"
        "🎉 <b>BOTH PLAYERS ANSWERED!</b>",
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

    # Anyone playing can start next round
    if query.from_user.id not in [
        game["player1"]["id"],
        game["player2"]["id"]
    ]:
        await query.answer(
            "❌ You are not a player.",
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

    players = []

    if game["player1"]:
        players.append(game["player1"]["id"])

    if game["player2"]:
        players.append(game["player2"]["id"])

    if user_id not in players:

        await query.answer(
            "❌ Only players can end the game.",
            show_alert=True
        )
        return

    await query.answer()

    del games[game_id]

    await query.edit_message_text(
        "🎮 <b>WOULD YOU RATHER</b>\n\n"
        "❌ <b>GAME ENDED</b>\n\n"
        "🔥 Thanks for playing!",
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
# START COMMAND
# =========================================================

async def start(update: Update, context):

    await update.message.reply_text(
        "🎮 <b>WOULD YOU RATHER</b>\n\n"
        "2-player game.\n\n"
        "Type @wouldyouratherobot in a chat "
        "to play.",
        parse_mode="HTML",
    )


# =========================================================
# MAIN
# =========================================================

def main():

    app = Application.builder().token(TOKEN).build()

    app.add_handler(
        CommandHandler("start", start)
    )

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
