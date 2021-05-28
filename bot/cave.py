import json

from bot.room import Room


def get_levels_in_cave() -> list:
    """
    Получает уровни пещеры по пять элементов
    Returns:
        list: list(list,list, list, list)
    """
    mas = list(range(1, 21))
    # random.shuffle( mas )
    list_levels = []
    for i in range(4):
        one = []

        for j in range(5):
            one.append(mas.pop(0))

        list_levels.append(one)
    return list_levels


def get_connects_on_first_level(cave: dict, one: list, two: list) -> None:
    for i in range(len(one)):
        room = one[i]
        # создаём комнату и связи
        cave[room] = []
        # элемент левее текущего
        cave[room].append(one[i - 1])
        # элемент что ниже находится
        cave[room].append(two[i])
        # Элемент правее этой комнаты
        cave[room].append(one[(i + 1) % 5])


def get_connects_on_second_level(cave_dict: dict, one: list, three: list, two: list) -> None:
    for i in range(len(two)):
        # Получаем комнату из второго уровня
        room = two[i]
        # создаём комнату и связи
        cave_dict[room] = []
        # Добавляем комнату что выше текущей
        cave_dict[room].append(one[i])
        cave_dict[room].append(three[i])
        cave_dict[room].append(three[(i + 1) % 5])


def get_connects_on_third_level(cave_dict: dict, four: list, three: list, two: list) -> None:
    for i in range(len(three)):
        room = three[i]
        # создаём комнату и связи
        cave_dict[room] = []
        # Комната что ниже текущей
        cave_dict[room].append(four[i])
        cave_dict[room].append(two[i])
        cave_dict[room].append(two[(i - 1)])


def get_connects_on_fourth_level(cave_dict: dict, four: list, three: list) -> None:
    for i in range(len(four)):
        room = four[i]
        # создаём комнату и связи
        cave_dict[room] = []
        # элемент левее текущего
        cave_dict[room].append(four[i - 1])
        # элемент что выше находится
        cave_dict[room].append(three[i])
        # Элемент правее этой комнаты
        cave_dict[room].append(four[(i + 1) % 5])


def create_cave_dict() -> dict:
    """
    Создает пещеру
    Returns:
        dict: {item: [near_item, near_item, near_item], ...}
    """
    # Заготовка лабиранта - граф пещеры
    cave_dict = {}
    # Получаем 4-ре уровня лабирината
    one, two, three, four = get_levels_in_cave()
    # Заполняем комнаты на первом уровне
    get_connects_on_first_level(cave_dict, one, two)
    # Заполняем комнаты на втором уровне
    get_connects_on_second_level(cave_dict, one, three, two)
    # Заполняем комнаты на третьем уровне
    get_connects_on_third_level(cave_dict, four, three, two)
    # Заполняем комнаты на 4ом уровне
    get_connects_on_fourth_level(cave_dict, four, three)
    # возвращаем пещеру
    return cave_dict


class Cave:
    """
    Представляет пещеру
    """
    dict_rooms = {}
    rooms = []

    def __init__(self):
        self.create_cave()

    def __str__(self):
        return self.rooms

    def create_cave(self):
        self.dict_rooms = create_cave_dict()
        self.rooms = [Room(room=r, room_connects=self.dict_rooms[r]) for r in self.dict_rooms]

    def update_cave(self):
        pass

    def delete_cave(self):
        pass


class CaveEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Cave):
            return obj.__dict__
        return json.JSONEncoder.default(self, obj)
