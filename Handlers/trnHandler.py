# Written by piroj,
# for the offline CLI budgeting tool,
# tEller.

# Components.
import os
import pickle
from datetime import datetime
from rich.prompt import Prompt
from rich.console import Console
import Resources.fmStrings as FmStr
console = Console(highlight=False)
# Locations.
CURD = os.path.dirname(os.path.abspath(__file__))
TRNSAVE = os.path.join(CURD, '../Saves', 'trnSave.pkl')
# Containers.
transactions = {}


# Auto load.
if os.path.exists(TRNSAVE):
    with open(TRNSAVE, 'rb') as file:
        trnLoad = pickle.load(file)
        transactions = trnLoad


# Record new transaction.
def record_new_transaction(name, amount):
    global transactions
    import Handlers.calHandler as CalHandler
    from Handlers.calHandler import dateDynamic
    if dateDynamic == "Auto":
        year, month, day = CalHandler.get_auto_date()
    else:
        year = dateDynamic['Year']
        month = dateDynamic['Month']
        day = dateDynamic['Day']
    if year not in transactions:
        transactions[year] = {}
    if month not in transactions[year]:
        transactions[year][month] = {}
    if day not in transactions[year][month]:
        transactions[year][month][day] = {}
    transactions[year][month][day][name] = amount
    save_trn()


# Check if transaction exists.
def check_if_transaction_exists(which):
    import Handlers.calHandler as CalHandler
    from Handlers.calHandler import dateDynamic
    if dateDynamic == "Auto":
        year, month, day = CalHandler.get_auto_date()
    else:
        year = dateDynamic['Year']
        month = dateDynamic['Month']
        day = dateDynamic['Day']
    todaysTransactions = transactions.get(year, {}).get(month, {}).get (day, {})
    if todaysTransactions is not None and which in todaysTransactions:
        return True
    else:
        return False


# Process add transaction.
def process_add_transaction():
    print(transactions)
    import Handlers.calHandler as CalHandler
    console.print(FmStr.fEMPTY)
    name = Prompt.ask(f"{FmStr.fPROMPT} Enter the name (no spaces/special characters)")
    if CalHandler.check_for_punctuation(name):
        console.print(FmStr.fEMPTY)
        console.print(f"{FmStr.fERROR} Invalid name.")
    else:
        console.print(f"{FmStr.fOK}  [bold red]{name}[/bold red] is valid.")
        if check_if_transaction_exists(name):
            console.print(FmStr.fEMPTY)
            console.print(f"{FmStr.fERROR} [bold red]{name}[/bold red] already exists.")
        else:
            console.print(f"{FmStr.fOK}  [bold red]{name}[/bold red] is unique.")
            console.print(FmStr.fEMPTY)
            amount = Prompt.ask(f"{FmStr.fPROMPT} Enter the amount")
            if CalHandler.check_for_amount_misformatting(amount):
                console.print(FmStr.fEMPTY)
                console.print(f"{FmStr.fERROR} Invalid amount.")
            else:
                console.print(f"{FmStr.fOK}  {amount} is valid.")
                console.print(f"{FmStr.fRECORD}  Recording new transaction...")
                amount = float(amount)
                record_new_transaction(name, amount)


# Process print transactions.
def process_print_transactions():
    import Handlers.calHandler as CalHandler
    from Handlers.calHandler import dateDynamic
    total = 0.0
    if dateDynamic == "Auto":
        year, month, day = CalHandler.get_auto_date()
    else:
        year = dateDynamic['Year']
        month = dateDynamic['Month']
        day = dateDynamic['Day']
    console.print(FmStr.fEMPTY)
    if year not in transactions:
        console.print(f"{FmStr.fERROR} No records for year {year}.")
        exit()
    if month not in transactions[year]:
        console.print(f"{FmStr.fERROR} No records for month {month}.")
        exit()
    console.print(f"{FmStr.fHEAD} {FmStr.wTRANS}")
    for date in transactions[year][month]:
        for transaction in transactions[year][month][date]:
            name = transaction
            amount = transactions[year][month][date][transaction]
            total += amount
            console.print(f"{FmStr.fPLUS}  {month}-{date}      {amount:<10} {name:<10}")
    console.print(f"{FmStr.fEQUAL}  [bold]{'Total':<10} {total:<10}[/bold]")


# Save budget subcategories.
def save_trn():
    with open(TRNSAVE, 'wb') as file:
        pickle.dump(transactions, file)

