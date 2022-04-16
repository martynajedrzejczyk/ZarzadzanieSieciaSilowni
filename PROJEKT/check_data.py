import cx_Oracle
import variables
import datetime
global cnxn
from update_data import czysc_po_trenerze
import re
from read_data import wybierz_sale, wybierz_recepcje, wybierz_kantorki

def sprawdz_klubowicz_grupa(pesel, id):
    insert = f"""select * from przynaleznosci_klubowiczow_do_grup where
            id_grupy = {id} and pesel_klubowicza = {pesel} """
    print(insert)
    cursor = variables.cnxn.cursor()
    cursor.execute(insert)
    if len(cursor.fetchall()) > 0:
        cursor.close()
        return "Blad"
    cursor.close()
    return None

def sprawdz_klubowicz_plan(pesel, nr):
    insert = f"""select * from cwicza_z_planem where
            nr_planu = {nr} and pesel_klubowicza = {pesel} """
    print(insert)
    cursor = variables.cnxn.cursor()
    cursor.execute(insert)
    if len(cursor.fetchall()) > 0:
        cursor.close()
        return "Blad"
    cursor.close()
    return None

def sprawdz_pracownicy(dane):
    pesel = dane[0]
    imie = dane[1]
    nazwisko = dane[2]
    pensja = dane[3]

    if pesel == "":
        return 'Wpisz pesel'
    if imie == "":
        return 'Wpisz imie'
    if nazwisko == "":
        return 'Wpisz nazwisko'
    if pensja == "":
        return 'Wpisz pensja'

    pensja = pensja.replace(",", ".")
    print(pensja, "   pensja", flush=True)
    etat = dane[4]
    #'Recepcjonista':
    #'Sprzątacz':
    #'Trener':

    #sprawdzanie peselu

    if not pesel.isdecimal():
        return "Pesel nie składa się z samych liczb"
    pesel = int(dane[0])
    if pesel > 99999999999:
        return "Pesel jest za długi"
    if len(dane[0]) < 11:
        return "Pesel jest za krótki"

    prac = f"""select pesel from pracownicy_perspektywa where pesel = {pesel} """
    cursor = variables.cnxn.cursor()
    cursor.execute(prac)

    if len(cursor.fetchall()) > 0:
        return "Istnieje pracownik o takim peselu, sprawdź jego poprawność"
    #sprawdzenie imienia
    cursor.close()

    if not imie.isalpha():
        return "Wpisano niepoprawne imie"

    #sprawdzenie nazwiska

    if not nazwisko.isalpha():
        return "Wpisano niepoprawne nazwisko"

    # sprawdzanie pensji
    if pensja == "":
        return "Podaj pensję"


    pensja2 = pensja
    if not pensja2.replace('.', '').isdecimal():
        return "Pensja podana w złym formacie"

    pensja = float(pensja)
    pensja = round(pensja, 2)
    if pensja > 99999.99:
        return "Pensja jest za duża"
    #sprawdzenie etatu

    if etat not in ['Recepcjonista', 'Sprzątacz', 'Trener']:
        return "Wybrano niepoprawny etat"

    if etat == "Sprzątacz":
        # nr kantorka
        select = f"""select nr_pomieszczenia from kantorki where adres_silowni = '{variables.wybranaSilownia}'  order by 1 desc"""
        cursor = variables.cnxn.cursor()
        cursor.execute(select)
        if len(cursor.fetchall()) == 0:
            return "Najpierw dodaj kantorek"
    elif etat == "Recepcjonista":
        select = f"""select nr_pomieszczenia from recepcje where adres_silowni = '{variables.wybranaSilownia}'  order by 1 desc"""
        cursor = variables.cnxn.cursor()
        cursor.execute(select)
        if len(cursor.fetchall()) == 0:
            return "Najpierw dodaj recepcję"
    return None

def sprawdz_szafki(dane):
    ilosc = dane[0]
    pomieszczenie = dane[1]

    if ilosc == "":
        return 'Wpisz ilosc'
    if pomieszczenie == "":
        return 'Wpisz pomieszczenie'

    if not pomieszczenie.isdecimal():
        return "Podano zły numer pomieszczenia"


    szatnie = f"""select nr_pomieszczenia from szatnie where nr_pomieszczenia = {int(pomieszczenie)} AND adres_silowni = '{variables.wybranaSilownia}' """
    cursor = variables.cnxn.cursor()
    cursor.execute(szatnie)

    if len(cursor.fetchall()) == 0:
        cursor.close()
        return "Nie ma takiej szatni"
    cursor.close()

    if not ilosc.isdecimal():
        return "Wybrano nieprawidłową ilosc szafek"
    return None

def sprawdz_pomieszczenia(dane):
    pomieszczenie = dane[0]
    pietro = dane[1]
    powierzchnia = dane[2]
    rodzaj = dane[3]

    if pomieszczenie == "":
        return 'Wpisz numer pomieszczenia'
    if pietro == "":
        return 'Wpisz pietro'
    if powierzchnia == "":
        return 'Wpisz powierzchnia'
    if rodzaj == "":
        return 'Wpisz rodzaj'


    if rodzaj.lower() == 'szatnia':
        rodzaj = 'szatnie'
    elif rodzaj.lower() == 'sala':
        rodzaj = 'sale'
    elif rodzaj.lower() == 'recepcja':
        rodzaj = 'recepcje'
    elif rodzaj.lower() == 'kantorek':
        rodzaj = 'kantorki'
    else:
        return 'Wybrano niepoprawny rodzaj pomieszczenia'

    if not pomieszczenie.isdecimal():
        return "Podano zły numer pomieszczenia"
    if len(pomieszczenie) > 3:
        return 'Podano za długi numer pomieszczenia'

    pom = f"""select nr_pomieszczenia from pomieszczenia_perspektywa where nr_pomieszczenia = {pomieszczenie} and adres_silowni = '{variables.wybranaSilownia}' """
    cursor = variables.cnxn.cursor()
    cursor.execute(pom)

    if len(cursor.fetchall()) > 0:
        return "Istnieje pomieszczenie o takim numerze, sprawdź jego poprawność"

    cursor.close()


    if not pietro.isdecimal():
        return "Wybrane piętro nie jest liczbą"

    if int(pietro) > 99:
        return "Podano zbyt wysokie piętro"

    powierzchnia = powierzchnia.replace(",", ".")
    if float(powierzchnia) > 999.99:
        return "Wybrana powierzchnia nie jest liczbą"
    return None

def sprawdz_plan(dane):
    opis = dane[0]
    pesel = dane[1]
    if opis == "":
        return 'Wpisz opis'
    if pesel == "":
        return 'Wpisz pesel'
    if len(opis) > 60:
        return 'Wpisany opis jest za długi'

    if not pesel.isdecimal():
        return "Podałeś zły pesel"
    pesel = int(pesel)

    trener = f"""select pesel from trenerzy where pesel = {pesel} """
    cursor = variables.cnxn.cursor()
    cursor.execute(trener)

    if len(cursor.fetchall()) == 0:
        return "Nie istnieje taki trener"

    cursor.close()

    return None

def sprawdz_grupe(dane):
    termin = dane[0]
    pesel = dane[1]
    sala = dane[2]
    if termin == "":
        return 'Wpisz termin'
    if pesel == "":
        return 'Wpisz pesel'
    if sala == "":
        return 'Wpisz salę'
    if not pesel.isdecimal():
        return "Wpisano niepoprawny pesel"

    if not termin.isdecimal():
        return "Wpisano niepoprawny termin. Wpisz dzień miesiąca - maksymalnie dwie cyfry."
    if int(termin) > 31:
        return "Wpisano niepoprawny dzień."

    trener = f"""select pesel from trenerzy where pesel = {pesel} """
    cursor = variables.cnxn.cursor()
    cursor.execute(trener)

    if len(cursor.fetchall()) == 0:
        return "Nie istnieje taki trener"
    variables.cnxn.commit()
    cursor.close()

    sal = f"""select nr_pomieszczenia from sale_cwiczeniowe where nr_pomieszczenia = {sala} and adres_silowni = '{variables.wybranaSilownia}' """
    cursor = variables.cnxn.cursor()
    cursor.execute(sal)

    if len(cursor.fetchall()) == 0:
        return "Nie istnieje taka sala"

    # unikat = f"""select to_char(termin_spotkania, 'dd') as data, id_grupy, pesel_trenera, nr_sali, adres_silowni from grupy_zorganizowane
    # where pesel_trenera = {pesel} and nr_sali = {sala} and data = '{termin}' and adres_silowni = '{variables.wybranaSilownia}' """
    # cursor.execute(unikat)


    unik = f"""select to_char(termin_spotkania, 'dd'), id_grupy, pesel_trenera, nr_sali, adres_silowni from grupy_zorganizowane
    where pesel_trenera = {pesel} and nr_sali = {sala} and to_char(termin_spotkania, 'dd') = '{termin}' and adres_silowni = '{variables.wybranaSilownia}' 
    """
    cursor.execute(unik)

    if len(cursor.fetchall()) > 0:
        cursor.close()
        return "Istnieje już taka grupa"

    variables.cnxn.commit()
    cursor.close()
    return None

def sprawdz_sprzet(dane):
    sprzet = dane[0] #id_sprzetu
    rodzaj = dane[1]
    stanowisko = dane[2]
    sala = dane[3]

    if sprzet == "":
        return 'Wpisz id sprzętu' #TODO- czy to nie powinno isc z sekwencji???
    if not sprzet.isdecimal():
        return "Podano złe id sprzętu"

    sprzet = int(sprzet)

    sprz = f"""select nr_urzadzenia from sprzety where nr_urzadzenia = {sprzet}  and adres_silowni = '{variables.wybranaSilownia}'  """
    cursor = variables.cnxn.cursor()
    cursor.execute(sprz)

    if len(cursor.fetchall()) > 0:
        return "Istnieje sprzet o takim id, sprawdź jego poprawność"
    # sprawdzenie imienia
    cursor.close()

    if rodzaj == "":
        return 'Wpisz rodzaj sprzętu'
    if stanowisko == "":
        return 'Wpisz stanowisko'
    if not stanowisko.isdecimal():
        return "Wpisano niepoprawne stanowisko"

    if int(stanowisko) > 999999:
        return "Podane stanowisko jest za duże"
    if sala == "":
        return 'Wpisz salę'
    sal = f"""select nr_pomieszczenia from sale_cwiczeniowe where nr_pomieszczenia = {sala} and adres_silowni = '{variables.wybranaSilownia}' """
    cursor = variables.cnxn.cursor()
    cursor.execute(sal)

    if len(cursor.fetchall()) == 0:
        return "Nie istnieje taka sala"


    cursor.close()
    return None

def sprawdz_klubowicz(dane):
    pesel = dane[0]
    nazwisko = dane[1]
    znizka = dane[2]
    od = dane[3]
    do = dane[4]

    if od == "" or do == "":
        return 'Podaj okres trwania ważności karnetu'

    if od[4] != '-' or od[7] != '-' or not od[:4].isdecimal() or not od[5:7].isdecimal() or not od[8:].isdecimal():
        return 'Wprowadzona data jest niepoprawna'

    if do[4] != '-' or do[7] != '-' or not do[:4].isdecimal() or not do[5:7].isdecimal() or not do[8:].isdecimal():
        return 'Wprowadzona data jest niepoprawna'

    if int(od[:4]) > int(do[:4]) or (int(od[:4]) == int(do[:4]) and int(od[5:7]) > int(do[5:7])) or (
            int(od[:4]) == int(do[:4]) and int(od[5:7]) == int(do[5:7]) and int(od[8:]) > int(do[8:])):
        return 'Okres ważności karnetu jest ujemny'

    if pesel == "":
        return 'Wpisz pesel'
    if not pesel.isdecimal():
        return "Wpisano niepoprawny pesel"

    klub = f"""select pesel from klubowicze where pesel = {pesel} """
    cursor = variables.cnxn.cursor()
    cursor.execute(klub)

    if len(cursor.fetchall()) > 0:
        return "Istnieje klubowicz o takim peselu, sprawdź jego poprawność"
    # sprawdzenie imienia
    variables.cnxn.commit()
    cursor.close()

    if nazwisko == "":
        return 'Wpisz nazwisko'

    if not nazwisko.isalpha():
        return "Wpisano niepoprawne nazwisko"

    if znizka.isdecimal():
        if int(znizka) > 100:
            return 'Wybrano za duza znizke'
    elif znizka != "":
        return 'Wybrana znizka musi byc liczbą'
    return None

def sprawdz_wlasciciele(dane):
    pesel = dane[0]
    imie = dane[1]
    nazwisko = dane[2]
    pensja = dane[3]

    pensja = pensja.replace(",", ".")

    if pesel == "":
        return 'Wpisz pesel'
    if not pesel.isdecimal():
        return "Pesel nie składa się z samych liczb"
    pesel = int(dane[0])
    if pesel > 99999999999:
        return "Pesel jest za długi"
    if pesel < 10000000000:
        return "Pesel jest za krótki"

    wlas = f"""select pesel from pracownicy_perspektywa where pesel = {pesel} """
    cursor = variables.cnxn.cursor()
    cursor.execute(wlas)

    if len(cursor.fetchall()) > 0:
        return "Istnieje pracownik o takim peselu, sprawdź jego poprawność"
    cursor.close()
    if imie == "":
        return 'Wpisz imię'
    if not imie.isalpha():
        return "Wpisano niepoprawne imie"

    if nazwisko == "":
        return 'Wpisz nazwisko'
    if not nazwisko.isalpha():
        return "Wpisano niepoprawne nazwisko"

    if pensja == "":
        return "Podaj pensję"


    pensja2 = pensja
    if not pensja2.replace('.', '').isdecimal():
        return "Pensja podana w złym formacie"


    pensja = float(pensja)
    pensja = round(pensja, 2)
    if pensja > 99999.99:
        return "Pensja jest za duża"

    return None


def sprawdz_silownie(dane):
    print(dane, flush=True)
    adres = dane[0]
    nazwa = dane[1]
    pesel =dane[2]

    if adres == "":
        return 'Wpisz adres'
    if nazwa == "":
        return 'Wpisz nazwę'
    if pesel == "":
        return 'Wpisz pesel'

    if not pesel.isdecimal():
        return "Pesel nie składa się z samych liczb"
    pesel = int(pesel)
    if pesel > 99999999999:
        return "Pesel jest za długi"
    if pesel < 10000000000:
        return "Pesel jest za krótki"

    wlas = f"""select * from silownie where pesel_wlasciciela = {pesel} """
    cursor = variables.cnxn.cursor()
    cursor.execute(wlas)

    if len(cursor.fetchall()) > 0:
        return "Właściciel posiada już siłownię"
    cursor.close()


    return None

# def sprawdz_silownie(dane):
#     print(dane, flush=True)
#     adres = dane[0]
#     nazwa = dane[1]
#     pesel =dane[2]
#
#     if adres == "":
#         return 'Wpisz adres'
#     if nazwa == "":
#         return 'Wpisz nazwę'
#     if pesel == "":
#         return 'Wpisz pesel'
#
#     if not pesel.isdecimal():
#         return "Pesel nie składa się z samych liczb"
#     pesel = int(pesel)
#     if pesel > 99999999999:
#         return "Pesel jest za długi"
#     if pesel < 10000000000:
#         return "Pesel jest za krótki"
#
#     wlas = f"""select pesel from wlasciciele where pesel = {pesel} """
#     cursor = variables.cnxn.cursor()
#     cursor.execute(wlas)
#
#     if len(cursor.fetchall()) == 0:
#         return "Nie istnieje wlasciciel o takim peselu"
#     cursor.close()
#
#
#     return None

def check_upd_wlasciciele(dane):
    imie = dane[1]
    nazwisko = dane[2]
    pensja = dane[4]
    premia = dane[5]

    if imie == '':
        return 'Nie wprowadzono imienia'
    if (not imie.isalpha()) or len(imie) > 15:
        return 'Wybrane imie jest niepoprawne'

    if nazwisko == '':
        return 'Nie wprowadzono nazwiska'
    if (not nazwisko.isalpha()) or len(nazwisko) > 15:
        return 'Wybrane nazwisko jest niepoprawne'


    if pensja == "":
        return "Nie wprowadzono pensji"
    pom_pen = pensja
    if not pom_pen.replace('.', '').isdecimal():
        return "Pensja podana w złym formacie"
    pensja = float(pensja)
    pensja = round(pensja, 2)
    if pensja > 99999.99:
        return "Pensja jest za duża"

    if premia == "":
        return "Nie wprowadzono premii"
    pom_prem = premia
    if not pom_prem.replace('.', '').isdecimal():
        return "Premia podana w złym formacie"
    premia = float(premia)
    premia = round(premia, 2)
    if premia > 99999.99:
        return "Premia jest za wysoka"
    return None

def check_upd_silownie(dane):
    nazwa = dane[1]
    if nazwa == '':
        return 'Nie wprowadzono nazwy'
    if len(nazwa) > 30:
        return 'Wprowadzono nazwa siłowni jest za długa'
    s = f"""select * from silownie WHERE pesel_wlasciciela = {dane[2]}"""
    cursor = variables.cnxn.cursor()
    cursor.execute(s)

    if len(cursor.fetchall()) > 0:
        return "Właściciel ma już siłownię"
    cursor.close()
    return None


def check_upd_pracownicy(dane):
    imie = dane[1]
    nazwisko = dane[2]
    pensja = dane[4]
    premia = dane[5]

    if imie == '':
        return 'Nie wprowadzono imienia'
    if (not imie.isalpha()) or len(imie) > 15:
        return 'Wybrane imię jest niepoprawne'

    if nazwisko == '':
        return 'Nie wprowadzono nazwiska'
    if (not nazwisko.isalpha()) or len(nazwisko) > 15:
        return 'Wybrane nazwisko jest niepoprawne'


    if pensja == "":
        return "Nie wprowadzono pensji"
    pom_pen = pensja
    if not pom_pen.replace('.', '').isdecimal():
        return "Pensja podana w złym formacie"
    pensja = float(pensja)
    pensja = round(pensja, 2)
    if pensja > 99999.99:
        return "Pensja jest za duża"

    if premia == "":
        return "Nie wprowadzono premii"
    pom_prem = premia
    if not pom_prem.replace('.', '').isdecimal():
        return "Premia podana w złym formacie"
    premia = float(premia)
    premia = round(premia, 2)
    if premia > 99999.99:
        return "premia jest za duża"

    print("TUTAJ nowy etat", dane[7], flush=True)
    nowy_etat = dane[7]
    numer = dane[6]
    if nowy_etat == "Recepcjonista":
        if int(numer) not in wybierz_recepcje():
            return "To nie jest recepcja"
    elif nowy_etat == "Trener":
        if numer != "Brak":
            return "Trener nie może mieć przypisanego pomieszczenia"
    elif nowy_etat == "Sprzątacz":
        if int(numer) not in wybierz_kantorki():
            return "To nie jest kantorek"
    return None

def chk_podwyzka(dane):
    podwyzka = dane[0]

    print(podwyzka)

    if not podwyzka.isdecimal():
        return "Wprowadzona podwyżka jest niepoprawna"

    if int(podwyzka) > 100:
        return "Wprowadzono za dużą podwyżkę"

    return None
def check_upd_klubowicze(dane):
    nazwisko = dane[1]
    od = dane[3]
    do = dane[4]
    znizka = dane[5]

    if nazwisko == '':
        return 'Nie wprowadzono nazwiska'

    if not nazwisko.isalpha():
        return 'Wybrane nazwisko jest niepoprawne'

    if znizka == '':
        return 'Nie wprowadzono zniżki'

    if not znizka.isdecimal():
        return 'wprowadzona znizka jest niepoprawna'
    znizka = int(znizka)
    if znizka > 100:
        return 'wprowadzona znizka jest zbyt wysoka'


    if od[4] != '-' or od[7] != '-' or not od[:4].isdecimal() or not od[5:7].isdecimal() or not od[8:].isdecimal():
        return 'Wprowadzona data jest niepoprawna'

    if int(od[:4]) > int(do[:4]) or (int(od[:4]) == int(do[:4]) and int(od[5:7]) > int(do[5:7])) or(int(od[:4]) == int(do[:4]) and int(od[5:7]) == int(do[5:7]) and int(od[8:]) > int(do[8:])):
        return 'Okres ważności karnetu jest ujemny'
    return None

def check_upd_sprzety(dane):
    rodzaj = dane[1]
    stanowisko = dane[2]

    if rodzaj == '':
        return 'Nie wprowadzono rodzaju sprzętu'

    if len(rodzaj) > 30:
        return 'Rodzaj sprzętu jest zbyt długi'

    if stanowisko == '':
        return 'Nie wprowadzono numeru stanowiska'

    if int(stanowisko) > 999999:
        return 'Wprowadzony numer stanowiska jest zbyt duży'

    if not stanowisko.isdecimal():
        return 'Wprowadzono niepoprawny numer stanowiska'

    return None

def check_upd_pomieszczenia(dane):
    pietro = dane[1]
    powierzchnia = dane[2]

    if pietro == '':
        return 'Nie wprowadzono piętra'

    if not pietro.isdecimal():
        return 'Wprowadzone piętro jest niepoprawne'

    if int(pietro) > 99:
        return 'Wprowadzono zbyt wysokie piętro'

    if powierzchnia == '':
        return 'Nie wprowadzono powierzchni'

    powierzchnia2 = powierzchnia.replace(".", "")
    if not powierzchnia2.isdecimal():
        return "wprowadzono powierzchnia nie jest liczbą"

    powierzchnia = float(powierzchnia)
    powierzchnia = round(powierzchnia,2)
    if powierzchnia > 999.99:
        return 'Wprowadzono za dużą powierzchnię'
    return None

def check_upd_plany(dane):
    opis = dane[1]

    if opis == '':
        return 'Nie wprowadzono opisu'

    if len(opis) > 60:
        return 'Wprowadzony opis jest za długi'
    return None

def check_upd_grupy(dane):
    termin = dane[1]

    if termin == '':
        return 'Nie wprowadzono terminu spotkania'
    if not termin.isdecimal():
        return 'Wprowadzono niepoprawny termin'
    if int(termin) > 31 or int(termin) < 1:
        return 'Wprowadzono niepoprawny termin'
    return None