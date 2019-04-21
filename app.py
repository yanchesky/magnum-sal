from flask import Flask, render_template, jsonify, json, request

from classes import Kopalnia, MagnumSal

from komponenty import SlotKostek, KostkiSoli
from komponenty import Targowisko, Karczma, Plac, Warsztat, Czerpalnia, Zamek

app = Flask(__name__)

# Parametry to odpowiednio liczba komnat i poziomów
kopalnia = Kopalnia(8, 3)

# Gra w postaci parametrów przyjmuje imiona graczy
gra = MagnumSal('Janek', "Alicja")

# Miejsca z których można korzystać raz na turę
zamek = Zamek(len(gra.gracze))
plac = Plac()
karczma = Karczma(len(gra.gracze))
warsztat = Warsztat()
czerpalnia = Czerpalnia()

# Sloty do targowiska. Drugis parametr to ceny kostek soli na targu
brazowaKostkaSoli = SlotKostek(KostkiSoli(1, 0, 0), 3, 3, 4, 5)
zielonaKostkaSoli = SlotKostek(KostkiSoli(0, 1, 0), 4, 5, 6)
bialaKostkaSoli = SlotKostek(KostkiSoli(0, 0, 1), 7, 8)

targ = Targowisko(brazowaKostkaSoli, zielonaKostkaSoli, bialaKostkaSoli)

gra.dodajBudynkiZPomocnikami(zamek, warsztat, czerpalnia, targ)


@app.route('/')
def stronaStartowa():
    ag = gra.aktualnyGracz
    zamowienia = lambda x: 3 if x==2 else x

    return render_template('glowna.html',
                           narzedzia=warsztat.narzedzia[:3],
                           resztaKart=[len(warsztat.narzedzia)-3,
                                       len(zamek.zamowieniaKrolewskie)-4],
                           zamowienia=zamek.zamowieniaKrolewskie[:zamowienia(len(gra.gracze))],
                           targ=targ.splaszczListe(),
                           kolejki=[zamek.kolejka.pierwszyEtap,
                                    zamek.kolejka.drugiEtap],
                           pomocnicy=gra.renderujPomocnikow(),
                           kopalnia=kopalnia,
                           zrealizowaneZamowieniaVar=zamek.zrealizowaneZamowienia,
                           maksZamowien=zamek.maksZrealizowanychZamowien,
                           playerTools=[x for x in ag.narzedzia if x.used is False] +
                           [x for x in ag.narzedzia if x.used is True],
                           ag=ag,
                           kosztGornikowVar=karczma.info(),
                           tydzien=gra.tydzien
                           )


@app.route('/karczma')
def budynekKarczmy():

    ag = gra.aktualnyGracz
    kg = karczma.kosztGornikow

    if ag.dostepnaAkcja(karczma):
        if len(kg) > 0:
            if ag.kasa >= kg[0]:
                log = "<u>{0}</u> kupił górnika za {1} groszy.".format(ag.imie, kg[0])
                ag.kasa -= kg.pop(0)
                ag.gornicy += 1
                karczma.aktualnaPozycja += 1
                ag.wykonajAkcje(karczma)

                return jsonify(
                    oknoGracza=ag.info(),
                    log=log,
                    zipek=karczma.aktualnaPozycja
                )
            else:
                log = "Nie stać cię na górnika"
                return jsonify(log=x, alrt=1)
        else:
            log = "Nie ma już dostępnych górników do zwerbowania w tym tygodniu"
            return jsonify(log=log, alrt=1, zipek=karczma.aktualnaPozycja)
    else:
        if karczma in ag.uzyteBudynki:
            alrt = 3
        if ag.akcje == 2:
            alrt = 2

        return jsonify(alrt=alrt)


@app.route('/droga-do-zamku')
def kolejkaDoZamku():

    ag = gra.aktualnyGracz
    glejt = False

    if ag.dostepnaAkcja(zamek) and ag.gornicy > 0:
        # Pobranie zadeklarowanych narzędzi
        zadeklarowaneNarzedzia = [x for x in json.loads(request.args.get('a', 0, type=str))]
        # Sprawdzenie czy znajduje się Glejt oraz potwierdzenie w back-endzie
        if "glejtkrolewski" in zadeklarowaneNarzedzia:
            if ag.uzyjNarzedzie("glejtkrolewski"):
                zamek.kolejka.wstawZGlejtem(ag)
                glejt = True
        else:
            zamek.kolejka.wstaw(ag)

        ag.wykonajAkcje(zamek)
        ag.gornicy -= 1

        log = "<u>{0}</u> wstawił się do kolejki".format(ag.imie)

        return jsonify(
            oknoGracza=ag.info(),
            lpGracza=ag.lpGracza,
            log=log,
            glejt=glejt
        )
    else:
        alrt=0
        if zamek in ag.uzyteBudynki:
            alrt = 3
        if ag.akcje == 2:
            alrt = 2

        return jsonify(alrt=alrt)


@app.route('/plac-zebralniczy')
def placZebralniczy():

    ag = gra.aktualnyGracz

    if ag.dostepnaAkcja(plac):
        ag.kasa += 1
        ag.wykonajAkcje(plac)

        log = "<u>{0}</u> wyżebrał 1 grosz".format(ag.imie)
        return jsonify(oknoGracza=ag.info(), log=log)
    else:
        alrt=0
        if plac in ag.uzyteBudynki:
            alrt = 3
        if ag.akcje == 2:
            alrt = 2

        return jsonify(alrt=alrt)


@app.route('/koniec-tury')
def koniecTury():

    ag = gra.aktualnyGracz
    log = "<u>{0}</u> zakończył turę".format(ag.imie)

    realizujeZamowienie = False
    if ag.uzywaGlejtu:
        ag.uzywaGlejtu = False

    odpoczywa = False

    if ag.akcje == 0:
        odpoczywa = ag.lpGracza
        kopalnia.odpocznijWszystkich(ag)
        log = " <u>{0}</u> zakończył turę i jego górnicy odpoczeli".format(ag.imie)

    gra.zakonczTure()

    gra.tury += 1
    ag = gra.aktualnyGracz
    alrt = 0
    targ.akcje = 0

    if zamek.zrealizowaneZamowienia >= zamek.maksZrealizowanychZamowien and gra.gracze.index(ag) == 0:
        kopalnia.wrocGornikowDoZasobow()
        targ.nowyTydzien()
        karczma.nowyTydzien()
        warsztat.nowyTydzien()
        zamek.nowyTydzien()
        gra.nowyTydzien()
        log = "Skończył się {0} tydzień".format(gra.tydzien)

        if gra.tydzien > zamek.iloscTygodni:
            koniecGry = True
        else:
            koniecGry = False

        info = render_template("podsumowanie.html",
                                gracze=gra.gracze,
                                iloscTur=gra.tury/len(gra.gracze),
                                koniecGry=koniecGry)

        return jsonify(reload=True, info = info)


    for realizujacyZamowienie in [x for x in zamek.kolejka.drugiEtap if x is ag]:
        zamek.kolejka.drugiEtap.remove(ag)
        if(zamek.posiadaWymaganeKostki(ag)):
            zamek.robiZamowienie.append(ag)
            realizujeZamowienie = True
            ag.zrealizowaneZamowienia += 1
            log += "<br/><u>{0}</u> realizuje zamówienie królewskie".format(ag.imie)

        else:
            ag.gornicy += 1
            ag.kasa -= 3
            log = "Nie masz wystarczająco soli na zrealizowanie zamówienia. Tracisz 3 grosze"
            alrt = 1

    if ag in zamek.kolejka.pierwszyEtap:
        zamek.kolejka.przesunKolejke(ag)

    # Nie pobiera więcej zamówienia jeśli się skończą
    if len(zamek.zamowieniaKrolewskie) > 3:
        zamowienia = zamek.zamowieniaKrolewskie[:4]
    else:
        zamowienia = zamek.zamowieniaKrolewskie

    x = render_template('kolejka.html', kolejki=[
                        zamek.kolejka.pierwszyEtap,
                        zamek.kolejka.drugiEtap])

    return jsonify(
        oknoGracza=ag.info(),
        que=x,
        log=log,
        alrt=alrt,
        realizujeZamowienie=realizujeZamowienie,
        odpoczywa=odpoczywa
    )


@app.route('/pomocnik')
def ustawPomocnika():

    ag = gra.aktualnyGracz


    if ag.dostepnaAkcja():
        indeks = request.args.get('a', 0, type=int)
        bzp = gra.budynkiZPomocnikami[indeks]
        if bzp.pomocnik is None and ag.gornicy > 0:
            ag.gornicy -= 1
            bzp.pomocnik = ag
            ag.wykonajAkcje()

            log = " <u>{0}</u> wstawił pomocnika do {1}".format(
                                                        ag.imie, bzp.nazwa)

            return jsonify(
                oknoGracza=ag.info(),
                log=log,
                wstawiam=True,
                gracz=ag.lpGracza * -33
            )

        elif bzp.pomocnik is ag:
            ag.gornicy += 1
            bzp.pomocnik = None

            log = " <u>{0}</u> zabrał pomocnika z {1}".format(
                                                    ag.imie, bzp.nazwa)

            return jsonify(
                oknoGracza=ag.info(),
                log=log,
                gracz=0,
                wstawiam=True
            )

        log = "Stanowisko pomocnika jest już zajęte"
        return jsonify(oknoGracza=ag.info(), log=log, alrt=1)

    else:
        return jsonify(alrt=2)


@app.route('/targ')
def targowisko():

    indeks = request.args.get('a', 0, type=int)
    ag = gra.aktualnyGracz

    if ag.dostepnaAkcja(targ) or targ.akcje < 2:

        narzedzia = [x for x in json.loads(request.args.get('b', 0, type=str))]

        target = targ.targetSlot(indeks)
        indeksDwa = targ.splaszczListe().index(target)
        alrt = 0

        if "glejthandlowy" in narzedzia:
            for x in ag.narzedzia:
                if x.id == "glejthandlowy" and x.used is False:
                    ag.uzywaGlejtu = True
                    x.used = True

        if ag.uzywaGlejtu:
            bonus = 1
        else:
            bonus = 0

        # Jeśli na klikniętym polu jest kostka, to kupuje
        if target.jestKostka:
            if ag.kasa >= target.cena:
                target.jestKostka = False
                ag.kasa -= target.cena - bonus
                ag.kostkiSoli += target.kostka
                targ.akcje += 1
                log = " <u>{0}</u> kupił kostkę za {1} grosze".format(
                    ag.imie, target.cena-bonus)
            else:
                log = "Nie stać cię na tę kostkę"
                alrt = 1

        else:
            if ag.kostkiSoli >= target.kostka:
                target.jestKostka = True
                ag.kasa += target.cena + bonus
                ag.kostkiSoli -= target.kostka
                targ.akcje += 1

                log = " <u>{0}</u> sprzedał kostkę za {1} grosze".format(
                    ag.imie, target.cena+bonus)
            else:
                log = "Nie masz takiej kostki soli"
                alrt = 1

        # Zapobiega podwójnej gratyfikacji pomocnika
        if targ.pomocnik and targ.akcje == 1:
            log += " {0} dostał za to 1 grosz".format(targ.pomocnik.imie)
            targ.pomocnik.kasa += 1

        if targ.akcje == 1:
            ag.wykonajAkcje(targ)


        return jsonify(
            oknoGracza=ag.info(),
            zmiennaJSON=indeksDwa,
            log=log,
            alrt=alrt
        )

    else:
        if targ in ag.uzyteBudynki:
            alrt = 3
        if ag.akcje == 2:
            alrt = 2

        return jsonify(alrt=alrt)


@app.route('/karty-narzedzi')
def narzedzia():

    ag = gra.aktualnyGracz
    indeks = request.args.get('a', 0, type=int)

    # Aby nie można było pobrać karty spoza widocznych
    if indeks > 2 or indeks < 0:
        indeks = 0

    kosztKarty = 3+int(indeks)

    if ag.dostepnaAkcja(warsztat):
        if ag.kasa >= kosztKarty:
            ag.wykonajAkcje(warsztat)
            ag.kasa -= kosztKarty
            ag.narzedzia.append(warsztat.narzedzia.pop(indeks))

            log = " <u>{0}</u> kupił {1} za {2} grosz".format(
                ag.imie, ag.narzedzia[-1].tytul, kosztKarty)

            if warsztat.pomocnik:
                log += " {0} dostał za to 1 grosz".format(
                    warsztat.pomocnik.imie)
                warsztat.pomocnik.kasa += 1

            # Uniemożliwia pobieranie narzędzi jeśli nie ma ich już w puli
            if len(warsztat.narzedzia) > 2:
                noweNarzedzie = warsztat.narzedzia[2].id
            else:
                noweNarzedzie = "puste"

            return jsonify(
                oknoGracza=ag.info(),
                narzedzie=noweNarzedzie,
                log=log,
            )

        else:
            log = "Nie stać cię na ten przedmiot"
            return jsonify(oknoGracza=ag.info(), log=log, alrt=1)

    else:
        alrt=0
        if warsztat in ag.uzyteBudynki:
            alrt = 3
        if ag.akcje == 2:
            alrt = 2

        return jsonify(alrt=alrt)


@app.route('/zamowienia-krolewskie')
def zamowienia():

    ag = gra.aktualnyGracz
    indeks = request.args.get('a', 0, type=int)

    if indeks < 0 or indeks > 3:
        indeks = 0

    if ag in zamek.robiZamowienie:
        kliknieteZamowienie = zamek.zamowieniaKrolewskie[indeks]
        if ag.kostkiSoli >= kliknieteZamowienie.kostkiSoli:
            wybraneZamowienie = zamek.zamowieniaKrolewskie.pop(indeks)
            zamek.robiZamowienie.remove(ag)
            ag.kostkiSoli -= wybraneZamowienie.kostkiSoli
            ag.kasa += wybraneZamowienie.nagroda
            zamek.zrealizowaneZamowienia += 1
            ag.gornicy += 1


            log = " <u>{0}</u> zrealizował zamówienie za {1} groszy.".format(
                ag.imie, wybraneZamowienie.nagroda)

            if zamek.pomocnik:
                log += " <u>{0}</u> dostał 1 grosz za pomocnika".format(
                    zamek.pomocnik.imie)
                zamek.pomocnik.kasa += 1

            if len(zamek.zamowieniaKrolewskie) > 3:
                nowaKarta = render_template(
                    'nowa_karta.html', zamowienie=zamek.zamowieniaKrolewskie[2])
            else:
                nowaKarta = None

            return jsonify(
                oknoGracza=ag.info(),
                log=log,
                nowaKarta=nowaKarta,
                zrealizowanychZamowien=zamek.zrealizowaneZamowienia,
                doRealizacji=len([x for x in zamek.robiZamowienie if x is ag]),
                realizujeZamowienie=True
            )

        else:
            log = "Nie posiadasz wymaganych kostek soli"
            ag.kasa -= 3
            return jsonify(oknoGracza=ag.info(), log=log, alrt=1)
    else:
        log = "Aby zrealizować zamówienie, musisz wstawić się do kolejki"
        return jsonify(log=log, alrt=1)


@app.route('/szyb')
def shaft():

    ag = gra.aktualnyGracz
    indeks = request.args.get('a', 0, type=int)

    kopalnia.zaznaczSzyb(indeks)

    # Jeśli nie ma gracza, wstawiany jest górnik. W przeciwnym wypadku jest
    # zabierany.

    if ag not in kopalnia.target.gracze:
        if (ag.gornicy > 0
        and kopalnia.sprawdzWstawienie()
        and ag.dostepnaAkcja()):
            zabiera = False
            ag.gornicy -= 1
            kopalnia.wstawGracza(ag)
            ag.wykonajAkcje()

            log = " <u>{0}</u> wstawił się do szybu nr: {1}".format(
                ag.imie, str(indeks+1))
        else:
            log = ""
            if not ag.gornicy > 0:
                log = "Nie masz wystarczająco górników"
            if not kopalnia.sprawdzWstawienie():
                log = "Nie ma zachowanej ciągłości. Nie można wstawić robotnika"
            if not ag.dostepnaAkcja():
                log = "Nie masz już wolnych akcji"
            return jsonify(oknoGracza=ag.info(), log=log, alrt=1)

    else:
        if kopalnia.sprawdzZabranie(ag):
            zabiera = True
            ag.gornicy += 1
            kopalnia.usunGracza(ag)
            alrt = 0
            log = " <u>{0}</u> usunął robotnika z szybu nr: {1}".format(ag.imie, str(indeks+1))
        else:
            zabiera = False
            alrt = 1
            log = "Nie można zabrać górnika. Musi zostać zachowana ciągłość"

        return jsonify(
            oknoGracza=ag.info(),
            log=log,
            alrt=alrt,
            zabiera=zabiera
        )

    return jsonify(
        oknoGracza=ag.info(),
        lpGracza=ag.lpGracza,
        zabiera=zabiera,
        log=log
    )


@app.route('/renderuj-modal')
def rend_mod():

    ag = gra.aktualnyGracz
    indeks = request.args.get('a', 0, type=int)

    # Rozpakowuje zagnieżdżone w sobie listy
    splaszczoneKomnaty = kopalnia.splaszczKomnaty()
    kopalnia.zaznaczKomnate(splaszczoneKomnaty[indeks])

    modal = render_template('modal.html',
                            gornicy=[x for x in kopalnia.target.gracze
                                if x is ag],
                            zmeczeniGracza=[x for x in kopalnia.target.zmeczeni
                                if x is ag],
                            reszta=[x for x in kopalnia.target.gracze
                                if x is not ag],
                            zmeczeniReszta=[x for x in kopalnia.target.zmeczeni
                                if x is not ag],
                            narzedzia=[x for x in ag.narzedzia
                                if x.id != "glejthandlowy"
                                and x.id != "glejtkrolewski"
                                and x.used is False],
                            kopalnia=kopalnia.target,
                            czerpakowaLista=kopalnia.przyciskiCzerpaka()
                            )
    return jsonify(oknoGracza=ag.info(), modal=modal)


@app.route('/komnata')
def room():

    ag = gra.aktualnyGracz
    indeks = request.args.get('a', '0', type=int)

    # Rozpakowuje zagniezdzone w sobie listy
    splaszczoneKomnaty = kopalnia.splaszczKomnaty()
    target = splaszczoneKomnaty[indeks]
    kopalnia.zaznaczKomnate(target)

    if ag.dostepnaAkcja():
        # Sprawdzam czy znajduje się tam górnik gracza. Jeśli nie zwracam true
        if ag.gornicy > 0 and kopalnia.sprawdzWstawienie():
            odkrywamy = False
            ag.wykonajAkcje()
            ag.gornicy -= 1
            kopalnia.wstawGracza(ag)
            if kopalnia.target.odkryte is False:
                kopalnia.target.odkryte = True
                odkrywamy = True

            log = " <b>{0}</b> wstawił robotnika do komnaty nr: {1}".format(
                ag.imie, str(indeks+1))

            return jsonify(
                oknoGracza=ag.info(),
                kostkiSoli=kopalnia.target.kostki.kostki,
                woda=kopalnia.target.woda,
                lpGracza=ag.lpGracza,
                log=log,
                odkrywam=odkrywamy,
                tlo=kopalnia.target.tlo
            )
        else:
            if ag.gornicy > 0:
                log = "Nie ma zachowanej ciągłości. Nie można wstawić robotnika"
            else:
                log = "Nie masz wolnych robotników"

            return jsonify(oknoGracza=ag.info(), log=log, alrt=1)

    else:
        return jsonify(alrt=2)


@app.route('/modal')
def modal():

    ag = gra.aktualnyGracz
    indeks = request.args.get('a', 0, type=int)

    if ag.dostepnaAkcja():

        narzedziaZadeklarowane = [x for x in json.loads(request.args.get('c', 0, type=str))]
        narzedziaPotwierdzone = []

        for x in narzedziaZadeklarowane:
            for y in ag.narzedzia:
                if y.id == x and y.used is False:
                    narzedziaPotwierdzone.append(y)
                    y.used = True
                    break

        # Wydobycie
        if indeks == 0:

            # Konwersja kostek do obiektu klasy KostkiSoli
            kostkiSoli = [int(x) for x in json.loads(request.args.get('b', 0, type=str))]
            kostkiObiekt = KostkiSoli(kostkiSoli.count(0),
                                    kostkiSoli.count(1),
                                    kostkiSoli.count(2))
            liczbaKostekSoli = len(kostkiSoli)

            kilofy = 0
            wozek = 0
            iloscWody = kopalnia.target.woda

            for x in narzedziaPotwierdzone:
                if x.id == "kilof":
                    x.used = True
                    kilofy += 1
                if x.id == 'wozek':
                    x.used = True
                    wozek += 1

            # Sprawdzenie czy zadeklarowane kostki zgadzają się z faktycznym stanem
            if kostkiObiekt <= kopalnia.target.kostki:
                print("Frontend-Backend - OK")
            else:
                print("Error przy wydobyciu kostek")
                kostkiObiekt = KostkiSoli(0, 0, 0)

            aktywniGornicy = kopalnia.target.gracze.count(ag)

            if aktywniGornicy > 0:
                if aktywniGornicy+kilofy >= liczbaKostekSoli + iloscWody:
                    listaWozka = []
                    plaskaLista = kopalnia.splaszczKopalnie()
                    kosztTransportu = kopalnia.kosztTransportu(
                        plaskaLista, liczbaKostekSoli, ag)

                    if wozek > 0:
                        listaWozka = kopalnia.wybierzKomnaty(
                            kopalnia.zastosujWozek(plaskaLista, ag), wozek)

                        roznica = 0
                        if liczbaKostekSoli == 1:
                            roznica = 1
                        elif liczbaKostekSoli > 1:
                            roznica = 2

                        kosztTransportu -= roznica*len(listaWozka)

                    if ag.kasa >= kosztTransportu:
                        kopalnia.rozliczTransport(
                            plaskaLista, listaWozka, liczbaKostekSoli, ag)
                        ag.kostkiSoli += kostkiObiekt
                        kopalnia.target.kostki -= kostkiObiekt
                        kopalnia.target.zmeczeni.append(ag)
                        kopalnia.target.gracze.remove(ag)
                        ag.wykonajAkcje()

                        # Pętla jest konieczna, aby przynajmniej 1 górnik się
                        # zmęczył przy wydobywaniu. Mogło to być ominięte przez
                        # wydobywanie z kilofem
                        for x in range(len(kostkiSoli)+iloscWody-kilofy-1):
                            kopalnia.target.zmeczeni.append(ag)
                            kopalnia.target.gracze.remove(ag)

                        log = " <u>{0}</u> wydobył sól w ilości: {1}".format(
                            ag.imie, liczbaKostekSoli)
                        return jsonify(
                            oknoGracza=ag.info(),
                            log=log,
                            wydobywam=True)
                    else:
                        log = "Nie stać cię na przetransportowanie soli"
            return jsonify(log=log, alrt=4)

        # Zabranie górnika
        if indeks == 2:
            if ag in kopalnia.target.gracze:
                if kopalnia.sprawdzZabranie(ag):
                    kopalnia.usunGracza(ag)
                    ag.gornicy += 1
                    log = "<u>{0}</u> usunął robotnika z komnaty nr: {1}".format(
                        ag.imie, str(indeks+1))

                    return jsonify(
                        oknoGracza=ag.info(),
                        log=log,
                        zabieram=True,
                        lpGracza=ag.lpGracza
                    )
                else:
                    log = "Nie można zabrać górnika. Musi zostać zachowana ciągłość"
            else:
                if ag in kopalnia.target.zmeczeni:
                    log = "Nie można usunąć zmęczonych górników"
                else:
                    log = "Nie ma górników do usunięcia"

            return jsonify(oknoGracza=ag.info(), log=log, alrt=1)

        # Wstawienie górnika
        if indeks == 1:
            if ag.gornicy > 0:
                log = "<u>{0}</u> wstawił górnika do szybu".format(ag.imie)
                kopalnia.wstawGracza(ag)
                ag.gornicy -= 1
                ag.wykonajAkcje()

                for x in narzedziaPotwierdzone:
                    if x.id == "lina":
                        kopalnia.wstawGracza(ag)
                        ag.gornicy -= 1

                return jsonify(
                    oknoGracza=ag.info(),
                    log=log,
                    wstawiam=True,
                    lpGracza=ag.lpGracza
                )
            else:
                log = "Nie masz wolnych górnikow"
                return jsonify(log=log, alrt=1)

        # Wydobycie wody za pomocą Czerpalni
        if indeks == 3:

            ag.wykonajAkcje(czerpalnia)
            kostkiWody = [int(x) for x in json.loads(request.args.get('b', 0, type=str))]
            cenaWydobycia = -1

            for x in range(len(kostkiWody)):
                cenaWydobycia = cenaWydobycia + x+1
                kopalnia.target.woda -= 1

            ag.kasa -= cenaWydobycia

            log = "<u>{0}</u> wydobył {1} wody z komnaty".format(
                ag.imie, len(kostkiWody))

            if czerpalnia.pomocnik:
                czerpalnia.pomocnik.kasa += 1
                log += " <u>{0}</u> dostał za to 1 grosz".format(
                    czerpalnia.pomocnik.imie)

            return jsonify(oknoGracza=ag.info(), log=log, wydobywam=True)

    else:
        return jsonify(alrt=2)


@app.route('/narzedzia-inne')
def miscTool():

    ag = gra.aktualnyGracz
    zmienna = request.args.get('a', 0, type=str)

    #
    if zmienna == "moveLeft" or zmienna == "moveRight":
        if(ag.uzyjNarzedzie("czerpak")):
            strona = kopalnia.sprawdzStroneKopalni(zmienna)
            if kopalnia.target.woda:
                kopalnia.przeniesWode(strona)
                log = "<u>{0}</u> przeniósł wodę czerpakiem".format(ag.imie)

                return jsonify(oknoGracza=ag.info(), log=log, czerpak=strona)
            else:
                return jsonify(alrt=1)

    if zmienna == "potw":
        if ag.uzyjNarzedzie("prowiant"):
            for x in range(2):
                if ag in kopalnia.target.zmeczeni:
                    kopalnia.target.zmeczeni.remove(ag)
                    kopalnia.target.gracze.append(ag)

            log = " <u>{0}</u> użył chleba".format(ag.imie)

            return jsonify(oknoGracza=ag.info(), log=log, chleb=True)

    return jsonify(alrt=1)


if __name__ == '__main__':
    app.run(debug=True)
