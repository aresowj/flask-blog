# -*- coding: utf-8 -*-

from blog import app
from blog.models import Tag, Category, fetch_all_instances


# get some global objects
# create tag dictionary for app-wide use
app.config['post_tags'] = {}
for tag in Tag.get_all_tags():
    app.config['post_tags'][tag.name] = tag.id
app.config['categories'] = fetch_all_instances(Category)

if __name__ == '__main__':
    app.run(host=app.config['SERVER_ADDRESS'], port=app.config['SERVER_PORT'], debug=app.config['DEBUG'])
