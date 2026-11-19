"""Automatiseringsprogram for hvad for noget mad og hvilke film jeg skal se til."""
# importerede moduler
from itertools import product
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
    parser.add_argument("--måltid", choices=("morgenmad", "frokost", "aftensmad", "snack"),
                        help="Vælg måltid uafhængigt af klokkeslættet.")
    parser.add_argument("--genre", choices=("komedie", "spænding", "drama", "jul"),
                        help="Vælg selv filmkategori.")
    parser.add_argument("--vis", choices=("begge", "mad", "film"), default="begge",
                        help="Få både mad og film eller kun den ene del.")
    parser.add_argument("--antal", type=int, choices=range(1, 51), metavar="1-50", default=1,
                        help="Antal forslag, der skal trækkes.")
    parser.add_argument("--seed", type=int, help="Gentag et tilfældigt udvalg med samme indstillinger.")
    parser.add_argument("--unik", action="store_true", help="Træk forskellige forslag uden gentagelser.")
    parser.add_argument("--madtid", type=int, metavar="MIN", help="Maksimal anslået tilberedningstid.")
    parser.add_argument("--servering", choices=("varm", "kold"), help="Vælg varm eller kold mad.")
    parser.add_argument("--type", choices=("film", "serie"), help="Vælg spillefilm eller serieafsnit.")
    parser.add_argument("--spilletid", type=int, metavar="MIN", help="Maksimal cirka-spilletid pr. titel.")
    parser.add_argument("--udelad", action="append", default=[], metavar="NAVN",
                        help="Udeluk en ret eller titel. Kan gentages.")
    return parser


parser = byg_parser()
args = parser.parse_args()
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
MÅLTIDER["snack"] = ["popcorn", "gulerodsstave", "ristede kikærter"]


# Omtrentlige minutter for en enkel portion. Thaiboks og kakaomælk er serveringsklare.
MADTID = {
    "havregrød": 10, "yoghurt": 2, "kakaomælk": 1,
    "Thaiboks": 5, "æg": 10, "frugt": 3,
    "bønner": 10, "gryderet": 45, "ratatouille": 40,
    "popcorn": 5, "gulerodsstave": 5, "ristede kikærter": 30,
}


KOLDE_RETTER = {"yoghurt", "kakaomælk", "frugt", "gulerodsstave"}


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


SERIER = {"How i met your mother", "Friends"}


# Cirka spilletid i minutter, for serier pr. afsnit.
SPILLETID = {
    "How i met your mother": 22, "Friends": 22, "Tømmermænd i Vegas": 100,
    "The Mechanic": 93, "White House Down": 131, "Interstellar": 169,
    "Greenbook": 130, "Shawshank Redemption": 142, "Intouchables": 112,
    "Home Alone": 103, "Elf": 97, "Die Hard": 132,
}


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
    rng = random.Random(args.seed)
    retter = madvalg() if args.vis != "film" else []
    if args.vis != "film" and args.madtid is not None:
        retter = [ret for ret in retter if MADTID[ret] <= args.madtid]
        if not retter:
            parser.error("Ingen retter passer til tilberedningstiden.")
    if args.vis != "film" and args.servering:
        retter = [ret for ret in retter if (ret in KOLDE_RETTER) == (args.servering == "kold")]
        if not retter:
            parser.error("Ingen retter passer til den valgte servering.")
    titler = []
    if args.vis != "mad":
        glad = args.glad
        træt = args.træt
        if not args.genre:
            glad = glad or spørg("Hvor glad er du fra 1-10? ")
            træt = træt or spørg("Hvor træt er du fra 1-10? ")
        titler = filmvalg(glad, træt)

    if args.vis != "mad" and args.type:
        titler = [titel for titel in titler if (titel in SERIER) == (args.type == "serie")]
        if not titler:
            parser.error("Ingen titler af den ønskede type. Prøv en anden genre.")

    if args.vis != "mad" and args.spilletid is not None:
        titler = [titel for titel in titler if SPILLETID[titel] <= args.spilletid]
        if not titler:
            parser.error("Ingen titler passer til spilletiden.")

    udeladt = {navn.strip().casefold() for navn in args.udelad}
    retter = [ret for ret in retter if ret.casefold() not in udeladt]
    titler = [titel for titel in titler if titel.casefold() not in udeladt]
    if args.vis != "film" and not retter:
        parser.error("Ingen retter tilbage efter filtrering.")
    if args.vis != "mad" and not titler:
        parser.error("Ingen titler tilbage efter filtrering.")

    if args.unik:
        mulige = list(product(retter or [None], titler or [None]))
        if args.antal > len(mulige):
            parser.error(f"Der findes kun {len(mulige)} forskellige forslag med disse valg.")
        forslag = rng.sample(mulige, args.antal)
    else:
        forslag = [(rng.choice(retter) if retter else None,
                    rng.choice(titler) if titler else None) for _ in range(args.antal)]

    for ret, titel in forslag:
        if ret and titel:
            print(f"Du burde spise {ret} og se {titel}.")
        elif ret:
            print(f"Du burde spise {ret}.")
        else:
            print(f"Du burde se {titel}.")


if __name__ == "__main__":
    main()
