from game import Game

values = [(9, 9), (19, 19), (29, 29), (39, 39), (49, 49), (59, 59), (69, 69)]

for m, n in values:
    g = Game(m, n, 4)
    g.start(True, (400,400))
