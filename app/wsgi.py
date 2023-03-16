from flask_migrate import Migrate
from app.config.config import app, db
from app.logger.Logger import Logger

l = Logger()

from app.models.AccountModel import AccountModel

migrate = Migrate(app, db)

app.app_context().push()

l.logger.info("Models pushing in database")