import random

from create_cave import create_cave


def get_action_rooms():
    rooms = list(range(1, 21))
    random.shuffle(rooms)
    action_rooms_dict = dict()
    action_rooms_dict['wumpus'] = rooms.pop(0)
    action_rooms_dict['player'] = rooms.pop(0)
    action_rooms_dict['bats'] = [rooms.pop(0), rooms.pop(0)]
    action_rooms_dict['closes'] = [rooms.pop(0), rooms.pop(0)]
    action_rooms_dict['golds'] = [rooms.pop(0) for _ in range(4)]
    return action_rooms_dict


def shuffle_bat_location(from_room, action_rooms_dict):
    """
    Изменяет в рандомном порядке местонахождение мыши
    Returns:
        None
    """
    # 20-ть комнат
    rooms = set(range(1, 21))
    # убираем мышь из комнаты в которой она сидела
    action_rooms_dict['bats'].remove(from_room)
    bats = set(action_rooms_dict['bats'])
    closes = set(action_rooms_dict['closes'])
    golds = set(action_rooms_dict['golds'])
    other = {action_rooms_dict['player'], action_rooms_dict['wumpus']}
    # доступные комнаты, без мышей, золота игрока, замка и вампуса
    allow_rooms = rooms - bats - closes - golds - other
    # выбираем рандомную комнату из списка доступных
    new_room = random.choice(list(allow_rooms))
    action_rooms_dict['bats'].append(new_room)


def attention_that_wumpus_is_near(action_rooms_dict: dict, cave_dict: dict) -> None:
    """
    Предупреждает о том что вампус в соседней комнате
    """
    if action_rooms_dict["wumpus"] in cave_dict[action_rooms_dict['player']]:
        print('Чую запах, кажется вампус рядом')


def method_name():
    global gold, arrows
    print("В комнате есть золото")
    gold += 500
    # Убираем из этой комнаты золото
    action_rooms['golds'].remove(action_rooms["player"])
    print("Вы купили стрелу")
    arrows += 1


if __name__ == "__main__":
    # создём пещеры
    cave = create_cave()
    # получаем комнаты с действиями
    action_rooms = get_action_rooms()

    # Количество стрел у игрка
    arrows = 0

    # Кол-во золота
    gold = 0

    while True:
        print('\n' + '-' * 20)
        print(f'Вы находитесь в комнате {action_rooms["player"]}')
        # предупреждает что вампус рядом
        attention_that_wumpus_is_near(action_rooms, cave)

        if action_rooms['player'] in action_rooms['closes']:
            # Если в комнате есть замок играем в игру

            answer = input('Тебя заперли, на двери замок, угадай число [1,5]: ')
            true_answer = str(random.randint(1, 5))
            # проверка ввода пользователя
            # Пока не введёт в нужном промежутке
            while answer not in {'1', '2', '3', '4', '5'}:
                print(f'\t{answer} - не число от 1 до 5')
                answer = input('Введи правильно: ')

            if answer != true_answer:
                print("Вампус кидает копьё")
                if random.choice([True, False]):
                    print("ВАМПУС ПОБЕДИЛ!!! ИГРА ОКОНЧЕНА")
                    break
                else:
                    print("ВАМПУС НЕ ПОПАЛ, СКОРЕЙ БЕГИ И ПРЯЧЬСЯ")

            else:
                answer = input(f"Выбирай куда пойдёшь {cave[action_rooms['player']]}: ")
                # проверка ввода пользователя
                # Пока не введёт в нужном промежутке
                while answer not in map(str, cave[action_rooms['player']]):
                    print(f'\tкомнаты {answer} нет среди  cave[action_rooms["player"]]')
                    answer = input('Введи правильно: ')

                action_rooms['player'] = int(answer)

        if action_rooms['player'] in action_rooms['bats']:
            # Иначе если в комнате летучая мышь
            # Переносим играка в рандомную комнату
            print("Внезапно тебя подхватила огромная летучая мышь")
            shuffle_bat_location(action_rooms["player"], action_rooms)
            action_rooms["player"] = random.randint(1, 20)
            print(f"И унесла тебя в комнату {action_rooms['player']}")

        if action_rooms["player"] in action_rooms['golds']:
            # В комнате есть золото
            method_name()

        if action_rooms["player"] == action_rooms['wumpus']:
            # если в комнате ВАМПУС
            print("КОМНАТА ОКАЗАЛАСЬ ЛОВУШКОЙ - ВАС СЪЕЛ ВАМПУС!!!\nКОНЕЦ ИГРЫ!")
            break
        else:
            # Комната пустая
            print(f"Двери внутри ведут в {cave[action_rooms['player']]}")

            if action_rooms["wumpus"] in cave[action_rooms['player']]:
                answer = input('\n\t1 - Стрелять\n\t2- Идти дальше\nЧто выбереш?: ')
                while answer not in ['1', '2']:
                    answer = input("Введи число от 1 до 2: ")

                if answer == '1':
                    room = input(f'Выбери куда стрелять {cave[action_rooms["player"]]}: ')
                    while room not in map(str, cave[action_rooms["player"]]):
                        room = input(f"Введи правильную дверь {cave[action_rooms['player']]}: ")
                    # Если он попал
                    if int(room) == action_rooms['wumpus']:
                        print("Вы ПОБЕДИЛИ")
                        break
                    else:
                        print('Вы промахнулись')
                else:
                    # Игрок выбрал идти
                    room = input(f'Выбери куда идти {cave[action_rooms["player"]]}: ')
                    while room not in map(str, cave[action_rooms["player"]]):
                        room = input(f"Введи правильную дверь {cave[action_rooms['player']]}: ")
                    action_rooms['player'] = int(room)
            else:
                # хищника нет - просто выбираем дверь
                room = input('Выбери куда идти: ')
                while room not in map(str, cave[action_rooms["player"]]):
                    room = input(f"Введи правильную дверь {cave[action_rooms['player']]}: ")
                action_rooms['player'] = int(room)
