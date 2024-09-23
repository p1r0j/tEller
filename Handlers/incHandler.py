# Written by piroj,
# for the offline CLI budgeting tool,
# tEller.

import os
import pickle
from rich.prompt import Prompt
from rich.console import Console
import Resources.fmStrings as FmStr
console = Console(highlight=False)
INCSAVE = 'Saves/incSave.pkl'
incomeSources = {}


# Auto load.
if os.path.exists(INCSAVE):
    with open(INCSAVE, 'rb') as file:
        incLoad = pickle.load(file)
        incomeSources = incLoad


# Record new income source.
def record_new_income_source(name, amount):
    global incomeSources
    incomeSources[name] = amount
    save_inc()


# Check if income source exists.
def check_if_income_source_exists(which):
    if which in incomeSources:
        return True
    else:
        return False


# Process add income source.
def process_add_income_source():
    import Handlers.calHandler as CalHandler
    console.print(FmStr.fEMPTY)
    name = Prompt.ask(f"{FmStr.fPROMPT} Enter the name (no spaces/special characters)")
    if CalHandler.check_for_punctuation(name):
        console.print(FmStr.fEMPTY)
        console.print(f"{FmStr.fERROR} Invalid name.")
    else:
        console.print(f"{FmStr.fOK}  [bold green]{name}[/bold green] is valid.")
        if check_if_income_source_exists(name):
            console.print(FmStr.fEMPTY)
            console.print(f"{FmStr.fERROR} [bold green]{name}[/bold green] already exists.")
        else:
            console.print(f"{FmStr.fOK}  [bold green]{name}[/bold green] is unique.")
            console.print(FmStr.fEMPTY)
            amount = Prompt.ask(f"{FmStr.fPROMPT} Enter the amount (monthly)")
            if CalHandler.check_for_amount_misformatting(amount):
                console.print(FmStr.fEMPTY)
                console.print(f"{FmStr.fERROR} Invalid amount.")
            else:
                console.print(f"{FmStr.fOK}  [bold green]{amount}[/bold green] is valid.")
                console.print(f"{FmStr.fRECORD}  Recording new income source...")
                amount = float(amount)
                record_new_income_source(name, amount)


# Process print income.
def process_print_income():
    if not incomeSources:
        console.print(FmStr.fEMPTY)
        console.print(f"{FmStr.fERROR} No income sources found.")
    else:
        totalIncome = 0
        for key, value in incomeSources.items():
            totalIncome += value
            console.print(f"{FmStr.fINC}  {key:<10} {value:>10}")
        console.print(f"{FmStr.fHEAD} {'Total':<10} {totalIncome:>10}")


# Save income sources.
def save_inc():
    with open(INCSAVE, 'wb') as file:
        pickle.dump(incomeSources, file)

