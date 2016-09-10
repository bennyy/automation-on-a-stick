import sys
sys.path.append("../modules")


from flask import Flask, render_template
from TellstickLib import TellstickLib
app = Flask(__name__)

@app.route('/')
def index():
    tmp = TellstickLib()

    return render_template('index.html', noOfDevices=tmp.getNumberOfDevices())

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

