import config
import asyncio
from logs.logger_config import setup_logger
from bot.create_bot import bot, dp, start_bot, stop_bot
from bot.services.watcher import match_watcher
from bot.handlers.admin import admin_router
from bot.handlers.user import user_router
from setup import create_jsondb_dir


async def main():
    create_jsondb_dir()
    dp.include_routers(admin_router, user_router)

    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    await bot.delete_webhook(drop_pending_updates=True)
    await asyncio.gather(
        match_watcher(),
        dp.start_polling(bot)
    )

if __name__ == "__main__":
    try:
        setup_logger()
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")