import sys
sys.path.append("../modules")

from TellstickLib import TellstickLib
tellstickLib = TellstickLib()

from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', noOfDevices=tellstickLib.getNumberOfDevices(), 
        devices=tellstickLib.getDevices())

@app.route('/lights', methods=['POST']) 
def lights():
    if request.form['mode'] == "1":
        tellstickLib.turnOn(request.form['light'])
    else:
        tellstickLib.turnOff(request.form['light'])
    return (request.form['light'], None)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=14895)

