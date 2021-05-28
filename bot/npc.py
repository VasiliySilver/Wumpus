import json


class Player:
    """
    Представляет игрока
    """
    def __init__(self, room, room_connects):
        self.room_connects = room_connects
        self.location = room

    def __repr__(self):
        return json.dumps(self.__dict__)

    def get_player_location(self):
        return f'Вы находитесь в комнате - {self.location}'

    def shot_at_the_wumpus(self):
        pass

    def delete_player(self):
        pass

    def some(self):
        pass


class Wumpus:
    """
    Представляет Вампуса
    """

    def __init__(self, room, room_connects):
        self.room_connects = room_connects
        self.location = room

    def __repr__(self):
        return json.dumps(self.__dict__)

    def spear_throw(self, player_location):
        pass


class Bat:
    """
    Представляет мышь
    """

    def __init__(self, room, room_connects):
        self.room_connects = room_connects
        self.location = room

    def __repr__(self):
        return json.dumps(self.__dict__)

    def change_player_location(self, player_location):
        pass


class Trap:
    """
    Представляет комнату ловушку
    """

    def __init__(self, room, room_connects):
        self.room_connects = room_connects
        self.location = room

    def __repr__(self):
        return json.dumps(self.__dict__)

    def play_or_die(self):
        pass


class Gold:
    """
    Представляет комнату с золотом
    """

    gold = 0

    def __init__(self, room, room_connects):
        self.room_connects = room_connects
        self.location = room

    def __str__(self):
        return self.gold

    def __repr__(self):
        return json.dumps(self.__dict__)

    def buy_spear(self):
        self.gold -= 1000
        return self.gold

    def take_gold(self):
        self.gold += 500
        return self.gold
