from datetime import date

from sqlalchemy import Column, Integer, String, Date, func

from models import db


class Expense(db.Model):
    __tablename__ = "expense"
    id = Column(Integer, primary_key=True)
    expenseDescription = Column(String(500), nullable=False)
    typeOfExpense = Column(Integer, nullable=False, index=True)
    amount = Column(Integer, nullable=False)
    date = Column(Date, nullable=False, default=func.current_time(), index=True)

    def to_dict(self):
        return {
            column.name: getattr(self, column.name) for column in self.__table__.columns
        }
