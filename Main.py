import PySimpleGUI as sg
import sqlite3
import sys
import os
from cryptography.fernet import Fernet
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class Cipher:
    def __init__(self):
        self.key = Fernet.generate_key().decode()
        self.conn = sqlite3.connect("PyBot.db")
        self.cur = self.conn.cursor()
        self.create_cipher_table()
        self.insert_key()

    def create_cipher_table(self):
        self.cur.execute("CREATE TABLE IF NOT EXISTS Cipher (Key TEXT)")

    def insert_key(self):
        self.cur.execute("INSERT INTO Cipher (Key) VALUES (?)", (self.key,))
        self.conn.commit()
        self.conn.close()

class SQLite:
    def __init__(self, database_path):
        self.conn = sqlite3.connect(database_path)
        self.cur = self.conn.cursor()
        self.create_billing_table()

    def create_billing_table(self):
        self.cur.execute("CREATE TABLE IF NOT EXISTS Billing (CardNumber TEXT, ExpDate TEXT, CVV TEXT, Name TEXT, Street TEXT, City TEXT, State TEXT)")

    def save_billing(self, billing):
        self.cur.execute("INSERT INTO Billing (CardNumber, ExpDate, CVV, Name, Street, City, State) VALUES (?, ?, ?, ?, ?, ?, ?)", billing)
        self.conn.commit()

class GUI:
    def __init__(self):
        self.window = None

    def create_main_window(self):
        layout = [
            [sg.Text("Website"), sg.Input(key="-WEBSITE-")],
            [sg.Button("Start Bot"), sg.Button("Options")]
        ]
        self.window = sg.Window("Py Bot", layout)

    def create_options_window(self):
        layout = [
            [sg.Text("Provided information will be saved locally only, if selected to.")],
            [sg.Text("Card Number"), sg.Input(key="-CARD-")],
            [sg.Text("Exp Date"), sg.Input(key="-EXPDATE-"), sg.Text("CVV"), sg.Input(key="-CVV-")],
            [sg.Text("Name on Card"), sg.Input(key="-NAME-")],
            [sg.Text("Street Address"), sg.Input(key="-STREET-")],
            [sg.Text("City"), sg.Input(key="-CITY-")],
            [sg.Text("State"), sg.Input(key="-STATE-")],
            [sg.CheckBox("Save Information for future use", key="-SAVEINFO-")],
            [sg.Button("Apply Info")]
        ]
        return sg.Window("Py Bot", layout)

    def main(self):
        self.create_main_window()
        while True:
            event, values = self.window.read()
            if event == "Start Bot":
                print("In development")
            if event == "Options":
                self.options()
            if event == sg.WIN_CLOSED:
                sys.exit()
        self.window.close()

    def options(self):
        options_window = self.create_options_window()
        while True:
            event, values = options_window.read()
            if event == "Apply Info":
                billing = (values["-CARD-"], values["-EXPDATE-"], values["-CVV-"], values["-NAME-"], values["-STREET-"], values["-CITY-"], values["-STATE-"])
                sqlite.save_billing(billing)
            if event == sg.WIN_CLOSED:
                break
        options_window.close()

if __name__ == '__main__':
    root = os.path.dirname(sys.argv[0])
    database_path = os.path.join(root, "PyBot.db")
    
    if not os.path.exists(database_path):
        with open(database_path, "w"):
            pass
    
    cipher = Cipher()
    sqlite = SQLite(database_path)
    
    gui = GUI()
    gui.main()