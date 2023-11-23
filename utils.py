import math

# Hilfsfunktionen für Wegfindung
def heuristik(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def euklidische_heuristik(a, b):
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)