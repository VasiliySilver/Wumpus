import json


class Room:
    """
    Представляет комнату
    """

    def __init__(self, room, room_connects, wumpus=None, player=None, bat=None, gold=None, trap=None):
        self.number = room
        self.room_connects = room_connects

    def __repr__(self):
        return json.dumps(self.__dict__)

    def __str__(self):
        return self.number

    def create_room(self):
        pass

    def update_room(self):
        pass


class RoomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Room):
            return obj.__dict__
        return json.JSONEncoder.default(self, obj)
