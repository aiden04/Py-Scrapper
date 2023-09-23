import PySimpleGUI as sg
import sqlite3
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class GUI:
    def main():
        layout = [
            [sg.Text("Website"), sg.Input(key="-WEBSITE-")],
            [sg.Button("Start Bot"), sg.Button("Options")]
            ]
        window = sg.Window("Py Bot", layout)
        while True:
            event, values = window.read()
            if event == "Start Bot":
                print("In development")
            if event == "Options":
                GUI.options()
            if event == sg.WIN_CLOSED:
                sys.exit()
        window.close()
    def options():
        layout = [
            ["Provided information will be saved locally only, if selected to.],
            [sg.Text("Card Number"), sg.Input(key="-CARD-")],
            [sg.Text("Name on Card"), sg.Input(key="-NAME-")],
            [sg.Text("Street Address"), sg.Input(key="-STREET-")],
            [sg.Text("City"), sg.Input(key="-CITY-")],
            [sg.Text("State"), sg.Input(key="-STATE-")],
            [sg.CheckBox("Save Information for future use", key="-SAVEINFO-")],
            [sg.Button("Apply Info")]
            ]
        window = sg.Window("Py Bot", layout)
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED:
                sys.exit()
        window.close()

GUI.main()
            
        