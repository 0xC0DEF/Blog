# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_python37_app]
from flask import *

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
doc_path="docs/"
app = Flask(__name__, template_folder='static/'+doc_path)

class CategoryNode:
    def __init__(self,href="",text="",children=[]):
        self.href=href
        self.text=text
        self.children=children

from os import listdir
from os.path import isfile, join

def build_category_tree(path, name):
    if isfile("static/"+doc_path+path):
        return CategoryNode("/"+path, name)
    return CategoryNode("/"+path, name, [build_category_tree(path+"/"+i, i) for i in listdir("static/"+doc_path+path)])

@app.route('/')
def hello():
    return render_template("base.html", category_root=build_category_tree("all", "all"))

@app.route('/<path:path>')
def render_path(path):
    if isfile("static/"+doc_path+path):
        if request.args.get('only-content')=='true':
            with open("static/"+doc_path+path, 'r') as f:
                return f.read()
        else:
            return render_template("/"+path, category_root=build_category_tree(path, path.rsplit('/', 1)[-1]))
    else:
        return render_template("base.html", category_root=build_category_tree(path, path.rsplit('/', 1)[-1]))

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python37_app]
