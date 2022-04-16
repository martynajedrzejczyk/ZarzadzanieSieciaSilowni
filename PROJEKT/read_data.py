
import cx_Oracle
import variables
import datetime



hostname = 'localhost'
servicename = 'xe'
login = 'system'
pwd = 'inf145374'
variables.cnxn = cx_Oracle.connect(user=login, password=pwd, dsn='%s/%s' % (hostname, servicename))
print("Polaczono z baza danych!", flush=True)

# def connect_to_database():
#     hostname = 'localhost'
#     servicename = 'xe'
#     login = 'system'
#     pwd = 'inf145374'
#     variables.cnxn = cx_Oracle.connect(user=login, password=pwd, dsn='%s/%s' % (hostname, servicename))
#     print("Polaczono z baza danych!", flush=True)
#     return variables.cnxn
#
#
#

def czytaj_statystyki():
    cursor = variables.cnxn.cursor()
    trenerzy = cursor.callfunc('silowniapackage.IlePracownikow', int, ("Trenerzy", variables.wybranaSilownia))
    recepcjonisci = cursor.callfunc('silowniapackage.IlePracownikow', int, ("Recepcjonisci", variables.wybranaSilownia))
    sprzatacze = cursor.callfunc('silowniapackage.IlePracownikow', int, ("Sprzatacze", variables.wybranaSilownia))
    cursor.close()
    return [trenerzy, recepcjonisci, sprzatacze]

# def wybierz_pesele_wlascicieli():
#     select = f"""select pesel from wlasciciele w
#     where (select count(*) from silownie having pesel_wlasciciela = w.pesel ) = 0
#     order by 1"""
#     cursor = variables.cnxn.cursor()
#     cursor.execute(select)
#     pomieszczenia = []
#     for item in cursor:
#         pomieszczenia.append(item[0])
#     cursor.close()
#     return pomieszczenia

def wybierz_pesele_wlascicieli():
    s =  f"""select count(*) from silownie"""
    cursor = variables.cnxn.cursor()
    cursor.execute(s)
    print(cursor.fetchall())
    if len(cursor.fetchall()) == 0:
        cursor.close()
        s2 = f"""select pesel from wlasciciele"""
        cursor = variables.cnxn.cursor()
        cursor.execute(s2)
        pomieszczenia = []
        for item in cursor:
            pomieszczenia.append(item[0])
        cursor.close()
        return pomieszczenia

    cursor.close()
    select = f"""select pesel from wlasciciele w
    where coalesce((select count(*) from silownie having pesel_wlasciciela = w.pesel ),0) = 0
    order by 1"""
    print()
    cursor = variables.cnxn.cursor()
    cursor.execute(select)
    pomieszczenia = []
    for item in cursor:
        pomieszczenia.append(item[0])
    cursor.close()
    return pomieszczenia


def wybierz_tabele():
    return ["Recepcjoniści", "Sprzątacze", "Trenerzy"]


def wybierz_etaty():
    return ["Recepcjonista", "Sprzątacz", "Trener"]

def wybierz_typ_pomieszczenia():
    return ["Recepcja", "Szatnia", "Kantorek", "Sala ćwiczeniowa"]

def wybierz_pomieszczenia(): #napisac funkcje sprawdzajaca w update czy to dobre pomieszczenie
    select = f"""select nr_pomieszczenia, typ from pomieszczenia_perspektywa where adres_silowni = '{variables.wybranaSilownia}' order by 1"""
    cursor = variables.cnxn.cursor()
    cursor.execute(select)
    pomieszczenia = []
    for item in cursor:
        pomieszczenia.append(item[0])
    cursor.close()
    return pomieszczenia

def wybierz_pesel_wlascicieli():
    select = f"""select pesel from wlasciciele order by 1"""
    cursor = variables.cnxn.cursor()
    cursor.execute(select)
    tab = []
    for item in cursor:
        tab.append(item[0])
    cursor.close()
    return tab

def wybierz_pesel_trenerow():
    select = f"""select pesel from trenerzy where adres_silowni = '{variables.wybranaSilownia}' order by 1"""
    cursor = variables.cnxn.cursor()
    cursor.execute(select)
    tab = []
    for item in cursor:
        tab.append(item[0])
    cursor.close()
    return tab

def wybierz_szatnie():
    select = f"""select nr_pomieszczenia from SZATNIE where adres_silowni = '{variables.wybranaSilownia}' order by 1"""
    cursor = variables.cnxn.cursor()
    cursor.execute(select)
    pomieszczenia = []
    for item in cursor:
        pomieszczenia.append(item[0])
    cursor.close()
    return pomieszczenia

def wybierz_recepcje():
    select = f"""select nr_pomieszczenia from recepcje where adres_silowni = '{variables.wybranaSilownia}' order by 1"""
    cursor = variables.cnxn.cursor()
    cursor.execute(select)
    pomieszczenia = []
    for item in cursor:
        pomieszczenia.append(item[0])
    cursor.close()
    return pomieszczenia

def wybierz_kantorki():
    select = f"""select nr_pomieszczenia from kantorki where adres_silowni = '{variables.wybranaSilownia}' order by 1"""
    cursor = variables.cnxn.cursor()
    cursor.execute(select)
    pomieszczenia = []
    for item in cursor:
        pomieszczenia.append(item[0])
    cursor.close()
    return pomieszczenia

def wybierz_pesel_trenera():
    select = f"""select pesel from trenerzy where adres_silowni = '{variables.wybranaSilownia}' order by 1"""
    cursor = variables.cnxn.cursor()
    cursor.execute(select)
    pomieszczenia = []
    for item in cursor:
        pomieszczenia.append(item[0])
    cursor.close()
    return pomieszczenia

def wybierz_sale():
    select = f"""select nr_pomieszczenia from sale_cwiczeniowe where adres_silowni = '{variables.wybranaSilownia}' order by 1"""
    cursor = variables.cnxn.cursor()
    cursor.execute(select)
    pomieszczenia = []
    for item in cursor:
        pomieszczenia.append(item[0])
    cursor.close()
    return pomieszczenia
#-------------------------- funkcje czytające skrócone


def read_table(nazwa):
    rows = []
    cursor = variables.cnxn.cursor()
    sqlTemplate = f""" SELECT * FROM {nazwa} order by 1 """
    cursor.execute(sqlTemplate)

    for item in cursor:
        rows.append(item)
    cursor.close()
    return rows

def read_table_adr(nazwa):
    rows = []
    cursor = variables.cnxn.cursor()
    sqlTemplate = f""" SELECT * FROM {nazwa} where adres_silowni = '{variables.wybranaSilownia}' order by 1 """
    cursor.execute(sqlTemplate)

    for item in cursor:
        item1 = item[0:-1]
        rows.append(item1)
    cursor.close()
    return rows


def read_column(nazwa):
    rows = []
    cursor = variables.cnxn.cursor()
    sqlTemplate = """ select column_name from all_tab_columns where table_name = :knazwa """
    cursor.prepare(sqlTemplate)
    cursor.execute(None, knazwa=nazwa)
    # cursor.execute(sqlTemplate)
    for item in cursor:
        rows.append(item[0])
        # print(item, flush=True)
    cursor.close()
    return rows

def read_column_adr(nazwa):
    rows = []
    cursor = variables.cnxn.cursor()
    sqlTemplate = """ select column_name from all_tab_columns where table_name = :knazwa """
    cursor.prepare(sqlTemplate)
    cursor.execute(None, knazwa=nazwa)
    # cursor.execute(sqlTemplate)
    for item in cursor:
        rows.append(item[0])
        # print(item, flush=True)
    cursor.close()
    rows.pop()
    return rows
#---------------------------- funkcje read ------------------------------


def read_pracownicy():
    rows = []
    cursor = variables.cnxn.cursor()
    select_name = """SELECT  pesel, imie, nazwisko, data_zatrudnienia, pensja, premia, nr_recepcji as
    nr_pomieszczenia, adres_silowni, 'Recepcjonista' as etat  FROM recepcjonisci where adres_silowni  = :adres_silowni  union all SELECT
    pesel, imie, nazwisko, data_zatrudnienia, pensja, premia, nr_kantorka as nr_pomieszczenia, adres_silowni, 'Sprzątacz' as etat  FROM
    sprzatacze where adres_silowni =  :adres_silowni  union all SELECT pesel, imie, nazwisko, data_zatrudnienia,
    pensja, premia, NULL as nr_pomieszczenia, adres_silowni, 'Trener' as etat  FROM trenerzy where adres_silowni  =  :adres_silowni """
    cursor.prepare(select_name)
    cursor.execute(None, adres_silowni=variables.wybranaSilownia)
    for item in cursor:
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

        if item[6] == None:
            lst = list(item)
            lst[6] = "Brak"
            item = tuple(lst)
        if item[5] == None:
            lst = list(item)
            lst[5] = 0.0
            item = tuple(lst)
        nazwaEtatu = item[-1]
        item1 = item[0:-2]
        item1 += (nazwaEtatu,)
        rows.append(item1)
        # print(item, flush=True)
    cursor.close()
    return rows


def read_pracownicy_etat(etat):  # etat przyjmuje tylko TRENERZY, SPRZATACZE, RECEPCJONISCI
    rows = []
    cursor = variables.cnxn.cursor()
    select_name = f"""SELECT  * FROM {etat} where adres_silowni  = '{variables.wybranaSilownia}' """
    print(select_name, flush=True)
    cursor.execute(select_name)
    for item in cursor:
        if etat == 'TRENERZY':
            item1 = item[0:-1]
            item1 += ('None', 'Trener',)
        elif etat == 'SPRZATACZE':
            item1 = item[0:-2]
            item1 += ('Sprzatacz',)
        else:
            item1 = item[0:-2]
            item1 += ('Recepcjonista',)
        rows.append(item1)
        print(item, flush=True)
    cursor.close()
    return rows

def column_pracownicy():
    return ['PESEL', 'IMIĘ', 'NAZWISKO', 'DATA ZATRUDNIENIA', 'PENSJA', 'PREMIA', 'NUMER POMIESZCZENIA', 'ETAT']

def read_wlasciciele():
    rows = []
    cursor = variables.cnxn.cursor()
    select_name = f"""SELECT  pesel, imie, nazwisko, data_zatrudnienia, pensja, coalesce(premia, 0) FROM wlasciciele """
    cursor.execute(select_name)
    for item in cursor:
        rows.append(item)
    cursor.close()
    return rows

def column_wlasciciele():
    return ['PESEL', 'IMIE', 'NAZWISKO', 'DATA ZATRUDNIENIA', 'PENSJA', 'PREMIA']

def read_silownie():
    rows = []
    cursor = variables.cnxn.cursor()
    select_name = f"""SELECT  * FROM silownie """
    cursor.execute(select_name)
    for item in cursor:
        rows.append(item)
    cursor.close()
    return rows

def column_silownie():
    return ['ADRES', 'NAZWA', 'PESEL_WLASCICIELA']

def read_pomieszczenia():
    rows = []
    cursor = variables.cnxn.cursor()
    select_name = """select nr_pomieszczenia, pietro, powierzchnia, 'Recepcja' as typ  from recepcje where adres_silowni 
    = :adr union all select nr_pomieszczenia, pietro, powierzchnia, 'Kantorek' as typ  from kantorki where adres_silowni 
    = :adr union all select nr_pomieszczenia, pietro, powierzchnia, 'Sala ćwiczeniowa' as typ  from sale_cwiczeniowe where adres_silowni 
    = :adr union all select nr_pomieszczenia, pietro, powierzchnia, 'Szatnia' as typ  from szatnie where 
    adres_silowni =  :adr order by pietro, nr_pomieszczenia """
    cursor.prepare(select_name)
    cursor.execute(None, adr=variables.wybranaSilownia)
    # print("as", flush=True)
    for item in cursor:
        rows.append(item)
        print(item, flush=True)
    cursor.close()
    return rows

def read_grupy():
    rows = []
    cursor = variables.cnxn.cursor()
    select_name = f"""select g.ID_GRUPY,to_date(g.TERMIN_SPOTKANIA, 'dd-mm-yyyy'),	trenerzy.imie as IMIĘ_TRENERA, trenerzy.nazwisko as NAZWISKO_TRENERA,
    g.NR_SALI from grupy_zorganizowane g inner join trenerzy on trenerzy.pesel = g.pesel_trenera
    where g.adres_silowni = '{variables.wybranaSilownia}' order by 1 """
    cursor.execute(select_name)
    for item in cursor:
        rows.append(item)
    cursor.close()
    return rows

def read_grupy_f_trener(nazwisko):
    rows = []
    cursor = variables.cnxn.cursor()
    select_name = f"""select g.ID_GRUPY,g.TERMIN_SPOTKANIA,	trenerzy.imie as IMIĘ_TRENERA, trenerzy.nazwisko as NAZWISKO_TRENERA,
        g.NR_SALI from grupy_zorganizowane g inner join trenerzy on trenerzy.pesel = g.pesel_trenera
        where g.adres_silowni = '{variables.wybranaSilownia}' and trenerzy.nazwisko = '{nazwisko}' order by 1 """
    cursor.execute(select_name)
    for item in cursor:
        rows.append(item)
    cursor.close()
    return rows

def read_grupy_f_sale(nr_sali):
    rows = []
    cursor = variables.cnxn.cursor()
    select_name = f"""select g.ID_GRUPY,g.TERMIN_SPOTKANIA,	trenerzy.imie as IMIĘ_TRENERA, trenerzy.nazwisko as NAZWISKO_TRENERA,
        g.NR_SALI from grupy_zorganizowane g inner join trenerzy on trenerzy.pesel = g.pesel_trenera
        where g.adres_silowni = '{variables.wybranaSilownia}' and g.nr_sali =  '{nr_sali}' order by 1 """
    cursor.execute(select_name)
    for item in cursor:
        rows.append(item)
    cursor.close()
    return rows

def read_klubowicze_f_id_grupy(id_grupy):  #podaje klubowiczow ktorzy sa w grupie o numerze id_grupy - filtr
    rows = []
    cursor = variables.cnxn.cursor()
    cursor.execute(
        f"""select pesel, nazwisko, klubowicze.nr_karty,  to_char(wazna_od, 'yyyy-mm-dd'), to_char(wazna_do, 'yyyy-mm-dd'), znizka 
from klubowicze inner join karnety on klubowicze.nr_karty = karnety.nr_karty
where pesel in (select pesel_klubowicza from przynaleznosci_klubowiczow_do_grup where id_grupy = '{id_grupy}') """)
    for item in cursor:
        if item[5] == None:
            lst = list(item)
            lst[5] = 0
            item = tuple(lst)
        rows.append(item)
        print(item, flush=True)
    cursor.close()
    return rows

def column_grupy():
    return ['ID GRUPY', 'TERMIN SPOTKANIA', 'IMIĘ TRENERA', 'NAZWISKO TRENERA', 'NUMER SALI']

def column_pomieszczenia():
    return ['NUMER POMIESZCZENIA', 'PIĘTRO', 'POWIERZCHNIA', 'TYP POMIESZCZENIA']

def read_pomieszczenia_typ(typ):  # etat przyjmuje tylko KANTORKI SALE_CWICZENIOWE RECEPCJE SZATNIE
    rows = []
    cursor = variables.cnxn.cursor()
    select_name = f"""SELECT  * FROM {typ} where adres_silowni  = '{variables.wybranaSilownia}' order by 2,1 """
    cursor.execute(select_name)
    typ = typ.lower().capitalize()
    for item in cursor:
        item1 = item[0:-1]
        item1 += (typ,)
        rows.append(item1)
        print(item, flush=True)
    cursor.close()
    return rows

def read_sprzet_rodzaj(rodzaj):
    rows = []
    cursor = variables.cnxn.cursor()
    select_name = f"""SELECT  * FROM sprzety where adres_silowni  = '{variables.wybranaSilownia}' and rodzaj = '{rodzaj}' """
    cursor.execute(select_name)
    for item in cursor:
        item1 = item[0:-1]
        rows.append(item1)
        # print(item, flush=True)
    cursor.close()
    return rows

def read_klubowicze_karnety():
    rows = []
    cursor = variables.cnxn.cursor()
    cursor.execute("select pesel, nazwisko, klubowicze.nr_karty, to_char(wazna_od, 'yyyy-mm-dd'), to_char(wazna_do, 'yyyy-mm-dd'), "
                   "znizka from klubowicze inner join karnety on klubowicze.nr_karty = karnety.nr_karty union all"
                   " select pesel, nazwisko, null as nr_karty, null as wazna_od, null as wazna_do, null as znizka from klubowicze "
                   "where coalesce(nr_karty, 0) = 0  order by nr_karty")
    for item in cursor:
        if item[5] == None:
            lst = list(item)
            lst[5] = 0
            item = tuple(lst)
        rows.append(item)
        print(item, flush=True)
    cursor.close()
    return rows


def column_klubowicze_karnety():
    return ['PESEL', 'NAZWISKO', 'NUMER KARTY', 'WAŻNA_OD', 'WAŻNA_DO', 'ZNIŻKA']

def read_plany():
    rows = []
    cursor = variables.cnxn.cursor()
    cursor.execute(
        f""" select nr_planu, opis, imie, nazwisko from plany_treningowe inner join trenerzy on pesel_trenera = pesel
where trenerzy.adres_silowni = '{variables.wybranaSilownia}' order by 1 """)
    for item in cursor:
        rows.append(item)
    cursor.close()
    return rows

def column_plany():
    return ['NUMER PLANU', 'OPIS PLANU', 'IMIĘ TRENERA', 'NAZWISKO TRENERA']

def read_plany_f_trener(nazwisko): #plany treningowe danego trenera, nwm czy potrzebne nam
    rows = []
    cursor = variables.cnxn.cursor()
    cursor.execute(
        f""" select nr_planu, opis, imie, nazwisko from plany_treningowe inner join trenerzy on pesel_trenera = pesel
where trenerzy.adres_silowni = '{variables.wybranaSilownia}' and nazwisko = '{nazwisko}' """)
    for item in cursor:
        rows.append(item)
    cursor.close()
    return rows

def read_klubowicze_f_plan(nr_planu): #klubowicze cwiczacy z tym planem
    rows = []
    cursor = variables.cnxn.cursor()
    cursor.execute(
        f"""select pesel, nazwisko, klubowicze.nr_karty, to_char(wazna_od, 'yyyy-mm-dd'), to_char(wazna_do, 'yyyy-mm-dd'), znizka 
    from klubowicze inner join karnety on klubowicze.nr_karty = karnety.nr_karty
    where pesel in (select pesel_klubowicza from cwicza_z_planem where nr_planu = '{nr_planu}') """)
    for item in cursor:
        if item[5] == None:
            lst = list(item)
            lst[5] = 0
            item = tuple(lst)
        rows.append(item)
        print(item, flush=True)
    cursor.close()
    return rows


#---------------------------- funckje insert ------------------------------
def insert_wlasciciele(pesel1, imie1, nazwisko1, pensja1, premia1):

    cursor = variables.cnxn.cursor()
    insert_wlasciciel = """INSERT INTO wlasciciele VALUES (:pesel, :imie, :nazwisko, :data_zatrudnienia, :pensja, :premia)"""
    cursor.prepare(insert_wlasciciel)
    cursor.execute(None, pesel=pesel1, imie=imie1, nazwisko=nazwisko1,
                   data_zatrudnienia=datetime.datetime.now(), pensja=float(pensja1), premia=float(premia1))
    variables.cnxn.commit()
    cursor.close()

def insert_silownie(adres1, nazwa1, pesel1):
    cursor = variables.cnxn.cursor()
    insert_wlasciciel = """INSERT INTO silownie VALUES (:adres, :nazwa, :pesel_wlasciciela)"""
    cursor.prepare(insert_wlasciciel)
    cursor.execute(None, adres = adres1, nazwa = nazwa1, pesel_wlasciciela = pesel1)
    variables.cnxn.commit()
    cursor.close()

def insert_kantorki(nrpom, piet, pow, adr):
    cursor = variables.cnxn.cursor()
    insert_wlasciciel = """INSERT INTO kantorki VALUES (:nr_pomieszczenia, :pietro, :powierzchnia, :adres_silowni)"""
    cursor.prepare(insert_wlasciciel)
    cursor.execute(None, nr_pomieszczenia = nrpom, pietro = piet, powierzchnia = pow, adres_silowni = adr)
    variables.cnxn.commit()
    cursor.close()

def insert_sale_cwiczeniowe(nrpom, piet, pow, adr):
    cursor = variables.cnxn.cursor()
    insert_wlasciciel = """INSERT INTO sale_cwiczeniowe VALUES (:nr_pomieszczenia, :pietro, :powierzchnia, :adres_silowni)"""
    cursor.prepare(insert_wlasciciel)
    cursor.execute(None, nr_pomieszczenia = nrpom, pietro = piet, powierzchnia = pow, adres_silowni = adr)
    variables.cnxn.commit()
    cursor.close()

def insert_recepcje(nrpom, piet, pow, adr):
    cursor = variables.cnxn.cursor()
    insert_wlasciciel = """INSERT INTO recepcje VALUES (:nr_pomieszczenia, :pietro, :powierzchnia, :adres_silowni)"""
    cursor.prepare(insert_wlasciciel)
    cursor.execute(None, nr_pomieszczenia = nrpom, pietro = piet, powierzchnia = pow, adres_silowni = adr)
    variables.cnxn.commit()
    cursor.close()

def insert_szatnie(nrpom, piet, pow, adr):
    cursor = variables.cnxn.cursor()
    insert_wlasciciel = """INSERT INTO szatnie VALUES (:nr_pomieszczenia, :pietro, :powierzchnia, :adres_silowni)"""
    cursor.prepare(insert_wlasciciel)
    cursor.execute(None, nr_pomieszczenia = nrpom, pietro = piet, powierzchnia = pow, adres_silowni = adr)
    variables.cnxn.commit()
    cursor.close()

def insert_trenerzy(pesel1, imie1, nazwisko1, pensja1, premia1, adres_silowni1):

    cursor = variables.cnxn.cursor()
    insert_wlasciciel = """INSERT INTO trenerzy VALUES (:pesel, :imie, :nazwisko, :data_zatrudnienia, :pensja, :premia, :adres_silowni)"""
    cursor.prepare(insert_wlasciciel)
    cursor.execute(None, pesel=pesel1, imie=imie1, nazwisko=nazwisko1,
                   data_zatrudnienia=datetime.datetime.now(), pensja=float(pensja1), premia=float(premia1), adres_silowni=adres_silowni1)
    variables.cnxn.commit()
    cursor.close()

def insert_sprzatacze(pesel1, imie1, nazwisko1, pensja1, premia1, nr, adres_silowni1):

    cursor = variables.cnxn.cursor()
    insert_wlasciciel = """INSERT INTO sprzatacze VALUES (:pesel, :imie, :nazwisko, :data_zatrudnienia, 
    :pensja, :premia, :nr_kantorka, :adres_silowni, :adres_silowni_s)"""
    cursor.prepare(insert_wlasciciel)
    cursor.execute(None, pesel=pesel1, imie=imie1, nazwisko=nazwisko1,
                   data_zatrudnienia=datetime.datetime.now(), pensja=float(pensja1),
                   premia=float(premia1), nr_kantorka = nr, adres_silowni = adres_silowni1, adres_silowni_s = adres_silowni1)
    variables.cnxn.commit()
    cursor.close()

def insert_recepcjonisci(pesel1, imie1, nazwisko1, pensja1, premia1, nr, adres_silowni1):

    cursor = variables.cnxn.cursor()
    insert_wlasciciel = """INSERT INTO sprzatacze VALUES (:pesel, :imie, :nazwisko, :data_zatrudnienia, 
    :pensja, :premia, :nr_recepcji, :adres_silowni, :adres_silowni_s)"""
    cursor.prepare(insert_wlasciciel)
    cursor.execute(None, pesel=pesel1, imie=imie1, nazwisko=nazwisko1,
                   data_zatrudnienia=datetime.datetime.now(), pensja=float(pensja1),
                   premia=float(premia1), nr_recepcji=nr, adres_silowni=adres_silowni1, adres_silowni_zatrudnony=adres_silowni1)
    variables.cnxn.commit()
    cursor.close()

def insert_karnety(nr, od, do, zniz, pesel):

    cursor = variables.cnxn.cursor()
    insert_wlasciciel = """INSERT INTO karnety VALUES (:nr_karty, :wazna_od, :wazna_do, :znizka, :pesel_klubowicza)"""
    cursor.prepare(insert_wlasciciel)
    cursor.execute(None, nr_karty = nr, wazna_od = od, wazna_do = do, znizka = zniz, pesel_klubowicza = pesel)
    variables.cnxn.commit()
    cursor.close()

def insert_klubowicze(pesel1, nazw):

    cursor = variables.cnxn.cursor()
    insert_wlasciciel = """INSERT INTO klubowicze (pesel, nazwisko) VALUES (:pesel, :nazwisko)"""
    cursor.prepare(insert_wlasciciel)
    cursor.execute(None, pesel = pesel1, nazwisko = nazw)
    variables.cnxn.commit()
    cursor.close()

def insert_plany_treningowe(opis1, pesel1):

    cursor = variables.cnxn.cursor()
    insert_wlasciciel = """INSERT INTO plany_treningowe (opis, pesel_trenera) VALUES (:opis, :pesel_trenera)"""
    cursor.prepare(insert_wlasciciel)
    cursor.execute(None, opis = opis1, pesel_trenera = pesel1)
    variables.cnxn.commit()
    cursor.close()

def insert_grupy_zorganizowane(termin, pesel, sala, adres):

    cursor = variables.cnxn.cursor()
    insert_wlasciciel = """INSERT INTO grupy_zorganizowane (termin_spotkania, pesel_trenera, nr_sali, adres_silowni) VALUES (:termin_spotkania, :pesel_trenera, :nr_sali, :adres_silowni)"""
    cursor.prepare(insert_wlasciciel)
    cursor.execute(None, termin_spotkania = termin, pesel_trenera = pesel, nr_sali = sala, adres_silowni = adres)
    variables.cnxn.commit()
    cursor.close()

def insert_sprzety(nr, rodz, stan, sala, adres):

    cursor = variables.cnxn.cursor()
    insert_wlasciciel = """INSERT INTO sprzety VALUES (:nr_urzadzenia, :rodzaj, :stanowisko, :nr_sali, :adres_silowni)"""
    cursor.prepare(insert_wlasciciel)
    cursor.execute(None, nr_urzadzenia = nr, rodzaj = rodz, stanowisko = stan, nr_sali = sala, adres_silowni = adres)
    variables.cnxn.commit()
    cursor.close()

def insert_cwicza_z_planem(pesel, nr):

    cursor = variables.cnxn.cursor()
    insert_wlasciciel = """INSERT INTO cwicza_z_planem VALUES (:pesel_klubowicza, :nr_planu)"""
    cursor.prepare(insert_wlasciciel)
    cursor.execute(None, pesel_klubowicza = pesel, nr_planu = nr)
    variables.cnxn.commit()
    cursor.close()

def insert_przynaleznosci_klubowiczow_do_grup(id, pes):

    cursor = variables.cnxn.cursor()
    insert_wlasciciel = """INSERT INTO przynaleznosci_klubowiczow_do_grup VALUES (:id_grupy, :pesel_klubowicza)"""
    cursor.prepare(insert_wlasciciel)
    cursor.execute(None, id_grupy = id, pesel_klubowicza = pes)
    variables.cnxn.commit()
    cursor.close()




