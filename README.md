# MECH 6318 Group 8 Final Project Code

This repository contains the code used for implementing and testing our optimization algorithm. Our simulation was run on a linux virtual machine (Manjaro XFCE) and we believe that the steps outlined here should be similar for any UNIX based operating system. This simulation can be run on a windows machine, however there is one dependency (Gunicorn) that does not work on windows. 

There was a noticeable decrease in the code speed during runtime on the windows machine, however the underlying algorithm remains the same. 

## Warehouse Simulation

This project makes use part of the SYSE 6301 semester project, which involves the simulation of an unmanned fulfillment center. The code and outline for the SYSE repository can be found here: https://gitlab.com/systems-iot/syse6301-robotics-fulfillment-project/-/tree/master

## Accessing the simulation

The simulation is a web application. It can be accessed here: https://robotic-fulfillment-syse6301.netlify.app/

The browser used for our simulations is firefox. It is recommended to keep the simulation window open, as anomalies can occur when the simulation window is minimized.


## Running the Simulation

In addition to the web application, you will also need two terminals, one to run the server, and one to run the controller.

### Installing the virtual environment

In a terminal, navigate to the project directory and  run the following command to create the virtual environment.

```
python -m venv venv
```

Then, activate the environment with the following,

```
source venv/bin/activate
```

> Windows users use ```.\venv\Scripts\activate.bat```

Once you see a little `(venv)` on your terminal,the environment is active

### Installing dependencies

In the project directory and with the environment active, run the following command

```
pip install -r requirements.txt
```

### Running the server
To run the server, you should open a terminal, and make sure you activate your virtual environment. 

```
source start.app.sh
```

> Windows users: run ```python -m uvicorn --reload --port 5000 app:app```

Wait until the server shows that a connection is successful. You will also know you are connected when the red X's disappear from the robots. Once you are connected you can run the controller.

### Running the controller

In a different terminal, you can run the `controller.py`.  Once again, make sure you activate your `venv`.  Once your virtual environment is activated, run the controller:

```
python controller.py
```

## Known bug

Occasionally, the robot will fail to pick up any packages upon visiting an intake despite having sufficient storage space. We assume that this is an issue with the web application, and it can be solved by restarting the simulation by clicking the reset button in the browser. It may take a couple of tries.