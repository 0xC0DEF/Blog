from flask import *
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
		return CategoryNode("/"+path, name[:-5])
	return CategoryNode("/"+path, name, [build_category_tree(path+"/"+i, i) for i in sorted(listdir("static/"+doc_path+path))])

@app.route('/')
def hello():
	return render_template("main.html", category_root=build_category_tree("all", "all"))

@app.route('/test')
def test():
	x=[]
	with open("static/docs/main.html", 'r') as f:
		x=f.readlines()
	with open("static/docs/main.html", 'w') as f:
		f.writelines(x[:-1]+["<p>test</p>\n{% endblock %}\n"])
	return render_template("main.html", category_root=build_category_tree("all", "all"))

@app.route('/robots.txt')
def robots():
	return app.send_static_file('robots.txt')

@app.route('/all')
def on_all():
	return render_path('all')

@app.route('/all/<path:path>')
def on_all_path(path):
	return render_path('all/'+path)

def render_path(path):
	if isfile("static/"+doc_path+path):
		if request.args.get('only-content')=='true':
			with open("static/"+doc_path+path, 'r') as f:
				return f.read()
		else:
			return render_template("/"+path, category_root=build_category_tree("all", "all"))
	else:
		dc=[("/"+path+"/"+i, i) for i in listdir("static/"+doc_path+path)]
		return render_template("directory.html", category_root=build_category_tree("all", "all"), directory_content=dc)

if __name__ == '__main__':
	# This is used when running locally only.
	app.run(host='127.0.0.1', port=8080, debug=True)
