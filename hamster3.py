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
        # Platzieren des Hamsters an einer zufälligen Position im Territorium
        r, s = random.randint(1, self.reihen - 2), random.randint(1, self.spalten - 2)
        while self.terr[r][s] != ' ':
            r, s = random.randint(1, self.reihen - 2), random.randint(1, self.spalten - 2)
        self.hamster_position = (r, s)
        self.terr[r][s] = 'H'  # 'H' steht für Hamster

    def draw(self, fenster):
        fenster.fill((255, 255, 255))  # Füllt das Fenster mit weißem Hintergrund

        # Zeichnet das Territorium Zelle für Zelle
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
terr = HamsterTerritorium(12, 16)
terr.platziere_hamster()
hamster = Hamster(terr)

# Hauptschleife des Spiels
weitermachen = True
while weitermachen:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            weitermachen = False  # Beendet das Spiel, wenn das Fenster geschlossen wird

    # Bewegt den Hamster und prüft, ob alle Körner gefunden wurden
    hamster.bewege()
    if hamster.hat_alles_gefunden():
        print(f"Level geschafft in {hamster.schritte} Schritten!")
        weitermachen = False

    # Zeichnet das Territorium und den Hamster
    terr.draw(fenster)

    # Aktualisiert den Bildschirm
    pygame.display.flip()
    clock.tick(20)  # Steuert die Aktualisierungsrate des Spiels

# Kurze Pause, damit der Spieler die Nachricht sehen kann
pygame.time.wait(2000)

# Beendet Pygame und schließt das Fenster
pygame.quit()
