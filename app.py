from flask import Flask
from flask_migrate import Migrate, upgrade

from RestClasses.ExpenseApi import ExpenseApi
from config import Config
from models import db
import logging

app = Flask(__name__)

app.logger.setLevel(logging.DEBUG)  # Set log level to INFO
handler = logging.FileHandler("app.log")  # Log to a file
app.logger.addHandler(handler)

app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app, db)

ExpenseApi(app)

with app.app_context():
    upgrade()

# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    app.run(debug=False)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
