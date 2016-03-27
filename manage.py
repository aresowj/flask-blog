from blog.web import app, run_app
from blog.models import Base
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Server

app.config['SQLALCHEMY_DATABASE_URI'] = app.config['CONNECTION_STRING']
migrate = Migrate(app, Base)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
manager.add_command('start', run_app())


if __name__ == '__main__':
    manager.run()
