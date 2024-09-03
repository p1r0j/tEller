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
    parser.add_argument("-pb", "--print-budget", action="store_true", help="print current budget subcategory")
    parser.add_argument("-pt", "--print-transactions", action="store_true", help="print current active month's transactions")
    parser.add_argument("-pr", "--print-report", action="store_true", help="print current active month's report")
    args = parser.parse_args()
    if args.set_date:
        query_set_date()
    elif args.add_income_source:
        query_add_income_source()
    elif args.add_budget_subcategory:
        query_add_budget_subcategory()
    elif args.add_transaction:
        query_add_transaction()
    elif args.print_budget:
        query_print_budget()
    elif args.print_transactions:
        query_print_transactions()
    elif args.print_report:
        query_print_report()


# Call main function.
if __name__ == "__main__":
    main()
