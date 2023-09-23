import PySimpleGUI as sg
import sqlite3
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

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
            if event == sg.WIN_CLOSED:
                break
        options_window.close()

if __name__ == '__main__':
    gui = GUI()
    gui.main()