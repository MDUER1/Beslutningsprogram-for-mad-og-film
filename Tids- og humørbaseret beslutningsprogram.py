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
    parser.add_argument("--måltid", choices=("morgenmad", "frokost", "aftensmad"),
                        help="Vælg måltid uafhængigt af klokkeslættet.")
    parser.add_argument("--genre", choices=("komedie", "spænding", "drama", "jul"),
                        help="Vælg selv filmkategori.")
    parser.add_argument("--vis", choices=("begge", "mad", "film"), default="begge",
                        help="Få både mad og film eller kun den ene del.")
    parser.add_argument("--antal", type=int, choices=range(1, 51), metavar="1-50", default=1,
                        help="Antal forslag, der skal trækkes.")
    return parser


args = byg_parser().parse_args()
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


MÅLTIDER = dict(zip(("morgenmad", "frokost", "aftensmad"), mad))


def madvalg():
    if args.måltid:
        return MÅLTIDER[args.måltid]
    if 6 <= dagstime <= 12:
        return mad[0]
    if 13 <= dagstime <= 17:
        return mad[1]
    if dagstime >= 18:
        return mad[2]
    return [ret for gruppe in mad for ret in gruppe]


GENRER = dict(zip(("komedie", "spænding", "drama", "jul"), film))


def filmvalg(glad, træt):
    if args.genre:
        return GENRER[args.genre]
    if glad <= 3 or træt <= 3:
        if måned in (11, 12, 1, 2):
            return film[3]
        return film[1] + film[2]
    if måned in range(3, 8):
        return film[2]
    return [titel for gruppe in film for titel in gruppe]


def main():
    retter = madvalg() if args.vis != "film" else []
    titler = []
    if args.vis != "mad":
        glad = args.glad
        træt = args.træt
        if not args.genre:
            glad = glad or spørg("Hvor glad er du fra 1-10? ")
            træt = træt or spørg("Hvor træt er du fra 1-10? ")
        titler = filmvalg(glad, træt)

    for _ in range(args.antal):
        ret = random.choice(retter) if retter else None
        titel = random.choice(titler) if titler else None
        if ret and titel:
            print(f"Du burde spise {ret} og se {titel}.")
        elif ret:
            print(f"Du burde spise {ret}.")
        else:
            print(f"Du burde se {titel}.")


if __name__ == "__main__":
    main()
