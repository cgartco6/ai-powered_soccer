# bot.py
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import data_fetcher
import predictor
from datetime import datetime

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Replace with your Telegram Bot Token
TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"

async def send_predictions(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send the predictions for today's games."""
    # Fetch today's games
    games = data_fetcher.fetch_todays_games()
    if not games:
        await update.message.reply_text("No games today.")
        return

    # For each game, get predictions
    message = "⚽️ *Today's Soccer Predictions* ⚽️\n\n"
    message += "_(Predictions by our AI, Hollywoodbets AI, and Betway AI)_\n\n"

    for idx, game in enumerate(games):
        home = game['home_team']
        away = game['away_team']
        message += f"*Game {idx+1}: {home} vs {away}*\n"
        message += f"Date: {game['date']}\n"
        # Add a brief on form, injuries, etc.
        home_form = ''.join(['W' if x==3 else 'D' if x==1 else 'L' for x in game['team_forms']['home']])
        away_form = ''.join(['W' if x==3 else 'D' if x==1 else 'L' for x in game['team_forms']['away']])
        message += f"Form:\n  {home}: {home_form}\n  {away}: {away_form}\n"
        message += f"Injuries: {len(game['injuries']['home'])} for {home}, {len(game['injuries']['away'])} for {away}\n"
        message += f"Weather: {game['weather']}, Pitch: {game['pitch']}, Ref: {game['referee']}\n"

        # Get predictions
        preds = predictor.predict_game(game)

        # Main model predictions
        main = preds['main_model']
        message += "\n*Our AI Prediction:*\n"
        message += f"  Outcome: {main['1x2'][0]} (confidence: {main['1x2'][1]*100:.1f}%)\n"
        message += f"  BTTS: {main['btts'][0]} (confidence: {main['btts'][1]*100:.1f}%)\n"
        message += f"  Correct Score: {main['correct_score'][0]} (confidence: {main['correct_score'][1]*100:.1f}%)\n"

        # Hollywoodbets
        holly = preds['hollywoodbets']
        message += "\n*Hollywoodbets AI:*\n"
        message += f"  Outcome: {holly['1x2'][0]} (confidence: {holly['1x2'][1]*100:.1f}%)\n"
        message += f"  BTTS: {holly['btts'][0]}\n"  # We might not have confidence for them? We do, but let's show
        message += f"  Correct Score: {holly['correct_score'][0]}\n"

        # Betway
        betway = preds['betway']
        message += "\n*Betway AI:*\n"
        message += f"  Outcome: {betway['1x2'][0]} (confidence: {betway['1x2'][1]*100:.1f}%)\n"
        message += f"  BTTS: {betway['btts'][0]}\n"
        message += f"  Correct Score: {betway['correct_score'][0]}\n"

        message += "--------------------------------\n\n"

    # Send the message (note: Telegram messages have a limit of 4096 characters, so we might need to split)
    # For now, we assume the message is not too long (5 games should be okay)
    await update.message.reply_text(message, parse_mode='Markdown')

def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("today", send_predictions))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()

if __name__ == "__main__":
    main()
