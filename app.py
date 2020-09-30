# coding: utf-8
from flask import Flask, request
from flask_restful import Resource, Api
import re

import json

app = Flask(__name__)
api = Api(app)

COLOR_START_PATTERN = '\{color:.*?\}'
COLOR_END_PATTERN = '\{color\}'
COLOR_PATTERN = '%s.*?%s' % (COLOR_START_PATTERN, COLOR_END_PATTERN)

SIZE_START_PATTERN = '\{font-size:.*?\}'
SIZE_END_PATTERN = '\{font-size\}'
SIZE_PATTERN = '%s.*?%s' % (SIZE_START_PATTERN, SIZE_END_PATTERN)

FONT_WEIGHT_START_PATTERN = '\{font-weight:.*?\}'
FONT_WEIGHT_END_PATTERN = '\{font-weight\}'
FONT_WEIGHT_PATTERN = '%s.*?%s' % (FONT_WEIGHT_START_PATTERN, FONT_WEIGHT_END_PATTERN)

class BlogPost(Resource):
    def trim_contents(self, pattern_text, array):
        split_data = re.split("(%s)" % pattern_text, array)
        split_trimed_data = []
        for dt in split_data:
            if dt == "":
                pass
            else:
                split_trimed_data.append(dt)       

        return split_trimed_data
    
    def split_contents(self, contents_original):
        response_contents = []
        for contents in contents_original.split('\n'):
            contents_array = []
            contents_array.append(contents)
            while True:
                split_flag = False
                for index in range(0, len(contents_array)):
                    color_data = re.search(COLOR_PATTERN, contents_array[index])
                    size_data = re.search(SIZE_PATTERN, contents_array[index])
                    font_weight_data = re.search(FONT_WEIGHT_PATTERN, contents_array[index])
                    if color_data:
                        split_trimed_data = self.trim_contents(color_data.group(0), contents_array[index])
                        if len(split_trimed_data) > 1:
                            split_flag = True

                        contents_array[index:index+1] = split_trimed_data
                    elif size_data:
                        split_trimed_data = self.trim_contents(size_data.group(0), contents_array[index])
                        if len(split_trimed_data) > 1:
                            split_flag = True

                        contents_array[index:index+1] = split_trimed_data
                    elif font_weight_data:
                        split_trimed_data = self.trim_contents(font_weight_data.group(0), contents_array[index])
                        if len(split_trimed_data) > 1:
                            split_flag = True

                        contents_array[index:index+1] = split_trimed_data
                        

                if split_flag == False:
                     break

            response_contents.append(contents_array)

        return response_contents

    def create_elem(self, start_pattern, end_pattern, text):
        start_tag = re.search(start_pattern, text).group(0)
        end_tag = re.search(end_pattern, text).group(0)
        style = start_tag.split('{')[1].split('}')[0]
        value = text.split(start_tag)[1].split(end_tag)[0]

        return {
            "type": "text",
            "style": style,
            "content": value
        } 

    def create_contents(self, contents):
        splited_contents = self.split_contents(contents)
        parsed_contents = []
        for raw in splited_contents:
            parsed_raw = []
            for elem in raw:
                color_data = re.search(COLOR_PATTERN, elem)
                size_data = re.search(SIZE_PATTERN, elem)
                font_weight_data = re.search(FONT_WEIGHT_PATTERN, elem)

                if color_data:
                    parsed_raw.append(self.create_elem(COLOR_START_PATTERN, COLOR_END_PATTERN, color_data.group(0)))
                elif size_data:
                    parsed_raw.append(self.create_elem(SIZE_START_PATTERN, SIZE_END_PATTERN, size_data.group(0)))
                elif font_weight_data:
                    parsed_raw.append(self.create_elem(FONT_WEIGHT_START_PATTERN, FONT_WEIGHT_END_PATTERN, font_weight_data.group(0)))
                else:
                    parsed_raw.append(
                        {
                            "type": "text",
                            "style": "undefined",
                            "content": elem
                        }
                    )
            parsed_contents.append(parsed_raw)
        return parsed_contents
                

    def post(self):
        data = request.data.decode('utf-8')
        data = json.loads(data)

        blog_data = {}
        blog_data['title'] = data['title']
        blog_data['tags'] = []
        split_tags = data['tags'].split(',')
        for tag in split_tags:
            if (tag == ''):
                pass
            else:
                blog_data['tags'].append(tag.strip())

        blog_data['contents'] = self.create_contents(data['contents'])

        print(json.dumps(blog_data))
        f = open("output.json", "w")
        json.dump(blog_data, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))

        return "ok"
        

                 

api.add_resource(BlogPost, '/api/blog-post')

if __name__ == '__main__':
    app.run(debug=True)