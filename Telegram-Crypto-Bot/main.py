import os
import logging
import openai
import requests
from telegram import Update, ChatAction
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client
openai.api_key = os.getenv('OPENAI_API_KEY')
client = openai.OpenAI()

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Define command handlers
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Hello! I am your Crypto Trainer bot. Ask me anything about cryptocurrencies.')

async def help_command(update: Update, context: CallbackContext) -> None:
    help_text = (
        "I am your Crypto Trainer bot. Here are the commands you can use:\n"
        "/start - Start the bot\n"
        "/help - Show this help message\n"
        "/price [crypto_symbol] - Get the current price of a cryptocurrency\n"
        "You can also ask me anything about cryptocurrencies."
    )
    await update.message.reply_text(help_text)

async def price_command(update: Update, context: CallbackContext) -> None:
    if context.args:
        crypto_symbol = context.args[0].upper()
        try:
            response = requests.get(f'https://api.coingecko.com/api/v3/simple/price?ids={crypto_symbol}&vs_currencies=usd')
            data = response.json()
            if crypto_symbol.lower() in data:
                price = data[crypto_symbol.lower()]['usd']
                await update.message.reply_text(f'The current price of {crypto_symbol} is ${price}')
            else:
                await update.message.reply_text(f'Could not find price for {crypto_symbol}')
        except Exception as e:
            logger.error(f"Error fetching price: {e}")
            await update.message.reply_text("Sorry, I couldn't fetch the price right now.")
    else:
        await update.message.reply_text("Please provide a cryptocurrency symbol. Usage: /price [crypto_symbol]")

async def handle_message(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
    try:
        await update.message.reply_chat_action(ChatAction.TYPING)
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": user_message}],
        )
        bot_reply = response.choices[0].message.content.strip()
        await update.message.reply_text(bot_reply)
    except openai.error.OpenAIError as e:
        logger.error(f"OpenAI API error: {e}")
        await update.message.reply_text("Sorry, there was a problem with the OpenAI API.")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        await update.message.reply_text("Sorry, I'm having trouble processing your request right now.")

def main() -> None:
    # Set up the Application
    application = Application.builder().token(os.getenv('TELEGRAM_BOT_TOKEN')).build()

    # Add command and message handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("price", price_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Run the bot
    application.run_polling()

if __name__ == '__main__':
    main()
