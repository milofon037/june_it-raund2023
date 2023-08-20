from aiogram import executor
from creater import dp


async def start_bot(_):
    print('Online')


async def finish(_):
    print('Offline')


from handlers.user import reg_handlers
reg_handlers(dp)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=start_bot, on_shutdown=finish)
