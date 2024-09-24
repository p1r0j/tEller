# Written by piroj,
# for the offline CLI budgeting tool,
# tEller.

# Components.
import os
import pickle
import string
from datetime import datetime
from rich.prompt import Prompt
from rich.console import Console
import Resources.fmStrings as FmStr
console = Console(highlight=False)
# Locations.
CALSAVE='Saves/calSave.pkl'
# Switches.
dateDynamic = "Auto"


# Auto load.
if os.path.exists(CALSAVE):
    with open(CALSAVE, 'rb') as file:
        calLoad = pickle.load(file)
        dateDynamic = calLoad


# Check date formatting.
def check_for_date_misformatting(actual, expected):
    return (actual.isdigit() and len(actual) == expected)


# Check for amount misformatting.
def check_for_amount_misformatting(which):
    try:
        amount = float(which)
        return False
    except ValueError:
        return True


# Check for punctuation.
def check_for_punctuation(which):
    return any(char in string.punctuation + ' ' for char in which)


# Set manual date.
def set_date_manual():
    global dateDynamic
    console.print(FmStr.fEMPTY)
    year = Prompt.ask(f"{FmStr.fPROMPT} Enter the year (YYYY)")
    if not check_for_date_misformatting(year, 4):
        console.print(FmStr.fEMPTY)
        console.print(f"{FmStr.fERROR} Invalid year.")
    else:
        console.print(f"{FmStr.fOK}  {year} is valid.")
        console.print(FmStr.fEMPTY)
        month = Prompt.ask(f"{FmStr.fPROMPT} Enter the month (MM)")
        if not check_for_date_misformatting(month, 2):
            console.print(FmStr.fEMPTY)
            console.print(f"{FmStr.fERROR} Invalid month.")
        else:
            console.print(f"{FmStr.fOK}  {month} is valid.")
            console.print(FmStr.fEMPTY)
            day = Prompt.ask(f"{FmStr.fPROMPT} Enter the day (DD)")
            if not check_for_date_misformatting(day, 2):
                console.print(FmStr.fEMPTY)
                console.print(f"{FmStr.fERROR} Invalid day.")
            else:
                console.print(f"{FmStr.fOK}  {day} is valid.")
                console.print(f"{FmStr.fRECORD}  Recording new date...")
                dateDynamic = {
                        'Year': year,
                        'Month': month,
                        'Day': day
                        }
                save_cal()


# Set auto date.
def set_date_auto():
    global dateDynamic
    console.print(f"{FmStr.fRECORD}  Recording new date...")
    dateDynamic = "Auto"
    save_cal()


# Confirm set date.
def confirm_set_date(which):
    if which == "Manual":
        console.print(FmStr.fEMPTY)
        console.print(f"{FmStr.fHEAD} The current date is set to {FmStr.wAUTO} mode.")
        console.print(FmStr.fEMPTY)
        answer = Prompt.ask(f"{FmStr.fPROMPT} Switch to {FmStr.wMANUAL} (Y/n)?")
        if answer.lower() == "n":
            exit()
        else:
            set_date_manual()
    else:
        console.print(FmStr.fEMPTY)
        console.print(f"{FmStr.fHEAD} The current date is set to {dateDynamic['Year']}-{dateDynamic['Month']}-{dateDynamic['Day']}.")
        console.print(FmStr.fEMPTY)
        answer = Prompt.ask(f"{FmStr.fPROMPT} Switch to {FmStr.wAUTO} (Y/n)?")
        if answer.lower() == "n":
            console.print(FmStr.fEMPTY)
            answer = Prompt.ask(f"{FmStr.fPROMPT} Update {FmStr.wMANUAL} date (Y/n)?")
            if answer.lower() == "n":
                exit()
            else:
                set_date_manual()
        else:
            set_date_auto()


# Process set date.
def process_set_date():
    global dateDynamic
    if dateDynamic == "Auto":
        confirm_set_date("Manual")
    else:
        confirm_set_date("Auto")


# Process print date.
def process_print_date():
    console.print(FmStr.fEMPTY)
    if dateDynamic == "Auto":
        autoDate = datetime.now()
        formattedDate = autoDate.strftime("%Y-%m-%d")
        console.print(f"{FmStr.fHEAD} The current date is {formattedDate}.")
    else:
        console.print(f"{FmStr.fHEAD} The current date is set to {dateDynamic['Year']}-{dateDynamic['Month']}-{dateDynamic['Day']}.")


# Save date.
def save_cal():
    with open(CALSAVE, 'wb') as file:
        pickle.dump(dateDynamic, file)

