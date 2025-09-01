import json
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os

DATA_FOLDER = "data"
SCHEDULES_FOLDER = os.path.join(DATA_FOLDER, "schedules")

# Load JSON from file
def load_latest_data():
    today_file = os.path.join(SCHEDULES_FOLDER, sorted(os.listdir(SCHEDULES_FOLDER))[-1])
    try:
        with open(today_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except Exception:
        return {"Stages": []}

def fmt_row(home, away, hs, as_, status):
    score = f"{hs}-{as_}" if hs is not None and as_ is not None else "–"
    return f"{home} {score} {away} ({status})"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome to Goal2Gol ⚽\nUse /live for live scores, /matches for fixtures, /help for help."
    )

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/start – Start the bot\n"
        "/live – Live football scores\n"
        "/matches – Today’s fixtures\n"
        "/help – This help"
    )

async def live(update: Update, context: ContextTypes.DEFAULT_TYPE):
    latest_data = load_latest_data()
    live_matches = []
    for league in latest_data.get("Stages", []):
        for evt in league.get("Events", []):
            if evt.get("Eps") not in ["NS", "FT", "Sched", "Cancelled", "Postponed", "Awarded"]:
                live_matches.append(evt)

    if not live_matches:
        await update.message.reply_text("No live matches right now.")
        return

    lines = [
        fmt_row(
            evt.get("T1")[0].get("Nm", "N/A") if evt.get("T1") else "N/A",
            evt.get("T2")[0].get("Nm", "N/A") if evt.get("T2") else "N/A",
            evt.get("Tr1"),
            evt.get("Tr2"),
            evt.get("Eps")
        )
        for evt in live_matches[:10]
    ]
    await update.message.reply_text("Live Scores:\n" + "\n".join(lines))

async def matches(update: Update, context: ContextTypes.DEFAULT_TYPE):
    latest_data = load_latest_data()
    fixtures = []
    for league in latest_data.get("Stages", []):
        for evt in league.get("Events", []):
            if evt.get("Eps") in ["NS", "Sched"]:
                fixtures.append(evt)

    if not fixtures:
        await update.message.reply_text("No fixtures available right now.")
        return

    lines = [
        fmt_row(
            evt.get("T1")[0].get("Nm", "N/A") if evt.get("T1") else "N/A",
            evt.get("T2")[0].get("Nm", "N/A") if evt.get("T2") else "N/A",
            evt.get("Tr1"),
            evt.get("Tr2"),
            evt.get("Eps")
        )
        for evt in fixtures[:10]
    ]
    await update.message.reply_text("Today’s Fixtures:\n" + "\n".join(lines))

# -----------------------------
# Main
# -----------------------------
async def main():
    from config import telegram_bot_token  # load token only
    if not telegram_bot_token or telegram_bot_token == "YOUR_BOT_TOKEN_HERE":
        print("Telegram bot token not configured. Exiting.")
        return

    app = ApplicationBuilder().token(telegram_bot_token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("live", live))
    app.add_handler(CommandHandler("matches", matches))

    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
