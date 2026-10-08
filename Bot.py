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
    ("have sex only in total darkness", "have sex under bright lights in front of a mirror"),
    ("only be able to use doggystyle for a year", "only be able to use missionary for a year"),
    ("have a fast 5-minute quickie in a risky place", "have a 2-hour marathon in bed"),
    ("have your partner talk filthy dirty to you the entire time", "have your partner stay completely silent except for breathing"),
    ("be woken up with oral sex", "wake your partner up with morning sex"),
    ("only ever finish while on top", "only ever finish while on your back"),
    ("have loud background music playing during sex", "have dead silence where every sound is clear"),
    ("give a 20-minute massage first", "receive a 20-minute massage first"),
    ("have sex on a plush carpet", "have sex on a cold shower floor"),
    ("try a brand-new position every single time", "stick to your absolute favorite position forever"),
    ("keep your socks on during sex", "keep a blindfold on the entire time"),
    ("have sex once a day every day", "have sex three times a day only on weekends"),
    ("be the one initiating intimacy 100% of the time", "always wait for your partner to start"),
    ("have sex outdoors in a secluded forest", "have sex on a high-rise balcony at night"),
    ("use warm massage oil during foreplay", "use cold ice cubes during foreplay"),
    ("have your partner bite your lower lip every time you kiss", "have your partner leave marks on your neck"),
    ("only do quickies for a month", "do 1-hour sessions with no finishing allowed for a month"),
    ("have intense morning passion", "have late-night exhausted passion"),
    ("wear matching silk pajamas to bed", "sleep completely unclothed every night"),
    ("have sex while standing up against a wall", "have sex lying on the floor"),
    ("focus 100% on foreplay for 45 minutes", "skip foreplay entirely and go straight to it"),
    ("have your partner control your movement completely", "have full freedom to move how you want"),
    ("have an intense session in a hot shower", "have an intense session in a warm jacuzzi"),
    ("be surprised with a sudden spontaneous hookup", "plan it out hours in advance"),
    ("only be allowed to use your hands during foreplay", "only be allowed to use your mouth"),
    ("have your partner whisper dirty secrets in your ear", "have your partner yell out your name"),
    ("have sex in a room filled with lit candles", "have sex under colored LED neon lights"),
    ("finish at the exact same second as your partner", "take turns focusing on each other"),
    ("have sex in a tent while camping", "have sex in a luxury penthouse suite"),
    ("have your partner wear heavy perfume or cologne", "have your partner smell completely natural"),
    ("be teased for an hour before starting", "get straight to the point in 30 seconds"),
    ("have sex on silk sheets", "have sex on a thick fur blanket"),
    ("only be able to make out for a week with no sex", "have sex with no kissing at all"),
    ("have your partner be very vocal during intimacy", "have your partner be very physical with their hands"),
    ("have sex in a pool", "have sex on a private beach"),
    ("do a full roleplay scenario with costumes", "keep things completely realistic"),
    ("have your partner hold your hands above your head", "clasp hands tightly with your partner"),
    ("have sex right after a workout", "have sex right after taking a warm bath"),
    ("only be allowed to use one position for an entire month", "change positions every 2 minutes"),
    ("have a passionate session during a thunderstorm", "have a passionate session on a hot sunny afternoon"),
    ("be completely tied up and teased for 30 minutes", "be the one doing the tying and teasing"),
    ("get edged for an hour before finishing", "finish within the first two minutes"),
    ("wear a remote-controlled toy in public", "go out to dinner completely commando"),
    ("have your hair pulled gently", "have your waist gripped firmly"),
    ("be blindfolded and surprised", "have your partner blindfolded while you tease them"),
    ("be completely dominated for a weekend", "be the strict partner setting every rule"),
    ("give up control of what you wear to bed for a week", "control what your partner wears to bed"),
    ("be spanked lightly during passion", "have your neck held gently"),
    ("have your partner order you around in bed", "have your partner beg you for what they want"),
    ("be handcuffed to a headboard", "have your ankles bound together"),
    ("use a feather to tease your partner's skin", "use your fingernails lightly on their skin"),
    ("play a game where every wrong answer loses clothing", "play a game where every right answer wins a kiss"),
    ("have your partner dictate how fast you move", "have your partner dictate when you are allowed to finish"),
    ("be denied physical touch for 24 hours while cuddling", "be touched constantly with no climax allowed"),
    ("try sensory deprivation with earplugs and blindfold", "try visual overload with mirrors all around"),
    ("have a partner who is extremely aggressive in bed", "have a partner who is extremely gentle and soft"),
    ("be forced to make eye contact the entire time", "not be allowed to look at each other at all"),
    ("use leather restraints", "use soft silk ribbons"),
    ("have your partner whisper strict commands", "have your partner whisper sweet praises"),
    ("play doctor and patient in a roleplay", "play teacher and student in a roleplay"),
    ("be forced to ask for permission before touching your partner", "have total freedom of touch"),
    ("have your partner control the pace completely", "have your partner control the volume of your voice"),
    ("wear a collar and leash in private", "have your partner wear a collar and leash for you"),
    ("be tickled until you cry", "be teased until you beg"),
    ("have a partner who loves light biting", "have a partner who loves deep scratching"),
    ("give a 10-minute lap dance", "receive a 10-minute lap dance"),
    ("be tied to a chair", "be tied flat on a bed"),
    ("have your partner blindfold you and feed you sweet fruits", "have your partner feed you cold ice"),
    ("play truth or dare where every dare is physical", "play truth or dare where every truth is explicit"),
    ("be praised for being good in bed", "be degraded in a dirty-talk way"),
    ("have your partner trace your entire body with a feather", "have your partner trace your body with warm candle wax"),
    ("be locked out of the bedroom unclothed for 10 seconds", "stay tied up for 10 minutes alone"),
    ("have your partner whisper explicit instructions in public", "have your partner touch you under a table"),
    ("play boss and secretary in a roleplay", "play strangers meeting at a bar"),
    ("have your partner control your breathing with deep kisses", "have your partner control your hips"),
    ("be subject to a strict 15-minute countdown clock", "have no concept of time during sex"),
    ("be lightly tapped on the cheek", "be lightly bitten on the shoulder"),
    ("have your partner inspect your body like an art piece", "have your partner immediately jump on you"),
    ("spend an entire night doing only foreplay", "spend an entire night with zero foreplay"),
    ("give up all control in the bedroom for a month", "take 100% control in the bedroom for a month"),
    ("give head for 20 minutes without receiving", "receive head for 20 minutes with hands tied"),
    ("use ice cubes during foreplay", "use warm dripping massage oil"),
    ("only touch your partner with your mouth or tongue for 15 minutes", "only touch your partner with your fingertips"),
    ("have your neck licked slowly", "have your inner thighs caressed gently"),
    ("receive oral sex in the morning before brushing teeth", "receive oral sex at night right before sleep"),
    ("have your partner tease your chest area for 20 minutes", "have your partner tease your lower body for 20 minutes"),
    ("taste chocolate syrup off your partner's skin", "taste whipped cream off your partner's skin"),
    ("have your ears gently nibbled on", "have your collarbone kissed repeatedly"),
    ("give oral sex in a moving car passenger seat", "give oral sex in a locked bathroom at a party"),
    ("have your partner use their hair to tease your chest", "have your partner use a soft silk scarf"),
    ("receive a foot massage that turns sensual", "receive a full scalp and head massage"),
    ("have your stomach kissed all the way down", "have your back kissed all the way up"),
    ("use flavored lube", "use natural warm oils"),
    ("have your partner suck on your fingers one by one", "have your partner kiss your palm deeply"),
    ("receive oral sex while sitting on a chair", "receive oral sex while lying on the edge of the bed"),
    ("have your partner trail cold water down your back", "have your partner blow warm breath down your stomach"),
    ("spend 30 minutes focusing entirely on kissing", "spend 30 minutes focusing entirely on physical touch"),
    ("have your partner bite your lip until it throbs", "have your partner lick your neck until you shiver"),
    ("receive head with your eyes wide open looking at them", "receive head with eyes closed in a blindfold"),
    ("touch your partner over their clothes for 30 minutes", "touch your partner under their clothes for 5 minutes"),
    ("have your hands held tightly while receiving oral", "have your legs held up while receiving oral"),
    ("lick fruit juice off your partner's chest", "lick honey off your partner's neck"),
    ("have your partner whisper sweet love notes during oral", "have your partner talk explicit dirty talk during oral"),
    ("receive oral sex standing up against a door", "receive oral sex lying flat on your stomach"),
    ("have your partner trace your lips with their tongue without kissing", "have your partner kiss you deeply for 2 minutes"),
    ("be covered in edible body paint", "be covered in warm chocolate"),
    ("have your thighs massaged until you beg", "have your lower back caressed gently"),
    ("give oral sex under a blanket", "give oral sex out in the open with full view"),
    ("have your partner use a vibration toy on you", "have your partner use only their hands"),
    ("kiss with full tongue passion for 10 minutes straight", "touch skin-to-skin silently for 10 minutes"),
    ("have your chest licked in a circular motion", "have your chest gently pinched"),
    ("receive oral sex while watching yourself in a mirror", "receive oral sex in pitch blackness"),
    ("have your partner gently blow warm air on your wet skin", "have your partner fan cold air on your wet skin"),
    ("give oral sex to completion", "stop oral sex right before and switch to penetration"),
    ("have your hips held completely still during oral", "be allowed to grind freely during oral"),
    ("lick warm syrup off your partner's stomach", "suck an ice cube out of your partner's mouth"),
    ("have your neck covered in hickeys", "keep your neck completely mark-free"),
    ("receive oral sex in an armchair", "receive oral sex on a kitchen island"),
    ("have your partner whisper how good you taste", "have your partner stay quiet and moan"),
    ("spend an entire hour doing only oral sex", "spend an hour doing only physical touching"),
    ("send an explicit nude photo right now", "send a 30-second voice note moaning their name"),
    ("record a private video together and watch it immediately", "take polaroid photos together"),
    ("let your partner go through all photos in your hidden album", "let your partner dictate your sleep outfit"),
    ("talk dirty during lunch break at work", "talk dirty right before you go to sleep"),
    ("receive a detailed 500-word erotic text story", "receive a 10-second sexy video clip"),
    ("do a video call hookup while traveling", "wait until you see each other in person"),
    ("send a picture of your underwear", "send a picture of your chest or abs"),
    ("have a shared secret folder of spicy photos", "keep spicy photos only on disappearing mode"),
    ("text dirty commands back and forth all day at work", "save all dirty talk for when you get home"),
    ("take a spicy photo in a mirror", "have your partner take photos of you"),
    ("send a voice note telling your partner what you want to do to them", "write a detailed paragraph about what you want to do"),
    ("have your partner send spicy photos while you are in a meeting", "have your partner send spicy photos while with family"),
    ("record an audio recording of your intimate session", "take high-quality still photos"),
    ("receive a teaser photo showing full silhouette", "receive a close-up detail shot"),
    ("live-stream a private session for just your partner when away", "send pre-recorded private videos"),
    ("have your partner save every spicy photo you send forever", "have spicy photos auto-delete after 24 hours"),
    ("send a photo showing skin with clothes halfway off", "send a photo fully unclothed with clever angles"),
    ("do a full text-based roleplay for two hours", "do a 15-minute voice call roleplay"),
    ("post a suggestive picture on your social story", "send an explicit picture privately"),
    ("have your partner describe their fantasy via audio", "have your partner describe their fantasy via text"),
    ("send a clip of you biting your lip", "send a clip of you blowing a kiss"),
    ("get a random spicy notification at 2:00 AM", "get a random spicy notification at 2:00 PM"),
    ("have your partner rate your spicy photos 1-10", "have your partner write a review paragraph for your photos"),
    ("send a photo from the shower", "send a photo from under the bedsheets"),
    ("do phone sex with full audio description", "do text-only sexting"),
    ("take a photo wearing your partner's shirt with nothing underneath", "take a photo wearing fancy lingerie"),
    ("send a video walking toward the camera unclothed", "send a video walking away from the camera"),
    ("have your partner send a photo of their favorite body part on themselves", "have them send a photo of their favorite part on you"),
    ("get a sext that says 'I want you right now'", "get a sext with a detailed explanation of why they want you"),
    ("do a video call where only one person is on camera", "do a video call where both people are on camera"),
    ("send a picture of your lips close up", "send a picture of your eyes looking hungry"),
    ("write an erotic bucket list together on a shared document", "talk about an erotic bucket list verbally"),
    ("send a photo with full lighting", "send a mysterious shadow photo"),
    ("have your partner text you dirty words during lunch break", "have your partner text you dirty words right before sleep"),
    ("take a polaroid that stays on your nightstand", "keep digital photos password-protected"),
    ("send a video showing your body", "send a video talking dirty to the camera"),
    ("receive a spicy photo when you least expect it", "receive a spicy photo after asking for one"),
    ("record a 5-second voice note whispering 'Come home'", "record a 5-second voice note whispering 'I'm waiting for you'"),
    ("do a video chat where you both strip slowly", "do a video chat where you talk dirty"),
    ("have your partner save your voice notes as their ringtone", "have your partner keep your voice notes in a private folder"),
    ("almost get caught hooking up in a parked car by security", "get overheard through thin walls"),
    ("have a quick hookup in a movie theater back row", "have a quick hookup in a high-end restaurant restroom"),
    ("go to an adult clothing store together", "go to a private adult resort"),
    ("hook up on a Ferris wheel at night", "hook up on a quiet private boat on a lake"),
    ("sneak out of a family dinner for a 10-minute quickie", "wait until everyone is asleep to hook up"),
    ("wear no underwear under your clothes on a fancy date night", "wear a hidden remote toy on a date night"),
    ("get caught by a best friend", "get caught by a complete stranger"),
    ("hook up in ocean waves at night", "hook up in a secluded hot spring"),
    ("touch each other discreetly under a blanket on an airplane", "touch each other in the airplane lavatory"),
    ("have sex in an elevator between floors", "have sex on a secluded rooftop balcony"),
    ("participate in a blindfolded surprise date", "participate in a fully planned luxury getaway"),
    ("hook up in the fitting room of a clothing store", "hook up in the back of a taxi with tinted windows"),
    ("do something risky on a public hiking trail", "do something risky on a deserted beach at sunset"),
    ("be overheard by neighbors making loud sounds", "have someone accidentally open the door on you"),
    ("go commando in jeans", "go commando in a skirt or dress"),
    ("kiss passionately in a crowded subway station", "kiss passionately in the rain in an empty parking lot"),
    ("hook up in a library corner behind bookshelves", "hook up in a museum exhibit hall"),
    ("have a quick session in a photo booth", "have a quick session in a VIP lounge area"),
    ("get caught by your partner's roommate", "have your partner's roommate hear everything"),
    ("hook up on the bonnet of a car under the stars", "hook up on the backseat of a car"),
    ("flash your partner quickly in an empty alleyway", "flash your partner in a private elevator"),
    ("do something spicy in a train overnight cabin", "do something spicy on a cruise ship balcony"),
    ("have your partner whisper explicit thoughts during a boring wedding", "have your partner whisper explicit thoughts during a movie"),
    ("hook up in a sauna", "hook up in an ice-cold swimming pool"),
    ("touch your partner's thigh under the table at a fancy dinner", "hold hands secretly under the table"),
    ("be caught kissing by security guards", "be asked to leave a venue for being too physical"),
    ("hook up in a tent at a loud music festival", "hook up in a quiet cabin in the woods"),
    ("leave a small visible bite mark on your partner's neck", "leave a scratch mark on your partner's back"),
    ("do a quickie in an office after work hours", "do a quickie in a school campus study room"),
    ("go to a drive-in movie and ignore the movie completely", "watch the movie while teasing your partner"),
    ("get caught by a police officer who gives you a warning", "get caught by a security guard who yells"),
    ("hook up in a hotel room with floor-to-ceiling glass windows", "hook up in a cozy basement"),
    ("wear a revealing outfit to a private party", "wear an elegant conservative outfit with nothing underneath"),
    ("kiss in a crowded club under strobe lights", "kiss in a dark corner of a quiet pub"),
    ("hook up on a hammock outdoors", "hook up on a trampoline at night"),
    ("have your partner tease you through a 3-hour road trip", "have your partner jump on you as soon as you arrive"),
    ("have a secret rendezvous during lunch hour at work", "have a secret rendezvous late at night after midnight"),
    ("hook up in a historic castle hotel", "hook up in an ultra-modern glass villa"),
    ("be seen by a drone flying outside a window", "be seen by someone through binoculars"),
    ("complete all 200 of these questions in one night", "do 10 questions every weekend for a year")
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
