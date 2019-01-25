import random


class KostkiSoli:
    # Koordynaty spritea z kostkami soli
    koordsy = ['-525px', '-562px', '-599px']

    def __init__(self, brazowa=1, zielona=0, biala=0):
        self.kostki = [brazowa, zielona, biala]
        self.brazowa = brazowa
        self.zielona = zielona
        self.biala = biala

    # Przeciążenie operatorów jest konieczne do poprawnego dodawania kostek
    # soli w przyjętej konwencji

    def __add__(self, nowe):
        tmp = []
        for x, y in zip(self.kostki, nowe.kostki):
            tmp.append(x+y)
        self.kostki = tmp
        return self

    def __sub__(self, nowe):
        tmp = []
        for x, y in zip(self.kostki, nowe.kostki):
            tmp.append(x-y)
        self.kostki = tmp
        return self

    # W tym wypadku przeciążenie operatorów umożliwia porównania kostek soli
    # w obiektach klasy KostkiSoli. Jeśli któryś z odpowiadających elementów
    # nie spełnia warunku, zwraca False

    def __ge__(self, nowe):
        tmp = []
        for x, y in zip(self.kostki, nowe.kostki):
            if not x >= y:
                return False
        return True

    def __le__(self, nowe):
        tmp = []
        for x, y in zip(self.kostki, nowe.kostki):
            if not x <= y:
                return False
        return True

    def __gt__(self, nowe):
        tmp = []
        for x, y in zip(self.kostki, nowe.kostki):
            if not x > y:
                return False
        return True

    def __lt__(self, nowe):
        tmp = []
        for x, y in zip(self.kostki, nowe.kostki):
            if not x < y:
                return False
        return True

    # Przeciążenie tego operatora zostało zastosowane na potrzeby poprawnego
    # działania sprawdzania czy dane kostki znajdują się w jakimś zbiorze.
    # np. if moje_kostki in zamowienia_krolewskie:
    # Jeśli kostek jest mniej zwraca False, a jeśli jest ich równo lub więcej
    # zwraca True

    def __eq__(self, nowe):
        tmp = []
        for x, y in zip(self.kostki, nowe.kostki):
            if x < y:
                return False
        return True

    # Liczy ilość kostek soli po każdym z rodzaju i zwraca sumę

    def __len__(self):
        tmp = 0
        for kostka in self.kostki:
            for x in range(kostka):
                tmp += 1
        return tmp


# Slot targu zajmowany jest przez 1 rodzaj kostek soli. Jest to odpowiednio 4,3,2
# dla brązowej, zielonej i białej.
class SlotKostek:
    def __init__(self, kostka, *cena):  # Ilość i cena kostek
        self.kostkiTargu = [KostkaTargu(x, kostka, self) for x in cena]


class KostkaTargu:
    def __init__(self, x, kostka, slot):
        self.slot = slot
        self.kostka = kostka
        self.jestKostka = False
        self.cena = x
        for lp, y in enumerate(kostka.kostki):
            if y:
                self.koordsy = KostkiSoli.koordsy[lp]
                break


class Kolejka:
    def __init__(self):
        self.pierwszyEtap = []
        self.drugiEtap = []

    def wstaw(self, x):
        self.pierwszyEtap.append(x)

    def wstawZGlejtem(self, x):
        self.drugiEtap.append(x)

    def przesunKolejke(self, x):
        self.drugiEtap.append(x)
        self.pierwszyEtap.remove(x)


class ZamowienieKrolewskie():
    def __init__(self, x):
        self.kostkiSoli = x
        self.obliczNagrode()

    def obliczNagrode(self):
        brazowa = self.kostkiSoli.brazowa
        zielona = self.kostkiSoli.zielona
        biala = self.kostkiSoli.biala

        kstk = (brazowa*5 + zielona*7 + biala*11) - (3 - (brazowa + zielona + biala))

        self.nagroda = kstk


class Narzedzie:
    def __init__(self, id, tytul):
        self.id = id
        self.tytul = tytul
        self.used = False


class Targowisko:
    def __init__(self, *sloty):
        self.nazwa = "Targowisko"
        self.pomocnik = None
        self.sloty = [slot for slot in sloty]
        self.akcje = 0
        self.ustawPoczatkoweKostki()

    # Zaznacza kliknięte miejsce na targu, a następnie kupuje bądz sprzedaje,
    # za odpowiednio najniższą i najwyższą cenę.
    def targetSlot(self, indeks):
        lista = self.splaszczListe()
        target = lista[indeks]

        if target.jestKostka:
            # Kupuje i szuka najniższej ceny
            for kostka in target.slot.kostkiTargu:
                if kostka.jestKostka:
                    return kostka
        else:
            # Sprzedaje i szuka najwyższej ceny
            for kostka in reversed(target.slot.kostkiTargu):
                if kostka.jestKostka is False:
                    return kostka

    # Zwraca listę wszystkich miejsc ja targu w formacie [b,z,B,b,z,B,b,z,b]
    # gdzie b - brązowa kostka soli; z - zielona; B - biała
    def splaszczListe(self):
        zwracanaLista = []
        for x in range(2):
            for y in range(3):
                zwracanaLista.append(self.sloty[y].kostkiTargu[x])
        for x in range(2):
            zwracanaLista.append(self.sloty[x].kostkiTargu[2])
        zwracanaLista.append(self.sloty[0].kostkiTargu[3])

        return zwracanaLista

    def ustawPoczatkoweKostki(self):
        szeregKostek = self.splaszczListe()
        for x in szeregKostek[-3:]:
            x.jestKostka = True


    # Dodaje brązową kostkę soli, jeśli wszystkie sloty są wolne
    def nowyTydzien(self):
        kostka = self.splaszczListe()
        kostka[-1].jestKostka = True
        kostka[-3].jestKostka = True


class Karczma:
    kosztGornikow = [5, 5, 5, 6, 6, 7, 8]

    def __init__(self, iloscGraczy=4):
        self.nazwa = "Karczma"
        self.copyKosztGornikow = Karczma.kosztGornikow[:]
        self.kosztGornikow = Karczma.kosztGornikow[abs(iloscGraczy - 4)*2:]
        self.startowaPozycja = abs(iloscGraczy - 4)*2
        self.aktualnaPozycja = self.startowaPozycja

    def info(self):
        tmp = []
        for x, y in enumerate(self.copyKosztGornikow):
            if x == self.aktualnaPozycja:
                tmp.append({'a': y, 'b': True})
            else:
                tmp.append({'a': y, 'b': False})

        return tmp

    def nowyTydzien(self):
        self.aktualnaPozycja = self.startowaPozycja


class Plac:
    def __init__(self):
        self.nazwa = "Plac"


class Warsztat:
    def __init__(self):
        self.nazwa = "Warsztat"
        self.pomocnik = None
        self.narzedziaWszystkie = [
            Narzedzie("kilof", "Kilof"),
            Narzedzie("kilof", "Kilof"),
            Narzedzie("kilof", "Kilof"),
            Narzedzie("lina", "Lina"),
            Narzedzie("lina", "Lina"),
            Narzedzie("lina", "Lina"),
            Narzedzie("czerpak", "Czerpak"),
            Narzedzie("czerpak", "Czerpak"),
            Narzedzie("czerpak", "Czerpak"),
            Narzedzie("prowiant", "Prowiant"),
            Narzedzie("prowiant", "Prowiant"),
            Narzedzie("prowiant", "Prowiant"),
            Narzedzie("wozek", "Wózek"),
            Narzedzie("wozek", "Wózek"),
            Narzedzie("wozek", "Wózek"),
            Narzedzie("glejthandlowy", "Glejt Handlowy"),
            Narzedzie("glejthandlowy", "Glejt Handlowy"),
            Narzedzie("glejthandlowy", "Glejt Handlowy"),
            Narzedzie("glejtkrolewski", "Glejt Królewski"),
            Narzedzie("glejtkrolewski", "Glejt Królewski"),
            Narzedzie("glejtkrolewski", "Glejt Królewski")]
        random.shuffle(self.narzedziaWszystkie)

        self.narzedzia = [self.narzedziaWszystkie.pop() for x in range(7)]

    def nowyTydzien(self):
        if self.narzedziaWszystkie:
            self.narzedzia = [self.narzedziaWszystkie.pop() for x in range(7)]
        else:
            self.narzedzia = []


class Czerpalnia:
    def __init__(self):
        self.nazwa = "Czerpalnia"
        self.pomocnik = None


class Zamek:
    def __init__(self, iloscGraczy=4):
        self.nazwa = "Zamek"
        self.pomocnik = None
        self.zrealizowaneZamowienia = 0
        self.maksZrealizowanychZamowien = 5
        if iloscGraczy == 2:
            self.maksZrealizowanychZamowien = 3
        self.iloscTygodni = 3
        self.kolejka = Kolejka()
        self.robiZamowienie = []
        self.zamowieniaKrolewskieWszystkie = [
            ZamowienieKrolewskie(KostkiSoli(0, 1, 1)),
            ZamowienieKrolewskie(KostkiSoli(1, 2, 0)),
            ZamowienieKrolewskie(KostkiSoli(2, 0, 1)),
            ZamowienieKrolewskie(KostkiSoli(0, 0, 2)),
            ZamowienieKrolewskie(KostkiSoli(0, 2, 1)),
            ZamowienieKrolewskie(KostkiSoli(1, 0, 2)),
            ZamowienieKrolewskie(KostkiSoli(0, 1, 2)),
            ZamowienieKrolewskie(KostkiSoli(0, 0, 3)),
            ZamowienieKrolewskie(KostkiSoli(0, 2, 0)),
            ZamowienieKrolewskie(KostkiSoli(1, 0, 1)),
            ZamowienieKrolewskie(KostkiSoli(1, 0, 1)),
            ZamowienieKrolewskie(KostkiSoli(0, 1, 1)),
            ZamowienieKrolewskie(KostkiSoli(1, 2, 0)),
            ZamowienieKrolewskie(KostkiSoli(2, 0, 1)),
            ZamowienieKrolewskie(KostkiSoli(0, 3, 0)),
            ZamowienieKrolewskie(KostkiSoli(1, 1, 1)),
            ZamowienieKrolewskie(KostkiSoli(2, 0, 0)),
            ZamowienieKrolewskie(KostkiSoli(2, 0, 0)),
            ZamowienieKrolewskie(KostkiSoli(1, 1, 0)),
            ZamowienieKrolewskie(KostkiSoli(1, 1, 0)),
            ZamowienieKrolewskie(KostkiSoli(0, 2, 0)),
            ZamowienieKrolewskie(KostkiSoli(3, 0, 0)),
            ZamowienieKrolewskie(KostkiSoli(2, 1, 0)),
            ZamowienieKrolewskie(KostkiSoli(2, 1, 0)),
        ]

        self.zamowieniaKrolewskie = [self.zamowieniaKrolewskieWszystkie.pop()
                                    for _ in range(8)]

        random.shuffle(self.zamowieniaKrolewskie)

    def nowyTydzien(self):
        if self.zamowieniaKrolewskieWszystkie:
            self.zamowieniaKrolewskie = [self.zamowieniaKrolewskieWszystkie.pop()
                                        for _ in range(8)]
            random.shuffle(self.zamowieniaKrolewskie)
        else:
            self.zamowieniaKrolewskie = []

    def posiadaWymaganeKostki(self, ag):
        if ag.kostkiSoli in [x.kostkiSoli for x in self.zamowieniaKrolewskie[:4]]:
            return True
        else:
            return False
