# coding: utf-8
from flask_restful import Resource
import os
import subprocess

DIRECTORY = os.path.dirname(__file__)
BASE_DIRECTORY = "%s/../" % DIRECTORY

class BlogList(Resource):
    def get(self):
        directory_list = subprocess.getoutput("ls %s/static" % BASE_DIRECTORY).split("\n")
        directory_list.sort(reverse=True)
        print(directory_list)

        return {
            "status": 200,
            "data": directory_list
        }

