"""Automatiseringsprogram for hvad for noget mad og hvilke film jeg skal se til."""
# importerede moduler
import argparse
import random
import datetime

def karakter(tekst):
    værdi = int(tekst)
    if not 1 <= værdi <= 10:
        raise ValueError
    return værdi


def spørg(spørgsmål):
    while True:
        try:
            return karakter(input(spørgsmål))
        except ValueError:
            print("Skriv et helt tal fra 1 til 10.")


def byg_parser():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--glad", type=int, choices=range(1, 11), metavar="1-10",
                        help="Angiv humør på forhånd.")
    parser.add_argument("--træt", type=int, choices=range(1, 11), metavar="1-10",
                        help="Angiv træthed på forhånd.")
    parser.add_argument("--tid", type=datetime.time.fromisoformat, metavar="TT:MM",
                        help="Vælg klokkeslættet for måltidet.")
    parser.add_argument("--dato", type=datetime.date.fromisoformat, metavar="ÅÅÅÅ-MM-DD",
                        help="Brug en bestemt dato til sæsonens filmvalg.")
    return parser


args = byg_parser().parse_args()
glad = args.glad or spørg("Hvor glad er du fra 1-10? ")
træt = args.træt or spørg("Hvor træt er du fra 1-10? ")
# Tidsvariabler
nu = datetime.datetime.now()
måned = (args.dato or nu.date()).month
dagstime = (args.tid or nu.time()).hour


# lister med info
mad = [
    ["havregrød", "yoghurt", "kakaomælk"],  # morgenmad
    ["Thaiboks", "æg", "frugt"],  # frokort
    ["bønner", "gryderet", "ratatouille"]  # Aftensmad
]

film = [
    ["How i met your mother", "Friends", "Tømmermænd i Vegas"],  # For humør
    ["The Mechanic", "White House Down", "Interstellar"],        # For træthed
    ["Greenbook", "Shawshank Redemption", "Intouchables"],  # For hele året \ jul
    ["Home Alone", "Elf", "Die Hard"]                            # For jul
]

# funktioner


def måltid_tidspunkt_baseret():

    if 6 <= dagstime <= 12:
        tilfældig_ret = random.choice(mad[0])
    elif 12 <= dagstime <= 17:
        tilfældig_ret = random.choice(mad[1])
    elif 18 <= dagstime <= 24:
        tilfældig_ret = random.choice(mad[2])
    else:
        tilfældig_ret = random.choice(random.choice(mad))
    return tilfældig_ret


def film_humør_baseret(glad, træt):
    if måned in [11, 12, 1, 2] and (glad <= 3 or træt <= 3):
        tilfældig_film = random.choice(film[3])
    elif glad <= 3 or træt <= 3:
        tilfældig_film = random.choice(film[random.choice([1, 2])])
    elif måned in range(3, 8):
        tilfældig_film = random.choice(film[2])
    else:
        tilfældig_film = random.choice(random.choice(film))
    return tilfældig_film


# kald funktionerne
tilfældig_film = film_humør_baseret(glad, træt)
tilfældig_ret = måltid_tidspunkt_baseret()

# print svar på valg
print(f"Du burde spise {tilfældig_ret} og se {tilfældig_film}.")
