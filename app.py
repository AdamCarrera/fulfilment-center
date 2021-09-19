from fastapi import FastAPI, Body, WebSocket
from fastapi.middleware.cors import CORSMiddleware

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

@app.post("/fulfillment-locations/{id}/status")
def update_location_status(id, body: dict = Body(...)):

    if not id in location_status:
        # initialize the entry for the location if not in the dictionary
        location_status[id] = {}

    location_status[id] = body

    return location_status[id]

@app.get("/fulfillment-locations/{id}")
def get_location_status(id):

    if id not in location_status:
        # initialize the entry for the location if not in the dictionary
        location_status[id] = {}

    return location_status[id]