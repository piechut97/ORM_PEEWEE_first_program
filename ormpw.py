#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from peewee import *
from pobieranie_danych import pobierz_dane

if os.path.exists('test.db'):
    os.remove('test.db')
# tworzymy instancję bazy używanej przez modele
baza = SqliteDatabase('test.db')  # ':memory:'


class BazaModel(Model):  # klasa bazowa
    class Meta:
        database = baza

# klasy Klasa i Uczen opisują rekordy tabel "klasa" i "uczen"
# oraz relacje między nimi
class Klasa(BazaModel):
    nazwa = CharField(null=False)
    profil = CharField(default='')


class Uczen(BazaModel):
    imie = CharField(null=False)
    nazwisko = CharField(null=False)
    klasa = ForeignKeyField(Klasa, related_name='uczniowie')


baza.connect()  # nawiązujemy połączenie z bazą
baza.create_tables([Klasa, Uczen], safe = True)  # tworzymy tabele

# dodajemy dwie klasy, jeżeli tabela jest pusta
if Klasa().select().count() == 0:
    inst_klasa = Klasa(nazwa='1A', profil='matematyczny')
    inst_klasa.save()
    inst_klasa = Klasa(nazwa='1B', profil='humanistyczny')
    inst_klasa.save()

# tworzymy instancję klasy Klasa reprezentującą klasę "1A"
inst_klasa = Klasa.select().where(Klasa.nazwa == '1A').get()

# lista uczniów, których dane zapisane są w słownikach
uczniowie = [
    {'imie': 'Tomasz', 'nazwisko': 'Nowak', 'klasa': inst_klasa},
    {'imie': 'Jan', 'nazwisko': 'Kos', 'klasa': inst_klasa},
    {'imie': 'Piotr', 'nazwisko': 'Kowalski', 'klasa': inst_klasa}
]

# dodajemy dane wielu uczniów
Uczen.insert_many(uczniowie).execute()

# odczytujemy dane z bazy


def czytajdane():
    for uczen in Uczen.select().join(Klasa):
        print(uczen.id, uczen.imie, uczen.nazwisko, uczen.klasa.nazwa)
    print()


czytajdane()

# zmiana klasy ucznia o identyfikatorze 2
inst_uczen = Uczen().select().join(Klasa).where(Uczen.id == 2).get()
inst_uczen.klasa = Klasa.select().where(Klasa.nazwa == '1B').get()
inst_uczen.save()  # zapisanie zmian w bazie

# usunięcie ucznia o identyfikatorze 3
Uczen.select().where(Uczen.id == 3).get().delete_instance()

czytajdane()


#dodawanie rekordów odczytanych z pliku
uczniowie = (pobierz_dane('C:\\Users\\Marcin\\Documents\\Python\\bazy danych\\uczniowie.csv'))

Uczen.insert_many(uczniowie).execute()

czytajdane()

while True:
    print("1. Wypisanie rekordów znajdujących się w bazie danych")
    print("2. Dodanie rekordu do bazy danych ")
    print("3. Zmodyfikowanie rekordów w bazie danych")
    print("4. Usunięcie rekordu z bazy")
    print("5. Koniec programu")
    menu = str(input("Podaj cyfrę z menu, aby wybrać co chcesz zrobić: "))

    if menu == "1":
        czytajdane()

    elif menu == "2":
        rekord = input("Po przecinku podaj dane do dodania do bazy ")
        rekord = tuple(map(str, rekord.split(", ")))
        if rekord[2] == '1A':
            class_id = '1'
        elif rekord[2] == "1B":
            class_id = '2'
        else:
            class_id = rekord[2]
        new_uczen = Uczen(imie = rekord[0], nazwisko = rekord[1], klasa = class_id)
        new_uczen.save()

    elif menu == "3":
        while True:
            print("Menu modyfikacji rekordu:")
            print("1. Zmiana imienia")
            print("2. Zmiana nazwiska")
            print("3. Zmiana klasy")
            print("4. Wyjście z menu modyfikacji rekordu")

            modd = str(input("Co chcesz zrobić? "))

            if modd == "1":
                new_name = str(input("Podaj nowe imie "))
                index = int(input("Podaj numer rekordu ucznia do zmiany imienia: "))
                change_uczen = Uczen().select().where(Uczen.id == index).get()
                change_uczen.imie = new_name
                change_uczen.save()

            elif modd == "2":
                new_name = str(input("Podaj nowe nazwisko "))
                index = int(input("Podaj numer rekordu ucznia do zmiany nazwiska: "))
                change_uczen = Uczen().select().where(Uczen.id == index).get()
                change_uczen.nazwisko = new_name
                change_uczen.save()

            elif modd == "3":
                new_name = str(input("Podaj nowa klase "))
                index = int(input("Podaj numer rekordu ucznia do zmiany klasy: "))
                change_uczen = Uczen().select().join(Klasa).where(Uczen.id == index).get()
                change_uczen.klasa = Klasa.select().where(Klasa.nazwa == new_name)
                change_uczen.save()

            elif modd == "4":
                break
            break
    elif menu == "4":
        indeks = input("Podaj indeks ucznia do usuniecia: ")
        Uczen.select().where(Uczen.id == indeks).get().delete_instance()
    elif menu == "5":
        print("Koniec programu!!!")
        baza.close()
        exit()
    else:
        print("Błąd danych!! Podaj poprawne dane!")
