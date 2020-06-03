# Max-Min 3-Disperzijski Problem

Implementacija algoritma za reševanje Max-Min 3-dispersion Problema (http://www.nakano-lab.cs.gunma-u.ac.jp/Papers/cocoon2019.pdf).

## Uporaba programa
Program se zažene z ukazom
`python main.py [options] [<ime vhodne datoteke>] [<ime izhodne datoteke>]`

Vsi argumenti so opcijski. Vhodna datoteka je privzeto nastavljena na `sys.stdin`, izhodna pa na `sys.stdout`. Možnosti za `options` so:
* `-m:` ali `--metrika=`: sprejme niz stevil `0` (L<sub>∞</sub>), `1` (L<sub>1</sub>) in `2` (L<sub>2</sub>). Naprimer `-m 12` uporabi metriki L<sub>1</sub> in L<sub>2</sub>. Privzeta vrednost je `-m 0`.
* `-t` ali `--time`: vrne porabljen čas za vsako metriko.
* `-p` ali `--plot`: nariše graf za vsako metriko.

### Oblika vhodnih podatkov
Vhodni podatki naj bodo tekstovna datoteka, kjer je v prvi vrstici zapisano število točk `n`, nato pa sledi `n` vrstic, kjer vsaka vsebuje dve vrednosti ločeni s presledkom.

Če želi uporabnik spremeniti format vhodne datoteke, naj spremeni in/ali povozi `fileFunctions.readFile` funkcijo v `main.py`.

### Oblika izhodnih podatkov
Prva vrstica bo oblike `3-dispersion in x`, kjer bo `x` nadomeščen z uporabljeno metriko. Sledile bodo 3 vrstice, kjer bo vsaka predstavljala svojo točko. Nato je opcijsko podana vrstica s porabljenim časom in na koncu še prazna vrstica.

Če želi uporabnik spremeniti format izhodne datoteke, naj spremeni in/ali povozi `fileFunctions.writeFile` funkcijo v `main.py`.

## Ostale datoteke
Datoteke `L_inf.py`, `L_1.py` in `L_2.py` vsebujejo kodo za računanje optimalnih rešitev Max-Min 3-disperzijskega problema vsaka s svojo metriko, kot opisano v članku. Datoteka `testCases.py` vsebuje testne primere iz našega članka. Datoteka `createGraphs.py` vsebuje kodo za generiranje psevdo-naključnih testnih primerov poljubnih velikosti. Datoteka `convexhull.py` vsebuje funkcije za delo s konveksnimi ovojnicami. Datoteka `quickmedian.py` vsebuje funkcije za iskanje mediane v pričakovanem linearnem času.
