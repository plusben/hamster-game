import random
import json

def generiere_spielfeld(breite, hoehe, hindernis_prozent):
    spielfeld = [[1 if x == 0 or x == breite - 1 or y == 0 or y == hoehe - 1 else 0 for x in range(breite)] for y in range(hoehe)]

    for y in range(1, hoehe - 1):
        for x in range(1, breite - 1):
            if random.random() < hindernis_prozent:
                spielfeld[y][x] = 1

    return spielfeld

def speichere_level(dateiname, level_liste):
    with open(dateiname, 'w') as datei:
        json.dump(level_liste, datei)

def generiere_level(anzahl_level, breite, hoehe, hindernis_min, hindernis_max):
    level_liste = []
    for _ in range(anzahl_level):
        hindernis_prozent = random.uniform(hindernis_min, hindernis_max)
        level_liste.append(generiere_spielfeld(breite, hoehe, hindernis_prozent))
    return level_liste

if __name__ == "__main__":
    anzahl_level = 5  # Anzahl der zu generierenden Level
    breite = 16  # Breite des Spielfelds
    hoehe = 12  # Höhe des Spielfelds
    hindernis_prozent = 0.2  # Prozentuale Wahrscheinlichkeit für Hindernisse
    hindernis_min = 0.15
    hindernis_max = 0.25
    level_liste = generiere_level(anzahl_level, breite, hoehe, hindernis_min, hindernis_max)
    speichere_level('levels.json', level_liste)
