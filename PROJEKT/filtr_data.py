global cnxn
import variables

def filtruj_pracownicy(filtr, wyrazenie):
    rows = []
    if filtr.lower() == 'etat':
        if wyrazenie.lower() not in ['sprzątacz','recepcjonista', 'trener']:
            return None
        elif wyrazenie.lower() == 'sprzątacz':
            sprzatacz = f"""select * from sprzatacze  WHERE adres_silowni = '{variables.wybranaSilownia}'"""
            cursor = variables.cnxn.cursor()
            cursor.execute(sprzatacz)
            for item in cursor:
                item1 = item[0:-2]
                item1 += ('Sprzatacz',)
                rows.append(item1)
            cursor.close()
            return rows
        elif wyrazenie.lower() == 'recepcjonista':
            recepcjonista = f"""select * from recepcjonisci  WHERE adres_silowni = '{variables.wybranaSilownia}'"""
            cursor = variables.cnxn.cursor()
            cursor.execute(recepcjonista)
            for item in cursor:
                item1 = item[0:-2]
                item1 += ('Recepcjonista',)
                rows.append(item1)
            cursor.close()
            return rows
        elif wyrazenie.lower() == 'trener':
            trener = f"""select * from trenerzy  WHERE adres_silowni = '{variables.wybranaSilownia}'"""
            cursor = variables.cnxn.cursor()
            cursor.execute(trener)
            for item in cursor:
                item1 = item[0:-1]
                item1 += ('None', 'Trener',)
                rows.append(item1)
            cursor.close()
            return rows

    elif filtr == "NAZWISKO":
        if not wyrazenie.isalpha():
            return None
        wybrane = f"""select * from pracownicy_perspektywa WHERE {filtr} = '{wyrazenie}'  AND adres_silowni = '{variables.wybranaSilownia}'"""

    elif filtr == "IMIĘ":
        if not wyrazenie.isalpha():
            return None
        wybrane = f"""select * from pracownicy_perspektywa WHERE imie = '{wyrazenie}' AND adres_silowni = '{variables.wybranaSilownia}'"""

    elif filtr == "DATA":
        if len(wyrazenie) != 10:
            return None
        if wyrazenie[2] != '-' or wyrazenie[5] != '-' or not wyrazenie[:2].isdecimal() or not wyrazenie[3:5].isdecimal() or not wyrazenie[6:].isdecimal():
            return None

        wybrane = f"""select * from pracownicy_perspektywa WHERE to_char(data_zatrudnienia, 'dd-mm-yyyy') = to_char('{wyrazenie}') and etat != 'Wlasciciel' AND adres_silowni = '{variables.wybranaSilownia}'"""

    else:
        if not wyrazenie.isdecimal():
            return None
        if filtr == "NUMER":
            filtr = "nr_pomieszczenia"
        wybrane = f"""select * from pracownicy_perspektywa WHERE {filtr} = {int(wyrazenie)}  and etat != 'Wlasciciel' AND adres_silowni = '{variables.wybranaSilownia}'"""
    cursor = variables.cnxn.cursor()
    rows = []
    cursor.execute(wybrane)
    for item in cursor:
        etat = f"""select etat from pracownicy_perspektywa where pesel = {item[0]} and etat != 'Wlasciciel' AND adres_silowni = '{variables.wybranaSilownia}' """
        cursor2 = variables.cnxn.cursor()
        cursor2.execute(etat)
        etat = cursor2.fetchone()[0]
        cursor2.close()

        print(item[3])
        tmp = str(item[3])[0:-9]
        year = tmp[:4]
        m = tmp[5:7]
        tmp = tmp[8:]
        tmp += '-'
        tmp += m
        tmp += '-'
        tmp += year
        # print(tmp)
        # item[3] = tmp
        lst = list(item)
        lst[3] = tmp
        item = tuple(lst)

        if etat == 'Trener':
            item1 = item[0:-2]
            item1 += ('Trener',)
        elif etat == 'Sprzątacz':
            item1 = item[0:-2]
            item1 += ('Sprzątacz',)
        else:
            item1 = item[0:-2]
            item1 += ('Recepcjonista',)
        rows.append(item1)
    if rows == []:
        return None # TODO  mozna zmienic do fitrowania zwracajacego puste rekordy
    cursor.close()
    return rows


def filtruj_klubowicz(filtr, wyrazenie):
    rows = []
    wybrane = ""
    print("filtr ", filtr)
    if filtr == "PESEL" or filtr == 'ZNIŻKA':
        if not wyrazenie.isdecimal():
            return None
        if filtr == 'ZNIŻKA':
            wybrane = f"""select pesel, nazwisko, klubowicze.nr_karty,  to_char(wazna_od, 'yyyy-mm-dd'), to_char(wazna_do, 'yyyy-mm-dd'), znizka from klubowicze join 
        karnety on klubowicze.nr_karty = karnety.nr_karty where coalesce(ZNIZKA, 0) = {wyrazenie}"""
        else:
            wybrane = f"""select pesel, nazwisko, klubowicze.nr_karty,  to_char(wazna_od, 'yyyy-mm-dd'), to_char(wazna_do, 'yyyy-mm-dd'), znizka from klubowicze join 
        karnety on klubowicze.nr_karty = karnety.nr_karty where {filtr} = {wyrazenie}"""
    elif filtr == "NUMER":
        if not wyrazenie.isdecimal():
            return None
        wybrane = f"""select pesel, nazwisko, klubowicze.nr_karty,  to_char(wazna_od, 'yyyy-mm-dd'), to_char(wazna_do, 'yyyy-mm-dd'), znizka from klubowicze join karnety on klubowicze.nr_karty = karnety.nr_karty WHERE klubowicze.nr_karty = {wyrazenie}"""
    elif filtr == "WAŻNA_OD":
        if len(wyrazenie) != 10:
            return None
        # if wyrazenie[4] != '-' or wyrazenie[7] != '-' or not wyrazenie[:4].isdecimal() or not wyrazenie[5:7].isdecimal() or not wyrazenie[8:].isdecimal():
        #     return None
        wyrazenie = wyrazenie.replace('-', '.')
        if wyrazenie[2] != '.' or wyrazenie[5] != '.' or not wyrazenie[:2].isdecimal() or not wyrazenie[
                                                                                              3:5].isdecimal() or not wyrazenie[
                                                                                                                      6:].isdecimal():
            return None
        wybrane = f"""select pesel, nazwisko, klubowicze.nr_karty,  to_char(wazna_od, 'yyyy-mm-dd'), to_char(wazna_do, 'yyyy-mm-dd'), znizka from klubowicze join karnety on klubowicze.nr_karty = karnety.nr_karty 
                WHERE to_char(wazna_od, 'dd.mm.yyyy') = to_char('{wyrazenie}') """
    elif filtr == "WAŻNA_DO":
        if len(wyrazenie) != 10:
            return None
        # if wyrazenie[4] != '-' or wyrazenie[7] != '-' or not wyrazenie[:4].isdecimal() or not wyrazenie[5:7].isdecimal() or not wyrazenie[8:].isdecimal():
        #     return None
        wyrazenie = wyrazenie.replace('-', '.')
        if wyrazenie[2] != '.' or wyrazenie[5] != '.' or not wyrazenie[:2].isdecimal() or not wyrazenie[
                                                                                              3:5].isdecimal() or not wyrazenie[
                                                                                                                      6:].isdecimal():
            return None
        wybrane = f"""select pesel, nazwisko, klubowicze.nr_karty,  to_char(wazna_od, 'yyyy-mm-dd'), to_char(wazna_do, 'yyyy-mm-dd'), znizka from klubowicze join karnety on klubowicze.nr_karty = karnety.nr_karty 
            WHERE to_char(wazna_do, 'dd.mm.yyyy') = to_char('{wyrazenie}') """
    else:
        if not wyrazenie.isalpha():
            return None
        wybrane = f"""select pesel, nazwisko, klubowicze.nr_karty,  to_char(wazna_od, 'yyyy-mm-dd'), to_char(wazna_do, 'yyyy-mm-dd'), znizka from klubowicze join 
        karnety on klubowicze.nr_karty = karnety.nr_karty where {filtr} = '{wyrazenie}' """

    cursor = variables.cnxn.cursor()
    print("wybrane:", wybrane)
    cursor.execute(wybrane)
    for item in cursor:

        print(item[3])
        tmp = str(item[3])#[0:-9]
        year = tmp[:4]
        m = tmp[5:7]
        tmp = tmp[8:]
        tmp += '-'
        tmp += m
        tmp += '-'
        tmp += year
        # print(tmp)
        # item[3] = tmp
        lst = list(item)
        lst[3] = tmp
        item = tuple(lst)

        tmp = str(item[4])  # [0:-9]
        year = tmp[:4]
        m = tmp[5:7]
        tmp = tmp[8:]
        tmp += '-'
        tmp += m
        tmp += '-'
        tmp += year
        # print(tmp)
        # item[3] = tmp
        lst = list(item)
        lst[4] = tmp
        item = tuple(lst)

        if item[5] == None:
            lst = list(item)
            lst[5] = 0
            item = tuple(lst)
        rows.append(item)
    cursor.close()
    if rows == []:
        return None
    return rows

def filtruj_pomieszczenia(filtr, wyrazenie):
    rows = []
    if filtr.lower() == 'typ':
        if not wyrazenie.isalpha():
            return None
        if wyrazenie.lower() == 'sala ćwiczeniowa':
            sala = f"""select * from sale_cwiczeniowe where adres_silowni = '{variables.wybranaSilownia}'"""
            cursor = variables.cnxn.cursor()
            cursor.execute(sala)
            for item in cursor:
                item1 = item[0:-1]
                item2 = item1 + ('Sala ćwiczeniowa',)
                rows.append(item2)
            cursor.close()
            if rows == []:
                return None
            return rows
        elif wyrazenie.lower() == 'recepcja':
            recepcja = f"""select * from recepcje where adres_silowni = '{variables.wybranaSilownia}'"""
            cursor = variables.cnxn.cursor()
            cursor.execute(recepcja)
            for item in cursor:
                item1 = item[0:-1]
                item2 = item1 + ('Recepcja',)
                rows.append(item2)
            cursor.close()
            if rows == []:
                return None
            return rows
        elif wyrazenie.lower() == 'szatnia':
            szatnia = f"""select * from szatnie where adres_silowni = '{variables.wybranaSilownia}'"""
            cursor = variables.cnxn.cursor()
            cursor.execute(szatnia)
            for item in cursor:
                item1 = item[0:-1]
                item2 = item1 + ('Szatnia',)
                rows.append(item2)
            cursor.close()
            if rows == []:
                return None
            return rows
        elif wyrazenie.lower() == 'kantorek':
            kantorek = f"""select * from kantorki where adres_silowni = '{variables.wybranaSilownia}'"""
            cursor = variables.cnxn.cursor()
            cursor.execute(kantorek)
            for item in cursor:
                item1 = item[0:-1]
                item2 = item1 + ('Kantorek',)
                rows.append(item2)
            cursor.close()
            if rows == []:
                return None
            return rows

    else:
        if not wyrazenie.isdecimal():
            return None
        if filtr == 'NUMER':
            filtr = 'nr_pomieszczenia'
        if filtr == 'PIĘTRO':
            filtr = "pietro"
        wybrane = f"""select * from pomieszczenia_perspektywa WHERE {filtr} = {wyrazenie} AND adres_silowni = '{variables.wybranaSilownia}'"""
        cursor = variables.cnxn.cursor()
        cursor.execute(wybrane)
        for item in cursor:
            typ = item[-1]
            item1 = item[0:-2]
            item2 = item1 + (typ,)
            rows.append(item2)
        cursor.close()
        if rows == []:
            return None
        return rows
    # return []

def filtruj_plany(filtr, wyrazenie):
    rows = []
    if filtr == "NUMER":
        if not wyrazenie.isdecimal():
            return None
        filtr = 'nr_planu'
        wybrane = f"""select nr_planu, opis, imie, nazwisko from plany_treningowe inner join trenerzy on pesel_trenera = pesel 
        WHERE {filtr} = {wyrazenie} AND adres_silowni = '{variables.wybranaSilownia}'"""
    elif filtr == "OPIS":
        if not wyrazenie.isalpha():
            return None
        wybrane = f"""select nr_planu, opis, imie, nazwisko from plany_treningowe inner join trenerzy on pesel_trenera = pesel 
        WHERE opis = '{wyrazenie}' AND adres_silowni = '{variables.wybranaSilownia}'"""
    elif filtr == "IMIĘ":
        if not wyrazenie.isalpha():
            return None
        wybrane = f"""select nr_planu, opis, imie, nazwisko from plany_treningowe inner join trenerzy on pesel_trenera = pesel 
        where imie = '{wyrazenie}' AND adres_silowni = '{variables.wybranaSilownia}'"""
    elif filtr == "NAZWISKO":
        if not wyrazenie.isalpha():
            return None
        wybrane = f"""select nr_planu, opis, imie, nazwisko from plany_treningowe inner join trenerzy on pesel_trenera = pesel 
        where nazwisko = '{wyrazenie}' AND adres_silowni = '{variables.wybranaSilownia}'"""
    cursor = variables.cnxn.cursor()
    cursor.execute(wybrane)
    for item in cursor:
        rows.append(item)
    cursor.close()
    if rows == []:
        return None
    return rows

def filtruj_grupy(filtr, wyrazenie):
    rows = []
    if filtr == "ID":
        if not wyrazenie.isdecimal():
            return None
        wybrane = f"""select g.ID_GRUPY,to_date(g.TERMIN_SPOTKANIA, 'dd-mm-yyyy'),	trenerzy.imie as IMIĘ_TRENERA, trenerzy.nazwisko as NAZWISKO_TRENERA,
    g.NR_SALI from grupy_zorganizowane g inner join trenerzy on trenerzy.pesel = g.pesel_trenera
    where g.adres_silowni = '{variables.wybranaSilownia}' and id_grupy = {wyrazenie} order by 1 """
    elif filtr == "TERMIN":
        if len(wyrazenie) >2:
            return None
        if not wyrazenie.isdecimal():
            return None
        wybrane = f"""select g.ID_GRUPY,to_date(g.TERMIN_SPOTKANIA, 'dd-mm-yyyy'),	trenerzy.imie as IMIĘ_TRENERA, trenerzy.nazwisko as NAZWISKO_TRENERA,
            g.NR_SALI from grupy_zorganizowane g inner join trenerzy on trenerzy.pesel = g.pesel_trenera
            where g.adres_silowni = '{variables.wybranaSilownia}' and to_char(termin_spotkania, 'dd') = to_char('{wyrazenie}')  order by 1 """
    elif filtr == "IMIĘ":
        if not wyrazenie.isalpha():
            return None
        wybrane = f"""select g.ID_GRUPY,to_date(g.TERMIN_SPOTKANIA, 'dd-mm-yyyy'),	trenerzy.imie as IMIĘ_TRENERA, trenerzy.nazwisko as NAZWISKO_TRENERA,
                   g.NR_SALI from grupy_zorganizowane g inner join trenerzy on trenerzy.pesel = g.pesel_trenera
                   where g.adres_silowni = '{variables.wybranaSilownia}' and imie = '{wyrazenie}'  order by 1 """
    elif filtr == 'NAZWISKO':
        if not wyrazenie.isalpha():
            return None
        wybrane = f"""select g.ID_GRUPY,to_date(g.TERMIN_SPOTKANIA, 'dd-mm-yyyy'),	trenerzy.imie as IMIĘ_TRENERA, trenerzy.nazwisko as NAZWISKO_TRENERA,
                           g.NR_SALI from grupy_zorganizowane g inner join trenerzy on trenerzy.pesel = g.pesel_trenera
                           where g.adres_silowni = '{variables.wybranaSilownia}' and nazwisko = '{wyrazenie}'  order by 1 """
    elif filtr == 'NUMER':
        if not wyrazenie.isdecimal():
            return None
        wybrane = f"""select g.ID_GRUPY,to_date(g.TERMIN_SPOTKANIA, 'dd-mm-yyyy'),	trenerzy.imie as IMIĘ_TRENERA, trenerzy.nazwisko as NAZWISKO_TRENERA,
                           g.NR_SALI from grupy_zorganizowane g inner join trenerzy on trenerzy.pesel = g.pesel_trenera
                           where g.adres_silowni = '{variables.wybranaSilownia}' and nr_sali = {wyrazenie}  order by 1 """
    cursor = variables.cnxn.cursor()
    cursor.execute(wybrane)
    for item in cursor:
        rows.append(item)
    cursor.close()
    if rows == []:
        return None
    return rows

def filtruj_sprzety(filtr, wyrazenie):
    if filtr == "NR_URZADZENIA":
        if not wyrazenie.isdecimal():
            return None
        wybrane = f""" SELECT * FROM sprzety where nr_urzadzenia = {wyrazenie} and adres_silowni = '{variables.wybranaSilownia}' order by 1 """
    elif filtr == "RODZAJ":
        if not wyrazenie.isalpha():
            return None
        wybrane = f""" SELECT * FROM sprzety where rodzaj = '{wyrazenie}' and adres_silowni = '{variables.wybranaSilownia}' order by 1 """
    elif filtr == 'STANOWISKO' or filtr == 'NR_SALI':
        if not wyrazenie.isdecimal():
            return None
        wybrane = f""" SELECT * FROM sprzety where {filtr} = {wyrazenie} and adres_silowni = '{variables.wybranaSilownia}' order by 1 """
    rows = []
    cursor = variables.cnxn.cursor()
    cursor.execute(wybrane)
    for item in cursor:
        item1 = item[0:-1]
        rows.append(item1)
    cursor.close()
    if rows == []:
        return None
    return rows

def filtruj_szafki(filtr, wyrazenie):
    if not wyrazenie.isdecimal():
        return None
    wybrane = f"""select * from szafki where {filtr} = {wyrazenie} and adres_silowni = '{variables.wybranaSilownia}' order by 2,1 """
    rows = []
    cursor = variables.cnxn.cursor()
    cursor.execute(wybrane)
    for item in cursor:
        item1 = item[0:-1]
        rows.append(item1)
    cursor.close()
    if rows == []:
        return None
    return rows

def filtruj_wlasciciele(filtr, wyrazenie):
    if filtr == 'PESEL' or filtr == 'PENSJA' or filtr == 'PREMIA':
        if not wyrazenie.isdecimal():
            return None
        wybrane = f"""select * from wlasciciele where {filtr} = {wyrazenie} order by 2,1 """
    elif filtr == "DATA":
        if len(wyrazenie) != 10:
            return None
        if wyrazenie[4] != '-' or wyrazenie[7] != '-' or not wyrazenie[:4].isdecimal() or not wyrazenie[5:7].isdecimal() or not wyrazenie[8:].isdecimal():
            return None
        wybrane = f"""select * from wlasciciele WHERE to_char(data_zatrudnienia, 'yyyy-mm-dd') = to_char('{wyrazenie}') """
    else:
        if not wyrazenie.isalpha():
            return None
        wybrane = f"""select * from wlasciciele where {filtr} = '{wyrazenie}' order by 2,1 """

    rows = []
    print(wybrane, flush=True)
    cursor = variables.cnxn.cursor()
    cursor.execute(wybrane)

    for item in cursor:
        rows.append(item)
        print('ITEMEK', item, flush=True)
    cursor.close()
    if rows == []:
        return None
    return rows

def filtruj_silownie(filtr, wyrazenie):
    if filtr == 'PESEL_WLASCICIELA':
        if not wyrazenie.isdecimal():
            return None
        wybrane = f"""select adres, nazwa, pesel_wlasciciela from silownie where {filtr} = {int(wyrazenie)} order by 2,1 """
    else:
        wybrane = f"""select adres, nazwa, pesel_wlasciciela from silownie where {filtr} = '{wyrazenie}' order by 2,1 """
    rows = []
    print(wybrane, flush=True)
    cursor = variables.cnxn.cursor()
    cursor.execute(wybrane)

    for item in cursor:
        rows.append(item)
        print('ITEMEK', item, flush=True)
    cursor.close()
    if rows == []:
        return None
    return rows
