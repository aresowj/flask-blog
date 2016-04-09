from blog.web import app, run_app
from blog.models import Base
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

migrate = Migrate(app, Base)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
manager.add_command('start', run_app())


if __name__ == '__main__':
    manager.run()
