import sys
sys.path.append("../modules")

from TellstickLib import TellstickLib
tl = TellstickLib()

from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', noOfDevices=tl.getNumberOfDevices(), 
        devices=tl.getDevices())

@app.route('/lights', methods=['POST']) 
def lights():
    if request.form['mode'] == "1":
        tl.turnOn(request.form['light'])
    else:
        tl.turnOff(request.form['light'])
    return (request.form['light'], None)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

