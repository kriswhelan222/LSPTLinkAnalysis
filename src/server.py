from flask import Flask
import linkAnalysis 

#Starting server
app = Flask(__name__)

@app.route('/getRanking')
def getRanking():
    return linkAnalysis.getRanking(URLlist)

@app.route('/insert', methods=["GET","POST"])
def insert():
	
    jsonObj = request.form['list']
    linkAnalysis.insert(jsonObj)

if __name__ == '__main__':
    app.run()