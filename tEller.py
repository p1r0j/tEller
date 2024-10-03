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


# Query print report.
def query_print_report():
    CalHandler.process_print_report()


# Query print transactions.
def query_print_transactions():
    TrnHandler.process_print_transactions()


# Query print budget subcategories.
def query_print_budget_subcategories():
    CatHandler.process_print_budget_subcategories()


# Query print income.
def query_print_income_sources():
    IncHandler.process_print_income_sources()


# Query print date.
def query_print_date():
    CalHandler.process_print_date()


# Query remove transaction.
def query_remove_transaction():
    TrnHandler.process_remove_transaction()


# Query remove budget subcategory.
def query_remove_budget_subcategory():
    CatHandler.process_remove_budget_subcategory()


# Query remove income source.
def query_remove_income_source():
    IncHandler.process_remove_income_source()


# Query edit budget subcategory.
def query_edit_budget_subcategory():
    CatHandler.process_edit_budget_subcategory()


# Query edit income source.
def query_edit_income_source():
    IncHandler.process_edit_income_source()


# Query edit transaction.
def query_edit_transaction():
    TrnHandler.process_edit_transaction()


# Query add transaction.
def query_add_transaction():
    TrnHandler.process_add_transaction()


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
    try:
        parser = argparse.ArgumentParser(description="tEller, the offline CLI budgeting tool.")
        parser.add_argument("-d", "--set-date", action="store_true", help="set current date")
        parser.add_argument("-i", "--add-income-source", action="store_true", help="add new income source")
        parser.add_argument("-b", "--add-budget-subcategory", action="store_true", help="add new budget subcategory")
        parser.add_argument("-t", "--add-transaction", action="store_true", help="add new transaction")
        parser.add_argument("-ei", "--edit-income-source", action="store_true", help="edit income source")
        parser.add_argument("-eb", "--edit-budget-subcategory", action="store_true", help="edit budget subcategory")
        parser.add_argument("-et", "--edit-transaction", action="store_true", help="edit transaction")
        parser.add_argument("-ri", "--remove-income-source", action="store_true", help="remove income source")
        parser.add_argument("-rb", "--remove-budget-subcategory", action="store_true", help="remove budget subcategory")
        parser.add_argument("-rt", "--remove-transaction", action="store_true", help="remove transaction")
        parser.add_argument("-pd", "--print-date", action="store_true", help="print current date")
        parser.add_argument("-pi", "--print-income-sources", action="store_true", help="print current income sources")
        parser.add_argument("-pb", "--print-budget-subcategories", action="store_true", help="print current budget subcategories")
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
        elif args.edit_budget_subcategory:
            query_edit_budget_subcategory()
        elif args.edit_transaction:
            query_edit_transaction()
        elif args.remove_income_source:
            query_remove_income_source()
        elif args.remove_budget_subcategory:
            query_remove_budget_subcategory()
        elif args.remove_transaction:
            query_remove_transaction()
        elif args.print_date:
            query_print_date()
        elif args.print_income_sources:
            query_print_income_sources()
        elif args.print_budget_subcategories:
            query_print_budget_subcategories()
        elif args.print_transactions:
            query_print_transactions()
        elif args.print_report:
            query_print_report()
        elif args.version:
            query_version()
    except:
        console.print(FmStr.fESC)


# Call main function.
if __name__ == "__main__":
    main()
