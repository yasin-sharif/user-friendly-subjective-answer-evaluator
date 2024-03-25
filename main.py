from flask import Flask,render_template,request,jsonify
import evaluate as ev

app = Flask(__name__)
value=1234

@app.route("/")
def hello_world():
    return render_template('home.html',data=value)

@app.route("/evaluate",methods=['post'])
def evaluate():
    response=request.form
    result=ev.evaluate(response['stu_ans'],response['solution'],response['keyword'])
    return render_template('evaluate.html',data=result)

@app.route("/automate",methods=['post'])
def automate():
    response=request.form
    result=ev.automate(response['filename'])
    return render_template('automate.html',data=result)