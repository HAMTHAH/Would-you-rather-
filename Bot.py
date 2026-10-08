import os
import random
import uuid
import html
import logging

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

BOT_TOKEN = os.environ["BOT_TOKEN"]

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# =========================================================
# WOULD YOU RATHER QUESTIONS
# =========================================================

QUESTIONS = [
    ("Would you rather", "be able to read minds", "be able to see the future"),
    ("Would you rather", "never use social media again", "never watch movies again"),
    ("Would you rather", "be rich but unknown", "be famous but only moderately wealthy"),
    ("Would you rather", "travel the world for free", "have a dream house for free"),
    ("Would you rather", "always know when someone is lying", "always get away with lying"),
    ("Would you rather", "have your crush read your mind", "read your crush's mind"),
    ("Would you rather", "send your crush a risky text", "call your crush unexpectedly"),
    ("Would you rather", "go on a surprise date", "plan every detail of the date"),
    ("Would you rather", "kiss your crush first", "wait for your crush to make the first move"),
    ("Would you rather", "have your best friend choose your date", "choose your best friend's date"),
    ("Would you rather", "be stuck on a date with your ex", "be stuck on a date with someone you hate"),
    ("Would you rather", "have unlimited money for one year", "have unlimited free travel for life"),
    ("Would you rather", "be extremely attractive", "be extremely charming"),
    ("Would you rather", "have perfect confidence", "have perfect looks"),
    ("Would you rather", "know exactly who likes you", "know exactly who dislikes you"),
    ("Would you rather", "receive a romantic message every morning", "receive a surprise gift every week"),
    ("Would you rather", "have your crush call you at midnight", "have your crush show up at your door"),
    ("Would you rather", "go on a beach date", "go on a rooftop date"),
    ("Would you rather", "have a secret admirer", "have a secret crush"),
    ("Would you rather", "flirt with someone you just met", "flirt with someone you've known for years"),
    ("Would you rather", "have your partner know your entire search history", "have them know every message you've ever sent"),
    ("Would you rather", "lose your phone for a week", "lose your wallet for a week"),
    ("Would you rather", "be caught staring at your crush", "be caught talking about your crush"),
    ("Would you rather", "accidentally text your crush something embarrassing", "accidentally text your parents something embarrassing"),
    ("Would you rather", "have your funniest moment go viral", "have your most embarrassing moment go viral"),
    ("Would you rather", "always say exactly what you're thinking", "never be able to explain yourself"),
    ("Would you rather", "have one perfect relationship", "have many exciting relationships"),
    ("Would you rather", "fall in love instantly", "fall in love slowly"),
    ("Would you rather", "date someone extremely romantic", "date someone extremely funny"),
    ("Would you rather", "have a partner who texts constantly", "have a partner who rarely texts"),
    ("Would you rather", "be the jealous one", "have a jealous partner"),
    ("Would you rather", "know your partner's biggest secret", "have them know yours"),
    ("Would you rather", "go on a spontaneous road trip", "have a luxury vacation planned for you"),
    ("Would you rather", "dance in public with your crush", "sing in public with your crush"),
    ("Would you rather", "get a surprise kiss", "give a surprise kiss"),
    ("Would you rather", "have your crush compliment you", "have your crush flirt with you"),
    ("Would you rather", "be able to pause time", "be able to rewind time"),
    ("Would you rather", "have unlimited food", "have unlimited money"),
    ("Would you rather", "live in a mansion alone", "live in a small house with your favorite people"),
    ("Would you rather", "be extremely lucky", "be extremely intelligent"),
    ("Would you rather", "never get embarrassed", "never get rejected"),
    ("Would you rather", "know your future partner's name", "know when you'll meet them"),
    ("Would you rather", "have your crush confess first", "confess first yourself"),
    ("Would you rather", "get flowers every week", "get chocolates every week"),
    ("Would you rather", "have a romantic dinner", "have a romantic movie night"),
    ("Would you rather", "be stuck in an elevator with your crush", "be stuck in traffic with your crush"),
    ("Would you rather", "have your crush call you cute", "have them call you attractive"),
    ("Would you rather", "have one unforgettable date", "have many good dates"),
    ("Would you rather", "be someone's first love", "be someone's last love"),
    ("Would you rather", "have a partner who is very protective", "have a partner who is very independent"),
    ("Would you rather", "always win arguments", "always avoid arguments"),
    ("Would you rather", "know every secret about your friends", "have none of your secrets known"),
    ("Would you rather", "have your crush accidentally see your notes about them", "have them hear you talking about them"),
    ("Would you rather", "go on a date without knowing where you're going", "choose exactly where you go"),
    ("Would you rather", "receive a handwritten love letter", "receive a long romantic text"),
    ("Would you rather", "have your crush remember every little detail about you", "have them surprise you constantly"),
    ("Would you rather", "have an adventurous partner", "have a calm partner"),
    ("Would you rather", "date someone who makes you laugh", "date someone who makes you feel safe"),
    ("Would you rather", "have your best friend as your roommate", "have your crush as your roommate"),
    ("Would you rather", "have unlimited confidence", "have unlimited charisma"),
    ("Would you rather", "be able to make anyone laugh", "be able to make anyone like you"),
    ("Would you rather", "have your crush send the first message", "have them call you first"),
    ("Would you rather", "go dancing together", "cook together"),
    ("Would you rather", "watch the sunrise together", "watch the sunset together"),
    ("Would you rather", "have a surprise birthday party", "have a surprise romantic date"),
    ("Would you rather", "always know what gift to buy", "always know what to say"),
    ("Would you rather", "have a partner who is extremely honest", "have one who is extremely understanding"),
    ("Would you rather", "be able to teleport anywhere", "fly anywhere"),
    ("Would you rather", "have your dream job", "have your dream relationship"),
    ("Would you rather", "be rich at 20", "be successful at 40"),
    ("Would you rather", "never have to sleep", "never have to eat"),
    ("Would you rather", "be able to speak every language", "be able to play every instrument"),
    ("Would you rather", "have a perfect memory", "have unlimited creativity"),
    ("Would you rather", "always be early", "always be exactly on time"),
    ("Would you rather", "have everyone admire you", "have a few people deeply love you"),
    ("Would you rather", "have your crush know you like them", "keep your crush guessing"),
    ("Would you rather", "be the one who makes the first move", "wait and see what happens"),
    ("Would you rather", "get a good morning text", "get a good night text"),
    ("Would you rather", "have a romantic nickname", "have a funny nickname"),
    ("Would you rather", "go on a fancy dinner date", "have a simple late-night date"),
    ("Would you rather", "be with someone adventurous", "be with someone mysterious"),
    ("Would you rather", "have a partner who is your best friend", "have a partner who challenges you"),
    ("Would you rather", "have your crush compliment your personality", "compliment your appearance"),
    ("Would you rather", "have one secret relationship", "have one public relationship"),
    ("Would you rather", "have your partner plan everything", "plan everything yourself"),
    ("Would you rather", "get caught flirting", "get caught checking someone's profile"),
    ("Would you rather", "have your crush sit next to you", "have them sit across from you"),
    ("Would you rather", "have a funny partner", "have a romantic partner"),
    ("Would you rather", "spend a whole day together", "spend one amazing hour together"),
    ("Would you rather", "have a partner who texts you memes", "texts you compliments"),
    ("Would you rather", "be someone's biggest crush", "be someone's biggest regret"),
    ("Would you rather", "have a perfect first date", "have an unforgettable second date"),
    ("Would you rather", "have your crush surprise you", "surprise your crush"),
    ("Would you rather", "be known as mysterious", "be known as charming"),
    ("Would you rather", "have your crush stare at you", "have them smile at you"),
    ("Would you rather", "get a secret admirer letter", "get an anonymous gift"),
    ("Would you rather", "know who your soulmate is", "know when you'll meet them"),
    ("Would you rather", "have your crush ask you out", "have them ask for your number"),
    ("Would you rather", "go on a midnight adventure", "have a lazy day together"),
    ("Would you rather", "have a partner who remembers everything", "have one who forgives everything"),
    ("Would you rather", "have someone fall for you first", "fall for someone first"),
    ("Would you rather", "be impossible to forget", "be impossible to replace"),
]

# =========================================================
# ACTIVE GAMES
# =========================================================

games = {}


# =========================================================
# HELPERS
# =========================================================

def new_question():
    return random.choice(QUESTIONS)


def player_name(user):
    return user.first_name or user.username or "Player"


def game_text(game):
    p1 = html.escape(game["p1_name"])
    p2 = html.escape(game["p2_name"])

    question, option_a, option_b = game["question"]

    answers = game["answers"]

    if game["status"] == "waiting":
        return (
            "🎮 <b>WOULD YOU RATHER</b>\n\n"
            f"👤 <b>Player 1:</b> {p1}\n"
            "👤 <b>Player 2:</b> Waiting...\n\n"
            "🔥 <b>Game created!</b>\n\n"
            "<i>Send this inline game to the person you're playing with, "
            "then they can tap JOIN GAME.</i>"
        )

    if game["status"] == "playing":
        answered = []

        if game["p1_id"] in answers:
            answered.append(p1)

        if game["p2_id"] in answers:
            answered.append(p2)

        status = ""

        if len(answered) == 1:
            status = (
                f"\n\n<i>{html.escape(answered[0])} has answered. "
                "Waiting for the other player...</i>"
            )
        else:
            status = "\n\n<i>Choose A or B. Your answer stays hidden.</i>"

        return (
            f"🔥 <b>WOULD YOU RATHER — ROUND {game['round']}</b>\n\n"
            f"👤 {p1}\n"
            f"👤 {p2}\n\n"
            f"<b>{html.escape(question)}</b>\n\n"
            f"🔥 <b>A)</b> {html.escape(option_a)}\n"
            f"😈 <b>B)</b> {html.escape(option_b)}"
            f"{status}"
        )

    if game["status"] == "results":
        answer1 = answers.get(game["p1_id"], "?")
        answer2 = answers.get(game["p2_id"], "?")

        a1 = "A" if answer1 == "A" else "B"
        a2 = "A" if answer2 == "A" else "B"

        return (
            f"🔥 <b>WOULD YOU RATHER — ROUND {game['round']}</b>\n\n"
            f"<b>{html.escape(question)}</b>\n\n"
            f"👤 <b>{p1}</b> chose <b>{a1}</b>\n"
            f"👤 <b>{p2}</b> chose <b>{a2}</b>\n\n"
            "😂 <i>Both answers revealed!</i>"
        )

    return "🛑 <b>GAME ENDED</b>"


def game_keyboard(game):
    if game["status"] == "waiting":
        return InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "🎮 JOIN GAME",
                    callback_data=f"join:{game['id']}"
                )
            ],
            [
                InlineKeyboardButton(
                    "🛑 LEAVE",
                    callback_data=f"leave:{game['id']}"
                )
            ],
        ])

    if game["status"] == "playing":
        return InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "🔥 A",
                    callback_data=f"a:{game['id']}"
                ),
                InlineKeyboardButton(
                    "😈 B",
                    callback_data=f"b:{game['id']}"
                ),
            ],
            [
                InlineKeyboardButton(
                    "🛑 LEAVE GAME",
                    callback_data=f"leave:{game['id']}"
                )
            ],
        ])

    if game["status"] == "results":
        return InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "🔥 NEXT QUESTION",
                    callback_data=f"next:{game['id']}"
                )
            ],
            [
                InlineKeyboardButton(
                    "🛑 END GAME",
                    callback_data=f"leave:{game['id']}"
                )
            ],
        ])

    return None


# =========================================================
# /START
# =========================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    username = context.bot.username or "YourBot"

    text = (
        "🎮 <b>WOULD YOU RATHER</b>\n\n"
        "Play a 2-player Would You Rather game directly "
        "inside your private chat.\n\n"
        "🔥 <b>How to play:</b>\n\n"
        f"1. Open your private chat with your friend.\n"
        f"2. Type <code>@{username}</code>\n"
        "3. Choose <b>🎮 Would You Rather</b>\n"
        "4. Tap <b>START GAME</b>\n"
        "5. Your friend taps <b>JOIN GAME</b>\n\n"
        "No group chat needed. 😈"
    )

    await update.message.reply_text(
        text,
        parse_mode="HTML"
    )


# =========================================================
# INLINE MODE
# =========================================================

async def inline_query(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "🎮 START GAME",
                callback_data="create"
            )
        ]
    ])

    message = (
        "🎮 <b>WOULD YOU RATHER</b>\n\n"
        "<i>2-player private game</i>\n\n"
        "Tap <b>START GAME</b> to create a game."
    )

    result = InlineQueryResultArticle(
        id=str(uuid.uuid4()),
        title="🎮 Would You Rather",
        description="Start a 2-player game in this private chat",
        input_message_content=InputTextMessageContent(
            message,
            parse_mode="HTML"
        ),
        reply_markup=keyboard,
    )

    await update.inline_query.answer(
        [result],
        cache_time=0,
        is_personal=True
    )


# =========================================================
# BUTTON HANDLER
# =========================================================

async def button_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    user = query.from_user
    data = query.data

    # -----------------------------------------------------
    # CREATE GAME
    # -----------------------------------------------------

    if data == "create":

        game_id = uuid.uuid4().hex[:10]

        question = new_question()

        game = {
            "id": game_id,
            "inline_message_id": query.inline_message_id,
            "p1_id": user.id,
            "p1_name": player_name(user),
            "p2_id": None,
            "p2_name": None,
            "round": 0,
            "question": question,
            "answers": {},
            "status": "waiting",
        }

        games[game_id] = game

        await query.edit_message_text(
            game_text(game),
            parse_mode="HTML",
            reply_markup=game_keyboard(game),
        )

        return

    # -----------------------------------------------------
    # GET GAME ID
    # -----------------------------------------------------

    try:
        action, game_id = data.split(":", 1)
    except ValueError:
        return

    game = games.get(game_id)

    if not game:
        await query.answer(
            "❌ This game no longer exists.",
            show_alert=True
        )
        return

    # -----------------------------------------------------
    # LEAVE GAME
    # -----------------------------------------------------

    if action == "leave":

        if user.id not in [game["p1_id"], game["p2_id"]]:
            await query.answer(
                "You are not part of this game.",
                show_alert=True
            )
            return

        game["status"] = "ended"

        await query.edit_message_text(
            "🛑 <b>GAME ENDED</b>\n\n"
            "<i>This Would You Rather game has been closed.</i>",
            parse_mode="HTML"
        )

        games.pop(game_id, None)

        return

    # -----------------------------------------------------
    # JOIN GAME
    # -----------------------------------------------------

    if action == "join":

        if game["status"] != "waiting":
            await query.answer(
                "❌ This game has already started.",
                show_alert=True
            )
            return

        if user.id == game["p1_id"]:
            await query.answer(
                "You are already Player 1.",
                show_alert=True
            )
            return

        game["p2_id"] = user.id
        game["p2_name"] = player_name(user)
        game["round"] = 1
        game["status"] = "playing"
        game["answers"] = {}

        await query.edit_message_text(
            game_text(game),
            parse_mode="HTML",
            reply_markup=game_keyboard(game),
        )

        return

    # -----------------------------------------------------
    # ANSWER A / B
    # -----------------------------------------------------

    if action in ["a", "b"]:

        if game["status"] != "playing":
            await query.answer(
                "❌ You cannot answer right now.",
                show_alert=True
            )
            return

        if user.id not in [game["p1_id"], game["p2_id"]]:
            await query.answer(
                "❌ You are not part of this game.",
                show_alert=True
            )
            return

        if user.id in game["answers"]:
            await query.answer(
                "✅ You already answered this round!",
                show_alert=True
            )
            return

        answer = "A" if action == "a" else "B"

        game["answers"][user.id] = answer

        # First player answered
        if len(game["answers"]) == 1:

            await query.edit_message_text(
                game_text(game),
                parse_mode="HTML",
                reply_markup=game_keyboard(game),
            )

            return

        # Both answered
        if len(game["answers"]) == 2:

            game["status"] = "results"

            await query.edit_message_text(
                game_text(game),
                parse_mode="HTML",
                reply_markup=game_keyboard(game),
            )

            return

    # -----------------------------------------------------
    # NEXT QUESTION
    # -----------------------------------------------------

    if action == "next":

        if game["status"] != "results":
            await query.answer(
                "Wait until both players answer.",
                show_alert=True
            )
            return

        if user.id not in [game["p1_id"], game["p2_id"]]:
            await query.answer(
                "You are not part of this game.",
                show_alert=True
            )
            return

        game["round"] += 1
        game["question"] = new_question()
        game["answers"] = {}
        game["status"] = "playing"

        await query.edit_message_text(
            game_text(game),
            parse_mode="HTML",
            reply_markup=game_keyboard(game),
        )

        return


# =========================================================
# MAIN
# =========================================================

def main():

    application = (
        Application.builder()
        .token(BOT_TOKEN)
        .build()
    )

    application.add_handler(
        CommandHandler("start", start)
    )

    application.add_handler(
        InlineQueryHandler(inline_query)
    )

    application.add_handler(
        CallbackQueryHandler(button_handler)
    )

    print("🔥 Would You Rather bot is running...")

    application.run_polling()


if __name__ == "__main__":
    main()
