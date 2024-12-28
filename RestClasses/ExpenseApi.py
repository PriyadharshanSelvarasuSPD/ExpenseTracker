from flask import Flask
from flask_restful import reqparse
from flask_restful.reqparse import RequestParser

from services.ExpenseService import ExpenseService


class ExpenseApi:
    def __init__(self, app: Flask):
        app.add_url_rule("/expense", "put_expense", self.add_expense, methods=["POST"])
        app.add_url_rule(
            "/expense/<int:expense_id>",
            "remove_expense",
            self.remove_expense,
            methods=["DELETE"],
        )
        app.add_url_rule(
            "/expense", "update_expense", self.update_expense, methods=["PUT"]
        )
        app.add_url_rule(
            "/expense/getAll",
            "get_all_expenses",
            self.get_all_expenses,
            methods=["GET"],
        )
        app.add_url_rule(
            "/expense/<int:expense_id>",
            "get_expense",
            self.get_expense,
            methods=["GET"],
        )
        self.expense_service = ExpenseService()

    def get_all_expenses(self):
        try:
            expenses = self.expense_service.getAllExpenses()
            return [expense.to_dict() for expense in expenses], 200
        except Exception as e:
            return f"Unable to retrieve expenses from the database", 500

    def get_expense(self, expense_id: int):
        try:
            expense = self.expense_service.getExpenseById(expense_id)
            if expense:
                return expense.to_dict(), 200
            else:
                return f"Expense with id {expense_id} not found", 404
        except Exception as e:
            return f"Unable to retrieve expense from the database", 500

    def add_expense(self):
        try:
            args = self.getRequestParser().parse_args()
            self.expense_service.addExpenseToDataBase(args)
            return "Successfully added to the db", 201
        except Exception:
            return "Unable to add entry to the db", 500

    def remove_expense(self, expense_id: int):
        try:
            self.expense_service.removeAnExpense(expense_id)
            return "Removed the entry from the database", 200
        except Exception as e:
            return "Unable to delete a entry from the database", 500

    def update_expense(self):
        try:
            args = self.getRequestParser().parse_args()
            self.expense_service.modifyExpense(args["id"], args)
            return "Successfully modified the entry in the database"
        except Exception as e:
            return "Unable to modify the entry in the database", 500

    def getRequestParser(self) -> RequestParser:
        requestParser: RequestParser = reqparse.RequestParser()
        requestParser.add_argument("id")
        requestParser.add_argument(
            "expense_description",
            type=str,
            required=True,
            help="Description is Mandatory",
        )
        requestParser.add_argument(
            "amount", type=int, required=True, help="Amount is Mandatory"
        )
        requestParser.add_argument(
            "type_of_expense", type=int, required=True, help="Expense Type is Mandatory"
        )
        requestParser.add_argument("date", type=str, required=False)
        return requestParser
