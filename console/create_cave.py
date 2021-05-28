def get_levels_in_cave():
    """
    Получает уровни пещеры по пять элементов
    Returns:
        list: list(list, list, list, list)
    """
    mas = list(range(1, 21))
    # random.shuffle( mas )
    massivs = []
    for i in range(4):
        one = []

        for j in range(5):
            one.append(mas.pop(0))

        massivs.append(one)
    return massivs


def get_connects_on_first_level(cave: dict, one: list, two: list) -> None:
    """
    Получаю связи для комнат первого уровня
    Args:
        cave:
        one:
        two:
    """
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


def get_connects_on_second_level(cave: dict, one: list, three: list, two: list) -> None:
    """
    Получаю связи для первого, второго и третего уровней
    Args:
        cave:
        one:
        three:
        two
    """
    for i in range(len(two)):
        # Получаем комнату из второго уровня
        room = two[i]
        # создаём комнату и связи
        cave[room] = []
        # Добавляем комнату что выше текущей
        cave[room].append(one[i])
        cave[room].append(three[i])
        cave[room].append(three[(i + 1) % 5])


def get_connects_on_third_level(cave: dict, four: list, three: list, two: list) -> None:
    """
    Получаю связи для третьего уровня
    Args:
        cave:
        four:
        three:
        two
    """
    for i in range(len(three)):
        room = three[i]
        # создаём комнату и связи
        cave[room] = []
        # Комната что ниже текущей
        cave[room].append(four[i])
        cave[room].append(two[i])
        cave[room].append(two[(i - 1)])


def get_connects_on_fourth_level(cave: dict, four: list, three: list) -> None:
    for i in range(len(four)):
        room = four[i]
        # создаём комнату и связи
        cave[room] = []
        # элемент левее текущего
        cave[room].append(four[i - 1])
        # элемент что выше находится
        cave[room].append(three[i])
        # Элемент правее этой комнаты
        cave[room].append(four[(i + 1) % 5])


def create_cave() -> dict:
    """
    Создает пещеру
    Returns:
        dict: {item: [near_item, near_item, near_item], ...}
    """
    # Заготовка лабиранта - граф пещеры
    cave = {}
    # Получаем 4-ре уровня лабирината
    one, two, three, four = get_levels_in_cave()
    # Заполняем комнаты на первом уровне
    get_connects_on_first_level(cave, one, two)
    # Заполняем комнаты на втором уровне
    get_connects_on_second_level(cave, one, three, two)
    # Заполняем комнаты на третьем уровне
    get_connects_on_third_level(cave, four, three, two)
    # Заполняем комнаты на 4ом уровне
    get_connects_on_fourth_level(cave, four, three)
    # возвращаем пещеру
    return cave
