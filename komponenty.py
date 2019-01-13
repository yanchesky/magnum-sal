import random


class KostkiSoli:
    # Koordynaty spritea z kostkami soli
    koordsy = ['-525px', '-562px', '-599px']

    def __init__(self, brazowa=1, zielona=0, biala=0):
        self.kostki = [brazowa, zielona, biala]
        self.brazowa = brazowa
        self.zielona = zielona
        self.biala = biala

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

    def __eq__(self, nowe):
        tmp = []
        for x, y in zip(self.kostki, nowe.kostki):
            if x < y:
                return False
        return True

    def __repr__(self):
        return "Kostki("+str(self.kostki)+")"

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
        brown = self.kostkiSoli.brazowa
        green = self.kostkiSoli.zielona
        white = self.kostkiSoli.biala

        kstk = (brown*5+green*7+white*11)-(3-(brown+green+white))

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
            for y in target.slot.kostkiTargu:
                if y.jestKostka:
                    return y
        else:
            # Sprzedaje i szuka najwyższej ceny
            for y in reversed(target.slot.kostkiTargu):
                if y.jestKostka == False:
                    return y

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


class Karczma:
    kosztGornikow = [5, 5, 5, 6, 6, 7, 8]

    def __init__(self, iloscGraczy=4):
        self.nazwa = "Karczma"
        self.copyKosztGornikow = Karczma.kosztGornikow[:]
        self.kosztGornikow = Karczma.kosztGornikow[abs(iloscGraczy-4)*2:]
        self.aktualnaPozycja = abs(iloscGraczy-4)*2

    def info(self):
        tmp = []
        for x, y in enumerate(self.copyKosztGornikow):
            if x == self.aktualnaPozycja:
                tmp.append({'a': y, 'b': True})
            else:
                tmp.append({'a': y, 'b': False})

        return tmp


class Plac:
    def __init__(self):
        self.nazwa = "Plac"


class Warsztat:
    def __init__(self):
        self.nazwa = "Warsztat"
        self.pomocnik = None
        self.narzedzia = [
            Narzedzie("kilof", "Kilof"),
            Narzedzie("lina", "Lina"),
            Narzedzie("czerpak", "Czerpak"),
            Narzedzie("prowiant", "Prowiant"),
            Narzedzie("wozek", "Wozek"),
            Narzedzie("glejthandlowy", "Glejt Handlowy"),
            Narzedzie("glejtkrolewski", "Glejt Królewski")]
        random.shuffle(self.narzedzia)


class Czerpalnia:
    def __init__(self):
        self.nazwa = "Czerpalnia"
        self.pomocnik = None


class Zamek:
    def __init__(self, iloscGraczy=4):
        self.nazwa = "Zamek"
        self.pomocnik = None
        self.zrealizowaneZamowienia = 0
        self.maksZrealizowanychZamowien = 7
        if iloscGraczy == 2:
            self.maksZrealizowanychZamowien = 4
        self.kolejka = Kolejka()
        self.robiZamowienie = []
        self.zamowieniaKrolewskie = [
            ZamowienieKrolewskie(KostkiSoli(2, 0, 0)),
            ZamowienieKrolewskie(KostkiSoli(2, 0, 0)),
            ZamowienieKrolewskie(KostkiSoli(1, 1, 0)),
            ZamowienieKrolewskie(KostkiSoli(1, 1, 0)),
            ZamowienieKrolewskie(KostkiSoli(0, 2, 0)),
            ZamowienieKrolewskie(KostkiSoli(3, 0, 0)),
            ZamowienieKrolewskie(KostkiSoli(2, 1, 0)),
            ZamowienieKrolewskie(KostkiSoli(2, 1, 0)),
            ZamowienieKrolewskie(KostkiSoli(1, 1, 1)),
            ZamowienieKrolewskie(KostkiSoli(1, 0, 1)),
            ZamowienieKrolewskie(KostkiSoli(0, 2, 1))
        ]
        random.shuffle(self.zamowieniaKrolewskie)

    def posiadaWymaganeKostki(self, ag):
        if ag.kostkiSoli in [x.kostkiSoli for x in self.zamowieniaKrolewskie[:4]]:
            return True
        else:
            return False
