import os
from flask import Flask, render_template
from core import *

app = Flask(__name__)

@app.route("/")
def render():
    return render_template('index.html')

@app.route("/receiver")
def worker():
    # Currently calculating top spread only
    spreads = top_five_spreads_route()
    return spreads



if __name__ == '__main__':
    app.run()
