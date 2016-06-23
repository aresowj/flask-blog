# -*- coding: utf-8 -*-

from app import app
import views

if __name__ == '__main__':
    app.run(host=app.config['SERVER_ADDRESS'], port=app.config['SERVER_PORT'], debug=app.config['DEBUG'])
