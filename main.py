import api
import asyncio
import threading
from myconfig.config import DEFAULT_COMMANDS
from aiogram.types import BotCommand, BotCommandScopeDefault
import time
from typing import Any
from references import *
import random
import aiogram.utils.deep_linking
from myconfig import config
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.state import StatesGroup, State
from aiogram import Bot, Dispatcher, types, F
from aiogram.fsm.context import FSMContext
from arq import ArqRedis, create_pool
from aiogram.enums import ParseMode
from aiogram.filters.command import Command
from aiogram.filters import CommandStart
from aiogram.types import Message
from database import db_handler

dp = Dispatcher()
bot = Bot(token=config.TELEBOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


@dp.message(Command("start"))
async def command_start_handler(message: Message) -> None:
    start = message.text.split(' ')
    """ Тактика: Реферал моего реферала - мой реферал """
    if db_handler.get_data_from_database(message.from_user.id) == []:
        db_handler.registration_user_in_bd(message.from_user.id, message.from_user.full_name)
        if len(start) == 2:
            db_handler.create_table_ref(f'a{start[1]}')
            db_handler.add_referal(f'a{start[1]}', message.from_user.id, 'referal1')
            db_handler.raise_balance(start[1])

            superior = db_handler.find_table_with_referer(f'a{start[1]}')
            await message.answer(str(superior))
            if superior != None:
                db_handler.add_referal(superior, message.from_user.id, 'referal2')
                db_handler.raise_balance(superior[1:], raise_value=10)

    button1 = types.InlineKeyboardButton(text="Quiz 1: Finance", callback_data='quiz1')
    button2 = types.InlineKeyboardButton(text="Quiz 2: Crypto", callback_data='quiz2')
    button3 = types.InlineKeyboardButton(text="Quiz 3: Meme coins", callback_data='quiz3')
    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [button1],
            [button2],
            [button3],
        ]
    )   
    
    await message.answer(f'{greeting}{description}{balance}{db_handler.get_data_from_database(message.from_user.id, value="balance")[0][0]} $QUIZ', reply_markup=keyboard)


@dp.callback_query(F.data.in_(['quiz1']))
async def process_quiz1(callback: types.CallbackQuery):
    """ У трёх хендлеров отличия во внесении типа викторины в базу данных для выдачи викторин и каналов"""
    ready = types.InlineKeyboardButton(text="I'm ready!", callback_data='ready')
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[[ready]])
    db_handler.select_quiz_data(1, callback.from_user.id)

    await callback.message.answer("Get ready for the quiz\n10 questions\n10 seconds per question\nPress the button below when you are ready", reply_markup=keyboard) 


@dp.callback_query(F.data.in_(['quiz2']))
async def process_quiz1(callback: types.CallbackQuery):
    ready = types.InlineKeyboardButton(text="I'm ready!", callback_data='ready')
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[[ready]])
    db_handler.select_quiz_data(2, callback.from_user.id)

    await callback.message.answer("Get ready for the quiz\n10 questions\n10 seconds per question\nPress the button below when you are ready", reply_markup=keyboard) 


@dp.callback_query(F.data.in_(['quiz3']))
async def process_quiz1(callback: types.CallbackQuery):
    ready = types.InlineKeyboardButton(text="I'm ready!", callback_data='ready')
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[[ready]])
    db_handler.select_quiz_data(3, callback.from_user.id)

    await callback.message.answer("Get ready for the quiz\n10 questions\n10 seconds per question\nPress the button below when you are ready", reply_markup=keyboard) 


@dp.callback_query(F.data.in_(['close1']))
async def process_close1(callback: types.CallbackQuery) -> Any:
    await callback.message.delete()


@dp.callback_query(F.data.in_(['ready']))
async def process_ready(callback: types.CallbackQuery) -> None:
    await callback.message.delete()
    quiz_number = db_handler.check_quiz_number(callback.from_user.id)
    # Проверка - пройдена ли викторина, затем отработка основного кода
    if db_handler.get_quiz_key(str(quiz_number), callback.from_user.id) != api.wrapped_key(int(quiz_number)):
        counter_list = [i for i in range (0, 10)]
        for _ in range(10):
            counter = random.choice(counter_list)
            data_for_poll: list = api.recombinate_questions_and_answers(
                db_handler.check_quiz_number(callback.from_user.id),
                counter
            )
            if type(data_for_poll) == list:
                db_handler.register_data(1, f'update users set v_end=FALSE where tg_id={callback.from_user.id}')
                
                question = data_for_poll[0][0]
                options = data_for_poll[1]
                correct_opt = data_for_poll[2][0]
                
                poll = await callback.message.answer_poll(
                    question=question,
                    type="quiz",
                    options=options,
                    correct_option_id=correct_opt,
                    is_anonymous=False,
                    open_period=20
                )
                db_handler.raise_counter(callback.from_user.id)
                db_handler.register_data(1, f"update {db_handler.TABLE} set correct_answer={poll.poll.correct_option_id} where tg_id={callback.from_user.id}")
                for _ in range(20):
                    if str(db_handler.get_quiz_end(callback.from_user.id)) == '1':
                        break
                    else:
                        await asyncio.sleep(1)
                await bot.delete_message(chat_id=callback.from_user.id, message_id=poll.message_id)
                counter_list.remove(counter)
            else:
                await callback.message.answer(
                    str(data_for_poll)
                )
                break

        url = api.wrapped_getting_url(quiz_number)
        share = types.InlineKeyboardButton(text="Share quiz", callback_data='button3')
        subscribe: Any = types.InlineKeyboardButton(text='Subscribe', url=url)
        check = types.InlineKeyboardButton(text="Check", callback_data='check')

        keyboard = types.InlineKeyboardMarkup(
            inline_keyboard=[
                [subscribe],
                [check],
                [share]
            ]
        )
        await callback.message.answer(f'Quiz over! You earned {db_handler.get_income_from_db(callback.from_user.id)}\nFor return to main menu press /start\n\nIf you liked our game, support us by subscribing to the channel and get 100 $QUIZ', reply_markup=keyboard)
        db_handler.zero_income(callback.from_user.id)
        db_handler.reject_this_quiz(quiz_number, callback.from_user.id, api.wrapped_key(quiz_number))
    else:
        close8 = types.InlineKeyboardButton(text="Close", callback_data='close1')
        keyboard = types.InlineKeyboardMarkup(
            inline_keyboard=[
                [close8]
            ]
        )
        await callback.message.answer("You've already taken this quiz! Try playing others or wait until a new one starts", reply_markup=keyboard)


@dp.poll_answer()
async def handle_poll_answer(quiz_answer: types.PollAnswer):
    """ Обработка ответа опрос """
    correct_answer = db_handler.register_data(1, f'select correct_answer from {db_handler.TABLE} where tg_id={quiz_answer.user.id}')
    if quiz_answer.option_ids[0] is not None:
        db_handler.register_data(1, f'update users set v_end=TRUE where tg_id={quiz_answer.user.id}')
    if quiz_answer.option_ids[0] == correct_answer[0][0]:
        db_handler.raise_balance(quiz_answer.user.id)
        db_handler.raise_income(quiz_answer.user.id)


# Обработка кнопок

@dp.callback_query(F.data.in_(['check']))
async def process_button_check(callback: types.CallbackQuery):
    """ Получение бонуса и проставление отметки в БД"""
    username = "@" + api.wrapped_getting_url(db_handler.check_quiz_number(callback.from_user.id))[13:]

    status = await bot.get_chat_member(chat_id=username, user_id=callback.from_user.id)

    print(status.status)
    if int(db_handler.select_flag_bonus(callback.from_user.id, db_handler.check_quiz_number(callback.from_user.id))[0][0]) != 1:
        if str(status.status) == 'ChatMemberStatus.MEMBER':
            db_handler.raise_balance(callback.from_user.id, raise_value=100)
            db_handler.register_data(callback.from_user.id, f"UPDATE {db_handler.TABLE} SET ch_{db_handler.check_quiz_number(callback.from_user.id)}=TRUE WHERE tg_id={callback.from_user.id}")
            await callback.message.answer("You received a bonus of 100 points! Thanks for subscribing. Return to main menu: /start")
        else:
            await callback.message.answer("You are not a member of this chat.")
    else:
        await callback.message.answer("You have already received this bonus before. To the main menu: /start")



@dp.callback_query(F.data.in_(['button3']))
async def process_button_ref(callback: types.CallbackQuery):
    """ Многоуровневая реферальная программа """
    link = await aiogram.utils.deep_linking.create_start_link(bot, str(callback.from_user.id), encode=False)

    close_ref = types.InlineKeyboardButton(text="Close", callback_data='close1')
    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [close_ref]
        ]
    )
    frens = db_handler.get_count_exc(table_name=f"a{callback.from_user.id}")
    alltime = db_handler.register_data(1, f'select ref from users where tg_id={callback.from_user.id}')
    await callback.message.answer(
        f"Your link for frens: {link}\n\nRefferals: {frens}\n\nLifetime earned: {alltime[0][0]}\n\nRefer your friends and earn 20 $QUIZ for each and 10 $QUIZ for their friend",
        reply_markup=keyboard
    )


@dp.message(Command("invite"))
async def process_command_ref(message: Message) -> None:
    link = await aiogram.utils.deep_linking.create_start_link(bot, str(message.from_user.id), encode=False)

    close_ref = types.InlineKeyboardButton(text="Close", callback_data='close1')
    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [close_ref]
        ]
    )
    frens = db_handler.get_count_exc(table_name=f"a{message.from_user.id}")
    alltime = db_handler.register_data(1, f'select ref from users where tg_id={message.from_user.id}')
    await message.answer(
        f"Your link for frens: {link}\n\nRefferals: {frens}\n\nLifetime earned: {alltime[0][0]}\n\nRefer your friends and earn 20 $QUIZ for each and 10 $QUIZ for their friend",
        reply_markup=keyboard
    )


# Админские команды
class Form(StatesGroup):
    add_new = State() 
    add_answers = State()

@dp.message(Command("addnewv"))
async def command_addnew_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.add_new)
    await message.answer("Введите вопрос, введите ответы через запятую, в конце (так же через запятую) укажите правильный ответ. Далее через точку с запятой укажите остальные вопросы с аналогичными параметрами\nПример: Столица Китая?, Шанхай, Пекин, Гуанчжоу, 1; В какой стране был изобретен кофе Капучино?, США, Франция, Италия, 2")


async def set_default_commands(bot: Bot):
    commands = []
    for i in DEFAULT_COMMANDS:
        commands.append(BotCommand(command=i[0], description=i[1]))

    await bot.set_my_commands(commands, BotCommandScopeDefault())


async def main():
    await set_default_commands(bot) 
    await dp.start_polling(bot) 


if __name__ == "__main__":
    asyncio.run(main())
