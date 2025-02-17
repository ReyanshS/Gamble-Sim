import random 
import time
import sqlite3
conn = sqlite3.connect('balances.db')

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    highest_balance REAL NOT NULL DEFAULT 0,
    money REAL NOT NULL DEFAULT 0
);
""")

def add_user(username, initial_money):
    conn = sqlite3.connect("balances.db")
    cursor = conn.cursor()

    cursor.execute("INSERT INTO users (username, highest_balance, money) VALUES (?, ?, ?)", 
                   (username, initial_money, initial_money))

    conn.commit()
    conn.close()

def get_balance(username):
    conn = sqlite3.connect("balances.db")
    cursor = conn.cursor()

    cursor.execute("SELECT money, highest_balance FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()

    conn.close()
    
    if result:
        money, highest_balance = result  # Unpacking the tuple
        return money, highest_balance  # Returning them separately
    else:
        print("Try entering a registered username")
        exit()
        return None, None  # If user not found, return None values

print("Welcome To Gambling Sim!")
print("You wager an amount of money on 3 numbers, if at least 2 numbers are the same you win DOUBLE your wager!")
print("JACKPOT(1000x) if all 3 numbers are the same")
print("enter any key to continue!")
input()

def update_balance(username, new_money):
    conn = sqlite3.connect("balances.db")
    cursor = conn.cursor()

    # Get current highest balance
    cursor.execute("SELECT highest_balance FROM users WHERE username = ?", (username.lower(),))
    result = cursor.fetchone()
    
    if result is None:
        print("User not found!")
        return

    highest_balance = max(result[0], new_money)  # Update highest balance if needed

    cursor.execute("UPDATE users SET money = ?, highest_balance = ? WHERE username = ?", 
                   (new_money, highest_balance, username))

    conn.commit()
    conn.close()




money = 100
highest_balance = money

user = ""

new_user = input("Are you registered(Y/N): ")

if new_user.lower() == "n":
    user = input("What would you like to be called: ")
    add_user(user, 100)
    time.sleep(0.2)
    print("Here is $100 to get you started!")
else:
    user = input("What is your username: ")
    balance = get_balance(user)
    money, highest_balance = balance
    if money <= 0:
        print("You are currently broke and have 0 dollars, wait 30 seconds for us to donate you $100")
        time.sleep(30)
        money = 100
    print(f"Your highest_balance is {highest_balance}")



while money > 0:
    print(f"You currently have ${money}")
    print("type exit to leave")
    valid = False
    while not valid:
        command = input("How much money do you want to gamble? ")
        if command.lower() == "exit":
            exit()
        wager = int(command)
        if wager <= money:
            valid = True
        else:
            print(f"You don't have enough money, you have ${money}")
    roll = 0
    for x in range(25):
        val = random.randint(100,999)
        print(val)
        time.sleep(0.1)
        if x == 24:
            roll = val
    time.sleep(0.5)
    if roll % 111 == 0:
        print(f"JACKPOT, you won ${wager * 1000}")
        money += wager * 1000
    elif any(str(roll).count(d) > 1 for d in set(str(roll))):
        print(f"Congratulations you won ${wager * 2}!")
        money += wager * 2
    else:
        print(f"L you lost ${wager}")
        money -= wager
    if money > highest_balance:
        highest_balance = money
    update_balance(user, money)
print(f"Your highest balance was {highest_balance}")
