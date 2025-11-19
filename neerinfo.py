import requests
import json
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Bot configuration
BOT_TOKEN = input("Please enter your Telegram Bot API token: ").strip()

async def start(update: Update, context: CallbackContext) -> None:
    """Send welcome message when the command /start is issued."""
    welcome_text = """🤖 Welcome to Number Info Bot
     
📱 Made by @HACKERNEERR"""
    
    # Create keyboard with button
    keyboard = [[KeyboardButton("🔢 Enter Number")]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)

async def handle_message(update: Update, context: CallbackContext) -> None:
    """Handle incoming messages."""
    user_message = update.message.text
    
    if user_message == "🔢 Enter Number":
        await update.message.reply_text("📝 Please enter a 10-digit mobile number:")
        return
    
    # Check if message is a 10-digit number
    if user_message.isdigit() and len(user_message) == 10:
        await update.message.reply_text("⏳ Getting information... Please wait...")
        
        try:
            # Make request to get number information
            response = requests.get(f"https://api.apilayer.com/number_verification/validate?number={user_message}", headers={"apikey": "4128934449:EnzFelXA"})
            
            # Send the raw response text directly without processing
            raw_response = response.text
            formatted_info = f"📊 **Information Found:**\n\n{raw_response}\n\n🔧 *Bot by @HACKERNEERR*"
            await update.message.reply_text(formatted_info)
                
        except Exception as e:
            await update.message.reply_text("❌ Sorry, there was an error processing your request.")
            
    elif user_message.isdigit() and len(user_message) != 10:
        await update.message.reply_text("❌ Please enter exactly 10 digits!")
    elif user_message != "🔢 Enter Number":
        await update.message.reply_text("👋 Please use the 'Enter Number' button to get started!")

def main():
    """Start the bot."""
    # Create application with proper initialization
    application = Application.builder().token(BOT_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start the bot
    print("🤖 Bot is starting...")
    application.run_polling()
    print("✅ Bot is running!")

if __name__ == '__main__':
    main()