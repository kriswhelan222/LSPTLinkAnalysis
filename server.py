from flask import Flask
import linkAnalysis 

#Starting server
app = Flask(__name__)

@app.route('/getRanking')
def hello_world():
    return linkAnalysis.getRanking(linkAnalysis.getGraph())

@app.route('/insert/', methods=["GET","POST"])
def login_page():
	
    jsonObj = request.form['list']
    linkAnalysis.insert(linkAnalysis.getGraph(), jsonObj)