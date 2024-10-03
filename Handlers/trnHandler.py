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
def record_new_transaction(year, month, day, name, amount, subcategory):
    global transactions
    if year not in transactions:
        transactions[year] = {}
    if month not in transactions[year]:
        transactions[year][month] = {}
    if day not in transactions[year][month]:
        transactions[year][month][day] = {}
    transactions[year][month][day][name] = {
            'Amount': amount,
            'Subcategory': subcategory
            }
    save_trn()


# Check if transaction exists.
def check_if_transaction_exists(which, year, month, day):
    todaysTransactions = transactions.get(year, {}).get(month, {}).get (day, {})
    if todaysTransactions is not None and which in todaysTransactions:
        return True
    else:
        return False


# Process add transaction.
def process_add_transaction():
    import Handlers.catHandler as CatHandler
    import Handlers.calHandler as CalHandler
    from Handlers.calHandler import dateDynamic
    if dateDynamic == "Auto":
        year, month, day = CalHandler.get_auto_date()
    else:
        year = dateDynamic['Year']
        month = dateDynamic['Month']
        day = dateDynamic['Day']
    console.print(FmStr.fEMPTY)
    name = Prompt.ask(f"{FmStr.fPROMPT} Enter the name (no spaces/special characters)")
    if CalHandler.check_for_punctuation(name):
        console.print(FmStr.fEMPTY)
        console.print(f"{FmStr.fERROR} Invalid name.")
    else:
        console.print(f"{FmStr.fOK}  [bold red]{name}[/bold red] is valid.")
        if check_if_transaction_exists(name, year, month, day):
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
                console.print(FmStr.fEMPTY)
                subcat = Prompt.ask(f"{FmStr.fPROMPT} Enter the budget subcategory")
                if not CatHandler.check_if_budget_subcategory_exists(subcat):
                    console.print(FmStr.fEMPTY)
                    console.print(f"{FmStr.fERROR} Invalid budget subcategory.")
                else:
                    console.print(f"{FmStr.fOK}  {subcat} is valid.")
                    console.print(f"{FmStr.fRECORD}  Recording new transaction...")
                    amount = float(amount)
                    record_new_transaction(year, month, day, name, amount, subcat)


# Process edit transaction.
def process_edit_transaction():
    global transactions
    import Handlers.catHandler as CatHandler
    import Handlers.calHandler as CalHandler
    from Handlers.calHandler import dateDynamic
    if dateDynamic == "Auto":
        year, month, day = CalHandler.get_auto_date()
    else:
        year = dateDynamic['Year']
        month = dateDynamic['Month']
        day = dateDynamic['Day']
    console.print(FmStr.fEMPTY)
    name = Prompt.ask(f"{FmStr.fPROMPT} Which transaction?")
    if CalHandler.check_for_punctuation(name):
        console.print(FmStr.fEMPTY)
        console.print(f"{FmStr.fERROR} Invalid name.")
    else:
        found = None
        for date in transactions[year][month]:
            if name in transactions[year][month][date]:
                found = date
                break
        if not found:
            console.print(FmStr.fEMPTY)
            console.print(f"{FmStr.fERROR} Invalid name.")
        else:
            console.print(FmStr.fEMPTY)
            newAmount = Prompt.ask(f"{FmStr.fPROMPT} Enter new amount")
            if CalHandler.check_for_amount_misformatting(newAmount):
                console.print(FmStr.fEMPTY)
                console.print(f"{FmStr.fERROR} Invalid amount.")
            else:
                console.print(f"{FmStr.fOK}  {newAmount} is valid.")
                console.print(FmStr.fEMPTY)
                newSubcat = Prompt.ask(f"{FmStr.fPROMPT} Enter new budget subcategory")
                if not CatHandler.check_if_budget_subcategory_exists(newSubcat):
                    console.print(FmStr.fEMPTY)
                    console.print(f"{FmStr.fERROR} Invalid budget subcategory.")
                else:
                    console.print(f"{FmStr.fOK}  {newSubcat} is valid.")
                    console.print(f"{FmStr.fRECORD}  Updating transaction...")
                    newAmount = float(newAmount)
                    record_new_transaction(year, month, found, name, newAmount, newSubcat)


# Process remove transaction.
def process_remove_transaction():
    global transactions
    import Handlers.catHandler as CatHandler
    import Handlers.calHandler as CalHandler
    from Handlers.calHandler import dateDynamic
    if dateDynamic == "Auto":
        year, month, day = CalHandler.get_auto_date()
    else:
        year = dateDynamic['Year']
        month = dateDynamic['Month']
        day = dateDynamic['Day']
    console.print(FmStr.fEMPTY)
    name = Prompt.ask(f"{FmStr.fPROMPT} Which transaction?")
    if CalHandler.check_for_punctuation(name):
        console.print(FmStr.fEMPTY)
        console.print(f"{FmStr.fERROR} Invalid name.")
    else:
        found = None
        for date in transactions[year][month]:
            if name in transactions[year][month][date]:
                found = date
                break
        if not found:
            console.print(FmStr.fEMPTY)
            console.print(f"{FmStr.fERROR} Invalid name.")
        else:
            del transactions[year][month][found][name]
            console.print(f"{FmStr.fRECORD}  Removing [bold red]{name}[/bold red]...")
            save_trn()


# Process print transactions.
def process_print_transactions():
    import Handlers.catHandler as CatHandler
    import Handlers.calHandler as CalHandler
    from Handlers.calHandler import dateDynamic
    total = 0.0
    essTotal = 0.0
    nessTotal = 0.0
    savTotal = 0.0
    subTotals = {}
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
    console.print(f"{FmStr.fHEAD} {FmStr.wMTRANS}")
    for date in transactions[year][month]:
        for transaction in transactions[year][month][date]:
            name = transaction
            amount = transactions[year][month][date][transaction]["Amount"]
            subcategory = transactions[year][month][date][transaction]["Subcategory"]
            category = CatHandler.check_if_budget_subcategory_exists(subcategory)
            total += amount
            if category == "Essentials":
                essTotal += amount
                essTotal = round(essTotal, 2)
            elif category == "Non-Essentials":
                nessTotal += amount
                nessTotal = round(nessTotal, 2)
            elif category == "Savings & Debt":
                savTotal += amount
                savTotal = round(savTotal, 2)
            else:
                console.print(f"{FmStr.fNOK}  [bold red]{name}[/bold red]'s budget subcategory has been changed or removed.")
            if subcategory not in subTotals:
                subTotals[subcategory] = 0.0
            subTotals[subcategory] += amount
            console.print(f"{FmStr.fMINUS}  {month}-{date}      {amount:<10} {name:<10} {subcategory:<10} {category:<10}")
    total = round(total, 2)
    console.print(f"{FmStr.fEQUAL}  [bold]{'Total':<10} {total:<10}[/bold]")
    console.print(FmStr.fEMPTY)
    console.print(f"{FmStr.fHEAD} {FmStr.wSTRANS}")
    scategorizedTotal = 0.0
    for subcategory, sub_total in subTotals.items():
        category = CatHandler.check_if_budget_subcategory_exists(subcategory)
        sub_total = round(sub_total, 2)
        scategorizedTotal += sub_total
        scategorizedTotal = round(scategorizedTotal, 2)
        console.print(f"{FmStr.fMINUS}  {subcategory:<10} {sub_total:<10} {category:<10}")
    console.print(f"{FmStr.fEQUAL}  [bold]{'Total':<10} {scategorizedTotal:<10}[/bold]")
    console.print(FmStr.fEMPTY)
    categorizedTotal = essTotal + nessTotal + savTotal
    categorizedTotal = round(categorizedTotal, 2)
    console.print(f"{FmStr.fHEAD} {FmStr.wCTRANS}")
    console.print(f"{FmStr.fMINUS}  {'Essentials':<21} {essTotal:<10}")
    console.print(f"{FmStr.fMINUS}  {'Non-Essentials':<21} {nessTotal:<10}")
    console.print(f"{FmStr.fMINUS}  {'Savings & Debt':<21} {savTotal:<10}")
    console.print(f"{FmStr.fEQUAL}  [bold]{'Total':<21} {categorizedTotal:<10}[/bold]")


# Save budget subcategories.
def save_trn():
    with open(TRNSAVE, 'wb') as file:
        pickle.dump(transactions, file)

