# Written by piroj,
# for the offline CLI budgeting tool,
# tEller.

# Components.
import os
import pickle
from rich.prompt import Prompt
from rich.console import Console
import Resources.fmStrings as FmStr
console = Console(highlight=False)
# Locations.
CURD = os.path.dirname(os.path.abspath(__file__))
CATSAVE = os.path.join(CURD, '../Saves', 'catSave.pkl')
# Containers.
subCats = {
        "Essentials": {},
        "Non-Essentials": {},
        "Savings & Debt": {}
        }


# Auto load.
if os.path.exists(CATSAVE):
    with open(CATSAVE, 'rb') as file:
        catLoad = pickle.load(file)
        subCats = catLoad


# Get budget category totals.
def get_budget_category_totals():
    essTotal = 0.0
    nessTotal = 0.0
    savTotal = 0.0
    for subcategory in subCats["Essentials"]:
        essTotal += subCats["Essentials"][subcategory]
    for subcategory in subCats["Non-Essentials"]:
        nessTotal += subCats["Non-Essentials"][subcategory]
    for subcategory in subCats["Savings & Debt"]:
        savTotal += subCats["Savings & Debt"][subcategory]
    essTotal = round(essTotal, 2)
    nessTotal = round(nessTotal, 2)
    savTotal = round(savTotal, 2)
    return essTotal, nessTotal, savTotal


# Record new budget subcategory.
def record_new_budget_subcategory(category, name, amount):
    global subCats
    subCats[category][name] = amount
    save_cat()


# Check if budget subcategory exists.
def check_if_budget_subcategory_exists(which):
    for category_name, category_dict in subCats.items():
        if which in category_dict:
            return category_name
    return False


# Process add budget subcategory.
def process_add_budget_subcategory():
    import Handlers.calHandler as CalHandler
    console.print(FmStr.fEMPTY)
    console.print(f"{FmStr.fHEAD} Please select a parent category.")
    console.print(f"{FmStr.fSEL1}  {FmStr.wESSENTIALS}")
    console.print(f"{FmStr.fSEL2}  {FmStr.wNESSENTIALS}")
    console.print(f"{FmStr.fSEL3}  {FmStr.wSAVDEBT}")
    console.print(FmStr.fEMPTY)
    sCat = Prompt.ask(f"{FmStr.fPROMPT} Enter number")
    if sCat == "1":
        console.print(f"{FmStr.fOK}  {FmStr.wESSENTIALS} selected.")
        sCat = "Essentials"
    elif sCat == "2":
        console.print(f"{FmStr.fOK}  {FmStr.wNESSENTIALS} selected.")
        sCat = "Non-Essentials"
    elif sCat == "3":
        console.print(f"{FmStr.fOK}  {FmStr.wSAVDEBT} selected.")
        sCat = "Savings & Debt"
    else:
        console.print(FmStr.fEMPTY)
        console.print(f"{FmStr.fERROR} Invalid choice.")
        exit()
    console.print(FmStr.fEMPTY)
    name = Prompt.ask(f"{FmStr.fPROMPT} Enter name")
    if CalHandler.check_for_punctuation(name):
        console.print(FmStr.fEMPTY)
        console.print(f"{FmStr.fERROR} Invalid name.")
    else:
        console.print(f"{FmStr.fOK}  {name} is valid.")
        if check_if_budget_subcategory_exists(name):
            console.print(FmStr.fEMPTY)
            console.print(f"{FmStr.fERROR} {name} already exists.")
        else:
            console.print(f"{FmStr.fOK}  {name} is unique.")
            console.print(FmStr.fEMPTY)
            amount = Prompt.ask(f"{FmStr.fPROMPT} Enter the amount (monthly)")
            if CalHandler.check_for_amount_misformatting(amount):
                console.print(FmStr.fEMPTY)
                console.print(f"{FmStr.fERROR} Invalid amount.")
            else:
                console.print(f"{FmStr.fOK}  {amount} is valid.")
                console.print(f"{FmStr.fRECORD}  Recording new budget subcategory...")
                amount = float(amount)
                record_new_budget_subcategory(sCat, name, amount)


# Process edit budget subcategory.
def process_edit_budget_subcategory():
    global subCats
    import Handlers.calHandler as CalHandler
    console.print(FmStr.fEMPTY)
    name = Prompt.ask(f"{FmStr.fPROMPT} Which budget subcategory?")
    if CalHandler.check_for_punctuation(name):
        console.print(FmStr.fEMPTY)
        console.print(f"{FmStr.fERROR} Invalid name.")
    else:
        found = None
        for category in ["Essentials", "Non-Essentials", "Savings & Debt"]:
            if name in subCats.get(category, {}):
                found = category
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
                console.print(f"{FmStr.fRECORD}  Updating budget subcategory...")
                newAmount = float(newAmount)
                record_new_budget_subcategory(found, name, newAmount)


# Process remove budget subcategory.
def process_remove_budget_subcategory():
    global subCats
    import Handlers.calHandler as CalHandler
    console.print(FmStr.fEMPTY)
    name = Prompt.ask(f"{FmStr.fPROMPT} Which budget subcategory?")
    if CalHandler.check_for_punctuation(name):
        console.print(FmStr.fEMPTY)
        console.print(f"{FmStr.fERROR} Invalid name.")
    else:
        found = None
        for category in ["Essentials", "Non-Essentials", "Savings & Debt"]:
            if name in subCats.get(category, {}):
                found = category
                break
        if not found:
            console.print(FmStr.fEMPTY)
            console.print(f"{FmStr.fERROR} Invalid name.")
        else:
            del subCats[found][name]
            console.print(f"{FmStr.fRECORD}  Removing [bold yellow]{name}[/bold yellow]...")
            save_cat()


# Process print budget subcategories.
def process_print_budget_subcategories():
    essTotal = 0.0
    nessTotal = 0.0
    savTotal = 0.0
    console.print(FmStr.fEMPTY)
    console.print(f"{FmStr.fHEAD} {FmStr.wESSENTIALS}")
    for subcategory in subCats["Essentials"]:
        amount = subCats["Essentials"][subcategory]
        essTotal += amount
        essTotal = round(essTotal, 2)
        console.print(f"{FmStr.fPLUS}  {subcategory:<10} {amount:<10}")
    console.print(f"{FmStr.fEQUAL}  [bold]{'Total':<10} {essTotal:<10}[/bold]")
    console.print(FmStr.fEMPTY)
    console.print(f"{FmStr.fHEAD} {FmStr.wNESSENTIALS}")
    for subcategory in subCats["Non-Essentials"]:
        amount = subCats["Non-Essentials"][subcategory]
        nessTotal += amount
        nessTotal = round(nessTotal, 2)
        console.print(f"{FmStr.fPLUS}  {subcategory:<10} {amount:<10}")
    console.print(f"{FmStr.fEQUAL}  [bold]{'Total':<10} {nessTotal:<10}[/bold]")
    console.print(FmStr.fEMPTY)
    console.print(f"{FmStr.fHEAD} {FmStr.wSAVDEBT}")
    for subcategory in subCats["Savings & Debt"]:
        amount = subCats["Savings & Debt"][subcategory]
        savTotal += amount
        savTotal = round(savTotal, 2)
        console.print(f"{FmStr.fPLUS}  {subcategory:<10} {amount:<10}")
    console.print(f"{FmStr.fEQUAL}  [bold]{'Total':<10} {savTotal:<10}[/bold]")


# Save budget subcategories.
def save_cat():
    with open(CATSAVE, 'wb') as file:
        pickle.dump(subCats, file)

