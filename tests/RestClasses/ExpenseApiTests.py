from unittest.mock import MagicMock, patch

import pytest
from flask import Flask

from RestClasses.ExpenseApi import ExpenseApi


class TestExpenseApi:
    @pytest.fixture(autouse=True)
    def setup_method(self):
        self.app = Flask(__name__)
        self.expense_api = ExpenseApi(self.app)
        self.expense_service_mock = MagicMock()
        self.expense_api.expense_service = self.expense_service_mock
        self.client = self.app.test_client()

    def test_get_all_expenses_returns_expenses(self):
        self.expense_service_mock.getAllExpenses.return_value = [
            MagicMock(to_dict=lambda: {"id": 1})
        ]
        response = self.client.get("/expense/getAll")
        assert response.status_code == 200
        assert response.json == [{"id": 1}]

    def test_get_all_expenses_handles_exception(self):
        self.expense_service_mock.getAllExpenses.side_effect = Exception("DB error")
        response = self.client.get("/expense/getAll")
        assert response.status_code == 500
        assert response.data.decode() == "Unable to retrieve expenses from the database"

    def test_get_expense_returns_expense(self):
        self.expense_service_mock.getExpenseById.return_value = MagicMock(
            to_dict=lambda: {"id": 1}
        )
        response = self.client.get("/expense/1")
        assert response.status_code == 200
        assert response.json == {"id": 1}

    def test_get_expense_handles_not_found(self):
        self.expense_service_mock.getExpenseById.return_value = None
        response = self.client.get("/expense/1")
        assert response.status_code == 404
        assert response.data.decode() == "Expense with id 1 not found"

    def test_get_expense_handles_exception(self):
        self.expense_service_mock.getExpenseById.side_effect = Exception("DB error")
        response = self.client.get("/expense/1")
        assert response.status_code == 500
        assert response.data.decode() == "Unable to retrieve expense from the database"

    @patch("RestClasses.ExpenseApi.ExpenseApi.getRequestParser")
    def test_add_expense_adds_expense(self, mock_getRequestParser):
        mock_parser = MagicMock()
        mock_parser.parse_args.return_value = {"id": 1}
        mock_getRequestParser.return_value = mock_parser
        response = self.client.post("/expense")
        assert response.status_code == 201
        assert response.data.decode() == "Successfully added to the db"

    @patch("RestClasses.ExpenseApi.ExpenseApi.getRequestParser")
    def test_add_expense_handles_exception(self, mock_getRequestParser):
        mock_parser = MagicMock()
        mock_parser.parse_args.side_effect = Exception("Parse error")
        mock_getRequestParser.return_value = mock_parser
        response = self.client.post("/expense")
        assert response.status_code == 500
        assert response.data.decode() == "Unable to add entry to the db"

    def test_remove_expense_removes_expense(self):
        response = self.client.delete("/expense/1")
        assert response.status_code == 200
        assert response.data.decode() == "Removed the entry from the database"

    def test_remove_expense_handles_exception(self):
        self.expense_service_mock.removeAnExpense.side_effect = Exception("DB error")
        response = self.client.delete("/expense/1")
        assert response.status_code == 500
        assert response.data.decode() == "Unable to delete a entry from the database"

    @patch("RestClasses.ExpenseApi.ExpenseApi.getRequestParser")
    def test_update_expense_updates_expense(self, mock_getRequestParser):
        mock_parser = MagicMock()
        mock_parser.parse_args.return_value = {"id": 1}
        mock_getRequestParser.return_value = mock_parser
        response = self.client.put("/expense")
        assert response.status_code == 200
        assert (
            response.data.decode() == "Successfully modified the entry in the database"
        )

    @patch("RestClasses.ExpenseApi.ExpenseApi.getRequestParser")
    def test_update_expense_handles_exception(self, mock_getRequestParser):
        mock_parser = MagicMock()
        mock_parser.parse_args.side_effect = Exception("Parse error")
        mock_getRequestParser.return_value = mock_parser
        response = self.client.put("/expense")
        assert response.status_code == 500
        assert response.data.decode() == "Unable to modify the entry in the database"
