import json
import random

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import motor.motor_asyncio
import traceback

from bot import config
from bot.session import Session

""" Инициализирую работу с базой """

# """ Ключ для работы с базой """
cluster = config.CLUSTER
client = motor.motor_asyncio.AsyncIOMotorClient(cluster)

""" База с которой работаю """

db = client["test"]

""" Таблица с которой работаю """
wumpus = db.wumpus

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

""" ГЛАВНАЯ КЛАВИАТУРА (НИЗ)"""


def MainKeyboard() -> types.ReplyKeyboardMarkup:
    keyboard_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    first = ('GitHub проекта 🏠',
             'Помощь❓')
    second = ('Wiki📃',
              'Контакты')
    third = 'Начать игру 🏰'
    keyboard_markup.row(*(types.KeyboardButton(text) for text in first))
    keyboard_markup.row(*(types.KeyboardButton(text) for text in second))
    keyboard_markup.row(third)
    return keyboard_markup


""" КЛАВИАТУРА КОНЦА ИГРЫ (НИЗ) """


def FinishKeyboard() -> types.ReplyKeyboardMarkup:
    keyboard_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    first = ('Начать игру 🏰',
             'Счёт')
    third = 'Главное меню 🏰'
    keyboard_markup.row(*(types.KeyboardButton(text) for text in first))
    keyboard_markup.row(third)
    return keyboard_markup


''' СООБЩЕНИЯ И ССЫЛКИ '''

HELLO_MESSAGE = '''Привет! Это игра в Охоту на Вампуса! Что будем делать? '''

GIT_HUB_LINK = '''[ ](https://github.com/VasiliySilver/Wumpus) Здесь расположен репозиторий проекта '''

''' ОБРАБОТЧИК КОМАНДЫ СТАРТ '''

HELP_TEXT = ''' 1 - В начале игры игрок случайным образом попадает в одну из комнат пещеры.
2 - За ход он может выстрелить в одну из комнат либо перейти в какую-нибудь.
3 - Количество стрел ограничено, всего их 5, если не осталось ни одной игрок погибает.
4 - В некоторых комнатах раставлены ловушки.
5 - В комнатах можно получить валюту чтобы избежать ловушек или покупки стрел.
УДАЧИ!
'''

WIKI_LINK = '''[ ](https://ru.wikipedia.org/wiki/Hunt_the_Wumpus)Мир «Hunt the Wumpus» — это пещера из 20 
пронумерованных комнат, каждая из которых соединена тоннелями с тремя другими, т. е. пещера представляет собой 
расплющенный додекаэдр (в последующих версиях используются топологии, основанные на икосаэдре, листе Мёбиуса, 
пчелиных сотах и др.)[2]. В начале игры персонаж случайным образом оказывается в одной из комнат пещеры. За ход он 
может либо выстрелить в одну из трёх соседних комнат, либо перейти в какую-нибудь из них. '''

''' ОБРАБОТЧИК КОМАНДЫ СТАРТ '''


@dp.message_handler(commands='start')
async def start_cmd_handler(message: types.Message, state):
    try:
        user = await db.wumpus.find_one({'tgid': {'$eq': message.from_user.id}})
        if user is None:
            await db.wumpus.insert_one({'tgid': message.from_user.id})
        await bot.send_message(message.from_user.id, HELLO_MESSAGE, reply_markup=MainKeyboard(), parse_mode='Markdown')
        await state.finish()
    except Exception as ex:
        print(ex)
        print(traceback.format_exc())
        await bot.send_message(message.from_user.id, 'Что-то пошло не так, 🤷🏼‍♀️ возврат в главное меню.',
                               reply_markup=MainKeyboard())


@dp.message_handler(commands='start', state="*")
async def start_restart_fix_cmd_handler(message: types.Message, state):
    try:
        await bot.send_message(message.from_user.id, HELLO_MESSAGE, reply_markup=MainKeyboard())
        await state.finish()
    except Exception as ex:
        print(ex)
        print(traceback.format_exc())
        await state.finish()
        await bot.send_message(message.from_user.id, 'Что-то пошло не так, 🤷🏼‍♀️ возврат в главное меню.',
                               reply_markup=MainKeyboard())


''' ОБРАБОТЧИК ГЛАВНОЙ КЛАВИАТУРЫ СООБЩЕНИЯ С КНОПОК '''


@dp.message_handler()
async def main_keyboard(message: types.Message, state):
    try:
        if message.text not in ['Начать игру 🏰', 'GitHub проекта 🏠', 'Помощь❓', 'Wiki📃', 'Контакты', '1', '2',
                                '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18',
                                '19', '20']:
            await bot.send_message(message.from_user.id,
                                   'Неизвестная команда, или возможно, я перезагрузился и забыл на чём мы остановились.\n Попробуйте ещё раз!',
                                   reply_markup=MainKeyboard())

        if message.text == 'Начать игру 🏰':
            # начинаю сессию
            session = Session(message.from_user.id)
            json_data_session = session.to_json()
            await db.wumpus.update_one({"tgid": message.from_user.id}, {"$set": {"session": json_data_session}})

            from pprint import pprint
            pprint(session.cave.dict_rooms)

            print(session.wumpus.location, 'WUMPUS LOCATION')
            print(session.player.location, 'PLAYER LOACTION')

            # получаю локации мышей, золота и ловушек
            bats_locations = [i.location for i in session.bats]
            golds_locations = [i.location for i in session.golds]
            traps_locations = [i.location for i in session.traps]

            # получаю list(list,list..)
            bats_room_connects = sum([i.room_connects for i in session.golds], [])
            golds_room_connects = sum([i.room_connects for i in session.golds], [])
            traps_room_connects = sum([i.room_connects for i in session.traps], [])

            # перевожу значения в integer
            bats_room_connects_int = [int(i) for i in bats_room_connects]
            golds_room_connects_int = [int(i) for i in golds_room_connects]
            traps_room_connects_int = [int(i) for i in traps_room_connects]

            print(golds_locations, 'golds')
            print(bats_locations, 'bats')
            print(traps_locations, 'traps')

            # в комнате рядом есть золото или мыши или ловушка
            player_in_gold_room_connects = int(session.player.location) in bats_room_connects_int
            player_in_bats_room_connects = int(session.player.location) in golds_room_connects_int
            player_in_traps_room_connects = int(session.player.location) in traps_room_connects_int

            # встроенная клавиатура
            keyboard_markup = types.InlineKeyboardMarkup()

            wumpus_is_near = session.check_that_wumpus_is_near()

            print(session.player.location)
            print(session.player.location)

            await check_if_player_in_bats_room_connects(keyboard_markup, message, session, player_in_bats_room_connects)

            await check_if_player_in_gold_room_connects(keyboard_markup, message, session, player_in_gold_room_connects)

            await check_if_player_in_traps_room_connects(keyboard_markup, message, session,
                                                         player_in_traps_room_connects)

            if wumpus_is_near:
                keyboard_markup.add(types.InlineKeyboardButton('Стрелять',
                                                               callback_data='shot'))
                keyboard_markup.add(types.InlineKeyboardButton('Идти дальше',
                                                               callback_data='move_on'))

                await bot.send_message(message.from_user.id, wumpus_is_near,
                                       reply_markup=keyboard_markup, parse_mode='Markdown')

            else:
                player_choices = session.get_player_choices()

                for player_choice in player_choices:
                    keyboard_markup.add(
                        types.InlineKeyboardButton(str(player_choice), callback_data=f'next_room{player_choice}'))

                await bot.send_message(message.from_user.id, session.get_message_for_player_choices(),
                                       reply_markup=keyboard_markup, parse_mode='Markdown')

        if message.text == 'GitHub проекта 🏠':
            await bot.send_message(message.from_user.id, GIT_HUB_LINK, reply_markup=MainKeyboard(), parse_mode='Markdown')
            state.finish()
        if message.text == 'Wiki📃':
            await bot.send_message(message.from_user.id, WIKI_LINK, reply_markup=MainKeyboard(), parse_mode='Markdown')
            state.finish()

        if message.text == 'Контакты':
            pass
        if message.text == 'Помощь❓':
            await bot.send_message(message.from_user.id, HELP_TEXT, reply_markup=MainKeyboard())
    except Exception as ex:
        print(ex)
        print(traceback.format_exc())
        await bot.send_message(message.from_user.id, 'Что-то пошло не так, 🤷🏼‍♀️ возврат в главное меню.',
                               reply_markup=MainKeyboard())


''' CALLBACK ДЛЯ ВЫБОРА КОМНАТ '''
list_rooms = ['next_room1', 'next_room2', 'next_room3', 'next_room4', 'next_room5', 'next_room6', 'next_room7',
              'next_room8', 'next_room9', 'next_room10', 'next_room11', 'next_room12', 'next_room13', 'next_room14',
              'next_room15', 'next_room16', 'next_room17', 'next_room18', 'next_room19', 'next_room20']


@dp.callback_query_handler(lambda cb: cb.data in list_rooms)
async def next_room(query: types.CallbackQuery):
    try:
        print('ВЫБОР КОМНАТЫ')

        # получаю выбор пользователя
        player_choice_number, session = await get_session_and_player_choice_number(query)

        from pprint import pprint
        pprint(session.cave.dict_rooms)

        print(player_choice_number, 'palyer_choice_number')

        # перехожу в комнату выбранную пользователем
        session.player_moves_to_another_room(player_choice_number)

        print(session.wumpus.location, 'WUMPUS LOCATION')
        print(session.player.location, 'PLAYER LOCATION')

        # получаю локации мышей, золота и ловушек
        bats_locations = [i.location for i in session.bats]
        golds_locations = [i.location for i in session.golds]
        traps_locations = [i.location for i in session.traps]

        # получаю list(list,list..)
        bats_room_connects = sum([i.room_connects for i in session.golds], [])
        golds_room_connects = sum([i.room_connects for i in session.golds], [])
        traps_room_connects = sum([i.room_connects for i in session.traps], [])

        # перевожу значения в integer
        bats_room_connects_int = [int(i) for i in bats_room_connects]
        golds_room_connects_int = [int(i) for i in golds_room_connects]
        traps_room_connects_int = [int(i) for i in traps_room_connects]

        print(golds_locations, 'golds')
        print(bats_locations, 'bats')
        print(traps_locations, 'traps')

        # проверяет что игров в комнате с золотом или мышами или попал в ловушку
        player_in_gold_location = int(session.player.location) in [int(i.location) for i in session.golds]
        player_in_bats_location = int(session.player.location) in [int(i.location) for i in session.bats]
        player_in_traps_location = int(session.player.location) in [int(i.location) for i in session.traps]

        # в комнате рядом есть золото или мыши или ловушка
        player_in_gold_room_connects = int(session.player.location) in bats_room_connects_int
        player_in_bats_room_connects = int(session.player.location) in golds_room_connects_int
        player_in_traps_room_connects = int(session.player.location) in traps_room_connects_int

        player_in_wumpus_location = int(session.player.location) == int(session.wumpus.location)

        # встроенная клавиатура
        keyboard_markup = types.InlineKeyboardMarkup()

        # есть ли вампус в соседней комнате
        wumpus_is_near = session.check_that_wumpus_is_near()

        await check_if_player_in_gold_room_connects(keyboard_markup, query, session, player_in_gold_room_connects)

        await check_if_player_in_bats_room_connects(keyboard_markup, query, session, player_in_bats_room_connects)

        await check_if_player_in_traps_room_connects(keyboard_markup, query, session, player_in_traps_room_connects)

        await check_if_wumpus_in_room_connects(keyboard_markup, query, wumpus_is_near)

        await check_if_player_in_bats_location(keyboard_markup, query, session, player_in_bats_location)

        await check_if_player_in_gold_location(keyboard_markup, query, session, player_in_gold_location)

        await check_if_player_in_trap_location(keyboard_markup, query, session, player_in_traps_location)

        await check_if_player_in_wumpus_location(query, player_in_wumpus_location)

        if not player_in_wumpus_location:
            if not player_in_bats_location:
                if not player_in_traps_location:
                    if not player_in_gold_location:
                        player_choices = session.get_player_choices()

                        for player_choice in player_choices:
                            keyboard_markup.add(
                                types.InlineKeyboardButton(str(player_choice),
                                                           callback_data=f'next_room{player_choice}'))

                        await bot.send_message(query.from_user.id, session.get_message_for_player_choices(),
                                               reply_markup=keyboard_markup, parse_mode='Markdown')

    except Exception as ex:
        print(ex)
        print(traceback.format_exc())
        await bot.send_message(query.from_user.id, 'Что-то пошло не так, 🤷🏼‍♀️ возврат в главное меню.',
                               reply_markup=MainKeyboard())


async def check_if_player_in_bats_location(keyboard_markup, query, session, check):
    if check:
        # проверяю пользователя на мышей
        bat_location = session.player.location
        # меняю локацию пользователя
        session.bat_change_player_location()

        answer = f''' 
                    ВНЕЗАПНО ТЕБЯ ПОДХВАТИЛА ОГРОМНАЯ МЫШЬ И УНЕСЛА В НЕИЗВЕСТНОМ НАПРВСЛЕНИИ...
                    Проснувшись ты оказался в комнате {session.player.location}
                    Выбери комнату {session.get_player_choices()}
                    '''

        player_choices = session.get_player_choices()

        for player_choice in player_choices:
            keyboard_markup.add(
                types.InlineKeyboardButton(str(player_choice), callback_data=f'next_room{player_choice}'))

        await bot.send_message(query.from_user.id, answer, reply_markup=keyboard_markup, parse_mode='Markdown')


async def check_if_wumpus_in_room_connects(keyboard_markup, query, wumpus_is_near):
    if wumpus_is_near:
        keyboard_markup.add(types.InlineKeyboardButton('Стрелять', callback_data='shot'))
        keyboard_markup.add(types.InlineKeyboardButton('Идти дальше', callback_data='move_on'))

        await bot.send_message(query.from_user.id, wumpus_is_near, parse_mode='Markdown')


async def check_if_player_in_bats_room_connects(keyboard_markup, query, session, check):
    if check:
        answer = ''' КАЖЕТСЯ В СОСЕДНЕЙ КОМНАТЕ КАКИЕ-ТО СТРАННЫЕ ЗВУКИ '''

        await bot.send_message(query.from_user.id, answer, parse_mode='Markdown')


async def check_if_player_in_traps_room_connects(keyboard_markup, query, session, check):
    if check:
        answer = ''' В ОДНОЙ ИЗ КОМНАТ ДУЕТ ВЕТЕР, КУДА ПОЙДЁМ '''

        await bot.send_message(query.from_user.id, answer, parse_mode='Markdown')


async def check_if_player_in_gold_room_connects(keyboard_markup, query, session, check):
    if check:
        GOLD_IN_NEAR_ROOM = 'В КОМНАТЕ РЯДОМ ЕСТЬ ЗОЛОТО, КУДА ПОЙДЁМ?)'

        await bot.send_message(query.from_user.id, GOLD_IN_NEAR_ROOM, parse_mode='Markdown')


async def check_if_player_in_gold_location(keyboard_markup, query, session, check):
    if check:
        answer = 'В КОМНАТЕ ЕСТЬ ЗОЛОТО, СЫГРАЙ В ИГРУ ЧТОБЫ ДОКУПИТЬ СТРЕЛЫ'
        keyboard_markup.add(types.InlineKeyboardButton('Сыграть', callback_data='play_gold'))
        keyboard_markup.add(types.InlineKeyboardButton('Идти дальше', callback_data='move_on'))

        await bot.send_message(query.from_user.id, answer, reply_markup=keyboard_markup, parse_mode='Markdown')


async def check_if_player_in_trap_location(keyboard_markup, query, session, check):
    if check:
        answer = 'КАК ТОЛЬКО ТЫ ВОШЁЛ КОМНАТА ЗАКРЫЛАСЬ, НА ДВЕРИ ЗАМОК УГАДАЙ ЧИСЛО'
        keyboard_markup.add(types.InlineKeyboardButton('УГАДАТЬ', callback_data='play_gold'))

        await bot.send_message(query.from_user.id, answer, reply_markup=keyboard_markup, parse_mode='Markdown')


async def check_if_player_in_wumpus_location(query, check):
    if check:
        answer = 'ВЫ ПРОИГРАЛИ ПОПАВ В ЛОВУШКУ К ВАМПУСУ, ИГРА ОКОНЧЕНА!!!'

        await bot.send_message(query.from_user.id, answer, reply_markup=FinishKeyboard(), parse_mode='Markdown')


''' ОБРАБОТЧИК КНОПКИ ДВИГАТЬСЯ ДАЛЬШЕ '''


@dp.callback_query_handler(lambda cb: cb.data in ['move_on'])
async def move_on(query: types.CallbackQuery):
    try:
        print('ДВИГАТЬСЯ ДАЛЬШЕ')
        # получаю выбор пользователя
        player_choice_number, session = await get_session_and_player_choice_number(query)

        # встроенная клавиатура
        keyboard_markup = types.InlineKeyboardMarkup()

        player_choices = session.get_player_choices()

        for player_choice in player_choices:
            keyboard_markup.add(types.InlineKeyboardButton(str(player_choice),
                                                           callback_data=f'next_room{player_choice}'))

        await bot.send_message(query.from_user.id, session.get_message_for_player_choices(),
                               reply_markup=keyboard_markup, parse_mode='Markdown')
    except Exception:
        print(traceback.format_exc())
        await bot.send_message(query.from_user.id, 'Что-то пошло не так, 🤷🏼‍♀️ возврат в главное меню.',
                               reply_markup=MainKeyboard())


''' ОБРАБОТЧИК КНОПКИ ВЫБОРА ВЫСТРЕЛА shot '''


@dp.callback_query_handler(lambda cb: cb.data in ['shot'])
async def shot(query: types.CallbackQuery):
    try:
        # получаю выбор пользователя
        print('ВЫСТРЕЛ')
        print(query.data)
        # получаю выбор пользователя
        player_choice_number, session = await get_session_and_player_choice_number(query)

        # встроенная клавиатура
        keyboard_markup = types.InlineKeyboardMarkup()
        player_choices = session.get_player_choices()

        # вырианты выбора комнат в которые можно выстрелить
        for player_choice in player_choices:
            keyboard_markup.add(types.InlineKeyboardButton(str(player_choice),
                                                           callback_data=f'shot_in_room{player_choice}'))

        await bot.send_message(query.from_user.id, session.get_message_for_player_shots(),
                               reply_markup=keyboard_markup, parse_mode='Markdown')

    except Exception:
        print(traceback.format_exc())
        await bot.send_message(query.from_user.id, 'Что-то пошло не так, 🤷🏼‍♀️ возврат в главное меню.',
                               reply_markup=MainKeyboard())


''' ОБРАБОТЧИК КНОПКИ СЫГРАТЬ play_gold '''


@dp.callback_query_handler(lambda cb: cb.data in ['play_gold'])
async def play_gold(query: types.CallbackQuery):
    try:

        print('ИГРА НА ЗОЛОТО')
        # получаю выбор пользователя и сессию
        player_choice_number, session = await get_session_and_player_choice_number(query)

        print(player_choice_number)

        # встроенная клавиатура
        keyboard_markup = types.InlineKeyboardMarkup()
        player_choices = list(range(1, 4))

        TAKE_GOLD = 'УГАДАЙ ЧИСЛО ОТ 1 ДО 3'

        # вырианты выбора комнат в которые можно выстрелить
        for player_choice in player_choices:
            keyboard_markup.add(types.InlineKeyboardButton(str(player_choice),
                                                           callback_data=f'take_gold{player_choice}'))

        await bot.send_message(query.from_user.id, TAKE_GOLD,
                               reply_markup=keyboard_markup, parse_mode='Markdown')

    except Exception:
        print(traceback.format_exc())
        await bot.send_message(query.from_user.id, 'Что-то пошло не так, 🤷🏼‍♀️ возврат в главное меню.',
                               reply_markup=MainKeyboard())


''' ОБРАБОТЧИК КНОПКИ ВЫБОРА ЧИСЛА (СЫГРАТЬ) '''


@dp.callback_query_handler(lambda cb: cb.data in ['take_gold1', 'take_gold2', 'take_gold3', 'take_gold4', 'take_gold5'])
async def take_gold(query: types.CallbackQuery):
    try:
        print('ИГРА НА ЗОЛОТО ВЫБИРАЮ ЧИСЛО take_gold')
        # получаю выбор пользователя
        player_choice_number, session = await get_session_and_player_choice_number(query)

        # встроенная клавиатура
        keyboard_markup = types.InlineKeyboardMarkup()

        choices = list(range(1, 4))

        win_choice = random.choice(choices)

        print(win_choice, 'win_choice')

        player_choices = session.get_player_choices()

        if win_choice == int(player_choice_number):
            # вырианты выбора комнат в которые можно выстрелить
            for player_choice in player_choices:
                keyboard_markup.add(
                    types.InlineKeyboardButton(str(player_choice), callback_data=f'next_room{player_choice}'))
            await bot.send_message(chat_id=query.from_user.id, text='Вы победили и получаете 500 золота. Куда дальше?',
                                   reply_markup=keyboard_markup, parse_mode='Markdown')

        else:
            for player_choice in player_choices:
                keyboard_markup.add(
                    types.InlineKeyboardButton(str(player_choice), callback_data=f'next_room{player_choice}'))

            await bot.send_message(query.from_user.id, text='ВЫ ПРОИГРАЛИ',
                                   reply_markup=FinishKeyboard(), parse_mode='Markdown')


    except Exception as ex:
        print(ex)
        print(traceback.format_exc())
        await bot.send_message(query.from_user.id, 'Что-то пошло не так, 🤷🏼‍♀️ возврат в главное меню.',
                               reply_markup=MainKeyboard())


''' ОБРАБОТЧИК КНОПКИ ВСКРЫТЬ open_up '''


@dp.callback_query_handler(lambda cb: cb.data in ['open_up'])
async def open_up(query: types.CallbackQuery):
    try:
        print('ОБРАБОТЧИК КНОПКИ ВСКРЫТЬ open_up')
        # получаю выбор пользователя и сессию
        player_choice_number, session = await get_session_and_player_choice_number(query)

        print(player_choice_number)

        # встроенная клавиатура
        keyboard_markup = types.InlineKeyboardMarkup()
        player_choices = list(range(1, 4))

        answer = 'УГАДАЙ ЧИСЛО ОТ 1 ДО 3'

        # вырианты выбора комнат в которые можно выстрелить
        for player_choice in player_choices:
            keyboard_markup.add(types.InlineKeyboardButton(str(player_choice),
                                                           callback_data=f'open_up{player_choice}'))

        await bot.send_message(query.from_user.id, answer,
                               reply_markup=keyboard_markup, parse_mode='Markdown')

    except Exception as ex:
        print(ex)
        print(traceback.format_exc())
        await bot.send_message(query.from_user.id, 'Что-то пошло не так, 🤷🏼‍♀️ возврат в главное меню.',
                               reply_markup=MainKeyboard())


''' ОБРАБОТЧИК КНОПКИ ВЫБИРА ЧИСЛА (ВСКРЫТЬ) '''


@dp.callback_query_handler(lambda cb: cb.data in ['open_up1', 'open_up2', 'open_up3'])
async def open_up_number(query: types.CallbackQuery):
    try:
        print(' ОБРАБОТЧИК КНОПКИ ВЫБИРА ЧИСЛА (ВСКРЫТЬ) ')
        # получаю выбор пользователя
        player_choice_number, session = await get_session_and_player_choice_number(query)

        # встроенная клавиатура
        keyboard_markup = types.InlineKeyboardMarkup()
        player_choices = session.get_player_choices()

        if player_choices == random.choice(list(range(1, 4))):
            win_gold = 'ВАМ ПОВЕЗЛО, ВЫ ПОДОБРАЛИ КОД ОТ ДВЕРИ И ВЫ СМОГЛИ ВЫЙТИ НАРУЖУ, ЧТО ДАЛЬШЕ?'

            # вырианты выбора комнат в которые можно выстрелить
            for player_choice in player_choices:
                keyboard_markup.add(
                    types.InlineKeyboardButton(str(player_choice), callback_data=f'next_room{player_choice}'))

            await bot.send_message(query.from_user.id, win_gold,
                                   reply_markup=keyboard_markup, parse_mode='Markdown')

        else:
            await bot.send_message(query.from_user.id,
                                   text='ВНЕЗАПНО В КОМНАТУ ВОРВАЛСЯ ВАМПУС - ВЫ ПРОИГРАЛИ, ЧТО ДАЛЬШЕ?',
                                   reply_markup=FinishKeyboard(), parse_mode='Markdown')

    except Exception as ex:
        print(ex)
        print(traceback.format_exc())
        await bot.send_message(query.from_user.id, 'Что-то пошло не так, 🤷🏼‍♀️ возврат в главное меню.',
                               reply_markup=MainKeyboard())


''' CALLBACK ДЛЯ ВЫБОРА ВЫСТРЕЛА '''
shot_in_rooms = ['shot_in_room1', 'shot_in_room2', 'shot_in_room3', 'shot_in_room4', 'shot_in_room5', 'shot_in_room6',
                 'shot_in_room7', 'shot_in_room8', 'shot_in_room9', 'shot_in_room10', 'shot_in_room11',
                 'shot_in_room12', 'shot_in_room13', 'shot_in_room14', 'shot_in_room15', 'shot_in_room16',
                 'shot_in_room17', 'shot_in_room18', 'shot_in_room19', 'shot_in_room20']


@dp.callback_query_handler(lambda cb: cb.data in shot_in_rooms)
async def shot_in_room(query: types.CallbackQuery):
    try:
        print('ВЫСТРЕЛ')

        # получаю выбор пользователя
        player_choice_number, session = await get_session_and_player_choice_number(query)

        if player_choice_number == session.wumpus.location:
            answer = 'ПОЗДРАВЛЯЮ, ВЫ ПОБЕДИЛИ!!!'

        else:
            answer = 'ВАМПУС ПОБЕДИЛ'

        await bot.send_message(query.from_user.id, answer,
                               reply_markup=FinishKeyboard(), parse_mode='Markdown')

    except Exception as ex:
        print(ex)
        print(traceback.format_exc())
        await bot.send_message(query.from_user.id, 'Что-то пошло не так, 🤷🏼‍♀️ возврат в главное меню.',
                               reply_markup=MainKeyboard())


async def get_session_and_player_choice_number(query):
    filter_player_choice_data = list(filter(str.isdigit, query.data))
    player_choice_number = ''.join(filter_player_choice_data)
    # получаю дату из базы
    answer = await db.wumpus.find_one({"tgid": query.from_user.id})
    answer_session = answer['session']
    session_dict = json.loads(answer_session)
    # создаю сессию
    session = Session(session_dict['tgid'])
    # получаю обхект
    session.get_from_db(session_dict)
    return player_choice_number, session


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)
