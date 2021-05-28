import json

from session import Session

session = Session('1234')

def dumper(obj):
    try:
        return obj.toJSON()
    except:
        return obj.__dict__
print(json.loads(str(session), default=dumper, indent=2))



a = list(range(1, 21))
b = [f'shot_wumpus{i}' for i in a]
print(b)

c = 'shot_wumpus_21'
v = list(filter(str.isdigit, c))
print(''.join(v))

some = ['shot_wumpus1', 'shot_wumpus2', 'shot_wumpus3', 'shot_wumpus4', 'shot_wumpus5', 'shot_wumpus6', 'shot_wumpus7', 'shot_wumpus8', 'shot_wumpus9', 'shot_wumpus10', 'shot_wumpus11', 'shot_wumpus12', 'shot_wumpus13', 'shot_wumpus14', 'shot_wumpus15', 'shot_wumpus16', 'shot_wumpus17', 'shot_wumpus18', 'shot_wumpus19', 'shot_wumpus20']
