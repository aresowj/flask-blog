from blog import app
from blog.models import Base, Tag, Category, fetch_all_instances
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

migrate = Migrate(app, Base)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


def setup_app():
    # get some global objects
    # create tag dictionary for app-wide use
    app.config['post_tags'] = {}
    for tag in Tag.get_all_tags():
        app.config['post_tags'][tag.name] = tag.id
    app.config['categories'] = fetch_all_instances(Category)
    return app

    
def run_app():
    this_app = setup_app()
    this_app.run(host=app.config['SERVER_ADDRESS'], port=app.config['SERVER_PORT'], debug=app.config['DEBUG'])

manager.add_command('start', run_app())

if __name__ == '__main__':
    manager.run()
