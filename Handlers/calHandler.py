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


# Confirm set date.
def confirm_set_date(which):
    if which == "Manual":
        console.print(FmStr.fEMPTY)
        console.print(f"{FmStr.fNEUTRAL} {FmStr.wTELLER} is currently set to {FmStr.wAUTO} mode.")
        console.print(FmStr.fEMPTY)
        answer = Prompt.ask(f"{FmStr.fPROMPT} Switch to {FmStr.wMANUAL}? (Y/n) ")
    else:
        console.print(FmStr.fEMPTY)
        console.print(f"{FmStr.fNEUTRAL} {FmStr.wTELLER} is currently set to {FmStr.wMANUAL} mode.")
        console.print(FmStr.fEMPTY)
        answer = Prompt.ask(f"{FmStr.fPROMPT} Switch to {FmStr.wAUTO}? (Y/n) ")


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

