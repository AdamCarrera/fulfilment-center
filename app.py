from fastapi import FastAPI, Body, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI()

# Enable a security setting for modern browsers (don't worry about this)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database that stores your robot states and commands.  
# This is what is known as an  "in memory" database.  
# This database has no persistance, and will get 
# reset upon a server resstart.
robots = {}
robot_commands = {}
location_status = {}
robot_websocket_connections = {}


# Route to update the status of a robot by name - the robots will 
# hit this route on a continual basis to update their status
@app.post("/devices/{id}/status")
def report_status(id, body: dict = Body(...)):
    robots[id] = body

    if not id in robot_commands:
        robot_commands[id] = {}

    return robot_commands[id]

# Route to return the status of the device
@app.get("/devices/{id}")
def get_robot(id):
    if id not in robots:
        robots[id] = {}
    return robots[id]

# Route to get the latest commands from your robot_commands object (database)
@app.get("/devices/{id}/commands")
def get_robot_commmands(id):
    if not id in robot_commands:
        return {}

    return robot_commands[id]

# Route that allows a mmanagement process to provide commands to the robots
@app.post("/devices/{id}/params")
def update_robot(id, body: dict = Body(...)):
    if not id in robot_commands:
        robot_commands[id] = {}

    robot_commands[id]["destination"] = body["destination"]
    robot_commands[id]["speed"] = body["speed"]
    robot_commands[id]["id"] = id

    return robot_commands[id]

# Posts a fulfillment location status - this is used by the docks and intake robotics
@app.post("/fulfillment-locations/{id}/status")
def update_location_status(id, body: dict = Body(...)):

    if not id in location_status:
        # initialize the entry for the location if not in the dictionary
        location_status[id] = {}

    location_status[id] = body

    return location_status[id]

# Route to get the current status of an intake or dock fulfillment location
@app.get("/fulfillment-locations/{id}")
def get_location_status(id):

    if id not in location_status:
        # initialize the entry for the location if not in the dictionary
        location_status[id] = {}

    return location_status[id]

# The constant websocket connection that allows for back and forth data flow between the robot and the API
@app.websocket("/device-data-stream/{id}")
async def websocket_endpoint(websocket: WebSocket, id: str):
    await websocket.accept()
    robot_websocket_connections[id] = websocket
    while True:
        data = await websocket.receive_text()
        robots[id] = json.loads(data)
        if id in robot_commands:
            await websocket.send_text(json.dumps(robot_commands[id]))