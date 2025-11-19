#!/usr/bin/env python3
"""
Telegram Bot for Phone Tracing and Vehicle Lookup
Main entry point for the bot application
"""

import asyncio
import logging
import os
import signal
import sys
from datetime import datetime

from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters
)

from config import Config
from bot_handlers import BotHandlers
from user_management import UserManager
from database import Database

# Logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    handlers=[
        logging.FileHandler("bot.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class TelegramBot:
    def __init__(self):
        self.config = Config()
        self.database = Database()
        self.user_manager = UserManager(self.database)
        self.handlers = BotHandlers(self.user_manager, self.config)
        self.application = None

    async def setup_bot(self):
        """Initialize bot"""
        try:
            await self.clear_webhooks()

            # Build app
            self.application = (
                Application.builder()
                .token(self.config.BOT_TOKEN)
                .build()
            )

            await self.add_handlers()

            logger.info("✅ Bot setup completed successfully")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to setup bot: {e}")
            return False

    async def clear_webhooks(self):
        """Clear old webhooks (Render only supports polling)."""
        try:
            import requests
            r = requests.post(
                f"https://api.telegram.org/bot{self.config.BOT_TOKEN}/deleteWebhook",
                timeout=10
            )
            if r.status_code == 200:
                logger.info("✅ Cleared existing webhooks")
            else:
                logger.warning("⚠️ Unable to clear webhook")
        except Exception as e:
            logger.warning(f"⚠️ Webhook clear error: {e}")

    async def add_handlers(self):
        """Load command + message handlers"""
        try:
            # Commands
            self.application.add_handler(CommandHandler("start", self.handlers.start_command))
            self.application.add_handler(CommandHandler("help", self.handlers.help_command))
            self.application.add_handler(CommandHandler("trace", self.handlers.trace_command))
            self.application.add_handler(CommandHandler("vehicle", self.handlers.vehicle_command))
            self.application.add_handler(CommandHandler("stats", self.handlers.stats_command))
            self.application.add_handler(CommandHandler("admin", self.handlers.admin_command))
            self.application.add_handler(CommandHandler("broadcast", self.handlers.broadcast_command))

            # Callback button handler
            self.application.add_handler(CallbackQueryHandler(self.handlers.button_callback))

            # Photo handler
            self.application.add_handler(MessageHandler(filters.PHOTO, self.handlers.photo_handler))

            # Text handler
            self.application.add_handler(
                MessageHandler(filters.TEXT & ~filters.COMMAND, self.handlers.text_handler)
            )

            # Error handler
            self.application.add_error_handler(self.handlers.error_handler)

            logger.info("✅ Handlers added")

        except Exception as e:
            logger.error(f"❌ Handler loading error: {e}")
            raise

    async def start_polling(self):
        """Start bot polling using PTB 20+ API"""
        try:
            logger.info("🚀 Starting bot polling...")
            await self.application.run_polling(
                drop_pending_updates=True,
                allowed_updates=["message", "callback_query"]
            )
        except Exception as e:
            logger.error(f"❌ Error during polling: {e}")
            raise

    async def stop_bot(self):
        """Graceful stop"""
        try:
            if self.application:
                logger.info("🛑 Stopping bot...")
                await self.application.stop()
                await self.application.shutdown()
                logger.info("✅ Bot stopped successfully")
        except Exception as e:
            logger.error(f"❌ Error stopping bot: {e}")


def signal_handler(signum, frame):
    logger.info(f"📡 Signal {signum} received, shutting down...")
    sys.exit(0)


async def main():
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        bot = TelegramBot()

        if await bot.setup_bot():
            await bot.start_polling()
        else:
            logger.error("❌ Bot setup failed")
            sys.exit(1)

    except Exception as e:
        logger.error(f"❌ Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("🛑 Bot stopped by user")
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
        sys.exit(1)
