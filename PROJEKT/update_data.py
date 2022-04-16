import cx_Oracle
import variables
import datetime

def dodaj_podwyzke(dane):
    ile = dane[0]
    etat = dane[1]
    if not ile.isdecimal():
        return ""
    if etat == "Recepcjoniści":
        etat = "Recepcjonisci"
    elif etat == "Sprzątacze":
        etat = "Sprzatacze"
    cursor = variables.cnxn.cursor()
    cursor.callproc('silowniapackage.PodwyzkaEtat', [ile, etat])
    cursor.close()
    variables.cnxn.commit()

def update_plany_treningowe(nowe_dane):
    cursor = variables.cnxn.cursor()
    update = f""" update plany_treningowe set opis = '{nowe_dane[1]}' where nr_planu = {nowe_dane[0]} """
    cursor.execute(update)
    variables.cnxn.commit()
    cursor.close()
    return

def update_klubowicze(nowe_dane):
    cursor = variables.cnxn.cursor()
    update = f""" update klubowicze set nazwisko = '{nowe_dane[1]}' where pesel = {nowe_dane[0]} """
    cursor.execute(update)
    variables.cnxn.commit()

    update = f"""update karnety set wazna_od = to_date('{nowe_dane[3]}', 'yyyy-mm-dd'), wazna_do = to_date('{nowe_dane[4]}', 'yyyy-mm-dd'), znizka = {nowe_dane[5]} where nr_karty = {nowe_dane[2]} """
    cursor.execute(update)
    variables.cnxn.commit()

    cursor.close()
    return

def update_grupy(nowe_dane):
    cursor = variables.cnxn.cursor()
    # update = f""" update grupy_zorganizowane set termin_spotkania = to_date({nowe_dane[1]}, 'dd-mm-rrrr'),
    #  nr_sali = {nowe_dane[4]} where id_grupy = {nowe_dane[0]} """
    update = """  update grupy_zorganizowane set termin_spotkania = to_date(:data, 'dd'),
     nr_sali = :sala where id_grupy = :id  """
    cursor.prepare(update)
    cursor.execute(None, data =nowe_dane[1], sala=nowe_dane[4], id=nowe_dane[0])
    # cursor.execute(update)
    print("update grupy ", flush=True)
    variables.cnxn.commit()
    cursor.close()
    return

def update_sprzety(nowe_dane):
    cursor = variables.cnxn.cursor()
    update = f"""  update sprzety set rodzaj='{nowe_dane[1]}', stanowisko={nowe_dane[2]} where nr_urzadzenia = {nowe_dane[0]} and nr_sali = {nowe_dane[3]} """
    cursor.execute(update)
    variables.cnxn.commit()
    cursor.close()
    return

def update_pracownicy(nowe_dane):
    cursor = variables.cnxn.cursor()
    zap = f""" select etat from pracownicy_perspektywa where pesel = {nowe_dane[0]} """
    cursor.execute(zap)
    stary_etat = cursor.fetchmany(1)
    print(stary_etat, "stary etat")
    stary_etat = stary_etat[0][0]
    if nowe_dane[5] == 'None':
        nowe_dane[5] = 0
    if stary_etat == nowe_dane[7]: #nie zmieniono etatu
        if stary_etat == 'Recepcjonista':
            zap = f""" update recepcjonisci set imie = '{nowe_dane[1]}', nazwisko = '{nowe_dane[2]}', pensja = {nowe_dane[4]}, 
            premia = {nowe_dane[5]}, nr_recepcji = {nowe_dane[6]} where pesel = {nowe_dane[0]} """
        elif stary_etat == "Sprzątacz":
            zap = f""" update sprzatacze set imie = '{nowe_dane[1]}', nazwisko = '{nowe_dane[2]}', 
            pensja = {nowe_dane[4]}, premia = {nowe_dane[5]}, nr_kantorka = {nowe_dane[6]} where pesel = {nowe_dane[0]}  """
        elif stary_etat == 'Trener':
            zap = f""" update trenerzy set imie = '{nowe_dane[1]}', nazwisko = '{nowe_dane[2]}', 
            pensja = {nowe_dane[4]}, premia = {nowe_dane[5]} where pesel = {nowe_dane[0]}  """
        cursor.execute(zap)
        variables.cnxn.commit()
    else:               #zmieniono etat

        #wczytanie nazwy tabeli
        print("stary etat", stary_etat)
        if stary_etat == 'Recepcjonista':
            tab = 'Recepcjonisci'
        elif stary_etat == 'Sprzątacz':
            tab = 'Sprzatacze'
        elif stary_etat == 'Trener':
            tab = 'Trenerzy'
            czysc_po_trenerze(nowe_dane[0])

        #wstawienie nowego pracownika
        if nowe_dane[7] == 'Recepcjonista':
            zap = f""" insert into Recepcjonisci (pesel, imie, nazwisko, pensja, premia, nr_recepcji, adres_silowni, adres_silowni_zatrudniony)
             values ( {nowe_dane[0]}, '{nowe_dane[1]}', '{nowe_dane[2]}', {nowe_dane[4]}, {nowe_dane[5]}, {nowe_dane[6]},
              '{variables.wybranaSilownia}', '{variables.wybranaSilownia}')
             """
        elif nowe_dane[7] == 'Sprzątacz':
            zap = f""" insert into Sprzatacze (pesel, imie, nazwisko, pensja, premia, nr_kantorka, adres_silowni, adres_silowni_s)
             values ({nowe_dane[0]}, '{nowe_dane[1]}', '{nowe_dane[2]}', {nowe_dane[4]}, {nowe_dane[5]}, {nowe_dane[6]},
              '{variables.wybranaSilownia}', '{variables.wybranaSilownia}')
             """
            print("Nowy sprzatacz")
        elif nowe_dane[7] == 'Trener':
            print("Nowy wtat to trener")
            zap = f""" insert into Trenerzy (pesel, imie, nazwisko, pensja, premia, adres_silowni)
             values ( {nowe_dane[0]}, '{nowe_dane[1]}', '{nowe_dane[2]}', {nowe_dane[4]}, {nowe_dane[5]}, '{variables.wybranaSilownia}') """
        cursor.execute(zap)

        #usuniecie pracownika
        zap = f""" delete from {tab} where pesel = {nowe_dane[0]} """
        cursor.execute(zap)


        variables.cnxn.commit()
        cursor.close()

def czysc_po_trenerze(pesel): #używamy w update_pracownicy()
    cursor = variables.cnxn.cursor()

            # wyszukanie grup zorganizowanych danego trenera
    grupy = f""" select id_grupy from grupy_zorganizowane where pesel_trenera = {pesel} """
    cursor.execute(grupy)
    id_grup = []
    for i in cursor.fetchall():
        id_grup.append(i[0]) # [1, 22]
    grupy = f"""delete from grupy_zorganizowane where id_grupy in ({str(id_grup).replace("[","").replace("]","")}) """

            # wyszukanie i usuniecie przynaleznosci klubowiczow do tych grup i usuniecie grup zorganizowanych
    przynaleznosci = f""" delete from Przynaleznosci_klubowiczow_do_grup where id_grupy in ({str(id_grup).replace("[","").replace("]","")}) """
    print(przynaleznosci)
    if len(id_grup) > 0:
        cursor.execute(przynaleznosci)
        cursor.execute(grupy)

        #wyszukanie planow treningowych
    plany = f"""select nr_planu from Plany_treningowe where pesel_trenera = {pesel}"""
    cursor.execute(plany)
    nr_planow = []
    for i in cursor.fetchall():
        nr_planow.append(i[0])  # [1, 22]
    plany = f"""delete from Plany_treningowe where nr_planu in ({str(nr_planow).replace("[", "").replace("]", "")}) """

    #wyszukanie cwicza_z_planem
    cwicza = f""" delete from Cwicza_z_planem where nr_planu in ({str(nr_planow).replace("[", "").replace("]", "")}) """
    if len(nr_planow) > 0:
        cursor.execute(cwicza)
        cursor.execute(plany)
    cursor.close()
    variables.cnxn.commit()

def update_pomieszczenia(nowe_dane):
    cursor = variables.cnxn.cursor()
    zap = f""" select typ from pomieszczenia_perspektywa where nr_pomieszczenia = {nowe_dane[0]} and adres_silowni = '{variables.wybranaSilownia}' """
    cursor.execute(zap)
    stare_pomieszczenie = cursor.fetchmany(1)

    stare_pomieszczenie = stare_pomieszczenie[0][0]
    print(stare_pomieszczenie, " stare pomieszczenie")
    print(nowe_dane[3], " nowe pomieszczenie")

    if stare_pomieszczenie == "Kantorek":
        star = "kantorki"
    elif stare_pomieszczenie == "Szatnia":  # ok
        star = "szatnie"
    elif stare_pomieszczenie == "Sala ćwiczeniowa":  # ok
        star = "sale_cwiczeniowe"
    elif stare_pomieszczenie == "Recepcja":  # ok
        star = "recepcje"

    typ = ""  #nowe pomieszczenie
    if nowe_dane[3] == "Recepcja":
        typ = "recepcje"
    elif nowe_dane[3] == "Szatnia":  # ok
        typ = "szatnie"
    elif nowe_dane[3] == "Kantorek":
        typ = "kantorki"
    elif nowe_dane[3] == "Sala ćwiczeniowa" or nowe_dane[3] == "Sala":  # ok
        typ = "sale_cwiczeniowe"

    if stare_pomieszczenie == nowe_dane[3]: #nie zmieniono typu pomieszczenia

        print("nie zmieniono pomieszczeina", flush=True)
        update = f""" update {typ} set pietro = {nowe_dane[1]}, powierzchnia = {nowe_dane[2]} where
         nr_pomieszczenia = {nowe_dane[0]} and adres_silowni = '{variables.wybranaSilownia}' """
        print(update)
        cursor.execute(update)
        cursor.close()
        variables.cnxn.commit()
        return None
    else:  #zmieniono typ pomieszczenia

        print("chcesz zmienic typ tego pomieszczenia stare pomieszczenie:", star, flush=True)
        print("Na to nowe pomieszczenie:", typ, flush=True)
        insert = f"""insert into {typ} (nr_pomieszczenia, pietro, powierzchnia, adres_silowni) 
        values ({nowe_dane[0]}, {nowe_dane[1]}, {nowe_dane[2]}, '{variables.wybranaSilownia}' ) """
        delete = f"""delete from {star} where nr_pomieszczenia = {nowe_dane[0]}  and adres_silowni = '{variables.wybranaSilownia}'"""
        print(insert)
        if stare_pomieszczenie == "Recepcja":
            rec = f"""select pesel from recepcjonisci where nr_recepcji = {nowe_dane[0]} and adres_silowni = '{variables.wybranaSilownia}'"""
            cursor.execute(rec)
            recepcjonisci = []
            for i in cursor.fetchall():
                recepcjonisci.append(i[0])
            if len(recepcjonisci) > 0:
                return "Znaleziono recepcjonistów korzystających z tej recepcji! Usuń ich lub przypisz ich do innej recepcji, aby zmienić typ tego pomieszczenia."
        elif stare_pomieszczenie == "Kantorek":
            rec = f"""select pesel from sprzatacze where nr_kantorka = {nowe_dane[0]} and adres_silowni = '{variables.wybranaSilownia}'"""
            cursor.execute(rec)
            s = []
            for i in cursor.fetchall():
                s.append(i[0])
            if len(s) > 0:
                return "Znaleziono sprzątaczy korzystających z tego kantorka! Usuń ich lub przypisz ich do innego kantorka, aby zmienić typ tego pomieszczenia."
        elif stare_pomieszczenie == "Sala ćwiczeniowa":
            grupy = []
            print("sprzwdzam sale", flush=True)
            przynaleznosci = []
            sprz = f"""select nr_urzadzenia from sprzety where nr_sali = {nowe_dane[0]} and adres_silowni = '{variables.wybranaSilownia}' """
            gru = f"""select id_grupy from grupy_zorganizowane where nr_sali = {nowe_dane[0]} and adres_silowni = '{variables.wybranaSilownia}' """
            cursor.execute(sprz)
            s = []
            for i in cursor.fetchall():
                s.append(i[0])
            if len(s) > 0:
                return "Znaleziono sprzęty stojące w tej sali. Przenieś je lub usuń, aby zmienić typ tego pomieszczenia."
            cursor.execute(gru)
            g = []
            for i in cursor.fetchall():
                g.append(i[0])
            if len(g) > 0:
                return "Znaleziono grupy ćwiczące w tej sali. Przenieś je lub usuń, aby zmienić typ tego pomieszczenia."
        elif stare_pomieszczenie == "Szatnia":
            sza = f"""select nr_szafki from szafki where nr_szatni = {nowe_dane[0]} and adres_silowni = '{variables.wybranaSilownia}'"""
            cursor.execute(sza)
            s = []
            for i in cursor.fetchall():
                s.append(i[0])
            if len(s) > 0:
                return "Aby zmienić to pomieszczenie na inne, usuń lub przenieś wszystkie szafki w nim stojące."
        cursor.execute(delete)
        cursor.execute(insert)
        return None

def update_wlasciciele(nowe_dane):
    cursor = variables.cnxn.cursor()
    update = f""" update wlasciciele set pensja = {round(float(nowe_dane[4]),2)}, 
    premia = {round(float((nowe_dane[5])),2)}, imie = '{nowe_dane[1]}', nazwisko='{nowe_dane[2]}' 
    where pesel = {nowe_dane[0]} """
    print(update)
    cursor.execute(update)
    variables.cnxn.commit()
    cursor.close()
    return

def update_silownie(nowe_dane):
    cursor = variables.cnxn.cursor()
    update = f""" update silownie set nazwa = '{nowe_dane[1]}', 
     pesel_wlasciciela = {nowe_dane[2]} where adres = '{nowe_dane[0]}' """
    print(update)
    cursor.execute(update)
    variables.cnxn.commit()
    cursor.close()
    return