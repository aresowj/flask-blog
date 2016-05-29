# -*- coding: utf-8 -*-

from blog import app
from blog.models import Base
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

migrate = Migrate(app, Base)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
