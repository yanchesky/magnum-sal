# Magnum Sal
### Port gry planszowej, umożliwijący przeprowadzenie rozgrywki z poziomu przeglądarki internetowej.

- [Instalacja](#instalacja)
- [Ustawienia](#ustawienia)
- [Zasady](#zasady)
- [Dodatkowe informacje](#dodatkowe-informacje)
- [Prawa autorskie](#prawa-autorskie)


![alt text](https://github.com/yanchesky/magnum-sal/raw/master/readmefiles/main.jpg)


## Instalacja
**1. Pobranie repozytorium**
```
git clone https://github.com/yanchesky/magnum-sal.git
```
**2. Instalacja Virtualenv**
```
pip install virtualenv
```
**3. Stworzenie wirtualnego środowiska w katalogu aplikacji**
```
virtualenv magnum_sal
```
**4. Aktywowanie wirtualnego środowiska**
```
source magnum_sal/bin/activate
```
**5. Instalacja wymaganych paczek**
```
pip install -r requirements.txt
```
## Ustawienia
**1. Otworzyć plik** `/app.py` **i wpisać imiona graczy. Min - 2, Max - 4**
```
28. gra = MagnumSal('Gracz1', 'Gracz2')
``` 
**2. Opcjonalnie ustawić ilość zamówień do zrealizowania. Domyślnie 7
```
29. MAX_ZREALIZOWANYCH_ZAMOWIEN = 7
```
**3. W folderze z aktywowanym środowiskiem wpisać komendę**
```
python app.py
```
**4. Wpisać w przeglądarkę internetową Firefox\*.**
```
127.0.0.1:5000
```
\*Niestety obecna wersja działa tylko na Firefoxie. Google Chrome i Safari mają problem z renderowaniem animacji obracania kart. 

## Zasady 

Pełne zasady gry są dostępne na stronie gry o tej samej nazwie na portalu https://rebel.pl

Link do pobrania [zasady gry](https://www.rebel.pl/e4u.php/1,ModFiles/Download/files/instrukcje/MagnumSal_rules_1.0.pdf)

Zmiany zaadaptowane do elektronicznej wersji gry, różniące się od wersji planszowej:

1. Pierwszy gracz, jest pierwszym wpisanym graczem. Nie odbywa się losowanie
2. Aktualna cena górników i pozostała ich ilość wyświetlona jest na górnym pasku
3. Ilość aktualnie zrealizowanych zamówień również wyświetlona jest na górnym pasku
4. Nigdy nie można złamać zasady łańcucha
5. Cena kupna lub sprzedaży kostki soli na targu, pojawia się po najechaniu myszką na odpowiednie miejsce
6. Użycie prowiantu i liny ograniczone jest tylko do 1 komnaty
7. Użycie wózka powoduje automatyczne znalezienie najopłacalniejszego miejsca do zastosowania. Jeśli jest ich więcej niż 1, to wybiera je losowo. Podwójne użycie wózka pozwala ominąć więcej komnat, a nie przewieźć więcej soli. Max 2 soli na wózek.
8. Podział pieniędzy za pomoc w transporcie kostek soli jest równomierny między graczy zajmujących komnatę, jeśli kwota jest podzielna na ilość graczy. W przeciwnym wypadku gracze są losowani. 

### Wstawianie górnika do kopalni
**Wstawienie do szybu**
Wstawienie do szybu następuje po kliknięciu w kartę szybu. Jeśli nie ma tam naszego górnika, to jest on wstawiany. Jeśli jest, to będzie on automatycznie zabierany. 

![gif](https://github.com/yanchesky/magnum-sal/raw/master/readmefiles/Untitled.gif)

**Wstawienie do komnaty**
Wstawienie do komnaty następuje automatycznie w przypadku, kiedy komnata jest jeszcze nieodkryta. Jeśli jest odkryta, pojawia się **okno komnaty** w którym możemy wykonać wstawienie lub zabranie górnika z szybu.

![gif](https://github.com/yanchesky/magnum-sal/raw/master/readmefiles/wstawienie.gif)

### Wydobycie soli oraz wody
Korzystanie z budynku szybu wodnego, odbywa się w oknie komnaty. Należy zaznaczyć tyle wody ile chce się wydobyć. Po zaznaczeniu pojawi się cena wydobycia i następnie trzeba kliknąć ikonę pompy. W przypadku wydobycia soli, należy analogicznie zaznaczyć kostki soli. Po zaznaczeniu, podniesie się tylu górników, ilu jest wymaganych do wydobycia konkretnej ilości soli.

![gif](https://github.com/yanchesky/magnum-sal/raw/master/readmefiles/wydobycie.gif)

### Odpodczynek
Aby górnicy odpoczeli, należy nie wykonywać żadnej akcji i wcisnąć przycisk końca tury

### Narzędzia
Wszystkie narzędzia z wyłączeniem glejtu królewskiego i glejtu handlowego, używane są z poziomu okna komnaty. Po kupieniu ich w warsztacie, pojawią w oknie komnaty pod sekcją wydobycia wody. Aby zadeklarować chęć użycia danego narzędzia należy na niego kliknąć, a następnie wykonać żądanie powiązane z danym narzedziem. Dla kilofa i wózka jest to wydobycie, dla liny wstawienie górnika. Prowiant i czerpak działają inaczej. Po kliknięciu, pojawi się odpowiednio przycisk potwierdzający albo strzałki ze stronami na które chcemy przenieść wodę. W przypadku tych narzędzi wystarczy kliknąć jeden z przycisków aby zrealizować chęć użycia narzędzia.

![gif](https://github.com/yanchesky/magnum-sal/raw/master/readmefiles/narzedzia.gif)

W przypadku glejtu królewskiego i handlowego, chęć użycia deklarujemy w **oknie zasobów gracza**.
W oknie zasobów mamy również informacje o aktualnym graczu i ilości jego wykonanych akcji, ilości wolnych górników, posiadanych kostkach soli oraz poniądzach.

![gif](https://github.com/yanchesky/magnum-sal/raw/master/readmefiles/oknogracza.jpg)

## Dodatkowe informacje
### Ograniczenia w bieżącej wersji gry
Projekt jest jeszcze w etapie produkcji alfa i niżej wymienione ograniczenia bedą systematycznie eliminowane.
- Rozgrywka trwa jeden tydzień, a nie trzy. Ilość zrealizowanych zamówień wymagana do ukończenia gry to 7
- Zawsze są widoczne 4 zamówienia królewskie niezależnie od ilości graczy
- Nie jest możliwa sprzedaż soli na targu jeśli wszystkie miejsca są zajęte, nawet jeśli używa się glejtu
- W warsztacie znajduje się po 1 narzędziu z rodzaju
- Zostały dodane 3 zamówienia królewskie, które wymagają posiadania białej kostki soli
- W karczmie zawsze jest dostępne 7 górników na grę
- Na targu można kupić i sprzedać tę samą kostkę soli
- Na koniec rozgrywki każde narzędzie jest warte 1 grosz

### Planowane wdrożenia
Poza wyeliminowaniem wyżej wymienionych ograniczeń, w planach jest wdrożenie następujących funkcji:
  - Poprawne działanie animacji na wszystkich przeglądarkach internetowych
  - Dodanie baz danych przechowujących zasoby graczy, stan gry, wyniki końcowe
  - Dodanie menu początkowe z logowaniem, opcją stworzenia stołów do gry i możliwością dołączenia do stołu
  - Umieścić aplikację na serwerze i z obsługą WebSocket 

## Prawa autorskie
Ilustracje planszy, komnat i szybów, narzędzi, grafiki monet oraz rewersów kart są dziełem Piotra Nowojewskiego. Zostały pobrane z serwisu https://boardgamegeek.com , gdzie zostały udostępnione przez autora.

Inne grafiki zostały pobrane ze strony http://punchev.com/fui-gameart-gui/ i przerobione do własnych wymagań. 

Projekt gry i zasady są dziełem Marcina Krupińskiego i Filipa Miłuńskiego.

Wydawcą gry planszowej jest Leonardo Games

Projekt powstał w celach naukowych aby nauczyć się podstaw języka programowania Python i JavaScript oraz jednocześnie żeby docenić twórców tej gry i zachęcić do zakupu planszowej wersji.
Materiał źródłowy został udostępniony publicznie, aby można było zweryfikować poprawność napisanego kodu.
