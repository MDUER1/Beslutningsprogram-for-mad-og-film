"""Automatiseringsprogram for hvad for noget mad og hvilke film jeg skal se til."""
# importerede moduler
import random
import datetime

# Variabler: Bruger-input
glad = int(input("hvor glad er du fra 1-10?"))
træt = int(input("hvor træt er du fra 1-10?"))
# Tidsvariabler
nu = datetime.datetime.now()
måned = nu.month
dagstime = nu.hour


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
    if 0 <= glad <= 3 or 0 <= træt <= 3:
        tilfældig_film = random.choice(film[random.choice([1, 2])])
    elif måned in [11, 12, 1, 2] and 0 <= glad <= 3 or 0 <= træt <= 3:
        tilfældig_film = random.choice(film[3])
    elif måned in range(3, 8) and 4 <= glad <= 10 or 4 <= træt <= 10:  # fra 3-10
        tilfældig_film = random.choice(film[2])
    else:
        tilfældig_film = random.choice(random.choice(film))
    return tilfældig_film


# kald funktionerne
tilfældig_film = film_humør_baseret(glad, træt)
tilfældig_ret = måltid_tidspunkt_baseret()

# print svar på valg
print(f"Du burde spise {tilfældig_ret} og se {tilfældig_film}.")
