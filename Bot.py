import os
import random
import logging

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# ============================================================
# SETTINGS
# ============================================================

BOT_TOKEN = os.environ["BOT_TOKEN"]

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# ============================================================
# WOULD YOU RATHER QUESTIONS
# ============================================================

QUESTIONS = [

    (
        "Would you rather get a romantic surprise date 💕 "
        "or a surprise weekend trip with someone you like? ✈️"
    ),

    (
        "Would you rather kiss your crush 😏 "
        "or have your crush confess their feelings to you? ❤️"
    ),

    (
        "Would you rather spend an entire night talking with your crush 🌙 "
        "or spend the entire day on a private date together? 😏"
    ),

    (
        "Would you rather receive a flirty good-morning text every day ☀️ "
        "or a flirty good-night text every night? 🌙"
    ),

    (
        "Would you rather have your crush hold your hand in public 🥰 "
        "or whisper something sweet in your ear? 😏"
    ),

    (
        "Would you rather go on a beach date 🌊 "
        "or a late-night city date? 🌃"
    ),

    (
        "Would you rather have someone remember every little thing about you ❤️ "
        "or always know exactly how to make you smile? 😏"
    ),

    (
        "Would you rather be stuck in an elevator with your crush 😳 "
        "or stuck in a car with them during a storm? 🌧️"
    ),

    (
        "Would you rather get a surprise kiss 😘 "
        "or a surprise hug from someone you really like? 🥰"
    ),

    (
        "Would you rather your crush compliment your face 😏 "
        "or compliment your body? 🔥"
    ),

    (
        "Would you rather have a romantic dinner for two 🍷 "
        "or a cozy movie night together? 🎬"
    ),

    (
        "Would you rather receive 100 flirty messages 📱 "
        "or one unforgettable date? ❤️"
    ),

    (
        "Would you rather have someone stare at you from across the room 👀 "
        "or come over and whisper something flirty to you? 😏"
    ),

    (
        "Would you rather accidentally send your crush a flirty message 😳 "
        "or accidentally like their oldest photo? 💀"
    ),

    (
        "Would you rather your crush know exactly who you like ❤️ "
        "or know your biggest secret? 👀"
    ),

    (
        "Would you rather have a slow romantic dance 💃 "
        "or a spontaneous adventure together? 🔥"
    ),

    (
        "Would you rather wake up next to your crush after a perfect date ❤️ "
        "or fall asleep talking to them on the phone? 📱"
    ),

    (
        "Would you rather have someone constantly tease you 😏 "
        "or constantly compliment you? 🔥"
    ),

    (
        "Would you rather have your crush choose your outfit 👗 "
        "or choose your date location? 😏"
    ),

    (
        "Would you rather share one secret with your crush 🤫 "
        "or hear one of theirs? 👀"
    ),

    (
        "Would you rather be called beautiful/handsome every day ❤️ "
        "or be called irresistible every night? 😏"
    ),

    (
        "Would you rather spend Valentine's Day together 💕 "
        "or celebrate your birthday together? 🎂"
    ),

    (
        "Would you rather receive flowers unexpectedly 🌹 "
        "or receive a handwritten love letter? 💌"
    ),

    (
        "Would you rather have someone flirt with you all night 😏 "
        "or make you laugh all night? 😂"
    ),

    (
        "Would you rather go on a secret date 🤫 "
        "or a very public romantic date? ❤️"
    ),

    (
        "Would you rather have your crush call you at midnight 🌙 "
        "or text you first every morning? ☀️"
    ),

    (
        "Would you rather be caught staring at your crush 👀 "
        "or be caught smiling at their messages? 😏"
    ),

    (
        "Would you rather know exactly what your crush thinks about you ❤️ "
        "or exactly what they dream about? 👀"
    ),

    (
        "Would you rather have chemistry immediately 🔥 "
        "or slowly develop an intense connection? ❤️"
    ),

    (
        "Would you rather have one amazing date you never forget 😏 "
        "or many cute dates together? 🥰"
    ),

    (
        "Would you rather be someone's biggest crush ❤️ "
        "or someone's secret obsession? 😏"
    ),

    (
        "Would you rather get a mysterious flirty text 👀 "
        "or a mysterious late-night phone call? 🌙"
    ),

    (
        "Would you rather sit next to your crush all night 😏 "
        "or have them sit across from you staring at you? 👀"
    ),

    (
        "Would you rather have someone compliment your smile 😊 "
        "or your eyes? 👀"
    ),

    (
        "Would you rather have your crush plan the perfect date ❤️ "
        "or let you plan it? 😏"
    ),

    (
        "Would you rather have a secret admirer 🤫 "
        "or secretly admire someone yourself? 👀"
    ),

    (
        "Would you rather be kissed under the stars 🌌 "
        "or during a rainy night? 🌧️"
    ),

    (
        "Would you rather have someone hold you close during a movie 🥰 "
        "or hold your hand during dinner? ❤️"
    ),

    (
        "Would you rather receive a voice message from your crush 🎙️ "
        "or a surprise video call? 📱"
    ),

    (
        "Would you rather spend a whole night laughing together 😂 "
        "or talking about your deepest secrets? ❤️"
    ),

    (
        "Would you rather have your crush steal your hoodie 😏 "
        "or steal your heart? ❤️"
    ),

    (
        "Would you rather be the first person they text every morning ☀️ "
        "or the last person they text every night? 🌙"
    ),

    (
        "Would you rather have someone flirt with you using eye contact 👀 "
        "or words? 😏"
    ),

    (
        "Would you rather have a romantic picnic 🧺 "
        "or a candlelit dinner? 🕯️"
    ),

    (
        "Would you rather spend a weekend alone with your crush ❤️ "
        "or go on a group trip where they secretly flirt with you? 😏"
    ),

    (
        "Would you rather know someone's biggest crush 👀 "
        "or their biggest secret? 🤫"
    ),

    (
        "Would you rather get caught flirting 😏 "
        "or catch someone flirting with you? 👀"
    ),

    (
        "Would you rather have someone make the first move 🔥 "
        "or make the first move yourself? 😏"
    ),

    (
        "Would you rather have a relationship full of playful teasing 😈 "
        "or endless romantic moments? ❤️"
    ),

    (
        "Would you rather get a surprise kiss on the cheek 😘 "
        "or a long hug? 🥰"
    ),

    (
        "Would you rather have someone remember your favorite song 🎵 "
        "or your favorite food? ❤️"
    ),

    (
        "Would you rather spend the night talking about your future 🌙 "
        "or planning your next adventure? ✈️"
    ),

    (
        "Would you rather have your crush call you cute 🥰 "
        "or irresistible? 😏"
    ),

    (
        "Would you rather have someone stare at you silently 👀 "
        "or tell you exactly what they're thinking? 😏"
    ),

    (
        "Would you rather receive a romantic surprise at home 🏠 "
        "or at a fancy restaurant? 🍷"
    ),

    (
        "Would you rather have someone make you blush 😳 "
        "or make you laugh uncontrollably? 😂"
    ),

    (
        "Would you rather have one unforgettable kiss 😘 "
        "or one unforgettable date? ❤️"
    ),

    (
        "Would you rather have your crush know your type 👀 "
        "or know that they're your type? 😏"
    ),

    (
        "Would you rather get a flirty compliment from a stranger 😏 "
        "or from your crush? ❤️"
    ),

    (
        "Would you rather spend a rainy day cuddled up watching movies 🌧️ "
        "or go out for a spontaneous adventure? 🔥"
    ),

    (
        "Would you rather have your crush send you a selfie 📸 "
        "or ask you to send one? 😏"
    ),

    (
        "Would you rather receive a mysterious love letter 💌 "
        "or an anonymous gift? 🎁"
    ),

    (
        "Would you rather have someone fall for your personality ❤️ "
        "or your looks? 😏"
    ),

    (
        "Would you rather be someone's first love ❤️ "
        "or their unforgettable love? 🔥"
    ),

    (
        "Would you rather have your crush accidentally reveal they like you 😳 "
        "or confess directly? ❤️"
    ),

    (
        "Would you rather go on a midnight drive 🌙 "
        "or watch the sunrise together? 🌅"
    ),

    (
        "Would you rather have someone call you their favorite person ❤️ "
        "or their biggest temptation? 😏"
    ),

    (
        "Would you rather be teased all evening 😈 "
        "or complimented all evening? 🔥"
    ),

    (
        "Would you rather have your crush sit extremely close to you 😏 "
        "or keep making intense eye contact? 👀"
    ),

    (
        "Would you rather receive a surprise date invitation 📱 "
        "or a surprise visit? ❤️"
    ),

    (
        "Would you rather have someone know exactly how to make you blush 😳 "
        "or exactly how to make you laugh? 😂"
    ),

    (
        "Would you rather have a romantic rooftop date 🌃 "
        "or a private beach date? 🌊"
    ),

    (
        "Would you rather have your crush tell their friends about you ❤️ "
        "or keep you as their secret? 🤫"
    ),

    (
        "Would you rather be asked out unexpectedly 😏 "
        "or ask someone out yourself? 🔥"
    ),

    (
        "Would you rather have someone flirt with you through texts 📱 "
        "or face-to-face? 👀"
    ),

    (
        "Would you rather have a crush on your best friend 😳 "
        "or have your best friend secretly crush on you? ❤️"
    ),

    (
        "Would you rather know who secretly likes you 👀 "
        "or never know and keep the mystery? 😏"
    ),

    (
        "Would you rather have someone make the first romantic move ❤️ "
        "or give you obvious hints? 👀"
    ),

    (
        "Would you rather spend your dream vacation with your crush ✈️ "
        "or your dream date with them at home? 😏"
    ),

    (
        "Would you rather receive a 2 AM 'I miss you' text 🌙 "
        "or a 7 AM 'good morning' text? ☀️"
    ),

    (
        "Would you rather have your crush compliment your outfit 👗 "
        "or your confidence? 🔥"
    ),

    (
        "Would you rather accidentally reveal your crush 😳 "
        "or accidentally reveal your biggest secret? 🤫"
    ),

    (
        "Would you rather have someone make you nervous 😏 "
        "or completely comfortable around them? ❤️"
    ),

    (
        "Would you rather have instant chemistry 🔥 "
        "or a slow-burn connection? ❤️"
    ),

    (
        "Would you rather receive a surprise kiss 😘 "
        "or be asked for one? 😏"
    ),

    (
        "Would you rather have someone say 'I want you' ❤️ "
        "or 'I can't stop thinking about you'? 😏"
    ),

    (
        "Would you rather be someone's secret crush 🤫 "
        "or their obvious crush? 👀"
    ),

    (
        "Would you rather have a romantic conversation until sunrise 🌅 "
        "or a spontaneous adventure until sunrise? 🔥"
    ),

    (
        "Would you rather have your crush know your deepest secret 🤫 "
        "or your biggest fantasy? 😏"
    ),

    (
        "Would you rather spend one perfect night together 🌙 "
        "or one perfect weekend together? ❤️"
    ),

    (
        "Would you rather have someone constantly make you smile 🥰 "
        "or constantly make you blush? 😏"
    ),

    (
        "Would you rather have your crush choose the first date location ❤️ "
        "or the second date? 😏"
    ),

    (
        "Would you rather have someone secretly screenshot your selfies 📸 "
        "or secretly save your messages? 👀"
    ),

    (
        "Would you rather be called gorgeous/handsome 😏 "
        "or irresistible? 🔥"
    ),

    (
        "Would you rather have a secret romantic connection 🤫 "
        "or a very obvious one? ❤️"
    ),

    (
        "Would you rather know your crush's biggest turn-on 😏 "
        "or their biggest weakness? 👀"
    ),

    (
        "Would you rather have your crush send the first message 📱 "
        "or make the first call? ❤️"
    ),

    (
        "Would you rather have a date that ends with a kiss 😘 "
        "or one that leaves you wanting another date? 😏"
    ),

    (
        "Would you rather be impossible to forget 🖤 "
        "or impossible to resist? 🔥"
    ),
]


# ============================================================
# ACTIVE GAMES
# ============================================================

games = {}


# ============================================================
# CREATE GAME
# ============================================================

def create_game(player1_id, player1_name, player2_id, player2_name):

    game_id = f"{player1_id}_{player2_id}"

    games[game_id] = {
        "player1": player1_id,
        "player1_name": player1_name,

        "player2": player2_id,
        "player2_name": player2_name,

        "round": 0,

        "question": None,

        "answer1": None,
        "answer2": None,

        "message_id": None,
    }

    return game_id


# ============================================================
# FIND GAME FOR USER
# ============================================================

def find_game(user_id):

    for game_id, game in games.items():

        if (
            game["player1"] == user_id
            or game["player2"] == user_id
        ):
            return game_id, game

    return None, None


# ============================================================
# /START
# ============================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    game_id, existing_game = find_game(user.id)

    if existing_game:

        await update.message.reply_text(
            "🎮 You're already in a game!\n\n"
            f"👤 Opponent: "
            f"{existing_game['player2_name'] if existing_game['player1'] == user.id else existing_game['player1_name']}"
        )

        return

    await update.message.reply_text(
        "🔥 WOULD YOU RATHER\n\n"
        "A 2-player game of difficult choices 😏\n\n"
        "To play:\n\n"
        "1️⃣ Send this bot to your friend.\n"
        "2️⃣ Both players open the bot.\n"
        "3️⃣ One player creates a game.\n\n"
        "Use /newgame to create a game."
    )


# ============================================================
# /NEWGAME
# ============================================================

async def new_game(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    game_id, existing_game = find_game(user.id)

    if existing_game:

        await update.message.reply_text(
            "⚠️ You're already in a game.\n"
            "Use /leave first."
        )

        return

    keyboard = [
        [
            InlineKeyboardButton(
                "🎮 CREATE GAME",
                callback_data="create_game"
            )
        ]
    ]

    await update.message.reply_text(
        "🔥 WOULD YOU RATHER\n\n"
        "Ready to challenge someone?\n\n"
        "Tap the button below to create a game.",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# ============================================================
# CREATE GAME BUTTON
# ============================================================

async def create_game_button(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    user = query.from_user

    game_id, existing_game = find_game(user.id)

    if existing_game:

        await query.edit_message_text(
            "⚠️ You're already in a game."
        )

        return

    keyboard = [
        [
            InlineKeyboardButton(
                "👥 JOIN MY GAME",
                callback_data=f"join_{user.id}"
            )
        ]
    ]

    await query.edit_message_text(
        "🎮 GAME CREATED!\n\n"
        f"👤 Player 1: {user.first_name}\n\n"
        "Send this message to your friend and have them "
        "press JOIN MY GAME.\n\n"
        "👇",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# ============================================================
# JOIN GAME
# ============================================================

async def join_game(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    player2 = query.from_user

    player1_id = int(
        query.data.split("_")[1]
    )

    if player1_id == player2.id:

        await query.answer(
            "You can't join your own game!",
            show_alert=True
        )

        return

    game_id, existing_game = find_game(player2.id)

    if existing_game:

        await query.answer(
            "You're already in another game.",
            show_alert=True
        )

        return

    # Get Player 1 information
    try:

        player1 = await context.bot.get_chat(
            player1_id
        )

        player1_name = player1.first_name

    except Exception:

        player1_name = "Player 1"

    game_id = create_game(
        player1_id,
        player1_name,
        player2.id,
        player2.first_name
    )

    game = games[game_id]

    await query.edit_message_text(
        "🔥 GAME STARTED!\n\n"
        f"👤 {player1_name}\n"
        f"👤 {player2.first_name}\n\n"
        "Get ready for some difficult choices... 😏"
    )

    await send_question(
        context,
        game_id
    )


# ============================================================
# SEND QUESTION
# ============================================================

async def send_question(
    context,
    game_id
):

    game = games.get(game_id)

    if not game:
        return

    game["round"] += 1

    game["answer1"] = None
    game["answer2"] = None

    question = random.choice(
        QUESTIONS
    )

    game["question"] = question

    keyboard = [
        [
            InlineKeyboardButton(
                "🔥 OPTION A",
                callback_data=f"answer_A_{game_id}"
            )
        ],
        [
            InlineKeyboardButton(
                "😈 OPTION B",
                callback_data=f"answer_B_{game_id}"
            )
        ],
    ]

    text = (
        f"🔥 WOULD YOU RATHER — ROUND {game['round']}\n\n"
        f"{question}\n\n"
        "Choose your answer below 👇\n\n"
        "Both players must answer."
    )

    # Send to both players
    for player_id in [
        game["player1"],
        game["player2"]
    ]:

        try:

            await context.bot.send_message(
                chat_id=player_id,
                text=text,
                reply_markup=InlineKeyboardMarkup(
                    keyboard
                )
            )

        except Exception as error:

            print(
                f"Could not message {player_id}: {error}"
            )


# ============================================================
# ANSWER
# ============================================================

async def answer(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    data = query.data

    parts = data.split("_")

    answer_value = parts[1]

    game_id = "_".join(parts[2:])

    game = games.get(game_id)

    if not game:

        await query.answer(
            "This game no longer exists.",
            show_alert=True
        )

        return

    user_id = query.from_user.id

    # Player 1
    if user_id == game["player1"]:

        if game["answer1"] is not None:

            await query.answer(
                "You already answered!",
                show_alert=True
            )

            return

        game["answer1"] = answer_value

        player_name = game["player1_name"]

    # Player 2
    elif user_id == game["player2"]:

        if game["answer2"] is not None:

            await query.answer(
                "You already answered!",
                show_alert=True
            )

            return

        game["answer2"] = answer_value

        player_name = game["player2_name"]

    else:

        await query.answer(
            "You're not part of this game.",
            show_alert=True
        )

        return

    await query.edit_message_reply_markup(
        reply_markup=None
    )

    # Tell player their answer was recorded
    await context.bot.send_message(
        chat_id=user_id,
        text=(
            f"✅ {player_name}, your answer is recorded!\n\n"
            "Waiting for the other player..."
        )
    )

    # Both answered
    if (
        game["answer1"] is not None
        and game["answer2"] is not None
    ):

        await reveal_answers(
            context,
            game_id
        )


# ============================================================
# REVEAL ANSWERS
# ============================================================

async def reveal_answers(
    context,
    game_id
):

    game = games.get(game_id)

    if not game:
        return

    a1 = game["answer1"]
    a2 = game["answer2"]

    same = a1 == a2

    a1_text = (
        "🔥 OPTION A"
        if a1 == "A"
        else
        "😈 OPTION B"
    )

    a2_text = (
        "🔥 OPTION A"
        if a2 == "A"
        else
        "😈 OPTION B"
    )

    if same:

        result = (
            "🔥 SAME ANSWER!\n\n"
            "You two are definitely on the same wavelength. 😏"
        )

    else:

        result = (
            "👀 DIFFERENT ANSWERS!\n\n"
            "Now you know where you disagree... 😈"
        )

    text = (
        f"🎯 ROUND {game['round']} RESULTS\n\n"
        f"👤 {game['player1_name']}: {a1_text}\n"
        f"👤 {game['player2_name']}: {a2_text}\n\n"
        f"{result}"
    )

    keyboard = [
        [
            InlineKeyboardButton(
                "🔥 NEXT QUESTION",
                callback_data=f"next_{game_id}"
            )
        ],
        [
            InlineKeyboardButton(
                "🛑 LEAVE GAME",
                callback_data=f"leave_{game_id}"
            )
        ],
    ]

    for player_id in [
        game["player1"],
        game["player2"]
    ]:

        try:

            await context.bot.send_message(
                chat_id=player_id,
                text=text,
                reply_markup=InlineKeyboardMarkup(
                    keyboard
                )
            )

        except Exception as error:

            print(
                f"Reveal error: {error}"
            )


# ============================================================
# NEXT QUESTION
# ============================================================

async def next_question(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    game_id = "_".join(
        query.data.split("_")[1:]
    )

    game = games.get(game_id)

    if not game:
        return

    # Only send next question once.
    if game.get("next_started"):
        return

    game["next_started"] = True

    await send_question(
        context,
        game_id
    )

    game["next_started"] = False


# ============================================================
# LEAVE GAME
# ============================================================

async def leave_game(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    game_id = "_".join(
        query.data.split("_")[1:]
    )

    game = games.get(game_id)

    if not game:
        return

    player_name = query.from_user.first_name

    for player_id in [
        game["player1"],
        game["player2"]
    ]:

        try:

            await context.bot.send_message(
                chat_id=player_id,
                text=(
                    "🛑 GAME ENDED\n\n"
                    f"{player_name} left the game.\n\n"
                    "Use /newgame to start another game."
                )
            )

        except Exception:
            pass

    del games[game_id]


# ============================================================
# BUTTON ROUTER
# ============================================================

async def button_router(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    data = query.data

    if data == "create_game":

        await create_game_button(
            update,
            context
        )

    elif data.startswith("join_"):

        await join_game(
            update,
            context
        )

    elif data.startswith("answer_"):

        await answer(
            update,
            context
        )

    elif data.startswith("next_"):

        await next_question(
            update,
            context
        )

    elif data.startswith("leave_"):

        await leave_game(
            update,
            context
        )


# ============================================================
# /LEAVE
# ============================================================

async def leave_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user_id = update.effective_user.id

    game_id, game = find_game(
        user_id
    )

    if not game:

        await update.message.reply_text(
            "You aren't currently in a game."
        )

        return

    for player_id in [
        game["player1"],
        game["player2"]
    ]:

        try:

            await context.bot.send_message(
                chat_id=player_id,
                text=(
                    "🛑 GAME ENDED\n\n"
                    f"{update.effective_user.first_name} "
                    "left the game."
                )
            )

        except Exception:
            pass

    del games[game_id]


# ============================================================
# MAIN
# ============================================================

def main():

    print(
        "================================"
    )

    print(
        "WOULD YOU RATHER BOT"
    )

    print(
        "================================"
    )

    application = (
        Application.builder()
        .token(BOT_TOKEN)
        .build()
    )

    application.add_handler(
        CommandHandler(
            "start",
            start
        )
    )

    application.add_handler(
        CommandHandler(
            "newgame",
            new_game
        )
    )

    application.add_handler(
        CommandHandler(
            "leave",
            leave_command
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            button_router
        )
    )

    print(
        "BOT IS RUNNING..."
    )

    application.run_polling()


# ============================================================
# START
# ============================================================

if __name__ == "__main__":
    main()
