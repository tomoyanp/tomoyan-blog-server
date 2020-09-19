# coding: utf-8
from flask import Flask, request
from flask_restful import Resource, Api

import json

app = Flask(__name__)
api = Api(app)

class BlogPost(Resource):
    def post(self):
        data = request.data.decode('utf-8')
        data = json.loads(data)
        print(data)
        # jsonData = request.json["data"]
        # print(jsonData)
        #data = request.data
        #print(data);
        #print(data["title"])
        #print(data["tags"])
        #print(data["contents"])

        return "ok"

api.add_resource(BlogPost, '/api/blog-post')

if __name__ == '__main__':
    app.run(debug=True)