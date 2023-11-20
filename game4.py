import pygame
import sys
import random
import time

# Globale Konstanten für die Fenstergröße
WIDTH, HEIGHT = 1200, 800

# Klasse für den Hamster
class Hamster:
    def __init__(self, x, y, name="Horst"):
        original_image = pygame.image.load('hamster.png')
        image_size = (39, 39)
        self.image = pygame.transform.scale(original_image, image_size)
        self.rect = self.image.get_rect(topleft=(x * 40 + 1, y * 40 + 1))
        self.direction = "up"
        self.move_requested = False
        self.name = name

    def move(self, level, koerner):
        print(f"Versuche, sich in Richtung {self.direction} zu bewegen")
        move_amount = 40
        original_position = self.rect.copy()

        if self.direction == "up":
            self.rect.y -= move_amount
        elif self.direction == "down":
            self.rect.y += move_amount
        elif self.direction == "left":
            self.rect.x -= move_amount
        elif self.direction == "right":
            self.rect.x += move_amount

        if self.check_collision(level, self.direction):
            self.rect = original_position
            self.change_direction_randomly(level)

    def change_direction_randomly(self, level):
        directions = ["up", "down", "left", "right"]
        random.shuffle(directions)  # Zufällige Reihenfolge der Richtungen
        for direction in directions:
            if not self.check_collision(level, direction):
                self.direction = direction
                print(f"Richtungsänderung zu {self.direction}")
                return
        print("Keine Richtung ohne Kollision gefunden")

    def check_collision(self, level, proposed_direction):
        print(f"Überprüfe Kollision für die Richtung {proposed_direction}")
        original_position = self.rect.copy()
        if proposed_direction == "up":
            self.rect.y -= 40
        elif proposed_direction == "down":
            self.rect.y += 40
        elif proposed_direction == "left":
            self.rect.x -= 40
        elif proposed_direction == "right":
            self.rect.x += 40

        colliding_obstacle = None
        for hindernis in level:
            if self.rect.colliderect(hindernis.rect):
                colliding_obstacle = hindernis
                break

        if colliding_obstacle:
            print(f"Kollision mit Hindernis bei {colliding_obstacle.rect}")
        elif not (0 <= self.rect.left < WIDTH and 0 <= self.rect.top < HEIGHT):
            print("Kollision mit Spielfeldgrenzen")

        self.rect = original_position
        return colliding_obstacle is not None or not (0 <= self.rect.left < WIDTH and 0 <= self.rect.top < HEIGHT)

# Klasse für das Gitter
class Gitter:
    # Konstruktor der Gitter-Klasse, wird aufgerufen, wenn eine neue Instanz der Klasse erstellt wird.
    def __init__(self, win, width, height):
        self.win = win  # Speichert das Pygame-Fensterobjekt, in dem das Gitter gezeichnet wird.
        self.width = width  # Die Breite des Gitters in Pixeln.
        self.height = height  # Die Höhe des Gitters in Pixeln.
        self.cell_size = 40  # Die Größe jeder Zelle im Gitter in Pixeln.

    # Methode zum Zeichnen des Gitters auf dem Fenster.
    def draw(self):
        # Zeichnet vertikale Linien des Gitters.
        for x in range(0, self.width, self.cell_size):  # Iteriert über die Breite des Gitters in Schritten von 'cell_size'.
            # Zeichnet eine vertikale Linie bei jeder x-Position.
            pygame.draw.line(self.win, (0, 0, 0), (x, 0), (x, self.height))  # Farbe der Linie ist Schwarz (0, 0, 0).

        # Zeichnet horizontale Linien des Gitters.
        for y in range(0, self.height, self.cell_size):  # Iteriert über die Höhe des Gitters in Schritten von 'cell_size'.
            # Zeichnet eine horizontale Linie bei jeder y-Position.
            pygame.draw.line(self.win, (0, 0, 0), (0, y), (self.width, y))  # Farbe der Linie ist ebenfalls Schwarz.


# Klasse für Hindernisse
class Hindernis:
    # Konstruktor der Hindernis-Klasse, wird aufgerufen, wenn eine neue Instanz der Klasse erstellt wird.
    def __init__(self, x, y, width, height):
        # Erstellt ein Rechteck-Objekt, das die Position und Größe des Hindernisses darstellt.
        # 'x' und 'y' sind die Koordinaten der oberen linken Ecke des Hindernisses.
        # 'width' und 'height' sind die Breite und Höhe des Hindernisses in Zellen, multipliziert mit 40 (der Zellgröße).
        self.rect = pygame.Rect(x * 40, y * 40, width * 40, height * 40)

        # Erstellt eine neue Oberfläche in Pygame, die das visuelle Bild des Hindernisses darstellt.
        # Die Größe der Oberfläche entspricht der Größe des Hindernisses.
        self.image = pygame.Surface((width * 40, height * 40))  # Korrigiert die Größe der Oberfläche.

        # Füllt die Oberfläche mit einer Farbe, in diesem Fall Schwarz (RGB-Wert (0, 0, 0)).
        self.image.fill((0, 0, 0))  # Färbt das Hindernis schwarz.

    # Methode zum Zeichnen des Hindernisses auf dem Fenster.
    def draw(self, win):
        # 'blit' ist eine Methode in Pygame, die eine Oberfläche auf einer anderen Oberfläche zeichnet.
        # In diesem Fall wird das Hindernis (self.image) auf dem übergebenen Fenster 'win' gezeichnet.
        # Die Position, an der das Bild gezeichnet wird, ist durch 'self.rect' bestimmt.
        win.blit(self.image, self.rect)

# Klasse für Körner im Spiel
class Korn:
    # Konstruktor der Korn-Klasse, wird aufgerufen, wenn eine neue Instanz der Klasse erstellt wird.
    def __init__(self, x, y):
        # Erstellt ein Rechteck-Objekt, das die Position und Größe des Korns darstellt.
        # 'x' und 'y' sind die Koordinaten der oberen linken Ecke des Korns.
        # Da die Größe eines Korns einer Zelle entspricht, werden sowohl Breite als auch Höhe auf 40 gesetzt.
        self.rect = pygame.Rect(x * 40, y * 40, 40, 40)

        # Erstellt eine neue Oberfläche in Pygame, die das visuelle Bild des Korns darstellt.
        # Die Größe der Oberfläche ist auf die Größe eines Korns (40x40 Pixel) festgelegt.
        self.image = pygame.Surface((40, 40))

        # Füllt die Oberfläche mit einer Farbe, in diesem Fall einem Gelbton (RGB-Wert (255, 215, 0)).
        # Diese Farbe repräsentiert das Korn.
        self.image.fill((255, 215, 0))  # Gelb für das Korn

    # Methode zum Zeichnen des Korns auf dem Fenster.
    def draw(self, win):
        # 'blit' ist eine Methode in Pygame, die eine Oberfläche auf einer anderen Oberfläche zeichnet.
        # In diesem Fall wird das Korn (self.image) auf dem übergebenen Fenster 'win' gezeichnet.
        # Die Position, an der das Bild gezeichnet wird, ist durch 'self.rect' bestimmt.
        win.blit(self.image, self.rect)


def main():
    try:
        # Initialisierung von Pygame
        pygame.init()

        # Fenstergröße für das Spiel festlegen
        WIDTH, HEIGHT = 1200, 800
        win = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pygame Hamster Spiel")

        # Definiert eine Farbe, die im Spiel verwendet wird
        WHITE = (255, 255, 255)

        # Funktion zum Verteilen einer bestimmten Anzahl von Körnern auf dem Spielfeld
        def verteileKoernerAnzahl(anzahlKoerner, level):
            koerner = []  # Liste, um die Körner zu speichern
            for _ in range(anzahlKoerner):
                x = random.randint(0, (WIDTH // 40) - 1)  # Zufällige X-Position
                y = random.randint(0, (HEIGHT // 40) - 1)  # Zufällige Y-Position

                # Überprüfen, ob das ausgewählte Feld bereits belegt ist
                belegt = any(hindernis.rect.collidepoint(x * 40, y * 40) for hindernis in level)
                if not belegt:
                    koerner.append(Korn(x, y))  # Korn hinzufügen, wenn das Feld frei ist
            return koerner

        # Funktion zur Generierung eines Labyrinths
        def generiereLabyrinth(breite, hoehe):
            # Initialisiert das Labyrinth als eine Matrix aus Wänden (1 bedeutet Wand)
            labyrinth = [[1 for x in range(breite)] for y in range(hoehe)]

            # Funktion zum Erstellen von Gängen im Labyrinth
            def erstelleGang(x, y):
                # Mögliche Richtungen für die Gänge
                richtungen = [(0, 1), (1, 0), (0, -1), (-1, 0)]
                random.shuffle(richtungen)  # Richtungen zufällig mischen

                for dx, dy in richtungen:
                    nx, ny = x + dx * 2, y + dy * 2
                    # Überprüfen, ob die neue Position innerhalb des Labyrinths ist und eine Wand ist
                    if 0 <= nx < breite and 0 <= ny < hoehe and labyrinth[ny][nx] == 1:
                        # Wand entfernen, um einen Gang zu erstellen
                        labyrinth[ny][nx] = 0
                        labyrinth[y + dy][x + dx] = 0

                        # Entscheiden, ob ein größerer Raum erstellt werden soll
                        if random.choice([True, False]):
                            for i in range(1, 3):  # Erweitere den Raum zufällig
                                extra_x, extra_y = nx + dx * i, ny + dy * i
                                if 0 <= extra_x < breite and 0 <= extra_y < hoehe:
                                    labyrinth[extra_y][extra_x] = 0

                        erstelleGang(nx, ny)  # Rekursiver Aufruf zum Weiterbau des Ganges

            # Startet den Gang-Generator von einer zufälligen Position
            start_x, start_y = random.randrange(0, breite, 2), random.randrange(0, hoehe, 2)
            labyrinth[start_y][start_x] = 0
            erstelleGang(start_x, start_y)

            # Erweitere den Raum an zufälligen Stellen für mehr "Räume"
            for _ in range(breite * hoehe // 10):
                rx, ry = random.randrange(0, breite), random.randrange(0, hoehe)
                if labyrinth[ry][rx] == 1:
                    labyrinth[ry][rx] = 0
                    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                        nx, ny = rx + dx, ry + dy
                        if 0 <= nx < breite and 0 <= ny < hoehe:
                            labyrinth[ny][nx] = 0

            # Fügt eine Mauer um das Spielfeld hinzu
            for x in range(breite):
                labyrinth[0][x] = 1  # Obere Mauer
                labyrinth[hoehe - 1][x] = 1  # Untere Mauer
            for y in range(hoehe):
                labyrinth[y][0] = 1  # Linke Mauer
                labyrinth[y][breite - 1] = 1  # Rechte Mauer

            return labyrinth

        # Funktion zur Bewegung des Hamsters
        def move_hamster(hamster, ziel):
            # Berechne die Richtung zum Zielkorn
            dx = ziel.rect.x - hamster.rect.x
            dy = ziel.rect.y - hamster.rect.y

            # Bestimme die Bewegungsrichtung (horizontal oder vertikal)
            if abs(dx) > abs(dy):
                # Bewege horizontal
                if dx > 0:
                    hamster.direction = "right"
                else:
                    hamster.direction = "left"
            else:
                # Bewege vertikal
                if dy > 0:
                    hamster.direction = "down"
                else:
                    hamster.direction = "up"

            # Führe die Bewegung aus
            hamster.move(level, koerner)

        # Funktion zum Finden des nächstgelegenen Korns
        def finde_naechstes_korn(hamster, koerner):
            hamster_position = (hamster.rect.x // 40, hamster.rect.y // 40)
            naechstes_korn = None
            kuerzeste_distanz = float('inf')

            for korn in koerner:
                korn_position = (korn.rect.x // 40, korn.rect.y // 40)
                distanz = ((hamster_position[0] - korn_position[0]) ** 2 + (hamster_position[1] - korn_position[1]) ** 2) ** 0.5
                if distanz < kuerzeste_distanz:
                    kuerzeste_distanz = distanz
                    naechstes_korn = korn

            return naechstes_korn

        # Funktion zum Finden einer freien Position im Labyrinth
        def finde_freie_position(hindernisse):
            while True:
                x = random.randint(0, (WIDTH // 40) - 1)
                y = random.randint(0, (HEIGHT // 40) - 1)
                position_belegt = any(hindernis.rect.collidepoint(x * 40, y * 40) for hindernis in hindernisse)
                if not position_belegt:
                    return x, y

        # Erstelle das Labyrinth und füge es als Hindernisse hinzu
        labyrinth = generiereLabyrinth(WIDTH // 40, HEIGHT // 40)
        level = []
        for y, reihe in enumerate(labyrinth):
            for x, zelle in enumerate(reihe):
                if zelle == 1:
                    level.append(Hindernis(x, y, 1, 1))

        # Erstelle den Hamster und das Gitter
        hamster_x, hamster_y = finde_freie_position(level)
        hamster = Hamster(hamster_x, hamster_y)
        gitter = Gitter(win, WIDTH, HEIGHT)

        # Statistiken und Timer für das Spiel
        start_time = time.time()
        schritte = 0
        koerner = verteileKoernerAnzahl(20, level)  # Verteilt 20 Körner auf dem Spielfeld

        # Timer für die automatische Bewegung des Hamsters
        hamster_move_timer = 0
        move_interval = 100  # Bewege den Hamster alle 100 Millisekunden

        # Hauptspiel-Schleife
        running = True
        while running:
            # Verarbeitet Ereignisse (wie z.B. das Schließen des Fensters)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Überprüft, ob es Zeit ist, den Hamster zu bewegen
            if pygame.time.get_ticks() - hamster_move_timer > move_interval:
                if koerner:  # Wenn Körner vorhanden sind
                    zielkorn = finde_naechstes_korn(hamster, koerner)
                    move_hamster(hamster, zielkorn)
                hamster_move_timer = pygame.time.get_ticks()

            # Zeichnet alle Elemente des Spiels
            win.fill(WHITE)
            for hindernis in level:
                hindernis.draw(win)
            for korn in koerner:
                korn.draw(win)
            gitter.draw()
            win.blit(hamster.image, hamster.rect)
            pygame.display.flip()

            # Spiel beenden, wenn alle Körner gesammelt wurden
            if not koerner:
                running = False
                end_time = time.time()
                gespielte_zeit = end_time - start_time
                print(f"Hamster {hamster.name} hat das Level in {gespielte_zeit:.2f} Sekunden mit {schritte} Schritten abgeschlossen.")
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")
    finally:
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()