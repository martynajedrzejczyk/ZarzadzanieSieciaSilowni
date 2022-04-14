drop package SilowniaPackage;
drop table Cwicza_z_planem;
drop table Przynaleznosci_Klubowiczow_Do_grup;
drop table Sprzety;
drop table Szafki;
drop table Klubowicze cascade constraints;
drop table Plany_treningowe;
drop table Grupy_zorganizowane;
drop table Karnety cascade constraints;
drop table Trenerzy;
drop table Sprzatacze;
drop table Recepcjonisci;
drop table Kantorki;
drop table Sale_cwiczeniowe;
drop table Recepcje;
drop table Szatnie;
drop table Silownie;
drop table Wlasciciele;
drop sequence id_nr_kart;
drop sequence id_nr_planu;
drop sequence id_nr_grupy;

drop view pracownicy_perspektywa;
drop view pomieszczenia_perspektywa;

create sequence id_nr_kart start with 1 increment by 1;
create sequence id_nr_planu start with 1 increment by 1;
create sequence id_nr_grupy start with 1 increment by 1;

create table Wlasciciele (
    pesel NUMBER(11) PRIMARY KEY,
    imie VARCHAR2(15) not null,
    nazwisko VARCHAR2(15) not null,
    data_zatrudnienia DATE default current_date not null,
    pensja NUMBER(7,2) not null,
    premia NUMBER(7,2) null
); 

create table Silownie (
    adres VARCHAR2(50) not null, 
    nazwa VARCHAR2(30) not null,
    pesel_wlasciciela NUMBER(11) references Wlasciciele(pesel) not null unique,
    PRIMARY KEY(adres)
);

create table Kantorki (
    nr_pomieszczenia NUMBER(3) not null,
    pietro NUMBER(2) not null,
    powierzchnia NUMBER(5,2),
    adres_silowni VARCHAR2(50),
    
    foreign key(adres_silowni) references Silownie(adres),
    primary key(nr_pomieszczenia, adres_silowni)
);

create table Sale_cwiczeniowe (
    nr_pomieszczenia NUMBER(3) not null,
    pietro NUMBER(2) not null,
    powierzchnia NUMBER(5,2) not null,
    adres_silowni VARCHAR2(50) not null,
    
    foreign key(adres_silowni) references Silownie(adres),
    primary key(nr_pomieszczenia, adres_silowni)
); 

create table Recepcje (
    nr_pomieszczenia NUMBER(3) not null,
    pietro NUMBER(2) not null,
    powierzchnia NUMBER(5,2) not null,
    adres_silowni VARCHAR2(50) not null,
    
    foreign key(adres_silowni) references Silownie(adres),
    primary key(nr_pomieszczenia, adres_silowni)
);

create table Szatnie (
    nr_pomieszczenia NUMBER(3),
    pietro NUMBER(2) not null,
    powierzchnia NUMBER(5,2) not null,
    adres_silowni VARCHAR2(50) not null,
    
    foreign key(adres_silowni) references Silownie(adres),
    primary key(nr_pomieszczenia, adres_silowni)
);  


create table Trenerzy (
    pesel NUMBER(11),
    imie VARCHAR2(15) not null,
    nazwisko VARCHAR2(15) not null,
    data_zatrudnienia DATE default current_date,
    pensja NUMBER(7,2) not null,
    premia NUMBER(7,2) null,

    adres_silowni  VARCHAR2(50) not null, 
     foreign key(adres_silowni) 
    references Silownie(adres),

    primary key(pesel)
); 

create table Sprzatacze (
    pesel NUMBER(11),
    imie VARCHAR2(15) not null,
    nazwisko VARCHAR2(15) not null,
    data_zatrudnienia DATE default current_date,
    pensja NUMBER(7,2) not null,
    premia NUMBER(7,2) null,

    nr_kantorka NUMBER(3) not null,
    adres_silowni VARCHAR2(50) not null,
    foreign key(nr_kantorka, adres_silowni) references Kantorki(nr_pomieszczenia, adres_silowni),

    adres_silowni_s VARCHAR2(50) not null,
    foreign key(adres_silowni_s) references Silownie(adres),

    primary key(pesel)
);

create table Recepcjonisci (
    pesel NUMBER(11),
    imie VARCHAR2(15) not null,
    nazwisko VARCHAR2(15) not null,
    data_zatrudnienia DATE default current_date,
    pensja NUMBER(7,2) not null,
    premia NUMBER(7,2) null,

    nr_recepcji NUMBER(3) not null,
    adres_silowni VARCHAR2(50) not null,
    foreign key(nr_recepcji, adres_silowni) references Recepcje(nr_pomieszczenia, adres_silowni),

    adres_silowni_zatrudniony VARCHAR2(50) not null, 
    foreign key(adres_silowni_zatrudniony) references Silownie(adres),

    primary key(pesel)
);

create table Karnety (
    nr_karty number(10) default id_nr_kart.nextval PRIMARY KEY, 
    wazna_od date not null,
    wazna_do date not null,
    znizka NUMBER(3) null,
    pesel_klubowicza number(11) unique not null 
);

create table Klubowicze (
    pesel number(11) PRIMARY KEY,
    nazwisko VARCHAR2(15) not null,
    nr_karty number(10) unique,
    constraint fk_nrkarty foreign key (nr_karty) references Karnety(nr_karty) on delete cascade
);  

alter table Karnety add constraint klucz_obcy_karnety_z_klubowiczow  foreign key (pesel_klubowicza) references Klubowicze(pesel) on delete cascade;

create table Plany_treningowe (
    nr_planu NUMBER(3) default id_nr_planu.nextval, --SEKWENCJA
    opis VARCHAR2(60) null,

    pesel_trenera NUMBER(11) not null,
    foreign key(pesel_trenera)
    references Trenerzy(pesel),

    primary key(nr_planu)
); 

create table Grupy_zorganizowane (
    id_grupy number(10) default id_nr_grupy.nextval PRIMARY KEY,
    termin_spotkania DATE not null,
    pesel_trenera NUMBER(11) not null, 

    foreign key(pesel_trenera) references Trenerzy(pesel),

    nr_sali NUMBER(3) not null, 
    adres_silowni VARCHAR2(50) not null,

    foreign key(nr_sali, adres_silowni)
    references Sale_cwiczeniowe(nr_pomieszczenia, adres_silowni)
);

alter table Grupy_zorganizowane add constraint unikalne1 unique(pesel_trenera, termin_spotkania, nr_sali, adres_silowni);

create table Sprzety (
    nr_urzadzenia NUMBER(6) not null,
    rodzaj VARCHAR2(30) not null,
    stanowisko NUMBER(6) not null,
    nr_sali NUMBER(3) not null,
    adres_silowni VARCHAR2(50) not null,
    
    foreign key(nr_sali, adres_silowni) 
    references Sale_cwiczeniowe(nr_pomieszczenia, adres_silowni),
    primary key(nr_urzadzenia, nr_sali, adres_silowni)
);  

create table Szafki (
    nr_szafki NUMBER(4) not null,
    nr_szatni NUMBER(3) not null, 
    adres_silowni VARCHAR2(50) not null, 
    
    foreign key(nr_szatni, adres_silowni) 
    references Szatnie(nr_pomieszczenia,adres_silowni),
    primary key(nr_szafki, nr_szatni, adres_silowni)
);  

create table Cwicza_z_planem (
    pesel_klubowicza NUMBER(11) references Klubowicze(pesel) on delete cascade,

    nr_planu NUMBER(3) not null, 
    foreign key(nr_planu)
    references Plany_treningowe(nr_planu),
    primary key(pesel_klubowicza, nr_planu)
);

create table Przynaleznosci_Klubowiczow_Do_grup (
    id_grupy NUMBER(10) references Grupy_zorganizowane(id_grupy),
    
    pesel_klubowicza NUMBER(11) references Klubowicze(pesel) on delete cascade,

    primary key(pesel_klubowicza, id_grupy)
);  

create or replace view pomieszczenia_perspektywa as
select nr_pomieszczenia, pietro, powierzchnia, adres_silowni, 'Kantorek' as typ from kantorki union all
select nr_pomieszczenia, pietro, powierzchnia, adres_silowni, 'Sala ćwiczeniowa' as typ from Sale_cwiczeniowe  union all
select nr_pomieszczenia, pietro, powierzchnia, adres_silowni, 'Recepcja' as typ from Recepcje  union all
select nr_pomieszczenia, pietro, powierzchnia, adres_silowni, 'Szatnia' as typ from Szatnie;


create or replace view pracownicy_perspektywa as
    SELECT pesel, imie, nazwisko, data_zatrudnienia, pensja, premia, nr_recepcji as nr_pomieszczenia, adres_silowni, 'Recepcjonista' as etat  FROM recepcjonisci   union all
    SELECT pesel, imie, nazwisko, data_zatrudnienia, pensja, premia, nr_kantorka as nr_pomieszczenia, adres_silowni, 'Sprzątacz' as etat  FROM  sprzatacze union all
    SELECT pesel, imie, nazwisko, data_zatrudnienia, pensja, premia, NULL as nr_pomieszczenia, adres_silowni, 'Trener' as etat  FROM trenerzy union all 
    select pesel, imie, nazwisko, data_zatrudnienia, pensja, premia, NULL as nr_pomieszczenia, null as adres_silowni, 'Wlasciciel' as etat  FROM wlasciciele;

CREATE OR REPLACE PACKAGE SilowniaPackage is
    procedure DodajSzafki
    (ileSzafek NATURAL, numerSzatni NUMBER, adresSilowni VARCHAR);
    procedure PodwyzkaEtat
    (procent number, etat varchar);
    function IlePracownikow
    (stanowisko VARCHAR, adres VARCHAR) return NUMBER; liczba NUMBER;
end SilowniaPackage;

CREATE OR REPLACE PACKAGE BODY SilowniaPackage IS
    function IlePracownikow (stanowisko VARCHAR, adres VARCHAR) return number is
    begin
        case 
            when stanowisko = 'Recepcjonisci' then
                select count(*) into liczba from Recepcjonisci where adres_silowni = adres ;
            when stanowisko = 'Trenerzy' then
                select count(*) into liczba from Trenerzy where adres_silowni = adres ;
            when stanowisko = 'Sprzatacze' then
                select count(*) into liczba from Sprzatacze where adres_silowni = adres ;
            else select 0 into liczba from dual;
        end case;
        return liczba;
    end IlePracownikow;
    procedure DodajSzafki (ileSzafek NATURAL, numerSzatni NUMBER, adresSilowni VARCHAR) is
    i number; minSzafka number;
    begin
        select max(nr_szafki) into minSzafka from Szafki where nr_szatni = numerSzatni and adresSilowni = adres_silowni;
        minSzafka := minSzafka + 1;
        i := ileSzafek;
        while i > 0  loop 
            insert into Szafki (nr_szafki, nr_szatni, adres_silowni) values
            (minSzafka, numerSzatni, adresSilowni);
            i := i - 1;
            minSzafka := minSzafka + 1;
        end loop;
    end DodajSzafki;
    procedure PodwyzkaEtat (procent number, etat varchar) is
    begin
        case etat
            when 'Wlasciciele' then
                update Wlasciciele set pensja = pensja + 0.01*procent*pensja;
            when 'Recepcjonisci' then
                update Recepcjonisci set pensja = pensja + 0.01*procent*pensja;
            when 'Trenerzy' then
                update Trenerzy set pensja = pensja + 0.01*procent*pensja;
            when 'Sprzatacze' then
                update Sprzatacze set pensja = pensja + 0.01*procent*pensja;
            end case;
    end PodwyzkaEtat;
end SilowniaPackage;

commit;



