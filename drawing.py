import pygame
from settings import FELDGROESSE

# Zeichenfunktionen
def zeichne_spielfeld(screen, spielfeld):
    """Zeichnet das Spielfeld basierend auf dem aktuellen Zustand.
    Args:
        screen: Pygame-Fenster, auf dem das Spielfeld gezeichnet wird.
        spielfeld: 2D-Array, das das Spielfeld repräsentiert.
    """
    for y, reihe in enumerate(spielfeld):
        for x, feld in enumerate(reihe):
            rect = pygame.Rect(x * FELDGROESSE, y * FELDGROESSE, FELDGROESSE, FELDGROESSE)
            if feld == 1:  # Hindernis
                pygame.draw.rect(screen, (0, 0, 0), rect)
            pygame.draw.rect(screen, (100, 100, 100), rect, 1)

def zeichne_koerner(screen, koerner):
    """Zeichnet Körner auf dem Spielfeld.
    Args:
        screen: Pygame-Fenster, auf dem die Körner gezeichnet werden.
        koerner: Liste der Koordinaten, wo Körner gezeichnet werden sollen.
    """
    for korn in koerner:
        pygame.draw.circle(screen, (255, 255, 0), (korn[0] * FELDGROESSE + FELDGROESSE // 2, korn[1] * FELDGROESSE + FELDGROESSE // 2), 15)

def zeichne_pfad(screen, pfad):
    """Zeichnet einen Pfad zwischen den Punkten.
    Args:
        screen: Pygame-Fenster, auf dem der Pfad gezeichnet wird.
        pfad: Liste der Punkte, die den Pfad bilden.
    """

    if pfad is None:
        return  # Beendet die Funktion frühzeitig, wenn pfad None ist

    for i in range(len(pfad) - 1):
        start_pos = (pfad[i][0] * FELDGROESSE + FELDGROESSE // 2, pfad[i][1] * FELDGROESSE + FELDGROESSE // 2)
        end_pos = (pfad[i + 1][0] * FELDGROESSE + FELDGROESSE // 2, pfad[i + 1][1] * FELDGROESSE + FELDGROESSE // 2)
        pygame.draw.line(screen, (255, 0, 0), start_pos, end_pos, 3)

def zeichne_zurueckgelegten_pfad(screen, pfad):
    """Zeichnet den zurückgelegten Pfad.
    Args:
        screen: Pygame-Fenster, auf dem der zurückgelegte Pfad gezeichnet wird.
        pfad: Liste der Punkte, die den zurückgelegten Pfad bilden.
    """
    for punkt in pfad:
        pygame.draw.circle(screen, (0, 0, 255), (punkt[0] * FELDGROESSE + FELDGROESSE // 2, punkt[1] * FELDGROESSE + FELDGROESSE // 2), 5)

def zeichne_text(screen, text, position, font_size=20, color=(255, 0, 0)):
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, position)

def zeichne_koordinaten(screen, koordinaten, position, font_size=14, color=(0, 0, 0)):
    font = pygame.font.Font(None, font_size)
    koordinaten_text = f"{koordinaten[0]}, {koordinaten[1]}"
    text_surface = font.render(koordinaten_text, True, color)
    screen.blit(text_surface, position)