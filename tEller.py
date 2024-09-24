# Written by piroj,
# for the offline CLI budgeting tool,
# tEller.

# Modules.
import string
import argparse
from rich.prompt import Prompt
from rich.console import Console
import Resources.fmStrings as FmStr
import Handlers.incHandler as IncHandler
import Handlers.catHandler as CatHandler
import Handlers.calHandler as CalHandler
import Handlers.trnHandler as TrnHandler
console = Console(highlight=False)
tEllerVersion = "0.0"


# Query version.
def query_version():
    console.print(FmStr.fEMPTY)
    console.print(f"{FmStr.fHEAD} v{tEllerVersion}")


# Query print income.
def query_print_income():
    IncHandler.process_print_income()


# Query print date.
def query_print_date():
    CalHandler.process_print_date()


# Query remove income source.
def query_remove_income_source():
    IncHandler.process_remove_income_source()


# Query edit income source.
def query_edit_income_source():
    IncHandler.process_edit_income_source()


# Query add budget subcategory.
def query_add_budget_subcategory():
    CatHandler.process_add_budget_subcategory()


# Query add income source.
def query_add_income_source():
    IncHandler.process_add_income_source()


# Query set date.
def query_set_date():
    CalHandler.process_set_date()


# Handle arguments.
def main():
    parser = argparse.ArgumentParser(description="tEller, the offline CLI budgeting tool.")
    parser.add_argument("-d", "--set-date", action="store_true", help="set current date")
    parser.add_argument("-i", "--add-income-source", action="store_true", help="add new income source")
    parser.add_argument("-b", "--add-budget-subcategory", action="store_true", help="add new budget subcategory")
    parser.add_argument("-t", "--add-transaction", action="store_true", help="add new transaction")
    parser.add_argument("-ei", "--edit-income-source", action="store_true", help="edit income source")
    parser.add_argument("-ri", "--remove-income-source", action="store_true", help="remove income source")
    parser.add_argument("-pb", "--print-budget", action="store_true", help="print current budget subcategory")
    parser.add_argument("-pd", "--print-date", action="store_true", help="print current date")
    parser.add_argument("-pi", "--print-income", action="store_true", help="print current income sources")
    parser.add_argument("-pt", "--print-transactions", action="store_true", help="print current active month's transactions")
    parser.add_argument("-pr", "--print-report", action="store_true", help="print current active month's report")
    parser.add_argument("-v", "--version", action="store_true", help="print current version")
    args = parser.parse_args()
    if args.set_date:
        query_set_date()
    elif args.add_income_source:
        query_add_income_source()
    elif args.add_budget_subcategory:
        query_add_budget_subcategory()
    elif args.add_transaction:
        query_add_transaction()
    elif args.edit_income_source:
        query_edit_income_source()
    elif args.remove_income_source:
        query_remove_income_source()
    elif args.print_budget:
        query_print_budget()
    elif args.print_date:
        query_print_date()
    elif args.print_income:
        query_print_income()
    elif args.print_transactions:
        query_print_transactions()
    elif args.print_report:
        query_print_report()
    elif args.version:
        query_version()


# Call main function.
if __name__ == "__main__":
    main()
