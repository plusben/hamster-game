"""
Hamster-Territorium Spiel mit Pygame

Dieses Spiel ist ein einfaches 2D-Puzzle-Spiel, entwickelt mit der Pygame-Bibliothek.
Das Ziel des Spiels ist es, einen virtuellen Hamster durch ein Territorium zu steuern,
um alle verstreuten Körner zu sammeln. Das Territorium ist ein Raster aus Kacheln,
wobei einige Kacheln als Mauern dienen, die nicht betreten werden können.

Eigenschaften des Spiels:
- Ein Hamster bewegt sich zufällig durch das Territorium.
- Der Hamster muss alle Körner im Territorium sammeln.
- Das Spiel zeigt visuell das Territorium, den Hamster, Körner und Mauern.
- Das Spiel endet, wenn alle Körner gesammelt wurden.

Pygame ist eine Open-Source-Bibliothek für die Entwicklung von Spielen in Python.
Sie bietet Funktionen zur Grafikdarstellung, Sound-Wiedergabe und zur Handhabung von Benutzereingaben.
In diesem Spiel wird Pygame verwendet, um das Spiel-Fenster zu erstellen, Grafiken zu rendern
und Benutzerinteraktionen wie das Schließen des Fensters zu verarbeiten.

GPL3.0 Licence - Benedikt Splinter https://github.com/plusben/hamster-game/
"""

import pygame
import random

# Konstanten
FENSTER_BREITE = 800  # Breite des Fensters in Pixeln
FENSTER_HOEHE = 600   # Höhe des Fensters in Pixeln
KACHEL_GROESSE = 50   # Größe der Kacheln, auf denen sich der Hamster bewegt
ANZAHL_KOERNER = 5    # Anzahl der Körner im Territorium

# Pygame initialisieren
pygame.init()  # Startet alle notwendigen Pygame-Module
fenster = pygame.display.set_mode((FENSTER_BREITE, FENSTER_HOEHE))  # Erstellt das Fenster
pygame.display.set_caption('Hamster-Territorium')  # Setzt den Titel des Fensters
clock = pygame.time.Clock()  # Für die Steuerung der Framerate

# Grafik für den Hamster laden und skalieren
hamster_bild = pygame.image.load('hamster.png').convert_alpha()  # Lädt das Hamster-Bild
hamster_bild = pygame.transform.scale(hamster_bild, (KACHEL_GROESSE, KACHEL_GROESSE))  # Skaliert das Bild

class Hamster:
    def __init__(self, terr):
        self.koerner_im_maul = 0  # Anzahl der Körner, die der Hamster gesammelt hat
        self.terr = terr  # Das Territorium, in dem sich der Hamster befindet
        self.position = self.terr.hamster_position  # Startposition des Hamsters
        self.schritte = 0  # Zählt die Anzahl der Schritte, die der Hamster macht

    def bewege(self):
        richtungen = [(0, -1), (1, 0), (0, 1), (-1, 0)]  # Mögliche Bewegungsrichtungen (Norden, Osten, Süden, Westen)
        richtung = random.choice(richtungen)  # Wählt eine zufällige Richtung aus
        neue_position = (self.position[0] + richtung[0], self.position[1] + richtung[1])  # Berechnet die neue Position

        # Überprüft, ob die neue Position innerhalb des Territoriums und nicht auf einer Mauer ist
        if (0 <= neue_position[0] < self.terr.reihen and
                0 <= neue_position[1] < self.terr.spalten and
                self.terr.terr[neue_position[0]][neue_position[1]] != '#'):
            # Aktualisiert die Position des Hamsters
            self.terr.terr[self.position[0]][self.position[1]] = ' '
            self.position = neue_position
            self.terr.hamster_position = neue_position
            # Nimmt ein Korn auf, wenn vorhanden
            if self.terr.terr[neue_position[0]][neue_position[1]] == 'k':
                self.koerner_im_maul += 1
                self.terr.terr[neue_position[0]][neue_position[1]] = ' '
            self.terr.terr[self.position[0]][self.position[1]] = 'H'
            self.schritte += 1  # Erhöht die Schrittzahl

    def hat_alles_gefunden(self):
        # Überprüft, ob noch Körner im Territorium vorhanden sind
        return not any('k' in reihe for reihe in self.terr.terr)

class HamsterTerritorium:
    def __init__(self, reihen, spalten):
        """
        Konstruktor der Klasse HamsterTerritorium.

        Args:
            reihen (int): Anzahl der Reihen im Territorium.
            spalten (int): Anzahl der Spalten im Territorium.

        Attributes:
            reihen (int): Speichert die Anzahl der Reihen im Territorium.
            spalten (int): Speichert die Anzahl der Spalten im Territorium.
            terr (List[List[str]]): Ein 2D-Array, das das Territorium darstellt. Jedes Element des Arrays
                                     repräsentiert eine Zelle des Territoriums, wobei Leerzeichen (' ')
                                     freie Zellen, '#' Mauern und 'k' Körner repräsentieren.
            hamster_position (Tuple[int, int]): Die aktuelle Position des Hamsters im Territorium,
                                                initialisiert mit None, wird später gesetzt.
        """

        self.reihen = reihen  # Anzahl der Reihen im Territorium
        self.spalten = spalten  # Anzahl der Spalten im Territorium
        # Erstellen eines 2D-Arrays, das das Territorium repräsentiert
        self.terr = [[' ' for _ in range(spalten)] for _ in range(reihen)]
        self.hamster_position = None  # Startposition des Hamsters, wird später gesetzt

        # Umgeben das Territorium mit Mauern
        for r in range(reihen):
            for s in range(spalten):
                if r == 0 or r == reihen - 1 or s == 0 or s == spalten - 1:
                    self.terr[r][s] = '#'  # '#' steht für Mauer

        # Platziere zufällig Körner im Territorium
        for _ in range(ANZAHL_KOERNER):
            r, s = random.randint(1, reihen - 2), random.randint(1, spalten - 2)
            while self.terr[r][s] != ' ':
                r, s = random.randint(1, reihen - 2), random.randint(1, spalten - 2)
            self.terr[r][s] = 'k'  # 'k' steht für Korn

    def platziere_hamster(self):
        """
        Platziert den Hamster an einer zufälligen Position im Territorium, die nicht von einer Mauer
        oder einem Korn besetzt ist.

        Die Position des Hamsters wird im Attribut `hamster_position` gespeichert und das entsprechende
        Zellenelement im Territorium wird auf 'H' gesetzt, um den Hamster zu markieren.
        """

        r, s = random.randint(1, self.reihen - 2), random.randint(1, self.spalten - 2)
        while self.terr[r][s] != ' ':
            r, s = random.randint(1, self.reihen - 2), random.randint(1, self.spalten - 2)
        self.hamster_position = (r, s)
        self.terr[r][s] = 'H'  # 'H' steht für Hamster

    def draw(self, fenster):
        fenster.fill((255, 255, 255))  # Füllt das Fenster mit weißem Hintergrund
        """
        Zeichnet das Territorium und seine Inhalte (Hamster, Mauern, Körner) auf das gegebene Pygame-Fenster.
        
        Args:
            fenster (pygame.Surface): Das Pygame-Fenster, auf dem das Territorium gezeichnet wird.
        
        Diese Methode geht durch jedes Element des Territoriums und zeichnet entsprechend der Zellinhalte 
        (Hamster, Mauern, Körner) auf das Fenster. Hamster werden mit dem Hamster-Bild dargestellt, Mauern 
        als schwarze Quadrate und Körner als gelbe Kreise.
        """

        for r in range(self.reihen):
            for s in range(self.spalten):
                element = self.terr[r][s]
                position = (s * KACHEL_GROESSE, r * KACHEL_GROESSE)

                if element == 'H':
                    fenster.blit(hamster_bild, position)  # Zeichnet den Hamster
                elif element == '#':
                    # Zeichnet eine schwarze Mauer
                    pygame.draw.rect(fenster, (0, 0, 0), (position[0], position[1], KACHEL_GROESSE, KACHEL_GROESSE))
                elif element == 'k':
                    # Zeichnet ein gelbes Korn
                    korn_mittelpunkt = (position[0] + KACHEL_GROESSE // 2, position[1] + KACHEL_GROESSE // 2)
                    pygame.draw.circle(fenster, (255, 255, 0), korn_mittelpunkt, KACHEL_GROESSE // 4)

                # Zeichnet Gitternetzlinien
                pygame.draw.rect(fenster, (200, 200, 200), (position[0], position[1], KACHEL_GROESSE, KACHEL_GROESSE), 1)


# Hauptteil des Programms

# Territorium und Hamster erstellen
terr = HamsterTerritorium(12, 16)  # Erstellt ein neues Territorium mit 12 Reihen und 16 Spalten.
terr.platziere_hamster()  # Platziert den Hamster an einer zufälligen Startposition im Territorium.
hamster = Hamster(terr)  # Erstellt ein Hamster-Objekt und übergibt das Territorium.

# Hauptschleife des Spiels
weitermachen = True
while weitermachen:
    # Überprüft alle Ereignisse, die seit dem letzten Durchlauf der Schleife aufgetreten sind.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            weitermachen = False  # Beendet die Schleife und damit das Spiel, wenn das Fenster geschlossen wird.

    # Bewegt den Hamster und prüft, ob alle Körner gefunden wurden
    hamster.bewege()  # Bewegt den Hamster in eine zufällige Richtung.
    if hamster.hat_alles_gefunden():
        print(f"Level geschafft in {hamster.schritte} Schritten!")
        weitermachen = False  # Beendet die Schleife, wenn alle Körner gefunden wurden.

    # Zeichnet das Territorium und den Hamster
    terr.draw(fenster)  # Zeichnet den aktuellen Zustand des Territoriums und des Hamsters auf dem Bildschirm.

    # Aktualisiert den Bildschirm
    pygame.display.flip()  # Aktualisiert den gesamten Bildschirm mit den gezeichneten Elementen.
    clock.tick(20)  # Begrenzt die Bildwiederholrate auf 20 Frames pro Sekunde, um die Spielgeschwindigkeit zu steuern.

# Kurze Pause, damit der Spieler die Nachricht sehen kann
pygame.time.wait(2000)  # Wartet 2000 Millisekunden (2 Sekunden), bevor das Programm weiterläuft.

# Beendet Pygame und schließt das Fenster
pygame.quit()  # Schließt das Pygame-Fenster und beendet alle Pygame-Prozesse.
