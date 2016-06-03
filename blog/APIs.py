# -*- coding: utf-8; -*-


import json
from flask import current_app as app, request


__author__ = 'Ares Ou'


@app.route('/api/v1/available_tags', methods=['GET'])
def api_available_tags():
    tag_keyword = request.args.get('term', None)
    all_tags = list(app.config['post_tags'].keys())
    if tag_keyword:
        available_tags = [tag_name for tag_name in all_tags if tag_keyword.lower() in tag_name.lower()]
    else:
        available_tags = all_tags
    return json.dumps(available_tags)