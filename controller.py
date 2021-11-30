import requests
import json
from time import sleep
import logging

logging.basicConfig(level=logging.INFO)
base_url = "localhost:5000"

# helpful variables that hold the coordinates for the intakes and docks
intake_A = [0, 750]
intake_B = [0, 500]
intake_C = [0, 250]

dock_A = [1000, 250]
dock_B = [1000, 500]
dock_C = [1000, 750]

destinations = [intake_A, intake_B, intake_C, dock_A, dock_B, dock_C]

def get_optimal_route(possible_destinations) -> dict:
    return(sorted(possible_destinations.items(), key=lambda x :
                  x[1]["efficiency"], reverse=True))

# Get possible destinations given robot position

def get_possible_destinations(pos, destinations, robot) -> dict:

    payloadCount = robot["payloadCount"]
    maxPayloadCount = robot["maxPayloadCount"]

    storage_space = maxPayloadCount - payloadCount

    # get status of intakes
    intake_A_status = get_fulfillmen_location_status("intake-A")["available"]
    intake_B_status = get_fulfillmen_location_status("intake-B")["available"]
    intake_C_status = get_fulfillmen_location_status("intake-C")["available"]


    # get staus of packages on dudette
    packs_for_A = dudette["payloadSplit"]["dock-A"]
    packs_for_B = dudette["payloadSplit"]["dock-B"]
    packs_for_C = dudette["payloadSplit"]["dock-C"]

    # calculate packages available to pickup from intake A
    if intake_A_status >= storage_space:
        available_at_A = storage_space
    else:
        available_at_A = intake_A_status

    # calculate packages available to pickup from intake B
    if intake_B_status >= storage_space:
        available_at_B = storage_space
    else:
        available_at_B = intake_B_status

    # calculate packages available to pickup from intake C
    if intake_C_status >= storage_space:
        available_at_C = storage_space
    else:
        available_at_C = intake_C_status

    # destinations
    intake_A = [0, 750]
    intake_B = [0, 500]
    intake_C = [0, 250]

    dock_A = [1000, 250]
    dock_B = [1000, 500]
    dock_C = [1000, 750]


    # TODO add efficiency 

    if pos==intake_A:
        return {
            "dock_A" : {
                "destination" : dock_A,
                "distance" : 1118.03,
                "efficiency" : packs_for_A / 1118.03
            },
            "dock_B" : {
                "destination" : dock_B,
                "distance" : 1030.78,
                "efficiency" : packs_for_B / 1030.78
            },
            "dock_C" : {
                "destination" : dock_C,
                "distance" : 1000,
                "efficiency" : packs_for_C / 1000
            },
            "intake_B" : {
                "destination" : intake_B,
                "distance" : 250,
                "efficiency" : available_at_B / 250
            }
        }
    elif pos==intake_B:
        return {
            "dock_A" : {
                "destination" : dock_A,
                "distance" : 1030.78,
                "efficiency" : packs_for_A / 1030.78
            },
            "dock_B" : {
                "destination" : dock_B,
                "distance" : 1000,
                "efficiency" : packs_for_B / 1000
            },
            "dock_C" : {
                "destination" : dock_C,
                "distance" : 1030.78,
                "efficiency" : packs_for_C / 1030.78
            },
            "intake_A" : {
                "destination" : intake_A,
                "distance" : 250,
                "efficiency" : available_at_A / 250
            },
            "intake_C" : {
                "destination" : intake_C,
                "distance" : 250,
                "efficiency" : available_at_B / 250
            }
        }
    elif pos==intake_C:
        return {
            "dock_A" : {
                "destination" : dock_A,
                "distance" : 1000,
                "efficiency" : packs_for_A / 1000
            },
            "dock_B" : {
                "destination" : dock_B,
                "distance" : 1030.78,
                "efficiency" : packs_for_B / 1030.78
            },
            "dock_C" : {
                "destination" : dock_C,
                "distance" : 1118.03,
                "efficiency" : packs_for_C / 1118.03
            },
            "intake_B" : {
                "destination" : intake_B,
                "distance" : 250,
                "efficiency" : available_at_B / 250
            }
        }
    elif pos==dock_A:
        return {
            "intake_A" : {
                "destination" : intake_A,
                "distance" : 1118.03,
                "efficiency" : available_at_A / 1118.03
            },
            "intake_B" : {
                "destination" : intake_B,
                "distance" : 1030.78,
                "efficiency" : available_at_B / 1030.78
            },
            "intake_C" : {
                "destination" : intake_C,
                "distance" : 1000,
                "efficiency" : available_at_C / 1000
            },
            "dock_B" : {
                "destination" : dock_B,
                "distance" : 250,
                "efficiency" : packs_for_B / 250
            }
        }
    # TODO calculate available packages to pick up, fill in rest of
    # efficiencies
    elif pos==dock_B:
        return {
            "intake_A" : {
                "destination" : intake_A,
                "distance" : 1030.78,
                "efficiency" : available_at_A / 1030.78
            },
            "intake_B" : {
                "destination" : intake_B,
                "distance" : 1000,
                "efficiency" : available_at_B / 1000
            },
            "intake_C" : {
                "destination" : intake_C,
                "distance" : 1030.78,
                "efficiency" : available_at_C / 1030.78
            },
            "dock_A" : {
                "destination" : dock_A,
                "distance" : 250,
                "efficiency" : packs_for_A / 250
            },
            "dock_C" : {
                "destination" : dock_C,
                "distance" : 250,
                "efficiency" : packs_for_C / 250
            }
        }
    elif pos==dock_C:
        return {
            "intake_A" : {
                "destination" : intake_A,
                "distance" : 1000,
                "efficiency" : available_at_A / 1000
            },
            "intake_B" : {
                "destination" : intake_B,
                "distance" : 1030.78,
                "efficiency" : available_at_B / 1030.78
            },
            "intake_C" : {
                "destination" : intake_C,
                "distance" : 1118.03,
                "efficiency" : available_at_C / 1118.03
            },
            "dock_B" : {
                "destination" : dock_B,
                "distance" : 250,
                "efficiency" : packs_for_B / 250
            }
        }


# Gets the fulfillment location status by doing a REST call to the cloud
def get_fulfillmen_location_status(id) -> dict:
    res = requests.get(f"http://{base_url}/fulfillment-locations/{id}",
                        headers={"Content-Type":"application/json"})
    return res.json()

# Sends a command for a specific robot for speed and destination
def post_robot_command(id, destination, speed) -> dict:
    res = requests.post(f"http://{base_url}/devices/{id}/params",
                        headers={"Content-Type":"application/json"},
                        data=json.dumps({
                            "destination": destination,
                            "speed":speed
                        }))
    return res.json()

# Helper function that gets a robot's status
def get_robot_status(id) -> dict:
    res = requests.get(f"http://{base_url}/devices/{id}",
                        headers={"Content-Type":"application/json"},
                    )
    return res.json()


# Set up the robots, move sue and dude  out of the way
logging.info("\tComanding initial movements...")
dude = post_robot_command("dude", [1000, 100], 20)
sue = post_robot_command("sue", [1000, 200], 20)
dudette = post_robot_command("dudette", intake_A, 20)

# Loop forever commanding robots and getting info from the warehouse
logging.info("\tStarting loop!")
while True:

    # get status of dudette
    dudette = get_robot_status("dudette")

    # TODO organize fulfillment center data into dictionary, created with one
    # function call, DONE

    # TODO determine distances from robot position, formulate optimization
    # problem, DONE

    # TODO put a conditional that only formulates the optimization problem when
    # near an intake or a dock, DONE 


    if "x" in dudette: # just make sure that dudette has stuff to report

        dudette_position = [dudette["x"], dudette["y"]]

        # Checks to see if dudette is near any intake or dock

        if any(destination == dudette_position for destination in destinations):

            dests = get_possible_destinations([dudette["x"], dudette["y"]],
                                              destinations, dudette)
            #print(dests)
            sorted_dest = get_optimal_route(dests)
            logging.info(f'\tThe optimal route is: {sorted_dest[0][1]}')
            #logging.info(f'at coordinates: {sorted_dest[0][1]["destination"]}')
            post_robot_command("dudette", sorted_dest[0][1]["destination"], 20)
            #TODO post robot command from sorted list, use first destination

    # Better watch performance on hitting your server...plus, do you really need to go that fast?  The robots aren't even reporting that fast...
    sleep(1)
