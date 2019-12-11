from flask import Flask
import linkAnalysis 

#Starting server
app = Flask(__name__)

@app.route('/getRanking')
def getRanking():
    return linkAnalysis.getRanking(URLlist)


@app.route('/insert', methods=["PUT"])
def insert():
    jsonObj = request.form.to_dict()
    linkAnalysis.insert(jsonObj)


@app.route('/delete', methods=["DELETE"])
def delete():
    jsonObj = request.form['list']
    linkAnalysis.delete(jsonObj)


if __name__ == '__main__':
    app.run()