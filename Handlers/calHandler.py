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


# Process set date.
def process_set_date():
    global dateDynamic
    if dateDynamic == "Auto":
        confirm_set_manual_date()
    else:
        confirm_set_auto_date()


# Save CAL.
def save_cal():
    with open(CALSAVE, 'wb') as file:
        pickle.dump(dateDynamic, file)

