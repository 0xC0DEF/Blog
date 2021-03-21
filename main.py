from flask import *
doc_path="docs/"
app = Flask(__name__, template_folder='static/'+doc_path)

class CategoryNode:
	def __init__(self,href="",text="",children=[]):
		self.href=href
		self.text=text
		self.children=children

from os import listdir
from os.path import isfile, join, isdir

def build_category_tree(path, name):
	if isfile("static/"+doc_path+path):
		return CategoryNode("/"+path, name[:-5])
	return CategoryNode("/"+path, name, [build_category_tree(path+"/"+i, i) for i in sorted(listdir("static/"+doc_path+path))])

@app.route('/')
def hello():
	return render_template("main.html", category_root=build_category_tree("all", "all"), article_name='')

@app.route('/robots.txt')
def robots():
	return app.send_static_file('robots.txt')

@app.route('/all')
def on_all():
	return render_path('all')

@app.route('/all/<path:path>')
def on_all_path(path):
	return render_path('all/'+path)

@app.errorhandler(404)
def page404(e):
	return render_template("404.html", category_root=build_category_tree("all", "all"), article_name='ERROR 404'),404

def render_path(path):
	if isfile("static/"+doc_path+path):
		print(path.split("/."))
		return render_template("/"+path, category_root=build_category_tree("all", "all"), article_name=path.split("/")[-1].split(".")[-2])
	elif isdir("static/"+doc_path+path):
		dc=[("/"+path+"/"+i, i) for i in listdir("static/"+doc_path+path)]
		return render_template("directory.html", category_root=build_category_tree("all", "all"), article_name=path.split("/")[-1], directory_content=dc)
	else:
		return page404(None)

if __name__ == '__main__':
	# This is used when running locally only.
	app.run(host='127.0.0.1', port=8080, debug=True)
