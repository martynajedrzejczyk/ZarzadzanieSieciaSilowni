import cx_Oracle
import variables
import datetime
global cnxn
from update_data import czysc_po_trenerze

def usun_pracownicy(klucz):
    table = f"""select etat from pracownicy_perspektywa where pesel = {klucz} """
    cursor = variables.cnxn.cursor()
    cursor.execute(table)
    table = cursor.fetchmany(1)[0][0]
    if table == 'Recepcjonista':
        table = 'Recepcjonisci'
    elif table == 'Sprzątacz':
        table = 'Sprzatacze'
    elif table == 'Trener':
        table = 'Trenerzy'
        czysc_po_trenerze(klucz)

    zap = f""" delete from {table} where pesel = {klucz} """
    cursor.execute(zap)
    variables.cnxn.commit()
    cursor.close()

def usun_sprzety(klucz1, klucz2):
    delete = f""" delete from sprzety where nr_urzadzenia = {klucz1} and nr_sali = {klucz2} and adres_silowni = '{variables.wybranaSilownia}'"""
    cursor = variables.cnxn.cursor()
    cursor.execute(delete)
    variables.cnxn.commit()
    cursor.close()

def sprawdz_czy_pracownicy(nr, typ): # uzywamy przed usun_pomieszczenie aby sprawdzic czy w recepcji nie ma recepcjonisty oraz w kantorku analogicznie
    if typ == 'Kantorek':
        prac = f"""select pesel from sprzatacze where nr_kantorka = {nr} and adres_silowni = '{variables.wybranaSilownia}' """
        cursor = variables.cnxn.cursor()
        cursor.execute(prac)
        if len(cursor.fetchall()) > 0:
            return "Znaleziono sprzątaczy korzystających z tego kantorka! Usuń ich lub przypisz ich do innego kantorka, aby usunąć to pomieszczenie."
    elif typ == 'Recepcja':
        prac = f"""select pesel from recepcjonisci where nr_recepcji = {nr} and adres_silowni = '{variables.wybranaSilownia}' """
        cursor = variables.cnxn.cursor()
        cursor.execute(prac)
        if len(cursor.fetchall()) > 0:
            return "Znaleziono recepcjonistów korzystających z tej recepcji! Usuń ich lub przypisz ich do innej recepcji, aby usunąć to pomieszczenie."
    elif typ == 'Szatnia':
        sza = f"""select nr_szafki from szafki where nr_szatni = {nr} and adres_silowni = '{variables.wybranaSilownia}'"""
        cursor = variables.cnxn.cursor()
        cursor.execute(sza)
        s = []
        for i in cursor.fetchall():
            s.append(i[0])
        if len(s) > 0:
            return "Aby usunąć tą szatnię, usuń lub przenieś najpierw wszystkie szafki w niej stojące."
    elif typ == 'Sala ćwiczeniowa':
        sprzety = []
        cursor = variables.cnxn.cursor()
        grupy = []
        przynaleznosci = []
        sprz = f"""select nr_urzadzenia from sprzety where nr_sali = {nr} and adres_silowni = '{variables.wybranaSilownia}' """
        gru = f"""select id_grupy from grupy_zorganizowane where nr_sali = {nr} and adres_silowni = '{variables.wybranaSilownia}' """
        cursor.execute(sprz)
        s = []
        for i in cursor.fetchall():
            s.append(i[0])
        if len(s) > 0:
            return "Znaleziono sprzęty stojące w tej sali. Przenieś je lub usuń, aby usunąć to pomieszczenie."
        cursor.execute(gru)
        g = []
        for i in cursor.fetchall():
            g.append(i[0])
        if len(g) > 0:
            return "Znaleziono grupy ćwiczące w tej sali. Przenieś je lub usuń, aby usunąć to pomieszczenie."
        return None
    return None

def usun_pomieszczenia(nr, typ):
    if typ == "Recepcja":
        typ = "recepcje"
    elif typ == "Szatnia": #ok
        typ = "szatnie"
    elif typ == "Kantorek":
        typ = "kantorki"
    elif typ == "Sala ćwiczeniowa": #ok
        typ = "sale_cwiczeniowe"

    zap = f""" delete from {typ} where nr_pomieszczenia = {nr} """
    cursor = variables.cnxn.cursor()
    cursor.execute(zap)
    variables.cnxn.commit()
    cursor.close()


def usun_plany(klucz):
    dcwicza = f""" delete from cwicza_z_planem where nr_planu = {klucz} """
    dplany = f""" delete from plany_treningowe where nr_planu = {klucz} """
    cursor = variables.cnxn.cursor()
    cursor.execute(dcwicza)
    cursor.execute(dplany)
    variables.cnxn.commit()
    cursor.close()

def usun_grupy(klucz):
    dgrupy = f""" delete from grupy_zorganizowane where id_grupy = {klucz} and adres_silowni = '{variables.wybranaSilownia}'"""
    dprzynaleznosci = f""" delete from przynaleznosci_klubowiczow_do_grup where id_grupy = {klucz} """
    cursor = variables.cnxn.cursor()
    cursor.execute(dprzynaleznosci)
    cursor.execute(dgrupy)
    variables.cnxn.commit()
    cursor.close()

def usun_szafki(klucz1, klucz2):
    delete = f""" delete from szafki where nr_szafki = {klucz1} and nr_szatni = {klucz2} and adres_silowni = '{variables.wybranaSilownia}'"""
    cursor = variables.cnxn.cursor()
    cursor.execute(delete)
    variables.cnxn.commit()
    cursor.close()

def usun_klubowicze(key):
    cursor = variables.cnxn.cursor()
    karty = f""" delete from karnety where pesel_klubowicza = {key} """
    delete = f""" delete from klubowicze where pesel = {key} """
    cursor.execute(karty)
    cursor.execute(delete)
    variables.cnxn.commit()
    cursor.close()

def usun_wlasciciele(key):
    cursor = variables.cnxn.cursor()
    delete = f""" delete from wlasciciele where pesel = {key} """
    cursor.execute(delete)
    variables.cnxn.commit()
    cursor.close()

def sprawdz_czy_wlasciciel(key):
    silownie = f"""select adres from silownie where pesel_wlasciciela = {key}"""
    cursor = variables.cnxn.cursor()
    cursor.execute(silownie)
    s = []
    for i in cursor.fetchall():
        s.append(i[0])
    cursor.close()
    if len(s) > 0:
        return "Znaleziono siłownie należące do tej osoby. Zmień ich własciciela, aby usunąć tą osobę z bazy danych."
    return None


def usun_klubowicza_z_planu(nr, pesel):
    delete = f"""delete from cwicza_z_planem where nr_planu = {nr} and pesel_klubowicza={pesel}"""
    cursor = variables.cnxn.cursor()
    cursor.execute(delete)
    cursor.close()

def usun_klubowicza_z_grupy(id_grupy, pesel):
    delete = f"""delete from przynaleznosci_klubowiczow_do_grup where id_grupy = {id_grupy} and pesel_klubowicza={pesel}"""
    cursor = variables.cnxn.cursor()
    cursor.execute(delete)
    cursor.close()

def usun_wszystkich_klubowiczow_z_grupy(id_grupy):
    delete = f"""delete from przynaleznosci_klubowiczow_do_grup where id_grupy = {id_grupy}"""
    cursor = variables.cnxn.cursor()
    cursor.execute(delete)
    cursor.close()


def usun_silownie(key):
    cursor = variables.cnxn.cursor()

    grupy = f"""select id_grupy from grupy_zorganizowane where adres_silowni = '{key}'"""
    cursor.execute(grupy)

    for i in cursor.fetchall():
        id = i[0]
        usun_wszystkich_klubowiczow_z_grupy(id)
        usun_grupy(id)
    grupy = f"""delete from grupy_zorganizowane where adres_silowni = '{key}'"""
    cursor.execute(grupy)


    sale = f"""select nr_pomieszczenia from sale_cwiczeniowe where adres_silowni = '{key}'"""
    cursor.execute(sale)
    for i in cursor.fetchall():
        nr = i[0]
        sprzety = f""" delete from sprzety where nr_sali = {nr} and adres_silowni = '{key}'"""
        cursor.execute(sprzety)

    szatnie = f"""select nr_pomieszczenia from szatnie where adres_silowni = '{key}'"""
    cursor.execute(szatnie)
    for i in cursor.fetchall():
        nr = i[0]
        szafki = f""" delete from szafki where nr_szatni = {nr} and adres_silowni = '{key}'"""
        cursor.execute(szafki)

    trenerzy = f"""select pesel from trenerzy where adres_silowni = '{key}'"""
    cursor.execute(trenerzy)
    for i in cursor.fetchall():
        klucz = i[0]
        # dcwicza = f""" delete from cwicza_z_planem where pesel_trenera = {klucz} """

        pl=f"""select nr_planu from plany_treningowe where pesel_trenera = {klucz}"""
        cursor2 = variables.cnxn.cursor()
        cursor3 = variables.cnxn.cursor()
        cursor2.execute(pl)
        for i in cursor2.fetchall():
            d = f"""delete from cwicza_z_planem where nr_planu = {i[0]}"""
            cursor3.execute(d)
        dplany = f""" delete from plany_treningowe where pesel_trenera  = {klucz} """
        # cursor.execute(dcwicza)
        cursor.execute(dplany)

    trenerzy = f"""delete from trenerzy where adres_silowni = '{key}'"""
    sp = f"""delete from sprzatacze where adres_silowni = '{key}'"""
    rec = f"""delete from recepcjonisci where adres_silowni = '{key}'"""
    cursor.execute(trenerzy)
    cursor.execute(sp)
    cursor.execute(rec)

    kantorki = f"""delete from kantorki where adres_silowni = '{key}'"""
    rec = f"""delete from recepcje where adres_silowni = '{key}'"""
    sa = f"""delete from sale_cwiczeniowe where adres_silowni = '{key}'"""
    sza = f"""delete from szatnie where adres_silowni = '{key}'"""
    cursor.execute(kantorki)
    cursor.execute(rec)
    cursor.execute(sa)
    cursor.execute(sza)

    delete = f""" delete from silownie where adres = '{key}' """
    cursor.execute(delete)
    variables.cnxn.commit()
    cursor.close()
