# Importiere erforderliche Module
from utils import euklidische_heuristik  # Importiere die Funktion 'heuristik' aus dem Modul 'utils'
import heapq  # Importiere das Modul 'heapq' für die Priority Queue
import collections  # Fehlender Import für namedtuple

# Definiere die Klasse 'Hamster'
class Hamster:
    def __init__(self, x, y, spielfeld):
        """
        Initialisiert einen Hamster mit seiner Position auf dem Spielfeld.

        Args:
            x (int): Die x-Koordinate des Hamsters.
            y (int): Die y-Koordinate des Hamsters.
            spielfeld (list): Die Darstellung des Spielfelds als 2D-Liste.
        """
        self.x = x
        self.y = y
        self.spielfeld = spielfeld
        self.pfad = []  # Aktueller Pfad des Hamsters
        self.zurueckgelegter_pfad = []  # Liste der bereits zurückgelegten Felder
        self.gesammelte_koerner = []  # Liste der gesammelten Körner
        self.richtung = 'rechts'  # Startet standardmäßig nach rechts

    def aktualisiere_pfad(self, ziel):
        """
        Aktualisiert den Pfad des Hamsters zum gegebenen Ziel mithilfe des A*-Algorithmus.

        Args:
            ziel (tuple): Das Ziel, zu dem der Pfad berechnet werden soll.
        """
        from hamstergame import a_stern  # Importiere die a_stern Funktion hier, um einen erneuten Import zu vermeiden
        self.pfad = a_stern(self.spielfeld, (self.x, self.y), ziel)
        print(f"Pfad nach aktualisiere_pfad: {self.pfad}")  # Debug-Ausgabe für den aktualisierten Pfad

    def naechster_schritt(self, koerner):
        """
        Führt den nächsten Schritt des Hamsters auf dem Spielfeld aus.

        Args:
            koerner (list): Liste der Körner auf dem Spielfeld.
        """
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

    Args:
        position (tuple): Die Position, die überprüft werden soll.
        spielfeld (list): Die Darstellung des Spielfelds als 2D-Liste.

    Returns:
        bool: True, wenn die Position gültig ist, andernfalls False.
    """
    x, y = position
    return 0 <= x < len(spielfeld[0]) and 0 <= y < len(spielfeld) and spielfeld[y][x] == 0

def a_stern(spielfeld, start, ziel):
    """
    Berechnet den kürzesten Pfad zwischen Start- und Zielposition auf dem Spielfeld mithilfe des A*-Algorithmus.

    Args:
        spielfeld (list): Die Darstellung des Spielfelds als 2D-Liste.
        start (tuple): Die Startposition (x, y).
        ziel (tuple): Die Zielposition (x, y).

    Returns:
        list: Der kürzeste Pfad als Liste von Positionen.
    """

    # Liste der möglichen Nachbarn eines Feldes (oben, rechts, unten, links)
    nachbarn = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    # Initialisierung der Priority Queue (zu_besuchen) mit Startposition und Kosten
    zu_besuchen = []
    kosten = {start: 0}  # Initialisiere die Kosten-Variable
    heapq.heappush(zu_besuchen, (0 + euklidische_heuristik(start, ziel), start))  # Priorität = Kosten + Heuristik
    pfad = {}  # Dictionary zur Verfolgung des Pfads

    # Schleife, die den A*-Algorithmus ausführt
    while zu_besuchen:
        _, aktuelle_position = heapq.heappop(zu_besuchen)  # Das Feld mit der niedrigsten Priorität wird entfernt

        # Prüfung, ob das Ziel erreicht wurde
        if aktuelle_position == ziel:
            weg = []
            while aktuelle_position != start:
                weg.append(aktuelle_position)
                aktuelle_position = pfad[aktuelle_position]  # Verfolge den Pfad rückwärts
            weg.append(start)
            return weg[::-1]  # Den Pfad in der richtigen Reihenfolge zurückgeben

        # Durchgehen der Nachbarn des aktuellen Feldes
        for richtung in nachbarn:
            nachbar = (aktuelle_position[0] + richtung[0], aktuelle_position[1] + richtung[1])

            # Überprüfen, ob der Nachbar eine gültige Position auf dem Spielfeld ist
            if gueltige_position(nachbar, spielfeld):
                neue_kosten = kosten[aktuelle_position] + 1

                # Überprüfen, ob der Nachbarfeld günstiger ist oder noch nicht besucht wurde
                if nachbar not in kosten or neue_kosten < kosten[nachbar]:
                    kosten[nachbar] = neue_kosten  # Aktualisiere die Kosten für den Nachbar
                    prioritaet = neue_kosten + euklidische_heuristik(nachbar, ziel)  # Berechne die Priorität
                    heapq.heappush(zu_besuchen, (prioritaet, nachbar))  # Füge den Nachbar zur Queue hinzu
                    pfad[nachbar] = aktuelle_position  # Verfolge den Pfad zum Nachbarfeld
                else:
                    # Debug-Ausgabe, wenn ein Nachbar ignoriert wird, weil er teurer ist
                    print(f"Ignoriere Nachbar {nachbar}, da neue Kosten {neue_kosten} >= aktuelle Kosten {kosten[nachbar]}")
            else:
                # Debug-Ausgabe, wenn ein Nachbar ignoriert wird, weil er ungültig ist
                print(f"Ignoriere Nachbar {nachbar}, da er eine ungültige Position ist")

    # Debug-Ausgabe, wenn kein Pfad gefunden wurde
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
