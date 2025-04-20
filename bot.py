import logging
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

# Enable logging (optional but recommended)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# --- Bot Command Handlers ---
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends a message when the /start command is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}! I'm your friendly echo bot. Send me a message!",
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends a message when the /help command is issued."""
    await update.message.reply_text("Send me any message, and I will echo it back to you!")

# --- Message Handler ---
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Echoes the user message."""
    logger.info(f"Received message from {update.effective_user.username}: {update.message.text}")
    await update.message.reply_text(f"You said: {update.message.text}")

# --- Error Handler ---
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    """Log Errors caused by Updates."""
    logger.error(f"Update {update} caused error {context.error}", exc_info=context.error)


# --- Main Bot Logic ---
def main():
    """Start the bot."""
    if not BOT_TOKEN:
        logger.error("Bot token not found! Please set the BOT_TOKEN environment variable or replace the placeholder.")
        return

    # Create the Application and pass it your bot's token.
    application = Application.builder().token(BOT_TOKEN).build()

    # --- Register Handlers ---
    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))

    # on non-command i.e message - echo the message on Telegram
    # Filters.TEXT filters for text messages, excluding commands
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Register the error handler
    application.add_error_handler(error_handler)

    # Start the Bot (using polling)
    logger.info("Starting bot polling...")
    application.run_polling() # Checks Telegram for new messages periodically

if __name__ == "__main__":
    main()