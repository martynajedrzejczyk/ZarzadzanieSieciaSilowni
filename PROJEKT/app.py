from flask import Flask, render_template, redirect, url_for, request
from read_data import *
from insert_data import *
from delete_data import *
from check_data import *
from filtr_data import *
from update_data import *
import variables
import datetime

app = Flask(__name__)
app.secret_key = "super secret key"


@app.route('/czytaj_filtr/<tabelka>')
def czytaj_filtr(tabelka):
    return redirect(url_for('pracownicy'))


@app.route('/dodaj_klubowicze', methods=["POST"])
def dodajklubowiczap():
    if request.method == 'POST':
        odczytane = []
        n = len(variables.last_page) + 1
        for i in range(n):
            odczytane.append(request.form[str(i)])
        print(odczytane, flush=True)
        error = sprawdz_klubowicz(odczytane)
        if error == None:
            dodaj_klubowicze(odczytane)
            #insert TODO
            return redirect(url_for('klubowicze'))
        else:
            return render_template('Pop-up-klubowicze.html', data=variables.last_page[1:], title=variables.last_page[0], error=error)


@app.route('/dodaj_do_grupy/<pesel>')
def dodajdogrupy(pesel):
    return render_template('dodaj_do_grupy.html', data=read_grupy(), names=column_grupy(), gymname = variables.nazwaSilowni, pesel=pesel)


@app.route('/dodaj_do_planu/<pesel>')
def dodajdoplanu(pesel):
    return render_template('dodaj_do_planu.html', data=read_plany(), names=column_plany(), gymname = variables.nazwaSilowni, pesel=pesel)


@app.route('/akceptuj-dodanie/<pesel>/<id>')
def akceptuj(pesel, id):
    error = sprawdz_klubowicz_grupa(pesel, id)
    if error == None:
        dodaj_klubowicz_grupa(pesel, id)
    return render_template('h_klubowicze.html', data=read_klubowicze_karnety(), names=column_klubowicze_karnety(), gymname = variables.nazwaSilowni)


@app.route('/akceptuj-plan/<pesel>/<nr>')
def akceptuj_plan(pesel, nr):
    error = sprawdz_klubowicz_plan(pesel, nr)
    if error == None:
        dodaj_klubowicz_plan(pesel, nr)
    return render_template('h_klubowicze.html', data=read_klubowicze_karnety(), names=column_klubowicze_karnety(),
                           gymname=variables.nazwaSilowni)


@app.route('/dodaj_klubowicze')
def dodajklubowocza():
    return render_template('Pop-up-klubowicze.html', data=variables.last_page[1:], title=variables.last_page[0])

@app.route('/statystyki')
def statystyki():
    s = czytaj_statystyki()
    return render_template('Pop-up-statystyki.html', tab = s, gymname=variables.nazwaSilowni)

# chyba niepotrzebne
# @app.route('/statystyki', methods=["POST"])
# def statystykip():
#     s = czytaj_statystyki()
#     return render_template('Pop-up-statystyki.html')

@app.route('/podwyzka')
def podwyzka():
    data = [' podwyżkę wszystkim pracownikom', 'Zakres [0-100%]', 'etat']
    return render_template('Pop-up-1.html', data=data[1:], title=data[0], etaty=wybierz_tabele(), label="Wybierz etat, któremu dasz podwyżkę: ", ile = 2)


@app.route('/podwyzka', methods=["POST"])
def podwyzkap():
    dane = [request.form["0"], request.form["1"]]
    data = [' podwyżkę wszystkim pracownikom', 'Zakres [0-100%]', 'etat']

    error= chk_podwyzka(dane)
    if error!=None:
        return render_template('Pop-up-1.html', data=data[1:], title=data[0], etaty=wybierz_tabele(), label="Wybierz etat, któremu dasz podwyżkę: ", ile = 2, error=error)
    else:
        dodaj_podwyzke(dane)
        return redirect(url_for('pracownicy'))

@app.route('/dodaj/<tabelka>', methods=["POST"])
def dodajp(tabelka):
    print('wcisnales przycisk dodaj', flush=True)
    if request.method == 'POST':
        odczytane = []
        error = None
        if tabelka == "sprzety":
            for i in range(4):
                odczytane.append(request.form[str(i)])
        elif tabelka == "szafki":
            for i in range(2):
                odczytane.append(request.form[str(i)])
        else:
            n = len(variables.last_page) - 1
            for i in range(n):
                odczytane.append(request.form[str(i)])
        print(odczytane, flush=True)
        if tabelka == "pracownicy":
            error = sprawdz_pracownicy(odczytane)
            if error == None:
                dodaj_pracownicy(odczytane)
                return redirect(url_for('pracownicy'))
            else:
                return render_template('Pop-up-1.html', data=variables.last_page[1:], etaty=wybierz_etaty(), label="Etat: ",
                                       title=variables.last_page[0], error=error, ile=len(variables.last_page)-1)
        elif tabelka == "pomieszczenia":
            error = sprawdz_pomieszczenia(odczytane)
            if error == None:
                dodaj_pomieszczenia(odczytane)
                return redirect(url_for('pomieszczenia'))
            else:
                return render_template('Pop-up-1.html', data=variables.last_page[1:],etaty=wybierz_typ_pomieszczenia(), label="Rodzaj pomieszczenia: ",
                                       title=variables.last_page[0], error=error, ile=len(variables.last_page)-1)
        elif tabelka == "plany_treningowe":
            error = sprawdz_plan(odczytane)
            if error == None:
                dodaj_plany(odczytane)
                return redirect(url_for('plany_treningowe'))
            else:
                return render_template('Pop-up-1.html', data=variables.last_page[1:],etaty=wybierz_pesel_trenerow(), label="Pesel trenera: ",
                                       title=variables.last_page[0], error=error, ile=len(variables.last_page)-1)
        elif tabelka == "grupy_zorganizowane":
            error = sprawdz_grupe(odczytane)
            if error == None:
                dodaj_grupe(odczytane)
                return redirect(url_for('grupy'))
            else:
                return render_template('Pop-up-2.html', data=variables.last_page[1:5], pesel=wybierz_pesel_trenerow(), sale=wybierz_sale(),
                                       title=variables.last_page[0], error=error, ile=len(variables.last_page)-1)
        elif tabelka == "sprzety":
            error = sprawdz_sprzet(odczytane)
            if error == None:
                dodaj_sprzet(odczytane)
                return redirect(url_for('sprzetp'))
            else:
                return render_template('Pop-up-1.html', data=variables.last_page[1:5], etaty=wybierz_sale(), label="Sala ćwiczeniowa: ",
                                       title=variables.last_page[0], error=error, ile=4)

        elif tabelka == "szafki":
            error = sprawdz_szafki(odczytane)
            if error == None:
                dodaj_szafki(odczytane)
                return redirect(url_for('szafki'))
            else:
                return render_template('Pop-up-1.html', data=variables.last_page[6:8], etaty=wybierz_szatnie(), label="Szatnia: ",
                                       title=variables.last_page[5], error=error, ile=2)
        elif tabelka == 'wlasciciele':
            error = sprawdz_wlasciciele(odczytane)
            if error == None:
                dodaj_wlasciciela(odczytane)
                print(tabelka, flush=True)
                return redirect(url_for('wlasciciele'))
            else:
                return render_template('Pop-up.html', data=variables.last_page[1:],
                                title=variables.last_page[0], ile=3, error=error)
        elif tabelka == 'silownie':
            error = sprawdz_silownie(odczytane)
            if error == None:
                dodaj_silownie(odczytane)
                print(tabelka, flush=True)
                return redirect(url_for('silownie'))
            else:
                return render_template('Pop-up-1.html', data=variables.last_page[1:],
                                       etaty=wybierz_pesele_wlascicieli(), label="Pesel wlasciciela: ",
                                       title=variables.last_page[0], error=error, ile=2)
        print(tabelka, flush=True)

    # if "sprzety" == tabelka:
    #     return render_template('Pop-up.html', data=variables.last_page[1:5], title=variables.last_page[0], error=error)
    # elif tabelka == "szafki":
    #     return render_template('Pop-up.html', data=variables.last_page[6:8], title=variables.last_page[5], error=error)
    # else:
    #     return render_template('Pop-up.html', data=variables.last_page[1:], title=variables.last_page[0], error=error)
@app.route('/wroc')
def wroc():
    print()
    if variables.last_page[0] == 'Pracownika':
        return redirect(url_for('pracownicy'))
    elif variables.last_page[0]  == 'Klubowicza':
        return redirect(url_for('klubowicze'))
    elif variables.last_page[0]  == 'Sprzęty':
        return redirect(url_for('szafki'))
    elif variables.last_page[0]  == 'Pomieszczenie':
        return redirect(url_for('pomieszczenia'))
    elif variables.last_page[0]  == 'Plan treningowy':
        return redirect(url_for('plany_treningowe'))
    elif variables.last_page[0]  == 'Grupę':
        return redirect(url_for('grupy'))
    elif variables.last_page[0]  == 'Właściciele':
        return redirect(url_for('wlasciciele'))
    elif variables.last_page[0]  == 'Siłownie':
        return redirect(url_for('silownie'))


@app.route('/dodaj/<tabelka>')
def dodaj(tabelka):
    if tabelka == "pracownicy":
        return render_template('Pop-up-1.html', data=variables.last_page[1:], etaty=wybierz_etaty(), label="Etat: ",
                               title=variables.last_page[0], ile=len(variables.last_page)-1)
    if "sprzety" == tabelka:
        return render_template('Pop-up-1.html', data=variables.last_page[1:5], title=variables.last_page[0], etaty=wybierz_sale(), label="Sala ćwiczeniowa: ", ile=4)
    elif tabelka == "szafki":
        return render_template('Pop-up-1.html', data=variables.last_page[6:8], title=variables.last_page[5], etaty=wybierz_szatnie(), label="Szatnia: ", ile=2)
    elif tabelka == "pomieszczenia":
        return render_template('Pop-up-1.html', data=variables.last_page[1:], ile=len(variables.last_page)-1, title=variables.last_page[0], etaty=wybierz_typ_pomieszczenia(), label="Rodzaj pomieszczenia: ")
    elif tabelka == "plany_treningowe":
        return render_template('Pop-up-1.html', ile=len(variables.last_page)-1, data=variables.last_page[1:], title=variables.last_page[0],
                               etaty=wybierz_pesel_trenerow(), label="Pesel trenera: ", )
    elif tabelka == "silownie":
        return render_template('Pop-up-1.html', data=variables.last_page[1:],
                               etaty=wybierz_pesele_wlascicieli(), label="Pesel wlasciciela: ",
                               title=variables.last_page[0], ile=3)
    elif "grupy_zorganizowane" == tabelka:
        return render_template('Pop-up-2.html', data=variables.last_page[1:5], title=variables.last_page[0],  pesel=wybierz_pesel_trenerow(), sale=wybierz_sale())


    else:
        return render_template('Pop-up.html', data=variables.last_page[1:], title=variables.last_page[0])


@app.route('/czytajFiltr/<tabelka>', methods=["POST"])
def filtr(tabelka):
    if tabelka == "pracownicy":
        if request.method == 'POST':
            wartosc = request.form["wartosc"]
            poczym = request.values.get("sortujpo")
            print(poczym)
            print(filtruj_pracownicy(poczym, wartosc))
            if filtruj_pracownicy(poczym, wartosc) == None:
                return redirect(url_for('pracownicy'))# TODO - error - jak w pomieszczeniach + napisac errora gdy zwracane jest 0 wierszy
            else:
                return render_template('static_pracownicy.html', data=filtruj_pracownicy(poczym, wartosc), names=column_pracownicy(),
                               etaty=wybierz_etaty(), numery_pomieszczen=wybierz_pomieszczenia(), gymname = variables.nazwaSilowni)
    elif tabelka == "klubowicze":
        if request.method == 'POST':
            wartosc = request.form["wartosc"]
            poczym = request.values.get("sortujpo")
            print(poczym)
            print(filtruj_klubowicz(poczym, wartosc))
            if filtruj_klubowicz(poczym, wartosc) == None:
                return redirect(url_for('klubowicze'))# TODO - error - jak w pomieszczeniach + napisac errora gdy zwracane jest 0 wierszy
            else:
                return render_template('static_klubowicze.html', data=filtruj_klubowicz(poczym, wartosc), names=column_klubowicze_karnety(), gymname = variables.nazwaSilowni)
    elif tabelka == "pomieszczenia":
        if request.method == 'POST':
            wartosc = request.form["wartosc"]
            poczym = request.values.get("sortujpo")
            print(poczym)
            print(filtruj_pomieszczenia(poczym, wartosc))
            if filtruj_pomieszczenia(poczym, wartosc) == None:
                return redirect(url_for('pomieszczenia'))# TODO - error - jak w pomieszczeniach + napisac errora gdy zwracane jest 0 wierszy
            else:
                return render_template('static_pomieszczenia.html', data=filtruj_pomieszczenia(poczym, wartosc), names=column_pomieszczenia(), typy_pomieszczen = wybierz_typ_pomieszczenia(), gymname = variables.nazwaSilowni)
    elif tabelka == "plany_treningowe":
        if request.method == 'POST':
            wartosc = request.form["wartosc"]
            poczym = request.values.get("sortujpo")
            print(poczym)
            # print(filtruj(poczym, wartosc))
            if filtruj_plany(poczym, wartosc) == None:
                return redirect(url_for('plany_treningowe'))
            else:
                return render_template('static_plany.html', data=filtruj_plany(poczym, wartosc), names=column_plany(), gymname = variables.nazwaSilowni)
    elif tabelka == "grupy":
        if request.method == 'POST':
            wartosc = request.form["wartosc"]
            poczym = request.values.get("sortujpo")
            print(poczym)
            if filtruj_grupy(poczym, wartosc) == None:
                return redirect(url_for('grupy'))
            else:
                return render_template('static_grupy.html', data=filtruj_grupy(poczym, wartosc), names=column_grupy(), gymname = variables.nazwaSilowni)
    elif tabelka == "sprzety":
        if request.method == 'POST':
            wartosc = request.form["wartosc1"]
            poczym = request.values.get("sortujpo")
            print(poczym)
            if filtruj_sprzety(poczym, wartosc) == None:
                return redirect(url_for('szafki'))
            else:
                return render_template('static_double_table.html', data=filtruj_sprzety(poczym, wartosc), gymname = variables.nazwaSilowni, names=read_column_adr('SPRZETY'), data2=read_table_adr('SZAFKI'), names2=read_column_adr('SZAFKI'))
    elif tabelka == "szafki":
        if request.method == 'POST':
            wartosc = request.form["wartosc2"]
            poczym = request.values.get("sortujpo")
            print(poczym)
            if filtruj_szafki(poczym, wartosc) == None:
                return redirect(url_for('szafki'))
            else:
                return render_template('static_double_table.html', data=read_table_adr('SPRZETY'),
                               names=read_column_adr('SPRZETY'), data2=filtruj_szafki(poczym, wartosc), gymname = variables.nazwaSilowni, names2=read_column_adr('SZAFKI'))
    elif tabelka == "wlasciciele":
        if request.method == 'POST':
            wartosc = request.form["wartosc"]
            poczym = request.values.get("sortujpo")
            print(poczym)
            print(filtruj_wlasciciele(poczym, wartosc))
            if filtruj_wlasciciele(poczym, wartosc) == None:
                return redirect(url_for('wlasciciele'))
            else:
                return render_template('static_wlasciciele.html', data=filtruj_wlasciciele(poczym, wartosc), names=column_wlasciciele())
    elif tabelka == "silownie":
        if request.method == 'POST':
            wartosc = request.form["wartosc"]
            poczym = request.values.get("sortujpo")
            print(poczym)
            print(filtruj_silownie(poczym, wartosc))
            if filtruj_silownie(poczym, wartosc) == None:
                return redirect(url_for('silownie'))
            else:
                return render_template('static_silownie.html', data=filtruj_silownie(poczym, wartosc),
                                   names=column_silownie(), pesele_wlascicieli=wybierz_pesel_wlascicieli())


@app.route('/klubowicze-w-grupie/<id_grupy>')
def klubowicze_w_grupie(id_grupy):
    variables.last_page = ['Klubowicza', 'PESEL', 'NAZWISKO', 'ZNIŻKA (%)']
    return render_template('klubowicze_w_grupie.html', data=read_klubowicze_f_id_grupy(id_grupy), names=column_klubowicze_karnety(), gymname = variables.nazwaSilowni, id_grupy=id_grupy)


@app.route('/usun-klubowicz-grupa/<pesel>/<grupa>')
def usun_klubowicz_grupa(pesel, grupa):
    usun_klubowicza_z_grupy(grupa, pesel)
    return render_template('h_klubowicze.html', data=read_klubowicze_karnety(), names=column_klubowicze_karnety(), gymname = variables.nazwaSilowni)

@app.route('/usun-klubowicz-plan/<pesel>/<grupa>')
def usun_klubowicz_plan(pesel, grupa):
    usun_klubowicza_z_planu(grupa, pesel)
    return render_template('h_klubowicze.html', data=read_klubowicze_karnety(), names=column_klubowicze_karnety(), gymname = variables.nazwaSilowni)


@app.route('/klubowicze-cwiczacy-z-planem/<nr_planu>')
def klubowicze_cwiczacy_z_planem(nr_planu):
    variables.last_page = ['Klubowicza', 'PESEL', 'NAZWISKO', 'ZNIŻKA (%)']
    return render_template('klubowicze_z_planem.html', data=read_klubowicze_f_plan(nr_planu), names=column_klubowicze_karnety(), gymname = variables.nazwaSilowni, nr_planu=nr_planu)


@app.route('/pracownicy', methods=["POST"])
def pracownicyp():
    if request.method == 'POST':
        print("xd", flush=True)
        odczytane = []
        for i in range(8):
            odczytane.append(request.form[str(i)])
        print(odczytane, flush=True)
        error = check_upd_pracownicy(odczytane)
        # error = sprawdz_update_pracownicy(odczytane)
        if error == None:
            update_pracownicy(odczytane)
    return render_template('h_pracownicy.html', data=read_pracownicy(), names=column_pracownicy(),
                           gymname=variables.nazwaSilowni, etaty=wybierz_etaty(),
                           numery_pomieszczen=wybierz_pomieszczenia(), error=error)


@app.route('/pracownicy')
def pracownicy():
    variables.last_page = ['Pracownika', 'PESEL', 'IMIE', 'NAZWISKO', 'PENSJA', 'ETAT']
    return render_template('h_pracownicy.html', data=read_pracownicy(), gymname = variables.nazwaSilowni, names=column_pracownicy(), etaty=wybierz_etaty(), numery_pomieszczen = wybierz_pomieszczenia())




@app.route('/klubowicze')
def klubowicze():
    variables.last_page = ['Klubowicza', 'PESEL', 'NAZWISKO', 'ZNIŻKA']
    return render_template('h_klubowicze.html', data=read_klubowicze_karnety(), names=column_klubowicze_karnety(), gymname = variables.nazwaSilowni)

@app.route('/klubowicze', methods=["POST"])
def klubowiczep():
    if request.method == 'POST':

        odczytane = []
        for i in range(6):
            odczytane.append(request.form[str(i)])
        print(odczytane, flush=True)
        error = check_upd_klubowicze(odczytane)
        if error == None:
            update_klubowicze(odczytane)
    return render_template('h_klubowicze.html', data=read_klubowicze_karnety(), names=column_klubowicze_karnety(), gymname = variables.nazwaSilowni, error=error)

@app.route('/sprzet')
def szafki():
    variables.last_page = ['Sprzęty', 'Numer urządzenia', 'Rodzaj', 'Stanowisko', 'Numer sali',  'Szafki', 'Ilosc szafek', 'Nr pomieszczenia']
    return render_template('h_double_table.html', data=read_table_adr('SPRZETY'), gymname = variables.nazwaSilowni, names=read_column_adr('SPRZETY'), data2=read_table_adr('SZAFKI'), names2=read_column_adr('SZAFKI'))
#   return render_template('h_double_table.html', data=read_sprzet_rodzaj('bieznia'), names=read_column_adr('SPRZETY'), data2=read_table_adr('SZAFKI'), names2=read_column_adr('SZAFKI'))

@app.route('/sprzet', methods=["POST"])
def sprzetp():
    if request.method == 'POST':
        sprzety_nowe = []
        szafki_nowe = []
        for i in range(4):
            sprzety_nowe.append(request.form[str(i)])
        error = check_upd_sprzety(sprzety_nowe)
        if error == None:
            update_sprzety(sprzety_nowe)
        # for i in range(2):
        #     if request.form['s'+str(i)]:
        #         szafki_nowe.append(request.form['s'+str(i)])

    return render_template('h_double_table.html', data=read_table_adr('SPRZETY'), gymname = variables.nazwaSilowni, names=read_column_adr('SPRZETY'), data2=read_table_adr('SZAFKI'), names2=read_column_adr('SZAFKI'),error=error)

@app.route('/pomieszczenie')
def pomieszczenia():
    variables.last_page = ['Pomieszczenie', 'Nr pomieszczenia', 'Pietro', 'Powierzchnia', 'Rodzaj']

    return render_template('h_pomieszczenia.html', data=read_pomieszczenia(), gymname = variables.nazwaSilowni, names=column_pomieszczenia(), typy_pomieszczen = wybierz_typ_pomieszczenia() , error=variables.pomieszczenia_error)

@app.route('/pomieszczenie', methods=["POST"])
def pomieszczeniap():
    if request.method == 'POST':
        odczytane = []
        for i in range(4):
            odczytane.append(request.form[str(i)])
        print(odczytane, flush=True)
        error = check_upd_pomieszczenia(odczytane)
        if error == None:
            error = update_pomieszczenia(odczytane)
        return render_template('h_pomieszczenia.html', data=read_pomieszczenia(), gymname = variables.nazwaSilowni, typy_pomieszczen = wybierz_typ_pomieszczenia(), names=column_pomieszczenia(), error=error)
@app.route('/plany_treningowe')
def plany_treningowe():
    variables.last_page = ['Plan treningowy', 'OPIS', 'pesel trenera']
    return render_template('h_plany.html', data=read_plany(), names=column_plany(), gymname = variables.nazwaSilowni)

@app.route('/plany_treningowe', methods=["POST"])
def plany_treningowep():
    if request.method == 'POST':
        odczytane = []
        for i in range(4):
            odczytane.append(request.form[str(i)])
        print(odczytane, flush=True)
        error = check_upd_plany(odczytane)
        if error == None:
            update_plany_treningowe(odczytane)
    return render_template('h_plany.html', data=read_plany(), names=column_plany(), gymname = variables.nazwaSilowni, error=error)


@app.route('/grupy')
def grupy():
    variables.last_page = ['Grupę', 'TERMIN SPOTKANIA', 'PESEL TRENERA', 'nr_sali']
    return render_template('h_grupy.html', data=read_grupy(), names=column_grupy(), sale=wybierz_sale(), gymname = variables.nazwaSilowni)

@app.route('/grupy', methods=["POST"])
def grupyp():
    if request.method == 'POST':
        odczytane = []
        for i in range(5):
            odczytane.append(request.form[str(i)])
        print(odczytane, flush=True)
        error = check_upd_grupy(odczytane)
        if error == None:
            update_grupy(odczytane)
    return render_template('h_grupy.html', data=read_grupy(), names=column_grupy(), sale=wybierz_sale(), gymname = variables.nazwaSilowni,error=error)


@app.route('/wlasciciele')
def wlasciciele():
    variables.last_page = ['Właściciele', 'Pesel', 'Imie', 'Nazwisko', 'Pensja']
    return render_template('h_wlasciciele.html', data=read_wlasciciele(), names=column_wlasciciele(), error=variables.wlasciciele_error)

@app.route('/wlasciciele', methods=["POST"])
def wlascicielep():
    if request.method == 'POST':
        odczytane = []
        for i in range(6):
            odczytane.append(request.form['s'+str(i)])
        print(odczytane, flush=True)
    error = check_upd_wlasciciele(odczytane)
    if error == None:
        update_wlasciciele(odczytane)
    return render_template('h_wlasciciele.html', data=read_wlasciciele(), names=column_wlasciciele(),error=error)

@app.route('/silownie')
def silownie():
    variables.last_page = ['Siłownie', 'Adres', 'Nazwa', 'Pesel właściciela']
    print(wybierz_pesel_wlascicieli())
    return render_template('h_silownie.html', data=read_silownie(), names=column_silownie(), pesele_wlascicieli=wybierz_pesel_wlascicieli())

@app.route('/silownie', methods=["POST"])
def silowniep():
    if request.method == 'POST':
        odczytane = []
        for i in range(3):
            odczytane.append(request.form[str(i)])
        print(odczytane, flush=True)
        error = check_upd_silownie(odczytane)
        if error == None:
            update_silownie(odczytane)
    return render_template('h_silownie.html', data=read_silownie(), names=column_silownie(), pesele_wlascicieli=wybierz_pesel_wlascicieli(), error=error)
#---------------------------- usuwanie ------------------------------

@app.route('/delete/<tabelka>/<klucz>')
def usuwanie(tabelka, klucz):
    print('Usuwamy z ', tabelka, flush=True)
    if tabelka == "pracownicy":
        usun_pracownicy(klucz)
        return redirect(url_for('pracownicy'))

    elif tabelka == "plany_treningowe":
        usun_plany(klucz)
        return redirect(url_for('plany_treningowe'))

    elif tabelka == "grupy":
        usun_grupy(klucz)
        return redirect(url_for('grupy'))

    elif tabelka == 'klubowicze':
        usun_klubowicze(klucz)
        return redirect(url_for('klubowicze'))

    elif tabelka == 'wlasciciele':
        variables.wlasciciele_error = None
        variables.wlasciciele_error = sprawdz_czy_wlasciciel(klucz)
        if variables.wlasciciele_error == None:
            usun_wlasciciele(klucz)
        return redirect(url_for('wlasciciele'))
    elif tabelka == 'silownie':
        usun_silownie(klucz)
        return redirect(url_for('silownie'))



@app.route('/delete/<tabelka>/<klucz1>/<klucz2>')
def usuwanie2(tabelka, klucz1, klucz2):
    if tabelka == "szafki":
        usun_szafki(klucz1, klucz2)
        return redirect(url_for('szafki'))

    elif tabelka == "sprzety":
        usun_sprzety(klucz1, klucz2)
        print("usuwam sprzet", flush=True)
        return redirect(url_for('szafki'))

    elif tabelka == "pomieszczenia":
        variables.pomieszczenia_error = None
        variables.pomieszczenia_error = sprawdz_czy_pracownicy(klucz1, klucz2)
        if variables.pomieszczenia_error != None:
            return redirect(url_for('pomieszczenia'))
        print("tu", flush=True)
        usun_pomieszczenia(klucz1, klucz2)
        return redirect(url_for('pomieszczenia'))

#---------------------------- logowanie ------------------------------
@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    variables.wybranaSilownia = ''
    if request.method == 'POST':
        if request.form['password'] != 'admin':
            error = 'Podano nieprawidłowe dane!'
        elif request.form['gymname'] == 'admin':
            return redirect(url_for('wlasciciele'))
        else:
            variables.nazwaSilowni = request.form['gymname']
            # print("asd", variables.wybranaSilownia, flush=True)
            cursor = variables.cnxn.cursor()
            select_name = """SELECT ADRES FROM SILOWNIE WHERE NAZWA = :nazwa_silowni"""
            cursor.prepare(select_name)
            cursor.execute(None, nazwa_silowni=variables.nazwaSilowni)
            for item in cursor:
                variables.wybranaSilownia = item[0]
            if variables.wybranaSilownia == '':
                return render_template('login.html', error='Podana siłownia nie istnieje')
            cursor.close()
            print('NAZWA: ', variables.nazwaSilowni, 'ADRES: ', variables.wybranaSilownia, flush = True)
            return redirect(url_for('pracownicy'))
    return render_template('login.html', error=error)

#---------------------------- main ------------------------------
if __name__ == '__main__':
    # connect_to_database()
    app.run(debug=True)


