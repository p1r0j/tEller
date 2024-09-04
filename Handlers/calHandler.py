# Written by piroj,
# for the offline CLI budgeting tool,
# tEller.

# Components.
import os
import string
import pickle
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
def check_date_formatting(actual, expected):
    return (actual.isdigit() and len(actual) == expected)


# Set manual date.
def set_date_manual():
    global dateDynamic
    console.print(FmStr.fEMPTY)
    year = Prompt.ask(f"{FmStr.fPROMPT} Enter the year (YYYY)")
    if not check_date_formatting(year, 4):
        console.print(FmStr.fEMPTY)
        console.print(f"{FmStr.fERROR} Invalid year.")
    else:
        console.print(FmStr.fEMPTY)
        month = Prompt.ask(f"{FmStr.fPROMPT} Enter the month (MM)")
        if not check_date_formatting(month, 2):
            console.print(FmStr.fEMPTY)
            console.print(f"{FmStr.fERROR} Invalid month.")
        else:
            console.print(FmStr.fEMPTY)
            day = Prompt.ask(f"{FmStr.fPROMPT} Enter the day (DD)")
            if not check_date_formatting(day, 2):
                console.print(FmStr.fEMPTY)
                console.print(f"{FmStr.fERROR} Invalid day.")
            else:
                console.print(f"{FmStr.fOK}  Recording new date...")
                dateDynamic = {
                        'Year': year,
                        'Month': month,
                        'Day': day
                        }
                save_cal()


# Set auto date.
def set_date_auto():
    global dateDynamic
    console.print(f"{FmStr.fOK}  Switching to {FmStr.wAUTO} mode...")
    dateDynamic = "Auto"
    save_cal()


# Confirm set date.
def confirm_set_date(which):
    if which == "Manual":
        console.print(FmStr.fEMPTY)
        console.print(f"{FmStr.fNEUTRAL} The current date is set to {FmStr.wAUTO} mode.")
        console.print(FmStr.fEMPTY)
        answer = Prompt.ask(f"{FmStr.fPROMPT} Switch to {FmStr.wMANUAL} (Y/n)?")
        if answer.lower() == "n":
            exit()
        else:
            set_date_manual()
    else:
        console.print(FmStr.fEMPTY)
        console.print(f"{FmStr.fNEUTRAL} The current date is set to {dateDynamic['Year']}-{dateDynamic['Month']}-{dateDynamic['Day']}.")
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


# Save CAL.
def save_cal():
    with open(CALSAVE, 'wb') as file:
        pickle.dump(dateDynamic, file)

