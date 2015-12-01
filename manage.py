from flask import Flask
from sqlalchemy import create_engine
import config
from models import *


app = Flask(__name__)
app.config.from_object(config)
app.config['SQLALCHEMY_DATABASE_URI'] = app.config['CONNECTION_STRING']
db = create_engine(app.config['CONNECTION_STRING'])

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
