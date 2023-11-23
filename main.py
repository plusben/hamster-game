import pygame
import sys
import json
import random
import subprocess
from settings import BILDSCHIRM_GROESSE, UHR_RATE, HAMSTER_BILD_PFAD, FELDGROESSE
from hamstergame import Hamster, a_stern
from drawing import zeichne_spielfeld, zeichne_koerner, zeichne_pfad, zeichne_zurueckgelegten_pfad, zeichne_text, zeichne_koordinaten


# Initialisierung von Pygame
pygame.init()
screen = pygame.display.set_mode(BILDSCHIRM_GROESSE)
clock = pygame.time.Clock()


# Führen Sie level_generieren.py aus
subprocess.run(['python', 'level_generator.py'])


# Funktion zum Laden eines Levels aus einer JSON-Datei
def lade_level(dateiname):
    with open(dateiname, 'r') as datei:
        return json.load(datei)


# Laden der Level aus 'levels.json'
level_liste = lade_level('levels.json')

# Beispiel: Zugriff auf das erste Level
erstes_level = level_liste[0]
# Hier können Sie dann Ihr Spiel mit diesem Level initialisieren

# Spielfelddefinition
spielfeld = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1],
    [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1],
    [1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1],
    [1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

pygame.display.set_caption("Hamster Spiel")  # Setze den Titel des Pygame-Fensters

# Laden des Hamsterbildes und Skalieren auf 48x48 Pixel
hamster_bild = pygame.image.load(HAMSTER_BILD_PFAD)
hamster_bild = pygame.transform.scale(hamster_bild, (46, 46))

# Initialisierung des Hamsters
hamster = Hamster(14, 10, spielfeld)
# Zielkoordinate für den Hamster
ziel = (6, 6)
korn_index = 0


# Funktion zum Generieren von Körnern auf dem Spielfeld
def generiere_koerner(spielfeld, anzahl_koerner):
    koerner = []
    freie_felder = [(x, y) for y in range(len(spielfeld)) for x in range(len(spielfeld[y])) if spielfeld[y][x] == 0]

    while len(koerner) < anzahl_koerner and freie_felder:
        korn_pos = random.choice(freie_felder)
        start = (hamster.x, hamster.y)
        ziel = korn_pos
        # Prüfe, ob ein Pfad zwischen dem Hamster und dem Korn existiert
        if a_stern(spielfeld, start, ziel):
            koerner.append(korn_pos)
            freie_felder.remove(korn_pos)

    return koerner

# Konfiguration
anzahl_koerner = 15  # Die gewünschte Anzahl von Körnern
koerner = generiere_koerner(spielfeld, anzahl_koerner)

spiel_geschafft = False
schritte = 0

# Funktion zur Initialisierung eines Levels
def initialisiere_level(level):
    global spielfeld, hamster, koerner, korn_index, spiel_geschafft
    spielfeld = level
    hamster = Hamster(14, 10, spielfeld)  # Startposition des Hamsters anpassen
    koerner = generiere_koerner(spielfeld, anzahl_koerner)
    korn_index = 0
    spiel_geschafft = False

# Initialisierung aller Level
for level in level_liste:
    initialisiere_level(level)

# Initialisierung aller Level
aktuelles_level_index = 0
initialisiere_level(level_liste[aktuelles_level_index])

# Spiel-Schleife
while aktuelles_level_index < len(level_liste):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((255, 255, 255))
    zeichne_spielfeld(screen, spielfeld)
    zeichne_koerner(screen, koerner)
    for y in range(len(spielfeld)):
        for x in range(len(spielfeld[y])):
            koordinaten_position = (x * FELDGROESSE + 5, y * FELDGROESSE + 5)
            zeichne_koordinaten(screen, (x, y), koordinaten_position)

    # Zeichne Informationen über den Hamster
    zeichne_text(screen, f"Hamster Position: ({hamster.x}, {hamster.y})", (10, 610))
    zeichne_text(screen, f"Gesammelte Körner: {len(hamster.gesammelte_koerner)} / {len(koerner)}", (10, 630))
    richtung = "N/A" if not hamster.pfad else f"({hamster.pfad[0][0] - hamster.x}, {hamster.pfad[0][1] - hamster.y})"
    zeichne_text(screen, f"Aktuelle Richtung: {richtung}", (10, 650))
    zeichne_text(screen, f"Anzahl Schritte: {schritte}", (10, 670))

    # Vor dem Zeichnen des Pfad-Textes prüfen, ob der Pfad existiert
    if hamster.pfad is not None:
        pfad_text = ', '.join([f"({p[0]}, {p[1]})" for p in hamster.pfad])
    else:
        pfad_text = "Kein Pfad verfügbar"

    zeichne_text(screen, f"Pfad: {pfad_text}", (10, 690), font_size=18)

    if not hamster.pfad or (hamster.x, hamster.y) == ziel:
        if korn_index < len(koerner):
            ziel = koerner[korn_index]
            hamster.aktualisiere_pfad(ziel)
        else:
            spiel_geschafft = True
            continue

    hamster.naechster_schritt(koerner)
    schritte += 1

    if (hamster.x, hamster.y) == ziel:
        if ziel in koerner:
            hamster.gesammelte_koerner.append(ziel)
            koerner.remove(ziel)
            korn_index += 1
            hamster.pfad = []  # Löschen des Pfades, damit ein neuer berechnet wird
        else:
            # Wenn das Ziel bereits erreicht und das Korn entfernt wurde
            if korn_index < len(koerner):
                ziel = koerner[korn_index]
                hamster.aktualisiere_pfad(ziel)
            else:
                spiel_geschafft = True

    # Zeichnen des Pfades und des Hamsters
    zeichne_pfad(screen, hamster.pfad)
    zeichne_zurueckgelegten_pfad(screen, hamster.zurueckgelegter_pfad)
    screen.blit(hamster_bild, (hamster.x * FELDGROESSE + 1, hamster.y * FELDGROESSE + 1))

    pygame.display.flip()
    clock.tick(UHR_RATE)

    if spiel_geschafft:
        aktuelles_level_index += 1
        if aktuelles_level_index < len(level_liste):
            initialisiere_level(level_liste[aktuelles_level_index])
        else:
            pygame.quit()
            sys.exit()

# Beendet Pygame, sobald alle Level abgeschlossen sind
pygame.quit()
