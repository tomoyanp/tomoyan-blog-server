# coding: utf-8
from flask import Flask, request
from flask_restful import Resource, Api

import json
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), 'apis'))

from blog_post import BlogPost
from blog_list import BlogList

app = Flask(__name__)
api = Api(app)

api.add_resource(BlogPost, '/api/blog-post')
api.add_resource(BlogList, '/api/blog-list')

if __name__ == '__main__':
    app.run(debug=True)