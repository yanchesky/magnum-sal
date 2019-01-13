import random
from flask import render_template

from komponenty import KostkiSoli, Narzedzie


class Komnata:

    pierwszyPoziom = [KostkiSoli(2, 1, 0), KostkiSoli(2, 1, 0),
                    KostkiSoli(3, 0, 0), KostkiSoli(3, 0, 0),
                    KostkiSoli(2, 0, 0), KostkiSoli(1, 2, 0),
                    KostkiSoli(1, 1, 0), KostkiSoli(1, 1, 0)]

    drugiPoziom = [KostkiSoli(3, 1, 0), KostkiSoli(0, 2, 1),
                    KostkiSoli(1, 0, 2), KostkiSoli(1, 2, 1),
                    KostkiSoli(2, 1, 1), KostkiSoli(1, 3, 0)]

    trzeciPoziom = [KostkiSoli(0, 3, 2), KostkiSoli(0, 1, 3),
                    KostkiSoli(0, 2, 3), KostkiSoli(0, 0, 4)]

    wodaPierwszyPoziom = [1, 1, 1, 1, 1, 1, 2, 0]
    wodaDrugiPoziom = [2, 2, 2, 2, 2, 3]

    random.shuffle(pierwszyPoziom)
    random.shuffle(wodaPierwszyPoziom)
    random.shuffle(wodaDrugiPoziom)

    def __init__(self, poziom):
        self.kostki = KostkiSoli(0, 0, 0)
        self.woda = 0
        self.gracze = []
        self.zmeczeni = []
        self.odkryte = False
        self.generujNadane(poziom)
        self.przydzielTlo(poziom)

    def generujNadane(self, poziom):
        if poziom == 0:
            self.kostki = Komnata.pierwszyPoziom.pop(0)
            self.woda = Komnata.wodaPierwszyPoziom.pop(0)
        if poziom == 1:
            self.kostki = Komnata.drugiPoziom.pop(0)
            self.woda = Komnata.wodaDrugiPoziom.pop(0)
        if poziom == 2:
            self.kostki = Komnata.trzeciPoziom.pop(0)

    def przydzielTlo(self, poziom):
        if poziom == 0:
            x = random.randint(0,7)

        if poziom == 1:
            x = random.randint(0,5)

        if poziom == 2:
            x = random.randint(0,3)

        self.tlo = "l"+str(poziom)+"k"+str(x)

class Szyb:
    def __init__(self):
        self.gracze = []
        self.zmeczeni = []
        self.komnatySasiadujace = []


class Kopalnia:

    def __init__(self, kmnt=8, pzm=3):
        self.komnaty = [[[Komnata(j) for i in range((kmnt//2)-1*j)]
                         for b in range(2)] for j in range(pzm)]
        self.szyb = [Szyb() for i in range(pzm*2)]

        self.target = None

        self.poziom = None
        self.opakowanieTargetu = None
        self.opakowanieOpakowania = None

        self.indeksSzybu = 0

    # Rozpakowuje zagnieżdżone listy w self.komnaty
    def splaszczKomnaty(self):
        temp = []
        for poziom in self.komnaty:
            for lewaprawa in poziom:
                for komnata in lewaprawa:
                    temp.append(komnata)
        return temp

    # Zaznacza i przechowuje w instancji: Klikniętą komnatę, przylegające komnaty, indeks poziomu i opakowanie komnat
    # Jako argument przyjmuje obiekt komnaty
    def zaznaczKomnate(self, komnata):

        def zaznaczZewnetrznaOprawe(target):
            for poziom in self.komnaty:
                for lewaprawa in poziom:
                    for komnata in lewaprawa:
                        if komnata is target:
                            self.opakowanieTargetu = lewaprawa
                            self.opakowanieOpakowania = poziom
                            self.poziom = self.komnaty.index(poziom)

        def zaznaczNastepnaKomnate(target):
            for obiekt in reversed(self.opakowanieTargetu):
                if obiekt is target:
                    break
                self.nastepnyObiekt = obiekt

        def zaznaczPoprzedniaKomnate(target):
            for obiekt in self.opakowanieTargetu:
                if obiekt is target:
                    break
                self.poprzedniObiekt = obiekt

        self.poprzedniObiekt = None
        self.nastepnyObiekt = None
        self.target = komnata

        zaznaczZewnetrznaOprawe(komnata)
        zaznaczNastepnaKomnate(komnata)
        zaznaczPoprzedniaKomnate(komnata)

        if not self.poprzedniObiekt:
            self.poprzedniObiekt = self.szyb[self.poziom*2+1]

    # Zaznacza komnatę szybu i jeśli są, przylegające komnaty kopalni
    # Jako argument przyjmuje indeks szybu

    def zaznaczSzyb(self, indeks):
        self.poprzedniObiekt = None
        self.indeksSzybu = indeks
        self.target = self.szyb[indeks]
        if indeks > 0:
            self.poprzedniObiekt = self.szyb[indeks-1]
            if not (indeks-1) % 2:
                print("Są komnaty obok")
                poziom = (indeks-1)//2
                for x in range(2):
                    self.target.komnatySasiadujace.append(self.komnaty[poziom][x][0])

    # Zwraca True, jeśli można wstawić górnika do szybu lub komnat kopalni
    def sprawdzWstawienie(self):

        if isinstance(self.target, Szyb):
            if not self.poprzedniObiekt:
                print("Do pierwszego szybu zawsze mozna sie wstawic")
                return True
            else:
                print("Sprawdzam, czy w szybie wyzej znajduja sie ludzie utrzymujacy ciaglosc")
                if len(self.poprzedniObiekt.gracze) > 0:
                    print("Są")
                    return True

                print("Nie znalazlem zadnego robotnika w komnacie wyzej")
                return False
        else:
            if len(self.poprzedniObiekt.gracze)+len(self.poprzedniObiekt.zmeczeni) > 0:
                return True
            print("Nie znalazlem zadnego robotnika w szybie obok")
            return False

    # Rozdziela pieniądze za pomoc w transporcie. Jako parametry wymagana jest
    # odpowiednio: splaszczona lista początek kopalni - zajmowana komnata;
    # komnaty omijane przez wózek. Pusta lista oznacza brak oraz ilość wydobywanych
    # kostek soli oraz gracz wykonujący wydobycie
    def rozliczTransport(self, plaskaLista, listaWozka, iloscKostek, ag):

        def dzielRozdaj(kostki, gracze):
            a = kostki//len(gracze)
            b = kostki % len(gracze)

            if a > 0:
                # Dodaje kase podzielną
                for gracz in gracze:
                    gracz.kasa += a
                    ag.kasa -= a
                    print(gracz.imie, "Otrzymał", a, "groszy za pomoc w transporcie w komnacie", komnata)

            # Rozdzielam losowo resztę
            if b != 0:
                y = random.sample(gracze, b)
                for x in y:
                    x.kasa += 1
                    ag.kasa -= 1
                    print(
                        x.imie, "Otrzymał 1 grosz za pomoc w transporcie na podstawie losowania w komnacie", komnata)

        for komnata in plaskaLista:
            if ag not in komnata.gracze and ag not in komnata.zmeczeni:
                if komnata not in listaWozka:
                    print("W tej komnacie nie działa wózek", komnata)
                    print(komnata.gracze)
                    dzielRozdaj(iloscKostek, komnata.gracze+komnata.zmeczeni)
                elif iloscKostek > 2:
                    print("W tej komnacie działa wózek", komnata)
                    dzielRozdaj(iloscKostek-2, komnata.gracze+komnata.zmeczeni)

    # Wylicza koszt potrzeny do przetransportowania wydobywanych kostek soli
    def kosztTransportu(self, splaszczonaKopalnia, liczbaKostekSoli, ag):
        komnatyBezGracza = 0
        for komnata in splaszczonaKopalnia:
            if ag not in komnata.gracze:
                komnatyBezGracza += 1
        return komnatyBezGracza*liczbaKostekSoli

    # Szuka wszystkich miejsc gdzie można z sensem zastosować wózek. Zwraca listę
    # z pojedynczymi lub podwojnymi listami z obiektami kopalni w których
    # ma działać wózek. [[],[],...]
    def zastosujWozek(self, lista, ag):

        combined = []
        lista.append(self.target)

        i = 0
        while i <= len(lista)-2:
            if ag not in lista[i].gracze:
                if ag not in lista[i+1].gracze:
                    combined.append([lista[i], lista[i+1]])
                else:
                    combined.append([lista[i]])
                i += 2
            else:
                i += 1

        return combined

    # Wybiera losowo omijane komnaty, priorytetyzując podwójne miejsca. Jako
    # parametry przyjmuje listę zwróconą przez zastosujWozek() oraz ilość wózków
    def wybierzKomnaty(self, lista, wozki):
        temp = []
        while wozki > 0:
            podw = []
            poj = []
            for x in lista:
                if len(x) > 1:
                    podw.append(x[0])
                    podw.append(x[1])
                else:
                    poj.append(x[0])

                lista.remove(x)

            if len(podw) == 0:
                temp.append(random.choice(poj))
            else:
                for i in range(2):
                    temp.append(podw[i])

            wozki -= 1

        return temp

    # Zwraca listę obiektów od początku kopalni do celu bez komnaty celu.

    def splaszczKopalnie(self):
        temp = []
        poziom = self.poziom*2+1
        for komnataSzybu in self.szyb:
            temp.append(komnataSzybu)
            if poziom == 0:
                for komnataKopalni in self.opakowanieTargetu:
                    if komnataKopalni is self.target:
                        return temp
                    temp.append(komnataKopalni)
            poziom -= 1

    # Zwraca True, jeśli zabranie górnika nie przerywa łańcucha
    def sprawdzZabranie(self, ag):

        if isinstance(self.target, Szyb):
            print("Sprawdzam czy w obecnym szybie znajduje się inny gracz.")
            # Jeśli w komnacie z ktorej zabierany jest robotnik sa robotnicy innych graczy, to mozna zabrac robotnika
            if len(self.target.gracze) > 1:
                return True
            print("Tylko robotnik gracza zostal znaleziony")

            print("Sprawdzam czy szyb posiada komnaty sąsiadujące")
            if len(self.target.komnatySasiadujace) > 0:
                print("Ma komnaty sąsiadujące. Sprawdzam, czy są w nich górnicy")
                for x in self.target.komnatySasiadujace:
                    if len(x.gracze+x.zmeczeni) > 0:
                        print("Znalazłem gracza w komnacie sąsiadującej. Nie mogę zabrać")
                        return False

            if self.indeksSzybu < 5:
                if len(self.szyb[self.indeksSzybu+1].gracze) > 0:
                    print("Zostal wykryty robotnik w komnacie nizej")
                    return False

            print("Nie wykryto robotnika w komnacie nizej. Robotnik zostal zabrany")
            print("- - - - - - - - - - - - - - - - - - - - - - - - - - -")
            return True
        else:
            if self.nastepnyObiekt is None:
                print("Zabrales robotnika z najbardziej oddalonej komnaty")
                return True
            else:
                print("- - - - - - - - - - - - - - - - - - - - - - - - - - -")
                print("Sprawdzam czy jest ktoś jeszcze w komnacie")
                if len(self.target.gracze+self.target.zmeczeni) > 1:
                    return True

                if len(self.nastepnyObiekt.gracze+self.nastepnyObiekt.zmeczeni) > 0:  # 4 ilosc graczy
                    return False

                print("Nie wykryto robotnika w komnacie obok. Robotnik zostal zabrany")
                print("- - - - - - - - - - - - - - - - - - - - - - - - - - -")
                return True

    # Przesuwa wodę na wybraną stronę po użyciu czerpaka. Jako parametr przyjmuje
    # ciąg znaków "moveForward" lub "moveBackward"
    def przeniesWode(self, x):

        self.target.woda -= 1

        if x == "moveForward":
            self.nastepnyObiekt.woda += 1
        if x == "moveBackward":
            self.poprzedniObiekt.woda += 1

    # Zmienia sygnały czerpaka "moveLeft" i "moveRight" na "moveForward" lub "moveBackward"
    # dla funkcji przeniesienia wody
    def sprawdzStroneKopalni(self, x):

        for y in self.opakowanieOpakowania:
            if y is self.opakowanieTargetu:
                strona = self.opakowanieOpakowania.index(y)
                if ((strona == 0 and x == "moveLeft") or (strona == 1 and x == "moveRight")):
                    return "moveForward"
                else:
                    return "moveBackward"


    def przyciskiCzerpaka(self):
        temp = [0,0]
        if self.nastepnyObiekt:
            temp[1] = 1
        if isinstance(self.poprzedniObiekt, Komnata):
            temp[0] = 1

        if self.opakowanieOpakowania.index(self.opakowanieTargetu) == 0:
            return temp[::-1]
        else:
            return temp

    # Odpoczywa wszystkich górników danego gracza w kopalni. Jako parametr
    # przyjmuje obiekt aktualnego gracza
    def odpocznijWszystkich(self, ag):
        lista = self.splaszczKomnaty()
        indeksy = []
        for komnata in [x for x in lista if ag in x.zmeczeni]:
            for gracz in [x for x in komnata.zmeczeni if x is ag]:
                komnata.zmeczeni.remove(gracz)
                komnata.gracze.append(gracz)
                indeksy.append(lista.index(komnata))

        return set(indeksy)

    def wstawGracza(self, gracz):
        self.target.gracze.append(gracz)

    def usunGracza(self, gracz):
        self.target.gracze.remove(gracz)


class Gracze:
    iloscAktualnychGraczy = 0

    def __init__(self, imie):
        self.gornicy = 7
        self.lpGracza = 1 + Gracze.iloscAktualnychGraczy
        self.kasa = 50 + Gracze.iloscAktualnychGraczy * 2
        self.akcje = 0
        self.uzyteBudynki = []
        self.kostkiSoli = KostkiSoli(3, 3, 2)
        self.imie = imie
        self.narzedzia = [Narzedzie("prowiant","Prowiant"),Narzedzie("czerpak","Czerpak"), Narzedzie("lina", "Lina")]
        self.uzywaGlejtu = False

    # Wyczerpuje narzędzie do rozpoczęcia następnego tygodnia. jako parametr
    # przyjmuje wybrane narzędzie. Zwraca True, jeśli wyczerpywanie przebiegło
    # pomyślnie
    def uzyjNarzedzie(self, zadeklarowaneNarzedzie):
        for szukaneNarzedzie in self.narzedzia:
            if szukaneNarzedzie.id == zadeklarowaneNarzedzie and szukaneNarzedzie.used == False:
                szukaneNarzedzie.used = True
                return True
        return False

    # Wykonuje akcję i opcjonalnie jako parametr przyjmuje budynek, dodając go
    # do puli budynków użytych
    def wykonajAkcje(self, budynek=None):
        self.akcje += 1
        if budynek:
            self.uzyteBudynki.append(budynek)

    # Zwraca True, jeśli gracz posiada wolne akcje i nie korzystał z budynku.
    # Opcjonalnie jako parametr przyjmuje budynek
    def dostepnaAkcja(self, budynek=None):
        if self.akcje < 22 and budynek not in self.uzyteBudynki:
            return True
        else:
            return False

    # Zwraca wszyskie informację o graczu w HTMLu
    def info(self):
        return render_template('info.html',
                               kostkiSoli=self.kostkiSoli,
                               hajs=self.kasa,
                               playerTools=[x for x in self.narzedzia if x.used is False]+
                                            [x for x in self.narzedzia if x.used is True],
                               gornicy=self.gornicy,
                               panel=0,
                               imie=self.imie,
                               akcje=self.akcje,
                               lpGracza=self.lpGracza
                               )


class MagnumSal:

    def __init__(self, *imiona):

        self.gracze = []
        for imie in imiona:
            self.gracze.append(Gracze(imie))
            Gracze.iloscAktualnychGraczy += 1
        self.licznikGraczy = 0
        self.aktualnyGracz = self.gracze[0]
        self.uzyteBudynki = []

        self.budynkiZPomocnikami = []

    # Dodaje do zmiennej budynki, które mają możliwość wstawienia górnika
    # jako pomocnika

    def dodajBudynkiZPomocnikami(self, *budynki):
        for x in budynki:
            self.budynkiZPomocnikami.append(x)

    # Kończy turę obecnego gracza, restuje akcje i czyści listę użytych budynków
    def zakonczTure(self):

        if self.licznikGraczy < len(self.gracze)-1:
            self.licznikGraczy += 1
            self.aktualnyGracz = self.gracze[self.licznikGraczy]
        else:
            self.licznikGraczy = 0
            self.aktualnyGracz = self.gracze[0]

        self.aktualnyGracz.uzyteBudynki = []
        self.aktualnyGracz.akcje = 0

    # Zwraca listę z 4 elementami. 0 jeśli nikt nie zajmuje stanowiska pomocniczego
    # kolejne cyfry oznaczają graczy zajmujących stanowisko
    def renderujPomocnikow(self):
        tmp = []
        for bzp in self.budynkiZPomocnikami:
            if bzp.pomocnik == None:
                tmp.append(0)
            else:
                tmp.append((bzp.pomocnik.lpGracza))
        return tmp

    # Wstawia górnika aktualnego gracza do budynku jako pomocnik
    def wstawPomocnika(self, x):
        self.budynkiZPomocnikami[x].pomocnik = self.aktualnyGracz
        self.aktualnyGracz.gornicy -= 1
        self.akcje += 1

    # Zabiera górnika aktualnego gracza z budynku
    def zabierzPomocnika(self, x):
        del self.budynkiZPomocnikami[x].pomocnik
        self.aktualnyGracz.gornicy += 1
