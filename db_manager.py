import sqlite3
from sqlite3 import Error
# import os


class DbManager:
    conn = None
    db = 'db.db'

    def setDBFileName(filename):
        DbManager.db = filename

    def __init__(self):
        self.conn = sqlite3.connect(DbManager.db)
        c = self.conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS Currency(
            Name VARCHAR(4) PRIMARY KEY
        )''')
        c.execute('''CREATE TABLE IF NOT EXISTS Wallet(
            Address VARCHAR(128) PRIMARY KEY,
            Currency VARCHAR(4),
            Status NUMERIC,
            FOREIGN KEY (Currency) REFERENCES Currency(Name)
        )''')
        c.execute('''CREATE TABLE IF NOT EXISTS Information(
            _id INTEGER PRIMARY KEY,
            Name VARCHAR(255),
            Website VARCHAR(255),
            Email VARCHAR(255),
            Json LONGTEXT
        )''')
        c.execute('''CREATE TABLE IF NOT EXISTS Account(
            _id INTEGER PRIMARY KEY,
            Host VARCHAR(255),
            Username VARCHAR(255),
            Info INT,
            FOREIGN KEY (Info) REFERENCES Information(ID)
        )''')
        c.execute('''CREATE TABLE IF NOT EXISTS AccountWallet(
            _id INTEGER PRIMARY KEY,
            Account INT,
            Wallet VARCHAR(128),
            RawURL VARCHAR(500),
            FOREIGN KEY (Account) REFERENCES Account(ID),
            FOREIGN KEY (Wallet) REFERENCES Wallet(Address)
        )''')
        try:
            c.execute('''INSERT INTO Currency VALUES ("BTC")''')
            c.execute('''INSERT INTO Currency VALUES ("ETH")''')
            c.execute('''INSERT INTO Currency VALUES ("ETC")''')
            c.execute('''INSERT INTO Currency VALUES ("XMR")''')
            c.execute('''INSERT INTO Currency VALUES ("BCH")''')
            c.execute('''INSERT INTO Currency VALUES ("LTC")''')
            c.execute('''INSERT INTO Currency VALUES ("DOGE")''')
        except Error:
            print()
        self.conn.commit()
        self.conn.close()

    def insertWallet(self, address, currency, status):
        self.conn = sqlite3.connect(DbManager.db)
        c = self.conn.cursor()
        try:
            c.execute('''INSERT INTO Wallet(Address, Currency, Status)
                VALUES (?,?,?)''', (address, currency, status,))
        except Error:
            print()
            return False
        self.conn.commit()
        self.conn.close()
        return True

    def insertWalletWithAccount(self, address, currency, status, account, url):
        self.conn = sqlite3.connect(DbManager.db)
        c = self.conn.cursor()
        try:
            c.execute('''INSERT INTO Wallet(Address, Currency, Status)
                VALUES (?,?,?)''', (address, currency, status,))
        except Error:
            print()
            return False
        self.conn.commit()
        self.conn.close()
        return self.insertAccountWallet(account, address, url)

    def insertInformation(self, name, website, email, json):
        self.conn = sqlite3.connect(DbManager.db)
        c = self.conn.cursor()
        try:
            c.execute('''INSERT INTO Information(Name, Website, Email, Json)
                VALUES (?,?,?,?)''', (name, website, email, json,))
        except Error:
            print()
            return -1
        c.execute('SELECT max(_id) FROM Information')
        max_id = c.fetchone()[0]
        self.conn.commit()
        self.conn.close()
        return max_id

    def insertAccount(self, host, username, info):
        self.conn = sqlite3.connect(DbManager.db)
        c = self.conn.cursor()
        try:
            c.execute('''INSERT INTO Account(Host, Username, Info)
                VALUES (?,?,?)''', (host, username, info,))
        except Error:
            print()
            return -1
        c.execute('SELECT max(_id) FROM Account')
        max_id = c.fetchone()[0]
        self.conn.commit()
        self.conn.close()
        return max_id

    def insertAccountNoInfo(self, host, username):
        self.conn = sqlite3.connect(DbManager.db)
        c = self.conn.cursor()
        try:
            c.execute('''INSERT INTO Account(Host, Username)
                VALUES (?,?)''', (host, username,))
        except Error:
            print()
            return -1
        c.execute('SELECT max(_id) FROM Account')
        max_id = c.fetchone()[0]
        self.conn.commit()
        self.conn.close()
        return max_id

    def insertAccountWallet(self, account, wallet, url):
        self.conn = sqlite3.connect(DbManager.db)
        c = self.conn.cursor()
        try:
            c.execute('''INSERT INTO AccountWallet(Account, Wallet, RawURL)
                VALUES (?,?,?)''', (account, wallet, url,))
        except Error:
            print()
            return -1
        c.execute('SELECT max(_id) FROM AccountWallet')
        max_id = c.fetchone()[0]
        self.conn.commit()
        self.conn.close()
        return max_id

    def findWallet(self, address):
        self.conn = sqlite3.connect(DbManager.db)
        c = self.conn.cursor()
        c.execute("SELECT * FROM Wallet WHERE address = ?", (address,))
        data = c.fetchone()
        self.conn.close()
        return (data is not None)

    def findAccount(self, host, username):
        self.conn = sqlite3.connect(DbManager.db)
        c = self.conn.cursor()
        c.execute("SELECT _id FROM Account WHERE Host = ? AND Username = ?",
                  (host, username,))
        data = c.fetchone()
        self.conn.close()
        if data is None:
            return -1
        else:
            return data[0]

    def insertNewInfo(self, address, currency, status, name, website, email,
                      json, host, username, url):
        self.insertWallet(address, currency, status)
        info = self.insertInformation(name, website, email, json)
        acc = self.insertAccount(host, username, info)
        self.insertAccountWallet(acc, address, url)
        return acc

    def insertMultipleAddresses(self, acc, wallets):
        for wallet in wallets:
            self.insertWallet(wallet.address, wallet.currency, wallet.status)
            self.insertAccountWallet(acc, wallet.address, wallet.file)


class Wallet:
    address = None
    currency = None
    status = None
    file = None

    def __init__(self, add, curr, f, u):
        self.address = add
        self.currency = curr
        self.file = f
        self.status = u


class PersonalInfo:
    name = ""
    website = ""
    email = ""
    json = ""

    def __init__(self, name, website, email, json):
        self.name = name
        self.website = website
        self.email = email
        self.json = json

# try:
#     os.remove('./db.db')
# except OSError:
#     pass
# manager = DbManager()
# manager.insertWallet("aaa", "BTC", "NA")
# info = manager.insertInformation("nome", "sito", "email", "json")
# acc = manager.insertAccount("host", "user", info)
# manager.insertAccountWallet(acc, "aaa", "file")
# acc2 = manager.insertNewInfo('bbb2', 'ETH', 'SI', 'nome cognome2',
#                                'sito.com2', 'email2', 'json2', 'host2',
#                                'username2', 'path2')
# x = [Wallet('bbb21', 'BTC', 'path21', 'NA'),
#      Wallet('bbb22', 'BCH', 'path22', 'NO')]
# manager.insertMultipleAddresses(acc2, x)
#
