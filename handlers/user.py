from creater import bot, db
from aiogram import types, Dispatcher
from keyboards import kb_menu, language, cancel, kb_check
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from translation import translations


class FSMcheckSNILS(StatesGroup):
     input_snils = State()


# @dp.callback_query_handler(lambda c: c.data and c.data.startswith('l_'))
async def setLanguage(c: types.CallbackQuery):
    lang = c.data[2:]
    u_id = c.from_user.id
    if not db.user_exists(u_id):
        db.add_user(u_id, lang)
        with open('photos/photo.jpg', 'rb') as photo:
            await bot.send_photo(chat_id=u_id,
                                 caption=translations[db.get_lang(u_id)]['W'] + translations[db.get_lang(u_id)]['HELLO'],
                                 photo=photo)
    else:
        db.set_lang(u_id, lang)
        await bot.send_message(u_id, translations[db.get_lang(u_id)]['UPD'], reply_markup=kb_menu(db.get_lang(u_id)))
    await c.message.delete()


# @dp.callback_query_handler(lambda c: c.data and c.data.startswith('n_'))
async def checking(c: types.CallbackQuery):
    snils = c.data[2:]
    number, k_number = snils[:-4], snils[-4:-2]
    remove = types.ReplyKeyboardRemove()
    if snils[-2:] == k_number:
        await bot.send_message(c.from_user.id,
                               f"{translations[db.get_lang(c.from_user.id)]['SN']} {number + k_number} "
                               f"{translations[db.get_lang(c.from_user.id)]['YES']}"
                               f"{translations[db.get_lang(c.from_user.id)]['DO']}", reply_markup=remove)
    else:
        await bot.send_message(c.from_user.id,
                               f"{translations[db.get_lang(c.from_user.id)]['SN']} {number + snils[-2:]} "
                               f"{translations[db.get_lang(c.from_user.id)]['YES']}"
                               f"{translations[db.get_lang(c.from_user.id)]['NOT']} "
                               f"{translations[db.get_lang(c.from_user.id)]['DO']}\n"
                               f"{translations[db.get_lang(c.from_user.id)]['CORR']} {number + k_number}",
                               reply_markup=remove)
    await c.message.delete()


# @dp.callback_query_handler(lambda c: c.data == 'cancel')
async def c_cancel(c: types.CallbackQuery):
    remove = types.ReplyKeyboardRemove()
    await bot.send_message(c.from_user.id, translations[db.get_lang(c.from_user.id)]['CANCELED'], reply_markup=remove)
    await c.message.delete()


# @dp.message_handler(commands=['start'])
async def start(m: types.Message):
    u_id = m.from_user.id
    if db.user_exists(u_id):
        date = int(m.date.hour)
        if date in range(5, 13):
            hello = translations[db.get_lang(u_id)]['GM']
        elif date in range(13, 18):
            hello = translations[db.get_lang(u_id)]['GA']
        elif date in range(18, 23):
            hello = translations[db.get_lang(u_id)]['GE']
        else:
            hello = translations[db.get_lang(u_id)]['GN']
        with open('photos/photo.jpg', 'rb') as photo:
            await bot.send_photo(chat_id=u_id, caption=hello + translations[db.get_lang(u_id)]['HELLO'],
                                 photo=photo,
                                 reply_markup=kb_menu(db.get_lang(u_id)))
    else:
        await m.answer(translations['ru']['CH'], reply_markup=language)


# @dp.message_handler(commands=['language'])
async def update_language(m: types.Message):
    await m.answer(translations[db.get_lang(m.from_user.id)]['CH'], reply_markup=language)


# @dp.message_handler(commands=['help'])
async def help_commands(m: types.Message):
    await m.answer(translations[db.get_lang(m.from_user.id)]['HELP'])


# @dp.message_handler(commands=['menu'])
async def menu(m: types.Message):
    await m.answer(translations[db.get_lang(m.from_user.id)]['MENU'], reply_markup=kb_menu(db.get_lang(m.from_user.id)))


# @dp.message_handler(lambda m: m.text == 'Отмена❌' or m.text == 'Cancel❌')
async def close(m: types.Message):
    remove = types.ReplyKeyboardRemove()
    await m.answer(translations[db.get_lang(m.from_user.id)]['CANCELED'], reply_markup=remove)


# @dp.message_handler(lambda m: m.text == 'Проверка СНИЛС✅✅✅' or m.text == 'SNILS verification✅✅✅')
async def input_number(m: types.Message):
    await m.answer(translations[db.get_lang(m.from_user.id)]['IN'], reply_markup=cancel)
    await FSMcheckSNILS.input_snils.set()


# @dp.message_handler(state="*", commands='cancel')
async def cancel_fsm(m: types.Message, state: FSMContext):
    cur_state = await state.get_state()
    if cur_state is None:
        return
    await state.finish()
    remove = types.ReplyKeyboardRemove()
    await m.answer(translations[db.get_lang(m.from_user.id)]['CANCELED'], reply_markup=remove)


# @dp.message_handler(state=FSMcheckSNILS.input_snils)
async def check_snils(m: types.Message, state: FSMContext):
    if m.text.isdigit() and len(m.text) == 11:
        summ = 0
        for i, el in enumerate(reversed(m.text[:9]), 1):
            summ += i * int(el)
        if summ < 100:
            k_number = str(summ)
        elif summ == 100 or summ == 101:
            k_number = '00'
        else:
            o_d = summ % 101
            if o_d == 100 or o_d == 101:
                k_number = '00'
            else:
                k_number = str(o_d)
        if len(k_number) == 1:
            k_number = '0' + k_number
        number = m.text[:3] + '-' + m.text[3:6] + '-' + m.text[6:9] + ' '
        await state.finish()
        await m.answer(f'Проверить СНИЛС {number + m.text[9:]}?',
                       reply_markup=kb_check(db.get_lang(m.from_user.id), 'n_' + number + k_number + m.text[9:]))
    else:
        await m.answer(translations[db.get_lang(m.from_user.id)]['DC'])
        await FSMcheckSNILS.input_snils.set()


# @dp.message_handler()
async def all_message(m: types.Message):
    await m.answer(translations[db.get_lang(m.from_user.id)]['DONT'])


def reg_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(setLanguage, lambda c: c.data and c.data.startswith('l_'))
    dp.register_callback_query_handler(checking, lambda c: c.data and c.data.startswith('n_'))
    dp.register_callback_query_handler(c_cancel, lambda c: c.data == 'cancel')
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(update_language, commands=['language'])
    dp.register_message_handler(help_commands, commands=['help'])
    dp.register_message_handler(menu, commands=['menu'])
    dp.register_message_handler(close, lambda m: m.text == 'Отмена❌' or m.text == 'Cancel❌')
    dp.register_message_handler(input_number,
                                lambda m: m.text == 'Проверка СНИЛС✅✅✅' or m.text == 'SNILS verification✅✅✅')
    dp.register_message_handler(cancel_fsm, state="*", commands='cancel')
    dp.register_message_handler(check_snils, state=FSMcheckSNILS.input_snils)
    dp.register_message_handler(all_message)
