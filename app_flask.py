from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import os
from flask_sockets import Sockets

# Instantiate your Flask Application
app = Flask(__name__)
sockets = Sockets(app)

# Get the port to run
PORT = os.getenv("PORT")
# Enable a security setting for modern browsers (don't worry about this)
cors = CORS(app)

# Database that stores your robot states and commands.  
# This is what is known as an  "in memory" database.  
# This database has no persistance, and will get 
# reset upon a server resstart.
robots = {}
robot_commands = {}
location_status = {}

# Route to update the status of a robot by name - the robots will 
# hit this route on a continual basis to update their status
@app.route("/devices/<id>/status", methods=["POST"])
def report_status(id):
    body = request.json
    robots[id] = body

    if not id in robot_commands:
        robot_commands[id] = {}

    return jsonify(robot_commands[id])

# Route to return the status of the device
@app.route("/devices/<id>", methods=["GET"])
def get_robot(id):
    if id not in robots:
        robots[id] = {}
    return jsonify(robots[id])

# Route to get the latest commands from your robot_commands object (database)
@app.route("/devices/<id>/commands", methods=["GET"])
def get_robot_commmands(id):

    if not id in robot_commands:
        return jsonify({})

    return jsonify(robot_commands[id])

# Route that allows a mmanagement process to provide commands to the robots
@app.route("/devices/<id>/params", methods=["POST"])
def update_robot(id):
    body = request.json

    if not id in robot_commands:
        robot_commands[id] = {}

    robot_commands[id]["destination"] = body["destination"]
    robot_commands[id]["speed"] = body["speed"]
    robot_commands[id]["id"] = id

    return jsonify(robot_commands[id])

@app.route("/fulfillment-locations/<id>/status", methods=["POST"])
def update_location_status(id):

    body = request.json

    if not id in location_status:
        # initialize the entry for the location if not in the dictionary
        location_status[id] = {}

    location_status[id] = body

    return jsonify(location_status[id])

@app.route("/fulfillment-locations/<id>", methods=["GET"])
def get_location_status(id):

    if id not in location_status:
        # initialize the entry for the location if not in the dictionary
        location_status[id] = {}

    return jsonify(location_status[id])    


@sockets.route('/device-report')
def echo_socket(ws):
    print(ws.client)
    while not ws.closed:
        message = ws.receive()
        ws.send(message)


# if __name__ == "__main__":
#     app.run(debug=True, port=PORT, host="0.0.0.0")

if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    server = pywsgi.WSGIServer(('0.0.0.0', int(PORT)), app, handler_class=WebSocketHandler)
    server.serve_forever()