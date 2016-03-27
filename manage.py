from blog.web import app
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from sqlalchemy import create_engine

app.config['SQLALCHEMY_DATABASE_URI'] = app.config['CONNECTION_STRING']
db = create_engine(app.config['CONNECTION_STRING'])

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.command
def hello():
    print('hello')

if __name__ == '__main__':
    manager.run()
