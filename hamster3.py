import pygame
import random

# Konstanten
FENSTER_BREITE = 800
FENSTER_HOEHE = 600
KACHEL_GROESSE = 50
ANZAHL_KOERNER = 5

# Pygame initialisieren
pygame.init()
fenster = pygame.display.set_mode((FENSTER_BREITE, FENSTER_HOEHE))
pygame.display.set_caption('Hamster-Territorium')
clock = pygame.time.Clock()  # Für die Steuerung der Framerate

# Grafik für den Hamster laden und skalieren
hamster_bild = pygame.image.load('hamster.png').convert_alpha()
hamster_bild = pygame.transform.scale(hamster_bild, (KACHEL_GROESSE, KACHEL_GROESSE))

class Hamster:
    def __init__(self, terr):
        self.koerner_im_maul = 0
        self.terr = terr
        self.position = self.terr.hamster_position
        self.schritte = 0  # Hinzugefügt, um die Anzahl der Schritte zu zählen

    def bewege(self):
        richtungen = [(0, -1), (1, 0), (0, 1), (-1, 0)]  # N, E, S, W
        richtung = random.choice(richtungen)
        neue_position = (self.position[0] + richtung[0], self.position[1] + richtung[1])

        # Überprüfen, ob die neue Position gültig ist (nicht auf Mauern oder außerhalb des Territoriums)
        if (0 < neue_position[0] < self.terr.reihen - 1 and
                0 < neue_position[1] < self.terr.spalten - 1 and
                self.terr.terr[neue_position[0]][neue_position[1]] != '#'):
            # Alte Position des Hamsters löschen
            self.terr.terr[self.position[0]][self.position[1]] = ' '
            # Position des Hamsters aktualisieren
            self.position = neue_position
            self.terr.hamster_position = neue_position
            # Korn aufnehmen, wenn vorhanden
            if self.terr.terr[neue_position[0]][neue_position[1]] == 'k':
                self.koerner_im_maul += 1
                self.terr.terr[neue_position[0]][neue_position[1]] = ' '
            # Neue Position des Hamsters markieren
            self.terr.terr[self.position[0]][self.position[1]] = 'H'
            self.schritte += 1  # Schritte zählen

    def hat_alles_gefunden(self):
        return not any('k' in reihe for reihe in self.terr.terr)
class HamsterTerritorium:
    def __init__(self, reihen, spalten):
        self.reihen = reihen
        self.spalten = spalten
        self.terr = [[' ' for _ in range(spalten)] for _ in range(reihen)]
        self.hamster_position = None  # wird später gesetzt
        # Umgeben das Territorium mit Mauern
        for r in range(reihen):
            for s in range(spalten):
                if r == 0 or r == reihen - 1 or s == 0 or s == spalten - 1:
                    self.terr[r][s] = '#'

        # Platziere zufällig Körner
        for _ in range(ANZAHL_KOERNER):
            r, s = random.randint(1, reihen - 2), random.randint(1, spalten - 2)
            while self.terr[r][s] != ' ':
                r, s = random.randint(1, reihen - 2), random.randint(1, spalten - 2)
            self.terr[r][s] = 'k'  # 'k' für Körner

    def platziere_hamster(self):
        r, s = random.randint(1, self.reihen - 2), random.randint(1, self.spalten - 2)
        while self.terr[r][s] != ' ':
            r, s = random.randint(1, self.reihen - 2), random.randint(1, self.spalten - 2)
        self.hamster_position = (r, s)
        self.terr[r][s] = 'H'  # 'H' für Hamster


    def draw(self, fenster):
        fenster.fill((255, 255, 255))  # Weißer Hintergrund

        # Zeichne das Territorium
        for r in range(self.reihen):
            for s in range(self.spalten):
                element = self.terr[r][s]
                position = (s * KACHEL_GROESSE, r * KACHEL_GROESSE)

                if element == 'H':
                    fenster.blit(hamster_bild, position)
                elif element == '#':
                    pygame.draw.rect(fenster, (0, 0, 0), (position[0], position[1], KACHEL_GROESSE, KACHEL_GROESSE))
                elif element == 'k':
                    korn_mittelpunkt = (position[0] + KACHEL_GROESSE // 2, position[1] + KACHEL_GROESSE // 2)
                    pygame.draw.circle(fenster, (255, 255, 0), korn_mittelpunkt, KACHEL_GROESSE // 4)

                # Zeichne Gitternetzlinien
                pygame.draw.rect(fenster, (200, 200, 200), (position[0], position[1], KACHEL_GROESSE, KACHEL_GROESSE), 1)



# Territorium und Hamster erstellen
terr = HamsterTerritorium(12, 16)
terr.platziere_hamster()
hamster = Hamster(terr)

# Hauptschleife
weitermachen = True
while weitermachen:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            weitermachen = False

    # Bewegung des Hamsters
    hamster.bewege()

    # Überprüfe, ob der Hamster alle Körner gesammelt hat
    if hamster.hat_alles_gefunden():
        print(f"Level geschafft in {hamster.schritte} Schritten!")
        weitermachen = False

    # Zeichnen
    terr.draw(fenster)

    # Bildschirm aktualisieren
    pygame.display.flip()
    clock.tick(20)  # Setzt die Geschwindigkeit, mit der sich der Hamster bewegt

# Warte kurz, damit der Spieler die Nachricht sehen kann
pygame.time.wait(2000)

# Pygame beenden
pygame.quit()