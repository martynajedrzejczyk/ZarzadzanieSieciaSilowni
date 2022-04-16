import cx_Oracle
import variables
import datetime


def dodaj_klubowicz_grupa(pesel, id):
    insert = f"""insert into przynaleznosci_klubowiczow_do_grup values 
        ( {id}, {pesel}) """
    print(insert)
    cursor = variables.cnxn.cursor()
    cursor.execute(insert)
    cursor.close()
    variables.cnxn.commit()

def dodaj_klubowicz_plan(pesel, nr):
    insert = f"""insert into cwicza_z_planem values 
        ( {pesel}, {nr}) """
    print(insert)
    cursor = variables.cnxn.cursor()
    cursor.execute(insert)
    cursor.close()
    variables.cnxn.commit()


def dodaj_szafki(dane):
    ilosc = int(dane[0])
    pomieszczenie = int(dane[1])

    cursor = variables.cnxn.cursor()
    cursor.callproc('silowniapackage.dodajszafki', [ilosc, pomieszczenie, variables.wybranaSilownia])
    cursor.close()
    variables.cnxn.commit()

def dodaj_sprzet(dane):
    sprzet = int(dane[0])  # id_sprzetu
    rodzaj = dane[1]
    stanowisko = int(dane[2])
    sala = int(dane[3])

    insert = f"""insert into sprzety values ({sprzet}, '{rodzaj}', {stanowisko}, {sala}, '{variables.wybranaSilownia}' ) """
    cursor = variables.cnxn.cursor()
    cursor.execute(insert)
    cursor.close()
    variables.cnxn.commit()


def dodaj_grupe(dane):
    termin = dane[0]
    pesel = int(dane[1])
    sala = int(dane[2])

    insert = f"""insert into grupy_zorganizowane (termin_spotkania, pesel_trenera, nr_sali, adres_silowni) values 
    (to_date('{termin}', 'dd'), {pesel}, {sala}, '{variables.wybranaSilownia}') """
    print(insert)
    cursor = variables.cnxn.cursor()
    cursor.execute(insert)
    cursor.close()
    variables.cnxn.commit()

def dodaj_plany(dane):
    opis = dane[0]
    pesel = int(dane[1])

    insert = f"""insert into plany_treningowe (opis, pesel_trenera) values ('{opis}', {pesel} )"""
    cursor = variables.cnxn.cursor()
    cursor.execute(insert)
    cursor.close()
    variables.cnxn.commit()

def dodaj_pomieszczenia(dane):
    pomieszczenie = int(dane[0])
    pietro = int(dane[1])
    powierzchnia = dane[2]
    rodzaj = dane[3]

    if rodzaj.lower() == 'szatnia':
        rodzaj = 'szatnie'
    elif rodzaj.lower() == 'sala':
        rodzaj = 'sale_cwiczeniowe'
    elif rodzaj.lower() == 'recepcja':
        rodzaj = 'recepcje'
    elif rodzaj.lower() == 'kantorek':
        rodzaj = 'kantorki'

    powierzchnia = powierzchnia.replace(",", ".")
    powierzchnia = float(powierzchnia)

    insert = f"""insert into {rodzaj} values ({pomieszczenie}, {pietro}, {powierzchnia}, '{variables.wybranaSilownia}') """
    cursor = variables.cnxn.cursor()
    cursor.execute(insert)
    cursor.close()
    variables.cnxn.commit()

def dodaj_pracownicy(dane):
    pesel = dane[0]
    imie = dane[1]
    nazwisko = dane[2]

    pensja = dane[3].replace(",", ".")
    pensja = float(pensja)
    etat = dane[4]
    tab = ""
    if etat == "Sprzątacz":
        #nr kantorka
        select = f"""select nr_pomieszczenia from kantorki order by 1 desc"""
        cursor = variables.cnxn.cursor()
        cursor.execute(select)
        for item in cursor:
            kantorek = item[0]
        insert = f"""insert into sprzatacze (pesel, imie, nazwisko, pensja, nr_kantorka, adres_silowni, adres_silowni_s) 
        values ( {pesel}, '{imie}', '{nazwisko}', {pensja}, {kantorek}, '{variables.wybranaSilownia}', '{variables.wybranaSilownia}'  ) """
        cursor.execute(insert)
        cursor.close()
        variables.cnxn.commit()

    elif etat == "Trener":
        insert = f"""insert into trenerzy (pesel, imie, nazwisko, pensja, adres_silowni) 
                values ( {pesel}, '{imie}', '{nazwisko}', {pensja}, '{variables.wybranaSilownia}') """
        cursor = variables.cnxn.cursor()
        cursor.execute(insert)
        cursor.close()
        variables.cnxn.commit()

    elif etat == "Recepcjonista":
        # nr recpcji
        select = f"""select nr_pomieszczenia from recepcje order by 1 desc"""
        cursor = variables.cnxn.cursor()
        cursor.execute(select)
        for item in cursor:
            kantorek = item[0]
        insert = f"""insert into recepcjonisci (pesel, imie, nazwisko, pensja, nr_recepcji, adres_silowni, adres_silowni_zatrudniony) 
                values ( {pesel}, '{imie}', '{nazwisko}', {pensja}, {kantorek}, '{variables.wybranaSilownia}', '{variables.wybranaSilownia}' ) """
        print(insert)
        cursor.execute(insert)
        cursor.close()
        variables.cnxn.commit()


def dodaj_klubowicze(dane):
    insert = f"""insert into klubowicze (pesel, nazwisko) values ({int(dane[0])}, '{dane[1]}') """
    cursor = variables.cnxn.cursor()
    cursor.execute(insert)

    if dane[2] == "":
        dane[2] = None
    else:
        dane[2] = int(dane[2])

    insert = f"""insert into karnety (wazna_od, wazna_do, znizka, pesel_klubowicza) values 
    (to_date('{dane[3]}', 'yyyy-mm-dd'), to_date('{dane[4]}', 'yyyy-mm-dd'), {int(dane[2])}, {int(dane[0])}) """

    print(insert)

    cursor.execute(insert)

    update = f"""update klubowicze set nr_karty = (
        select nr_karty from karnety where pesel_klubowicza = {int(dane[0])}
    ) where pesel = {dane[0]} """

    cursor.execute(update)
    #TODO -  czy tu nie powinno byc commita??
    print("wstawilismy pracownika", flush=True)

#napisac dodac karnet i zupdatetowac klubowiczow i wpisac im ten nr_karty #TODO

def dodaj_wlasciciela(dane):

    dane[3] = dane[3].replace(",", ".")

    insert = f"""insert into wlasciciele(pesel, imie, nazwisko, pensja) values ({int(dane[0])}, '{dane[1]}','{dane[2]}',{float(dane[3])}) """
    cursor = variables.cnxn.cursor()
    cursor.execute(insert)

    cursor.close()
    variables.cnxn.commit()

    print("wstawilismy właściciela", flush=True)

def dodaj_silownie(dane):

    insert = f"""insert into silownie(adres, nazwa, pesel_wlasciciela) values ('{(dane[0])}', '{dane[1]}',{int(dane[2])}) """
    cursor = variables.cnxn.cursor()
    cursor.execute(insert)
    print(insert)
    cursor.close()
    variables.cnxn.commit()

    print("wstawilismy właściciela", flush=True)