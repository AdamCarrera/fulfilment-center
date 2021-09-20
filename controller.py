import requests
import json
from time import sleep

base_url = "192.168.2.27:9080"

# helpful variables that hold the coordinates for the intakes and docks
intake_A = [0, 750]
intake_B = [0, 500]
intake_C = [0, 250]

dock_A = [1000, 250]
dock_B = [1000, 500]
dock_C = [1000, 750]

# Gets the fulfillment location status by doing a REST call to the cloud
def get_fulfillmen_location_status(id):
    res = requests.get(f"http://{base_url}/fulfillment-locations/{id}", 
                        headers={"Content-Type":"application/json"}) 
    return res.json()

# Sends a command for a specific robot for speed and destination
def post_robot_command(id, destination, speed):
    res = requests.post(f"http://{base_url}/devices/{id}/params", 
                        headers={"Content-Type":"application/json"}, 
                        data=json.dumps({
                            "destination": destination,
                            "speed":speed
                        }))
    return res.json()

# Helper function that gets a robot's status
def get_robot_status(id):
    res = requests.get(f"http://{base_url}/devices/{id}", 
                        headers={"Content-Type":"application/json"}, 
                    )
    return res.json()


# Set up the robots
print("Comanding initial movements...")
dude = post_robot_command("dude", intake_A, 20)
sue = post_robot_command("sue", intake_B, 20)
dudette = post_robot_command("dudette", intake_C, 20)

# Loop forever commanding robots and getting info from the warehouse
print("Starting loop!")
while True:

    # Get dude's status
    dude = get_robot_status("dude")
    if "x" in dude: # just make sure that dude has stuff to report
        # gets the status of intake-A
        intake_A_status = get_fulfillmen_location_status("intake-A")

        # Checks to see if dude is at intake-A by comparing coordinates.  If not, check if he is at dock A
        if dude["x"] == intake_A[0] and dude["y"] == intake_A[1]:
            post_robot_command("dude", dock_A, 20)
            print("Commanded Dude to Dock A")
        elif dude["x"] == dock_A[0] and dude["y"] == dock_A[1]:
            post_robot_command("dude", intake_A, 20)
            print("Commanded Dude to Intake A")

    
    # Do same crap for sue
    sue = get_robot_status("sue")
    if "x" in sue:
        intake_B_status = get_fulfillmen_location_status("intake-B")
        if sue["x"] == intake_B[0] and sue["y"] == intake_B[1]:
            post_robot_command("sue", dock_B, 20)
            print("Commanded Sue to Dock B")
        elif sue["x"] == dock_B[0] and sue["y"] == dock_B[1]:
            post_robot_command("sue", intake_B, 20)
            print("Commanded Sue to Intake B")

    # Do same crap for dudette
    dudette = get_robot_status("dudette")
    if "x" in dudette:
        intake_C_status = get_fulfillmen_location_status("intake-C")
        if dudette["x"] == intake_C[0] and dudette["y"] == intake_C[1]:
            post_robot_command("dudette", dock_C, 20)
            print("Commanded Dudette to Dock C")
        elif dudette["x"] == dock_C[0] and dudette["y"] == dock_C[1]:
            post_robot_command("dudette", intake_C, 20) 
            print("Commanded Dudette to Intake C")       
        

    # Better watch performance on hitting your server...plus, do you really need to go that fast?  The robots aren't even reporting that fast...
    sleep(1)
