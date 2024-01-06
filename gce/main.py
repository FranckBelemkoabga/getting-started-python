# Copyright 2019 Google LLC All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# from flask import Flask
# app = Flask(__name__)


# @app.route('/', methods=['GET'])
# def say_hello():
#     return "Hello, yo!"

import flask
from flask import Flask, request, send_file
from flask_cors import CORS
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import json

app = flask.Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.get("/")
def hello():
    who = flask.request.args.get("who", "World")
    return f"Hello {who}!\n"


@app.route('/generate-plot', methods=['POST'])
def generate_plot():
    # Parse the JSON data sent from the Flutter app
    data = request.json.get('data', [])

    # Create a plot using the data
    fig, ax = plt.subplots()
    ax.plot(data)

    # Save the plot to a BytesIO buffer
    buf = BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)

    # Return the plot as a raw image
    return send_file(buf, mimetype='image/png')



#just for testing
@app.route('/plot.png')
def plot_png():
    # Create a plot
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3, 4], [1, 4, 2, 3])

    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"<img src='data:image/png;base64,{data}'/>"

# if __name__ == "__main__":
#     app.run(host='0.0.0.0', port=8080, debug=True)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
