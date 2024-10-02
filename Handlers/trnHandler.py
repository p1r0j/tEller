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
    from Handlers.calHandler import dateDynamic
    if dateDynamic == "Auto":
        autoDate = datetime.now()
        activeYear = autoDate.strftime("%Y")
        activeMonth = autoDate.strftime("%m")
        activeDay = autoDate.strftime("%d")
    else:
        activeYear = dateDynamic['Year']
        activeMonth = dateDynamic['Month']
        activeDay = dateDynamic['Day']
    if activeYear not in transactions:
        transactions[activeYear] = {}
    if activeMonth not in transactions[activeYear]:
        transactions[activeYear][activeMonth] = {}
    if activeDay not in transactions[activeYear][activeMonth]:
        transactions[activeYear][activeMonth][activeDay] = {}
    transactions[activeYear][activeMonth][activeDay][name] = amount
    save_trn()


# Check if transaction exists.
def check_if_transaction_exists(which):
    from Handlers.calHandler import dateDynamic
    if dateDynamic == "Auto":
        autoDate = datetime.now()
        activeYear = autoDate.strftime("%Y")
        activeMonth = autoDate.strftime("%m")
        activeDay = autoDate.strftime("%d")
    else:
        activeYear = dateDynamic['Year']
        activeMonth = dateDynamic['Month']
        activeDay = dateDynamic['Day']
    todaysTransactions = transactions.get(activeYear, {}).get(activeMonth, {}).get (activeDay, {})
    if todaysTransactions is not None and which in todaysTransactions:
        return True
    else:
        return False


# Process add transaction.
def process_add_transaction():
    import Handlers.calHandler as CalHandler
    console.print(FmStr.fEMPTY)
    name = Prompt.ask(f"{FmStr.fPROMPT} Enter the name (no spaces/special characters)")
    if CalHandler.check_for_punctuation(name):
        console.print(FmStr.fEMPTY)
        console.print(f"{FmStr.fERROR} Invalid name.")
    else:
        console.print(f"{FmStr.fOK}  {name} is valid.")
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


# Save budget subcategories.
def save_trn():
    with open(TRNSAVE, 'wb') as file:
        pickle.dump(transactions, file)

