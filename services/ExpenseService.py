from models import Expense, db
from datetime import datetime


class ExpenseService:
    def __init__(self):
        pass

    def getAllExpenses(self):
        try:
            return Expense.query.all()
        except Exception as e:
            print(
                f"Exception occurred while retrieving expenses from the database: {e}"
            )
            raise e

    def getExpenseById(self, expense_id: int):
        try:
            return Expense.query.get(expense_id)
        except Exception as e:
            print(
                f"Exception occurred while retrieving the expense with id {expense_id}: {e}"
            )
            raise e

    def addExpenseToDataBase(self, requestArg: dict):
        try:
            parsed_date = datetime.strptime(requestArg["date"], "%Y-%m-%d")
            expense: Expense = Expense(
                expenseDescription=requestArg["expense_description"],
                typeOfExpense=requestArg["type_of_expense"],
                amount=requestArg["amount"],
                date=parsed_date.strftime("%Y-%m-%d"),
            )
            db.session.add(expense)
            db.session.commit()
            print(f"Added Expense to the database: {expense.typeOfExpense}")
        except Exception as e:
            print(f"Exception occurred while adding the expense to the database: {e}")
            raise e

    def removeAnExpense(self, requestId: int):
        try:
            expense: Expense = Expense.query.get(requestId)
            if expense:
                db.session.delete(expense)
                db.session.commit()
                print(f"Deleted the entry from the database: {requestId}")
            else:
                print(
                    "The Expense is not available in the db. It may have either deleted already or the id may be different"
                )
                raise Exception
        except Exception as e:
            print(f"Exception occurred while deleting the entry from the db: {e}")
            raise e

    def modifyExpense(self, expenseId: int, newExpensePayload: dict):
        try:
            expense: Expense = Expense.query.get(expenseId)
            if expense:
                parsed_date = datetime.strptime(newExpensePayload["date"], "%Y-%m-%d")
                expense.typeOfExpense = newExpensePayload["type_of_expense"]
                expense.expenseDescription = newExpensePayload["expense_description"]
                expense.amount = newExpensePayload["amount"]
                expense.date = parsed_date.strftime("%Y-%m-%d")
                db.session.commit()
                print(f"Expense updated for the id: {expenseId}")
            else:
                print(f"Expense is not found in the database for the id: {expenseId}")
                raise Exception
        except Exception as e:
            print(f"Error occurred while updating the entry in the database: {e}")
            raise e
