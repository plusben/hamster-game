# Importiere erforderliche Module
from utils import heuristik  # Importiere die Funktion 'heuristik' aus dem Modul 'utils'
import heapq  # Importiere das Modul 'heapq' für die Priority Queue
import sys  # Importiere das Modul 'sys' für Systemfunktionen
import pygame  # Importiere das Modul 'pygame' für die Spielentwicklung
import collections  # Fehlender Import für namedtuple

# Definiere die Klasse 'Hamster'
class Hamster:
    def __init__(self, x, y, spielfeld):
        self.x = x
        self.y = y
        self.spielfeld = spielfeld
        self.pfad = []
        self.zurueckgelegter_pfad = []
        self.gesammelte_koerner = []  # Liste der gesammelten Körner
        self.richtung = 'rechts'  # Startet standardmäßig nach rechts

    def aktualisiere_pfad(self, ziel):
        from hamstergame import a_stern  # Importiere die a_stern Funktion hier, um einen erneuten Import zu vermeiden
        self.pfad = a_stern(self.spielfeld, (self.x, self.y), ziel)
        print(f"Pfad nach aktualisiere_pfad: {self.pfad}")  # Debug-Ausgabe für den aktualisierten Pfad

    def naechster_schritt(self, koerner):
        if self.pfad:
            naechster_schritt = self.pfad.pop(0)
            if self.spielfeld[naechster_schritt[1]][naechster_schritt[0]] == 0:
                self.x, self.y = naechster_schritt
                self.zurueckgelegter_pfad.append(naechster_schritt)
                if naechster_schritt in koerner:
                    self.gesammelte_koerner.append(naechster_schritt)
                    koerner.remove(naechster_schritt)
                print(f"Hamster bewegt sich zu: ({self.x}, {self.y})")  # Debug-Ausgabe für die Bewegung des Hamsters
            else:
                print(f"Nächstes Feld ({naechster_schritt[0]}, {naechster_schritt[1]}) ist blockiert.")
        else:
            print("Kein verbleibender Pfad im naechster_schritt")  # Debug-Ausgabe, wenn kein Pfad vorhanden ist


# Benanntes Tupel für Positionen
Position = collections.namedtuple('Position', ['x', 'y'])


def gueltige_position(position, spielfeld):
    """
    Überprüft, ob die Position auf dem Spielfeld gültig ist.
    """
    x, y = position
    return 0 <= x < len(spielfeld[0]) and 0 <= y < len(spielfeld) and spielfeld[y][x] == 0

def a_stern(spielfeld, start, ziel):
    nachbarn = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    zu_besuchen = []
    kosten = {start: 0}  # Initialisiere die Kosten-Variable
    heapq.heappush(zu_besuchen, (0 + heuristik(start, ziel), start))
    pfad = {}  # Dictionary zur Verfolgung des Pfads

    while zu_besuchen:
        _, aktuelle_position = heapq.heappop(zu_besuchen)

        if aktuelle_position == ziel:
            weg = []
            while aktuelle_position != start:
                weg.append(aktuelle_position)
                aktuelle_position = pfad[aktuelle_position]
            weg.append(start)
            return weg[::-1]

        for richtung in nachbarn:
            nachbar = (aktuelle_position[0] + richtung[0], aktuelle_position[1] + richtung[1])

            if gueltige_position(nachbar, spielfeld):
                neue_kosten = kosten[aktuelle_position] + 1
                if nachbar not in kosten or neue_kosten < kosten[nachbar]:
                    kosten[nachbar] = neue_kosten
                    prioritaet = neue_kosten + heuristik(nachbar, ziel)
                    heapq.heappush(zu_besuchen, (prioritaet, nachbar))
                    pfad[nachbar] = aktuelle_position

    print("Kein Pfad gefunden")


def test_a_stern():
    spielfeld = [
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ]
    start = (1, 1)
    ziel = (4, 4)
    pfad = a_stern(spielfeld, start, ziel)
    print(f"Berechneter Pfad von {start} nach {ziel}: {pfad}")

if __name__ == "__main__":
    test_a_stern()