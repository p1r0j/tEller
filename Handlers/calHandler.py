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
CURD = os.path.dirname(os.path.abspath(__file__))
CALSAVE = os.path.join(CURD, '../Saves', 'calSave.pkl')
# Switches.
dateDynamic = "Auto"


# Auto load.
if os.path.exists(CALSAVE):
    with open(CALSAVE, 'rb') as file:
        calLoad = pickle.load(file)
        dateDynamic = calLoad


# Get auto date.
def get_auto_date():
    autoDate = datetime.now()
    year = autoDate.strftime("%Y")
    month = autoDate.strftime("%m")
    day = autoDate.strftime("%d")
    return year, month, day


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
    console.print(f"{FmStr.fHEAD} {FmStr.wDATE}")
    if dateDynamic == "Auto":
        autoDate = datetime.now()
        formattedDate = autoDate.strftime("%Y-%m-%d")
        console.print(f"{FmStr.fEQUAL}  {formattedDate}.")
    else:
        console.print(f"{FmStr.fEQUAL}  {dateDynamic['Year']}-{dateDynamic['Month']}-{dateDynamic['Day']}.")


# Process print report.
def process_print_report():
    import Handlers.incHandler as IncHandler
    import Handlers.catHandler as CatHandler
    import Handlers.calHandler as CalHandler
    from Handlers.catHandler import subCats
    from Handlers.calHandler import dateDynamic
    from Handlers.trnHandler import transactions
    IncHandler.process_print_income_sources()
    incTotal = IncHandler.get_income_total()
    console.print(FmStr.fEMPTY)
    console.print(f"{FmStr.fHEAD} {FmStr.wBUDGET}")
    essTotal, nessTotal, savTotal = CatHandler.get_budget_category_totals()
    catTotal = essTotal + nessTotal + savTotal
    catTotal = round(catTotal, 2)
    if catTotal > 0:
        essPer = round((essTotal / catTotal) * 100, 2)
        nessPer = round((nessTotal / catTotal) * 100, 2)
        savPer = round((savTotal / catTotal) * 100, 2)
    else:
        essPer = nessPer = savPer = 0
    console.print(f"{FmStr.fPLUS}  {'Essentials':<21} {essTotal:<10} {essPer}%")
    console.print(f"{FmStr.fPLUS}  {'Non-Essentials':<21} {nessTotal:<10} {nessPer}%")
    console.print(f"{FmStr.fPLUS}  {'Savings & Debt':<21} {savTotal:<10} {savPer}%")
    console.print(f"{FmStr.fEQUAL}  [bold]{'Total':<21} {catTotal:<10}[/bold]")
    console.print(FmStr.fEMPTY)
    console.print(f"{FmStr.fHEAD} {FmStr.wSCAT}")
    scatTotal = 0.0
    for subcategory in subCats["Essentials"]:
        budget = subCats["Essentials"][subcategory]
        scatTotal += budget
        console.print(f"{FmStr.fPLUS}  {subcategory:<10} {budget:<10} {'Essentials':<10}")
    for subcategory in subCats["Non-Essentials"]:
        budget = subCats["Non-Essentials"][subcategory]
        scatTotal += budget
        console.print(f"{FmStr.fPLUS}  {subcategory:<10} {budget:<10} {'Non-Essentials':<10}")
    for subcategory in subCats["Savings & Debt"]:
        budget = subCats["Savings & Debt"][subcategory]
        scatTotal += budget
        console.print(f"{FmStr.fPLUS}  {subcategory:<10} {budget:<10} {'Savings & Debt':<10}")
    scatTotal = round(scatTotal, 2)
    console.print(f"{FmStr.fEQUAL}  [bold]{'Total':<10} {scatTotal:<10}[/bold]")
    console.print(FmStr.fEMPTY)
    console.print(f"{FmStr.fHEAD} {FmStr.wSTRANS}")
    trnTotal = 0.0
    etrnTotal = 0.0
    ntrnTotal = 0.0
    sdtrnTotal = 0.0
    strnTotal = 0.0
    strnTotals = {}
    if dateDynamic == "Auto":
        year, month, day = CalHandler.get_auto_date()
    else:
        year = dateDynamic['Year']
        month = dateDynamic['Month']
        day = dateDynamic['Day']
    if year not in transactions:
        console.print(FmStr.fEMPTY)
        console.print(f"{FmStr.fERROR} No records for year {year}.")
        exit()
    if month not in transactions[year]:
        console.print(FmStr.fEMPTY)
        console.print(f"{FmStr.fERROR} No records for month {month}.")
        exit()
    for date in transactions[year][month]:
        for transaction in transactions[year][month][date]:
            name = transaction
            amount = transactions[year][month][date][transaction]["Amount"]
            subcategory = transactions[year][month][date][transaction]["Subcategory"]
            category = CatHandler.check_if_budget_subcategory_exists(subcategory)
            trnTotal += amount
            if category == "Essentials":
                etrnTotal += amount
                etrnTotal = round(etrnTotal, 2)
            elif category == "Non-Essentials":
                ntrnTotal += amount
                ntrnTotal = round(ntrnTotal, 2)
            elif category == "Savings & Debt":
                sdtrnTotal += amount
                sdtrnTotal = round(sdtrnTotal, 2)
            else:
                console.print(f"{FmStr.fNOK}  [bold red]{name}[/bold red]'s budget subcategory has been changed or removed.")
            if subcategory not in strnTotals:
                strnTotals[subcategory] = 0.0
            strnTotals[subcategory] += amount
    trnTotal = round(trnTotal, 2)
    for subcategory, sub_total in strnTotals.items():
        category = CatHandler.check_if_budget_subcategory_exists(subcategory)
        sub_total = round(sub_total, 2)
        strnTotal += sub_total
        strnTotal = round(strnTotal, 2)
        strnBud = subCats[category][subcategory]
        sub_per = round((sub_total / strnBud) * 100, 2)
        console.print(f"{FmStr.fMINUS}  {subcategory:<10} {sub_total:<10} {sub_per}%")
    strnPer = round((strnTotal / scatTotal) * 100, 2)
    console.print(f"{FmStr.fEQUAL}  [bold]{'Total':<10} {strnTotal:<10} {strnPer}%[/bold]")
    console.print(FmStr.fEMPTY)
    console.print(f"{FmStr.fHEAD} {FmStr.wCTRANS}")
    etrnPer = round((etrnTotal / essTotal) * 100, 2)
    ntrnPer = round((ntrnTotal / nessTotal) * 100, 2)
    sdtrnPer = round((sdtrnTotal / savTotal) * 100, 2)
    trnPer = round ((trnTotal / catTotal) * 100, 2)
    console.print(f"{FmStr.fMINUS}  {'Essentials':<21} {etrnTotal:<10} {etrnPer}%")
    console.print(f"{FmStr.fMINUS}  {'Non-Essentials':<21} {ntrnTotal:<10} {ntrnPer}%")
    console.print(f"{FmStr.fMINUS}  {'Savings & Debt':<21} {sdtrnTotal:<10} {sdtrnPer}%")
    console.print(f"{FmStr.fEQUAL}  [bold]{'Total':<21} {trnTotal:<10} {trnPer}%[/bold]")
    console.print(FmStr.fEMPTY)
    console.print(f"{FmStr.fHEAD} {FmStr.wNET}")
    netDiff = round((incTotal - trnTotal), 2)
    netPer = round((trnTotal / incTotal) * 100, 2)
    console.print(f"{FmStr.fPLUS}  {'Income':<10} {incTotal:<10}")
    console.print(f"{FmStr.fMINUS}  {'Expenses':<10} {trnTotal:<10}")
    console.print(f"{FmStr.fEQUAL}  [bold]{'Diff':<10} {netDiff:<10} {netPer}%[/bold]")


# Save date.
def save_cal():
    with open(CALSAVE, 'wb') as file:
        pickle.dump(dateDynamic, file)

