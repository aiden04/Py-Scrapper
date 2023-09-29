import PySimpleGUI as sg
import sqlite3, sys, os, requests, urllib
from cryptography.fernet import Fernet
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from fake_useragent import UserAgent as ua


class ScrapeDoProxyManager:
    def __init__(self, url, api_key):
        self.url = url
        self.auth = api_key
        self.current_proxy = None
        print(f"Proxy Manager Initialized with Url '{url}', and api_key '{api_key}'")

    def get_proxy(self):
        encoded_url = urllib.parse.quote(self.url)
        print(f"Encoded Url: {encoded_url}")
        print(f"API Key: {self.auth}")
        self.current_proxy = "http://api.scrape.do?token={}&url={}".format(self.auth, encoded_url)
        print(f"Current Proxy: {self.current_proxy}")
        return self.current_proxy

    def make_request(self, url):
        response = requests.request("GET", url)
        print(response.text)
        return

class Cipher:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.cur = self.conn.cursor()
        self.key = self.get_key()
        if self.key is None:
            self.create_cipher_table()
        print("Cipher initialized with key:", self.key)

    def create_cipher_table(self):
        # Create the Cipher table if it doesn't exist
        self.cur.execute("CREATE TABLE IF NOT EXISTS Cipher (Key TEXT)")
        self.conn.commit()
        self.make_key()
        print("Cipher Table Created.")

    def get_key(self):
        # Retrieve the encryption key from the Cipher table
        try:
            self.cur.execute("SELECT Key FROM Cipher")
            row = self.cur.fetchone()
            return row[0]
        except:
            return None
    def make_key(self):
        key = Fernet.generate_key().decode()
        print("Cipher Key Created.")
        print(f"Cipher Key: {key}")
        self.cur.execute("INSERT INTO Cipher (Key) VALUES (?)", (key,))
        self.conn.commit()

    def encrypt(self, input_text):
        cipher_suite = Fernet(self.key.encode())
        encrypted_text = cipher_suite.encrypt(input_text.encode()).decode()
        print(f"input: {input_text}")
        print(f"output: {encrypted_text}")
        return encrypted_text

    def decrypt(self, input_text):
        cipher_suite = Fernet(self.key.encode())
        decrypted_text = cipher_suite.decrypt(input_text.encode()).decode()
        print(f"input: {input_text}")
        print(f"output: {decrypted_text}")
        return decrypted_text

class SQLite:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.cur = self.conn.cursor()
        self.key = Cipher(db_path).get_key()
        self.db_path = db_path

    def save_billing(self, billing):
        # Create the Billing table if it doesn't exist
        self.cur.execute("CREATE TABLE IF NOT EXISTS Billing (CardNumber TEXT, ExpDate TEXT, CVV TEXT, Name TEXT, Street TEXT, City TEXT, State TEXT)")
        cipher = Cipher(self.db_path)
        encrypted_billing = [cipher.encrypt(value) for value in billing]
        self.cur.execute("INSERT INTO Billing (CardNumber, ExpDate, CVV, Name, Street, City, State) VALUES (?, ?, ?, ?, ?, ?, ?)", encrypted_billing)
        self.conn.commit()

    def clear_billing(self):
        if self.check_table("Billing"):
            # Drop the Billing table to clear billing information
            self.cur.execute("DROP TABLE IF EXISTS Billing")
            print("Billing information cleared!")
        else:
            print("Billing information not found.")

    def check_table(self, table):
        # Check if a table exists in the database
        self.cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table,))
        return bool(self.cur.fetchone())

    def autofill_billing(self):
        self.cur.execute("SELECT CardNumber, ExpDate, CVV, Name, Street, City, State FROM Billing")
        billing = self.cur.fetchone()
        if billing:
            cipher = Cipher(self.db_path)
            decrypted_billing = [cipher.decrypt(value) for value in billing]
            return decrypted_billing
        return None
    def save_login(self, login):
        self.cur.execute("CREATE TABLE IF NOT EXISTS Login (Username TEXT, Password TEXT)")
        encrypted_login = [cipher.encrypt(value) for value in login]
        self.cur.execute("INSERT INTO Login (Username, Password) VALUES (?, ?)", encrypted_login)
        self.conn.commit()


class GUI:
    def __init__(self, db_path):
        self.db_path = db_path
        self.ttk_theme = "clam"
        self.window = None
        self.in_options = False  # Flag to track if in options window
        self.run_main_loop = True  # Flag to control running the main loop
        sg.theme("SystemDefault")

    def create_main_window(self):
        layout = [
            [sg.Text("Ticket Master Scrapper", font=("Helvetica", 20))],
            [sg.Text("Please provide Card Information in the options window.")],
            [sg.Text("Enter the section of the Ticket Master link after 'https://www.ticketmaster.com/event/'")],
            [sg.Text("-" * 100)],
            [sg.Text("Website:"), sg.Text("https://www.ticketmaster.com/event/"), sg.Input(key="-WEBSITE-", size=(15, 1))],
            [sg.Button("Start Bot", size=(10, 1)), sg.Button("Options", size=(10, 1))]
        ]
        self.window = sg.Window("Py Bot", layout, use_ttk_buttons=True, ttk_theme=self.ttk_theme, element_justification="center", finalize=True)

    def create_options_window(self):
        layout = [
            [sg.Text("Options", font=("Helvetica", 20))],
            [sg.Text(f'Save information to:\n"{self.db_path}"', font=("Helvetica", 10))],
            [sg.Text("-----------------Ticket Master Login-----------------")],
            [sg.Text("Username", size=(11, 1)), sg.Input(key="-USERNAME-", size=(18, 1))],
            [sg.Text("Password", size=(11, 1)), sg.Input(key="-PASSWORD-", size=(18, 1))],
            [sg.Text("--------------------------Billing--------------------------")],
            [sg.Text("Card Number", size=(11, 1)), sg.Input(key="-CARD-", size=(18, 1))],
            [sg.Text("Exp Date", size=(11, 1)), sg.Input(key="-EXPDATE-", size=(5, 1)), sg.Text("CVV"), sg.Input(key="-CVV-", size=(5, 1))],
            [sg.Text("Name on Card", size=(11, 1)), sg.Input(key="-NAME-", size=(18, 1))],
            [sg.Text("Street Address", size=(11, 1)), sg.Input(key="-STREET-", size=(18, 1))],
            [sg.Text("City", size=(11, 1)), sg.Input(key="-CITY-", size=(18, 1))],
            [sg.Text("State", size=(11, 1)), sg.Input(key="-STATE-", size=(18, 1))],
            [sg.Checkbox("Save Information for future use", key="-SAVEINFO-", font=("Helvetica", 10))],
            [sg.Button("Apply Info", size=(10, 1)), sg.Button("Clear Saved Info", size=(15, 1)), sg.Button("Back", size=(10, 1))],
        ]
        return sg.Window("Py Bot", layout, use_ttk_buttons=True, ttk_theme=self.ttk_theme, element_justification="center")

    def options(self):
        options_window = self.create_options_window()
        sqlite = SQLite(self.db_path)
        saved_data = sqlite.check_table("Billing")
        if saved_data:
            billing = sqlite.autofill_billing()
            if billing:
                for key, value in zip(["-CARD-", "-EXPDATE-", "-CVV-", "-NAME-", "-STREET-", "-CITY-", "-STATE-"], billing):
                    options_window[key].update(value)
        while True:
            event, values = options_window.read()
            if event == "Apply Info":
                save_info = values["-SAVEINFO-"]
                if save_info:
                    billing = [values["-CARD-"], values["-EXPDATE-"], values["-CVV-"], values["-NAME-"], values["-STREET-"], values["-CITY-"], values["-STATE-"]]
                    print(f"Provided Billing: {billing}")
                    db = SQLite(self.db_path)
                    db.save_billing(billing)
                    print("Encrypted Billing Saved!")
                    login = [values["-USERNAME-"], values["-PASSWORD-"]]
                    print(f"Provided Login: {login}")
                    db.save_login(login)
                    print("Encrypted Login Saved!")
                    sg.popup(f"Saved Encrypted Billing and Login Information to {self.db_path}")
                else:
                    temp_card = values["-CARD-"]
                    temp_expdate = values["-EXPDATE-"]
                    temp_cvv = values["-CVV-"]
                    temp_name = values["-NAME-"]
                    temp_street = values["-STREET-"]
                    temp_city = values["-CITY-"]
                    temp_state = values["-STATE-"]
                    billing = [temp_card, temp_expdate, temp_cvv, temp_name, temp_street, temp_city, temp_state]
                    print(f"Provided Billing Information: {billing}")
                    print("Billing Information will not be saved locally, only temporarily used in the program, and is then flushed when the program is terminated.")
                    sg.popup("Information Applied Temporarily")
            if event == "Clear Saved Info":
                sqlite.clear_billing()
                sg.popup("Billing Information Cleared!")
                for key in ["-CARD-", "-EXPDATE-", "-CVV-", "-NAME-", "-STREET-", "-CITY-", "-STATE-"]:
                    options_window[key].update("")
            if event == 'Back':
                options_window.close()
                self.in_options = False  # Set the flag to indicate returning to the main window
                break  # Exit the options loop
            if event == sg.WIN_CLOSED:
                break
        options_window.close()

    def main(self):
        self.create_main_window()
        print(f"DataBase Local Path: {self.db_path}")
        Cipher(self.db_path)
        while self.run_main_loop:  # Check the flag before entering the main loop
            event, values = self.window.read()
            if event == "Start Bot":
                    #Initialize proxie and vpn rotation
                target_url = "https://httpbin.co/ip"
                api_key = ""
                proxy_manager = ScrapeDoProxyManager(target_url, api_key)
                proxy = proxy_manager.get_proxy()
                print(f"Retrieved Proxy: {proxy}")
                driver_options = webdriver.ChromeOptions()
                driver_options.add_argument("--disable-blink-features=AutomationControlled") 
                driver_options.add_argument("--proxy-server=%s" % proxy) 
                user_agent = ua.random
                print(f"User Agent Selected: {user_agent}")
                driver_options.add_argument(f"--user-agent={user_agent}")
                driver_options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
                driver_options.add_experimental_option("useAutomationExtension", False)
                print(f"Current Driver Options: {driver_options}")
                driver = webdriver.Chrome(driver_options)
                driver.get("https://www.ticketmaster.com/event/")
            if event == "Options":
                self.in_options = True  # Set the flag to indicate entering the options window
                self.options()
            if event == sg.WIN_CLOSED:
                if not self.in_options:
                    self.run_main_loop = False  # Set the flag to exit the main loop
                else:
                    self.in_options = False  # Reset the flag when closing the options window

        self.window.close()

if __name__ == '__main__':
    root = os.path.dirname(sys.argv[0])
    database_path = f"{root}/PyBot.db"
    print(f"DataBase Location: {database_path}")

    if not os.path.exists(database_path):
        print("No database found, creating database.")
        open(database_path, "w").close()  # Create an empty database file

    cipher = Cipher(database_path)  # Create Cipher instance and initialize the table and key if needed

    # Initialize temporary billing information
    global temp_card, temp_expdate, temp_cvv, temp_name, temp_street, temp_city, temp_state

    gui = GUI(database_path)
    gui.create_main_window()  # Create the main window before calling gui.main()
    gui.main()
