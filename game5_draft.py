import pygame
import sys
import random
import time


WIDTH, HEIGHT = 1200, 800

# Klasse für den Hamster
class Hamster:
    def __init__(self, x : int, y:int, name :str ="Horst") ->None:
        original_image = pygame.image.load('hamster.png')
        image_size = (39, 39)  # Zielgröße des Hamsterbildes
        self.image = pygame.transform.scale(original_image, image_size)
        self.rect = self.image.get_rect(topleft=(x * 40 + 1, y * 40 + 1))  # Leichte Verschiebung um 1 Pixel
        self.direction = "up"
        self.move_requested = False
        self.name = name

    def move(self, hindernisse: list, koerner: list) ->None:  # type: ignore [type-arg]
        move_amount = 40  # Die Größe eines Feldes
        original_position = self.rect.copy()

        # Bewegung basierend auf der aktuellen Richtung
        if self.direction == "up":
            self.rect.y -= move_amount
        elif self.direction == "down":
            self.rect.y += move_amount
        elif self.direction == "left":
            self.rect.x -= move_amount
        elif self.direction == "right":
            self.rect.x += move_amount

        # Kollision mit Hindernissen
        if self.check_collision(hindernisse):
            self.rect = original_position
            self.change_direction_randomly()

        # Aufnahme von Körnern
        for korn in koerner[:]:
            if self.rect.colliderect(korn.rect):
                koerner.remove(korn)

    def change_direction_randomly(self) -> None:
        directions = ["up", "down", "left", "right"]
        self.direction = random.choice(directions)

    def check_collision(self, hindernisse: list ) -> bool: # type: ignore [type-arg]
        for hindernis in hindernisse:
            if self.rect.colliderect(hindernis.rect):
                return True
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        return False


# Klasse für das Gitter
class Gitter:
    def __init__(self, win: pygame.Surface, width: int, height:int) ->None:
        self.win = win
        self.width = width
        self.height = height
        self.cell_size = 40

    def draw(self) -> None:
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.win, (0, 0, 0), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.win, (0, 0, 0), (0, y), (self.width, y))


# Klasse für Hindernisse
class Hindernis:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.rect = pygame.Rect(x * 40, y * 40, width * 40, height * 40)
        self.image = pygame.Surface((width * 40, height * 40))  # Korrigiere die Größe
        self.image.fill((0, 0, 0))  # Färbe das Hindernis schwarz

    def draw(self, win: pygame.Surface) -> None:
        win.blit(self.image, self.rect)


# Klasse für Körner
class Korn:
    def __init__(self, x: int, y: int) ->None:
        self.rect = pygame.Rect(x * 40, y * 40, 40, 40)
        self.image = pygame.Surface((40, 40))
        self.image.fill((255, 215, 0))  # Gelb für das Korn

    def draw(self, win: pygame.Surface) -> None:
        win.blit(self.image, self.rect)


class Node:
    def __init__(self, parent=None, position=None) ->None: # type: ignore [no-untyped-def]  unclear
        self.parent = parent
        self.position = position
        self.g = 0
        self.h = 0
        self.f = 0


def main() ->None:
    try:
        # Initialisierung von Pygame
        pygame.init()

        # Fenstergröße
        ## WIDTH, HEIGHT = 1200, 800
        win = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pygame Hamster Spiel")

        # Farben
        WHITE = (255, 255, 255)



        def verteileKoernerAnzahl(anahlKoerner: int, level: list[Hindernis] ) ->list[Korn]:
            koerner = []
            for _ in range(anahlKoerner):
                x = random.randint(0, (WIDTH // 40) - 1)
                y = random.randint(0, (HEIGHT // 40) - 1)

                # Prüfen, ob das Feld bereits belegt ist (Hindernis oder anderes Korn)
                belegt = any(hindernis.rect.collidepoint(x * 40, y * 40) for hindernis in level)
                if not belegt:
                    koerner.append(Korn(x, y))
            return koerner

        def generiereLabyrinth(breite: int, hoehe: int) -> list[list[int]]:
            # Initialisiere das Labyrinth als eine Matrix aus Wänden
            labyrinth = [[1 for x in range(breite)] for y in range(hoehe)]

            def erstelleGang(x: int, y: int) -> None:
                richtungen = [(0, 1), (1, 0), (0, -1), (-1, 0)]
                random.shuffle(richtungen)

                for dx, dy in richtungen:
                    nx, ny = x + dx * 2, y + dy * 2
                    if 0 <= nx < breite and 0 <= ny < hoehe and labyrinth[ny][nx] == 1:
                        labyrinth[ny][nx] = 0
                        labyrinth[y + dy][x + dx] = 0

                        # Zufällig entscheiden, ob ein größerer Raum erstellt werden soll
                        if random.choice([True, False]):
                            for i in range(1, 3):  # Erweitere den Raum zufällig um 1 bis 2 zusätzliche Zellen
                                extra_x, extra_y = nx + dx * i, ny + dy * i
                                if 0 <= extra_x < breite and 0 <= extra_y < hoehe:
                                    labyrinth[extra_y][extra_x] = 0

                        erstelleGang(nx, ny)

                # Starte den Generator von einer zufälligen Position

            start_x, start_y = random.randrange(0, breite, 2), random.randrange(0, hoehe, 2)
            labyrinth[start_y][start_x] = 0
            erstelleGang(start_x, start_y)

            # Erweitere den Raum an zufälligen Stellen für mehr "Räume"
            for _ in range(breite * hoehe // 10):  # Anzahl der Erweiterungen
                rx, ry = random.randrange(0, breite), random.randrange(0, hoehe)
                if labyrinth[ry][rx] == 1:
                    labyrinth[ry][rx] = 0
                    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                        nx, ny = rx + dx, ry + dy
                        if 0 <= nx < breite and 0 <= ny < hoehe:
                            labyrinth[ny][nx] = 0

            # Mauer um das Spielfeld hinzufügen
            for x in range(breite):
                labyrinth[0][x] = 1  # Obere Mauer
                labyrinth[hoehe - 1][x] = 1  # Untere Mauer
            for y in range(hoehe):
                labyrinth[y][0] = 1  # Linke Mauer
                labyrinth[y][breite - 1] = 1  # Rechte Mauer

            return labyrinth

        def move_hamster(hamster: Hamster, ziel: Korn) -> None:
            start = (hamster.rect.x // 40, hamster.rect.y // 40)
            end = (ziel.rect.x // 40, ziel.rect.y // 40)
            return

        def finde_naechstes_korn(hamster: Hamster, koerner: list[Korn]) -> Korn | None :
            hamster_position = (hamster.rect.x // 40, hamster.rect.y // 40)
            # naechstes_korn = None
            kuerzeste_distanz = float('inf')

            for korn in koerner:
                korn_position = (korn.rect.x // 40, korn.rect.y // 40)
                distanz = ((hamster_position[0] - korn_position[0]) ** 2 + (hamster_position[1] - korn_position[1]) ** 2) ** 0.5
                if distanz < kuerzeste_distanz:
                    kuerzeste_distanz = distanz
                    naechstes_korn = korn
            return naechstes_korn


        # Erstelle das Labyrinth
        labyrinth = generiereLabyrinth(WIDTH // 40, HEIGHT // 40)

        # Füge das Labyrinth als Hindernisse hinzu
        level = []
        for y, reihe in enumerate(labyrinth):
            for x, zelle in enumerate(reihe):
                if zelle == 1:
                    level.append(Hindernis(x, y, 1, 1))

        # Hamster und Gitter erstellen
        hamster = Hamster(5, 5)  # Platziert den Hamster bei (200, 200) mit dem Namen Horst
        gitter = Gitter(win, WIDTH, HEIGHT)

        # Statistiken
        start_time = time.time()
        schritte = 0

        # Füge hier die Körner hinzu, stelle aber sicher, dass sie nicht auf Hindernissen platziert werden
        koerner = verteileKoernerAnzahl(20, level)

        # Hauptspiel-Schleife mit automatischer Bewegung des Hamsters
        hamster_move_timer = 0
        move_interval = 100  # Bewege den Hamster alle 100 Millisekunden


        # Hauptspiel-Schleife
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            if pygame.time.get_ticks() - hamster_move_timer > move_interval:
                if koerner:  # Wenn es Körner gibt
                    zielkorn = finde_naechstes_korn(hamster, koerner)  # Implementieren Sie diese Funktion
                    move_hamster(hamster, zielkorn)
                hamster_move_timer = pygame.time.get_ticks()

            # Zeichne Hindernisse, Körner und den Hamster
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
