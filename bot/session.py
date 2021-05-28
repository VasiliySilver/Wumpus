import json
import random
# from typing import List, Any

from bot.cave import Cave
from bot.npc import Wumpus, Bat, Gold, Trap, Player


class Session:
    """
    Сессия игры
    """
    __counter = 0

    def __init__(self, tgid):
        Session.__counter += 1
        print(Session.__counter)

        self.tgid = tgid
        self.cave = Cave()

        self.tmp_list_rooms = list(range(1, 20))
        random.shuffle(self.tmp_list_rooms)

        tmp_room = self.tmp_list_rooms.pop(0)
        self.player = Player(tmp_room, self.cave.dict_rooms[tmp_room])

        tmp_room = self.tmp_list_rooms.pop(0)
        self.wumpus = Wumpus(tmp_room, self.cave.dict_rooms[tmp_room])

        tmp_bat1 = self.tmp_list_rooms.pop(0)
        tmp_bat2 = self.tmp_list_rooms.pop(0)
        self.bats = [Bat(tmp_bat1, self.cave.dict_rooms[tmp_bat1]), Bat(tmp_bat2, self.cave.dict_rooms[tmp_bat2])]

        tmp_gold1 = self.tmp_list_rooms.pop(0)
        tmp_gold2 = self.tmp_list_rooms.pop(0)
        tmp_gold3 = self.tmp_list_rooms.pop(0)
        tmp_gold4 = self.tmp_list_rooms.pop(0)
        self.golds = [Gold(tmp_gold1, self.cave.dict_rooms[tmp_gold1]),
                      Gold(tmp_gold2, self.cave.dict_rooms[tmp_gold2]),
                      Gold(tmp_gold3, self.cave.dict_rooms[tmp_gold3]),
                      Gold(tmp_gold4, self.cave.dict_rooms[tmp_gold4])]

        tmp_trap1 = self.tmp_list_rooms.pop(0)
        tmp_trap2 = self.tmp_list_rooms.pop(0)
        self.traps = [Trap(tmp_trap1, self.cave.dict_rooms[tmp_trap1]),
                      Trap(tmp_trap2, self.cave.dict_rooms[tmp_trap2])]

    def __str__(self):
        return f'Текущая сессия: {self.__counter}'

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def get_from_db(self, data) -> None:
        Session(data['tgid'])
        # id пользователя
        self.tgid = data['tgid']

        # создаю пещеру
        self.cave = Cave()
        self.cave.dict_rooms = data['cave']['dict_rooms']
        self.cave.rooms = data['cave']['rooms']

        # получаю игрока
        self.player = Player(data['player']['location'], data['player']['room_connects'])

        # получаю вампуса
        self.wumpus = Wumpus(data['wumpus']['location'], data['wumpus']['room_connects'])

        # получаю мышей
        self.bats = [Bat(i['location'], i['room_connects']) for i in data['bats']]

        # получаю золото
        self.golds = [Gold(i['location'], i['room_connects']) for i in data['golds']]

        # получаю ловушки
        self.traps = [Trap(i['location'], i['room_connects']) for i in data['traps']]

    def check_that_wumpus_is_near(self) -> str:
        """
        Предупреждает о том что вампус в соседней комнате
        """
        if self.wumpus.location in self.player.room_connects:
            print('Чую запах, кажется вампус рядом')
            return 'Чую запах, кажется вампус рядом!!! Что будем делать?'

    def get_player_choices(self) -> str:
        """
        Получает варианты комнат которые может выбрать пользователь
        """
        return self.player.room_connects

    def get_message_for_player_choices(self):
        return f'Выбери одну из комнат - {self.get_player_choices()}'

    def get_message_for_player_shots(self):
        return f'Выбери одну из комнат куда будите стрелять - {self.get_player_choices()}'

    def get_wumpus_location(self):
        return self.wumpus.location

    def get_player_location(self):
        return self.player.location

    def check_if_trap(self):
        if self.player.location in [i.location for i in self.traps]:
            return True

        else:
            return False

    def bat_change_player_location(self):
        """
        Изменяет в рандомном порядке местонахождение мыши
        Returns:
            None
        """
        # получаю 20-ть комнат
        rooms = list(range(1, 21))
        # получаю локации мышей
        bats_locations = [i.location for i in self.bats]
        # получаю локации с золотом
        gold_locations = [i.location for i in self.golds]
        # получаю локации с ловушками
        trap_locations = [i.location for i in self.traps]
        # локации на удаление
        locations_for_delete = bats_locations + gold_locations + trap_locations
        locations_for_delete.append(self.wumpus.location)
        # доступные локации
        allow_locations = set(rooms) - set(locations_for_delete)
        # выбираем рандомную комнату из списка доступных
        new_room = random.choice(list(allow_locations))

        new_rooms = self.cave.dict_rooms[str(new_room)]
        print(new_rooms, 'new_rooms')
        self.player.location = new_room
        self.player.room_connects = new_rooms

    def player_moves_to_another_room(self, location):
        self.player.location = location
        self.player.room_connects = self.cave.dict_rooms[location]
