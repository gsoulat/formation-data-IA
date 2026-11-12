"""Validation structurelle des numéros de TVA — module fourni.

CE QUE CE MODULE FAIT, ET CE QU'IL NE FAIT PAS
==============================================
Il vérifie qu'un numéro est **bien formé** : bon code pays, bonne longueur, bons
caractères, et surtout **clé de contrôle correcte**. Chaque État membre calcule
cette clé à sa façon ; les dix algorithmes présents dans le jeu sont implémentés
ici pour vous éviter d'en recopier les spécifications.

Il ne dit **rien** de l'existence réelle du numéro. Un numéro peut passer toutes
ces vérifications sans avoir jamais été attribué à une entreprise. Seul VIES
peut trancher cela — et c'est le sujet de votre travail.

Lisez le code avant de l'utiliser : vous devrez expliquer en soutenance ce que
recouvre « structurellement valide », et pourquoi cela ne suffit pas.

Usage :
    from validation_structure import normaliser, valider, PAYS_COUVERTS

    normaliser(" fr 27 552032534 ")   -> "FR27552032534"
    valider("FR27552032534")          -> (True,  "ok")
    valider("FR99552032534")          -> (False, "cle_invalide")
"""

from __future__ import annotations

import re

# --------------------------------------------------------------------------
# Normalisation
# --------------------------------------------------------------------------

def normaliser(brut: str | None) -> str:
    """Met un numéro sous forme canonique : majuscules, sans séparateurs.

    « fr 27 552032534 », « FR-27552032534 » et « fr.27552032534 » donnent tous
    « FR27552032534 ». Ce sont des accidents de saisie, pas des erreurs de fond :
    ces numéros sont valides une fois nettoyés.
    """
    return re.sub(r"[^A-Z0-9]", "", (brut or "").upper())


# --------------------------------------------------------------------------
# Clés de contrôle, un algorithme par État membre
# --------------------------------------------------------------------------

def _chiffres(n: str) -> list[int]:
    return [int(c) for c in n]


def _fr(n: str) -> bool:
    """France : 2 chiffres de clé + 9 chiffres de SIREN.

    clé = (12 + 3 × (SIREN mod 97)) mod 97
    """
    if not re.fullmatch(r"\d{11}", n):
        return False
    return int(n[:2]) == (12 + 3 * (int(n[2:]) % 97)) % 97


def _be(n: str) -> bool:
    """Belgique : 10 chiffres, débutant par 0 ou 1. Les 2 derniers sont la clé.

    clé = 97 − (les 8 premiers chiffres mod 97)
    """
    if not re.fullmatch(r"[01]\d{9}", n):
        return False
    return int(n[8:]) == 97 - (int(n[:8]) % 97)


def _nl(n: str) -> bool:
    """Pays-Bas : 9 chiffres + « B » + 2 chiffres.

    Les 8 premiers chiffres sont pondérés 9, 8, … 2 ; le 9e est la clé, égale à
    la somme modulo 11. Attention : le suffixe « B## » n'entre PAS dans le calcul.
    """
    if not re.fullmatch(r"\d{9}B\d{2}", n):
        return False
    d = _chiffres(n[:9])
    return sum(d[i] * (9 - i) for i in range(8)) % 11 == d[8]


def _lu(n: str) -> bool:
    """Luxembourg : 8 chiffres. Les 2 derniers = les 6 premiers mod 89."""
    if not re.fullmatch(r"\d{8}", n):
        return False
    return int(n[6:]) == int(n[:6]) % 89


def _pt(n: str) -> bool:
    """Portugal : 9 chiffres, pondération 9 à 2, clé mod 11 (0 si reste 0 ou 1)."""
    if not re.fullmatch(r"\d{9}", n):
        return False
    d = _chiffres(n)
    reste = sum(d[i] * (9 - i) for i in range(8)) % 11
    return d[8] == (0 if reste in (0, 1) else 11 - reste)


def _dk(n: str) -> bool:
    """Danemark : 8 chiffres, pondération 2,7,6,5,4,3,2,1 ; somme divisible par 11."""
    if not re.fullmatch(r"\d{8}", n):
        return False
    return sum(x * p for x, p in zip(_chiffres(n), [2, 7, 6, 5, 4, 3, 2, 1])) % 11 == 0


def _fi(n: str) -> bool:
    """Finlande : 8 chiffres, pondération 7,9,10,5,8,4,2 ; un reste de 1 est interdit."""
    if not re.fullmatch(r"\d{8}", n):
        return False
    d = _chiffres(n)
    reste = sum(x * p for x, p in zip(d[:7], [7, 9, 10, 5, 8, 4, 2])) % 11
    return reste != 1 and d[7] == (0 if reste == 0 else 11 - reste)


def _pl(n: str) -> bool:
    """Pologne : 10 chiffres, pondération 6,5,7,2,3,4,5,6,7 ; clé = somme mod 11."""
    if not re.fullmatch(r"\d{10}", n):
        return False
    d = _chiffres(n)
    return sum(x * p for x, p in zip(d[:9], [6, 5, 7, 2, 3, 4, 5, 6, 7])) % 11 == d[9]


def _luhn_valide(d: list[int]) -> bool:
    """Algorithme de Luhn : le dernier chiffre EST la clé, il n'est jamais doublé.

    Le doublement commence donc au chiffre qui le précède, en partant de la droite.
    (C'est l'erreur classique sur cet algorithme.)
    """
    total, doubler = 0, False
    for x in reversed(d):
        if doubler:
            x *= 2
            if x > 9:
                x -= 9
        total += x
        doubler = not doubler
    return total % 10 == 0


def _it(n: str) -> bool:
    """Italie : 11 chiffres, contrôlés par Luhn."""
    return bool(re.fullmatch(r"\d{11}", n)) and _luhn_valide(_chiffres(n))


def _se(n: str) -> bool:
    """Suède : 12 chiffres, terminés par « 01 » ; Luhn sur les 10 premiers."""
    return bool(re.fullmatch(r"\d{12}", n)) and n[10:] == "01" and _luhn_valide(_chiffres(n[:10]))


CONTROLES = {"FR": _fr, "BE": _be, "NL": _nl, "LU": _lu, "PT": _pt,
             "DK": _dk, "FI": _fi, "PL": _pl, "IT": _it, "SE": _se}

PAYS_COUVERTS = sorted(CONTROLES)


def valider(brut: str | None) -> tuple[bool, str]:
    """Valide un numéro et renvoie (valide, motif).

    Motifs possibles : `ok`, `vide`, `trop_court`, `pays_non_couvert`,
    `cle_invalide`. À vous de décider ce que votre pipeline fait de chacun —
    notamment de `pays_non_couvert`, qui n'est PAS une invalidité mais une
    limite de ce module.
    """
    n = normaliser(brut)
    if not n:
        return False, "vide"
    if len(n) < 4:
        return False, "trop_court"
    pays, reste = n[:2], n[2:]
    controle = CONTROLES.get(pays)
    if controle is None:
        return False, "pays_non_couvert"
    return (True, "ok") if controle(reste) else (False, "cle_invalide")
