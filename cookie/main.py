import os
import time
import timeit
import random
import json
import getpass
from threading import Thread
import keyboard
from guide import guide_txt
from news import starter_news, intermediate_news, pro_news, legendary_news, mythical_news


# ========= DATABASE (local JSON save) =========
SAVE_FILE = "save.json"

def load_data():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f)

db = load_data()

# ========= USER =========
username = getpass.getuser()  # your PC username
if username not in db:
    db[username] = [0, *([0] * 16), True]

# ========= GAME SETUP =========
upgrades = []
cookies = db[username][0]
reset_cps = True
headline = f"Welcome back, {username}!"
golden_cookie = 0
golden_cookie_content = ""

# ========= HELPERS =========
def rgb(r, g, b):
    return f"\033[38;2;{r};{g};{b}m"

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

# ========= AUTO CLICKER =========
def ac():
    global cookies
    while True:
        cookies += 1
        time.sleep(5)

auto_clicker = Thread(target=ac, daemon=True)
auto_clicker.start()

# ========= SHOP =========
class Upgrade:
    def __init__(self, name, cost, cps, cpc):
        self.name = name
        self.cost = cost
        self.cps = cps  # cookies per second
        self.cpc = cpc  # cookies per click

    def update_cost(self):
        self.cost += int(self.cost / 10)

Cursor = Upgrade('Cursor', 15, 0.1, 0)
Grandma = Upgrade('Grandma', 100, 1, 0)
Fingers = Upgrade('Fingers', 400, 1, 1)
Farm = Upgrade('Farm', 1100, 8, 1)
Mine = Upgrade('Mine', 12000, 47, 1)
Factory = Upgrade('Factory', 130000, 260, 2)
Bank = Upgrade('Bank', 1400000, 1400, 0)
Temple = Upgrade('Temple', 2000000, 7800, 5)
Wizard_Tower = Upgrade('Wizard Tower', 330000000, 44000, 10)
Shipment = Upgrade('Shipment', 5100000000, 260000, 0)
Alchemy_Lab = Upgrade('Alchemy Lab', 75000000000, 1600000, 10)
Portal = Upgrade('Portal', 1000000000000, 10000000, 30)
Time_Machine = Upgrade('Time Machine', 14000000000000, 65000000, 100)
Cookie_Monster = Upgrade('Cookie Monster', 180000, 350, 1000)
Blaster = Upgrade('Blaster', 20000000, 0, 3500)
Hacker = Upgrade('Hacker', 200000000000000, 6000000000000, 1000000000)

shop = [Cursor,Grandma,Fingers,Farm,Mine,Factory,Bank,Temple,Wizard_Tower,
        Shipment,Alchemy_Lab,Portal,Time_Machine,Cookie_Monster,Blaster,Hacker]

# ========= RESTORE UPGRADES =========
for idx, upgrade in enumerate(shop, start=1):
    for i in range(db[username][idx]):
        upgrades.append(upgrade)

# ========= GAME START =========
clear()
print("Press [ENTER] to start the game\nPress [G] for guide\nPress [R] to redeem codes")

while True:
    if keyboard.is_pressed("enter"):
        break
    elif keyboard.is_pressed("g"):
        print(guide_txt)
        input('\nPress [ENTER] to continue')
        break
    elif keyboard.is_pressed("r"):
        clear()
        code_input = input('Enter redeem code here: ')
        if code_input == "e829WFf" and db[username][-1]:
            cookies += 127
            print("\n+127 cookies!\n")
            db[username][-1] = False
        elif not db[username][-1]:
            print("\nGift already claimed!\n")
        else:
            print("\nInvalid redeem code...\n")
        input('Press [ENTER] to continue')
        break

clear()

# ========= GAME LOOP =========
while True:
    # shop + stats update
    cps = sum(u.cps for u in upgrades)
    cpc = 1 + sum(u.cpc for u in upgrades)
    cookies = round(cookies, 2)

    print(f"\n{username}'s Cookie Clicker 🍪   |   {cookies} cookies   |   CPS: {cps}   |   CPC: {cpc}")
    print("Press [SPACE/ENTER] to click, [1-5] to buy, [S] to save")

    start = timeit.default_timer()

    # wait for a keypress
    key = keyboard.read_event(suppress=True).name
    end = timeit.default_timer()

    if key in ["space", "enter"] and end - start > 0.04:
        cookies += cpc
    elif key in ['1','2','3','4','5']:
        index = int(key) - 1
        upgrade = shop[index]
        if cookies >= upgrade.cost:
            cookies -= upgrade.cost
            upgrades.append(upgrade)
            upgrade.update_cost()
    elif key == 's':
        db[username] = [cookies, *[upgrades.count(u) for u in shop], db[username][-1]]
        save_data(db)
        print("Progress saved!")
        time.sleep(1)

    clear()
